"""
This module houses all commands to be sent from the GSE to the PIC as well as packetization functions
"""
# IMPORTED MODULES
from byte import *

# ------------------------------------------PACKETIZATION AND CRC----------------------------------------------------- #

""" Determines the cyclic redundancy check for the given data """
def getCRC(data):
    sum1 = SEED[0]
    sum2 = SEED[1]

    for i in range(0, len(data)):
        sum1 += data[i]
        sum2 += sum1

    checksum = bytes([sum2 % 255]) + bytes([sum1 % 255])
    return checksum


""" Takes in an op code and the data desired to be sent. Builds the packet from the sync pattern, op code, data length,
data, and crc. Then takes the packet and converts into usable byte type data that can be sent using serial comms """
def buildPacket(opcode, data):
    if data is None:
        # Find the length of the data in hex (1 byte) (for no length should be 0x00)
        data_length = bytes([0])
        # Create a raw packet to determine the CRC (packet = opcode/data length)
        op_len_data = opcode + data_length
    else:
        # Find the length of the data in hex (1 byte)
        data_length = bytes([len(data)])
        # Create a raw packet to determine the CRC (packet = opcode/data length/data)
        op_len_data = opcode + data_length + data
    # find CRC
    CRC = getCRC(op_len_data)
    # append CRC on to the packet (packet = opcode/data length/data/CRC)
    op_len_data_crc = op_len_data + CRC
    # Concatenate the sync pattern with the opcode, data and crc (packet = sync pattern/opcode/data length/data/CRC)
    packet = SYNC_PATTERN + op_len_data_crc
    # Return the packet
    return packet


# ------------------------------------------REQUEST DATA/ CONTROL BOARDS---------------------------------------------- #
""" Request a housekeeping packet """
def HK_REQ(ser):
    ser.write(buildPacket(CDH_HK_REQUEST, None))


""" Request a science packet """
def SCI_REQ(ser):
    ser.write(buildPacket(CDH_SCI_REQUEST, None))


""" Request a configuration packet """
def CONFIG_REQ(ser):
    ser.write(buildPacket(CDH_CONFIG_REQUEST, None))


""" Send a configuration packet to set the operational mode """
def CONFIG_OP(ser, data):
    ser.write(buildPacket(CDH_CONFIG_OP, data))


""" Command the activation/deactivation of the Analog Board """
def ANALOG_CTRL(ser, data):
    ser.write(buildPacket(CDH_ANALOG_CTRL, data))


""" Command the activation/deactivation of the Scalar Board (and magnetometer) No.1 """
def SCALAR1_CTRL(ser, data):
    ser.write(buildPacket(CDH_SCALAR1_CTRL, data))


""" Command the activation/deactivation of the Scalar Board (and magnetometer) No.2 """
def SCALAR2_CTRL(ser, data):
    ser.write(buildPacket(CDH_SCALAR2_CTRL, data))


""" Command the activation/deactivation of the Star Tracker No.1 """
def STAR_TRACK1_CTRL(ser, data):
    ser.write(buildPacket(CDH_STAR_TRACK1_CTRL, data))


""" Command the activation/deactivation of the Star Tracker No.2 """
def STAR_TRACK2_CTRL(ser, data):
    ser.write(buildPacket(CDH_STAR_TRACK2_CTRL, data))


""" Send the time of tone to the VRuM """
def TIME_OF_TONE(ser, data):
    ser.write(buildPacket(CDH_TIME_OF_TONE, data))


""" Command the activation/deactivation of the Science Stream """
def SCIENCE_STREAM_CTRL(ser, data):
    ser.write(buildPacket(CDH_SCIENCE_STREAM_CTRL, data))


# ---------------------------------------------------RECEIVE DATA----------------------------------------------------- #
""" Response to the request for a housekeeping packet """
def HK_OUT_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        return data
    else:
        print("Cyclic Redundancy Check Failed... Housekeeping Data Was Not Received Properly")
        return None


""" Response to a request for a science packet """
def SCI_OUT_OP(ser, opcode):
    data_length = ser.read(1)  # data length for science packet = 255
    packet_version_id = ser.read(2)  # reads packet version and packet identification
    seq_flag_packet_counter = ser.read(2)
    packet_data_length = ser.read(2)  # find packet data length
    packet_data_field = ser.read(int.from_bytes(packet_data_length, "big") + 1)  # read packet data
    CRC = ser.read(2)
    data = packet_version_id + seq_flag_packet_counter + packet_data_length + packet_data_field
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        return data
    else:
        print("Cyclic Redundancy Check Failed... Science Data Was Not Received Properly")


""" Response to a request for a configuration packet """
def CONFIG_OUT_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        return data
    else:
        print("Cyclic Redundancy Check Failed... Configuration Acknowledgement Was Not Received Properly")


""" Acknowledge the reception of a new configuration packet to set the operational mode """
def CONFIG_ACK_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        print("Configuration Acknowledgement Received")
        return True
    else:
        print("Cyclic Redundancy Check Failed... Configuration Acknowledgement Was Not Received Properly")
        return False


""" Acknowledge the reception of the command requesting the activation/deactivation of the Analog Board """
def ANALOG_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        if data == ON:
            return True
        elif data == OFF:
            return False
        else:
            print("Data Incorrect for Specified Operational Code!")
    else:
        print("Cyclic Redundancy Check Failed... Analog Operation Was Not Received Properly")
        return None


""" Acknowledge the reception of the command requesting the activation/deactivation of the Scalar Board No.1 """
def SCALAR1_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        if data == ON:
            return True
        elif data == OFF:
            return False
        else:
            print("Data Incorrect for Specified Operational Code!")
    else:
        print("Cyclic Redundancy Check Failed... Scalar 1 Operation Was Not Received Properly")
        return None


""" Acknowledge the reception of the command requesting the activation/deactivation of the Scalar Board No.2 """
def SCALAR2_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        if data == ON:
            return True
        elif data == OFF:
            return False
        else:
            print("Data Incorrect for Specified Operational Code!")
    else:
        print("Cyclic Redundancy Check Failed... Scalar 2 Operation Was Not Received Properly")
        return None


""" Acknowledge the reception of the command requesting the activation/deactivation of the Star Tracker No.1 """
def STAR_TRACK1_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        if data == ON:
            return True
        elif data == OFF:
            return False
        else:
            print("Data Incorrect for Specified Operational Code!")
    else:
        print("Cyclic Redundancy Check Failed... Star Tracker 1 Operation Was Not Received Properly")
        return None


""" Acknowledge the reception of the command requesting the activation/deactivation of the Star Tracker No.2 """
def STAR_TRACK2_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        if data == ON:
            return True
        elif data == OFF:
            return False
        else:
            print("Data Incorrect for Specified Operational Code!")
    else:
        print("Cyclic Redundancy Check Failed... Star Tracker 2 Operation Was Not Received Properly")
        return None


""" Acknowledge the reception of the time of tone command """
def TIME_ACK_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        return True
    else:
        print("Cyclic Redundancy Check Failed... Time of Tone Acknowledgement Was Not Received Properly")
        return False


""" Acknowledge the reception of the science stream enable/disable """
def SCIENCE_STREAM_OP(ser, opcode):
    data_length = ser.read(1)
    data = ser.read(int.from_bytes(data_length, "big"))
    CRC = ser.read(2)
    packet = opcode + data_length + data
    if CRC == getCRC(packet):
        if data == ON:
            return True
        elif data == OFF:
            return False
        else:
            print("Data Incorrect for Specified Operational Code!")
    else:
        print("Cyclic Redundancy Check Failed... Science Stream Operation Was Not Received Properly")
        return None
