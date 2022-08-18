"""
This module handles all serial port communications
"""
# IMPORTED MODULES
import byte
from send import *
from variables import *
import housekeeping
import science
import commands
# Time modules
from datetime import datetime
from time import time

# -----------------------------------------SEND/RECEIVE FUNCTIONS----------------------------------------------------- #

""" When connection is established, sends a housekeeping request every 10 seconds and a science request every second """
def scheduler(app):
    if serial_port[0] is None:
        pass
    else:
        while app.power and not app.exit.is_set():
            send_data(byte.CDH_HK_REQUEST, None)  # send housekeeping request

            for i in range(0, 10):
                d1 = datetime(1970, 1, 1, 0, 0, 0)
                d2 = datetime(1980, 1, 6, 0, 0, 0)
                current_time = int(time() - (d2 - d1).total_seconds())

                send_data(byte.CDH_TIME_OF_TONE, int.to_bytes(current_time, 4, "little"))

                app.exit.wait(1)


""" sends data through the serial port/ builds packet based on op-code and data """
def send_data(opcode, data):
    if serial_port[0] is None:
        print("No Connection Established... Data Will Not Be Transmitted or Received!")
    else:
        match opcode:
            case byte.CDH_HK_REQUEST:
                HK_REQ(serial_port[0])
            case byte.CDH_SCI_REQUEST:
                SCI_REQ(serial_port[0])
            case byte.CDH_CONFIG_REQUEST:
                CONFIG_REQ(serial_port[0])
            case byte.CDH_CONFIG_OP:
                CONFIG_OP(serial_port[0], data)
            case byte.CDH_ANALOG_CTRL:
                ANALOG_CTRL(serial_port[0], data)
            case byte.CDH_SCALAR1_CTRL:
                SCALAR1_CTRL(serial_port[0], data)
            case byte.CDH_SCALAR2_CTRL:
                SCALAR2_CTRL(serial_port[0], data)
            case byte.CDH_STAR_TRACK1_CTRL:
                STAR_TRACK1_CTRL(serial_port[0], data)
            case byte.CDH_STAR_TRACK2_CTRL:
                STAR_TRACK2_CTRL(serial_port[0], data)
            case byte.CDH_TIME_OF_TONE:
                TIME_OF_TONE(serial_port[0], data)
            case byte.CDH_SCIENCE_STREAM_CTRL:
                SCIENCE_STREAM_CTRL(serial_port[0], data)
            case _:
                # should never enter default case
                print("Something Went Horribly Wrong...")


""" Check for data in the UART port and perform the required action based on the given operational code """
def receive_data():
    # create a deque for the sync patter
    check = deque([bytes(0), bytes(0), bytes(0), bytes(0)])

    while True:
        # populate the sync pattern deque and check it alongside the actual sync pattern
        check.popleft()
        check.append(serial_port[0].read(1))
        if bytes(0).join(check) == byte.SYNC_PATTERN:
            opcode = serial_port.read(1)
            # find the corresponding op code which will call the necessary function to process the data
            match opcode:
                case byte.VRUM_HK_OUT_OP:
                    housekeeping.update_housekeeping(HK_OUT_OP(serial_port[0], opcode))
                    if housekeeping_display[0] is True:
                        housekeeping.update_housekeeping_display()
                    break
                case byte.VRUM_SCI_OUT_OP:
                    science.update_science(SCI_OUT_OP(serial_port[0], opcode))
                    if science_display[0] is True:
                        science.update_science_display()
                    break
                case byte.VRUM_CONFIG_OUT_OP:
                    data = CONFIG_OUT_OP(serial_port[0], opcode)
                    commands.update_config(data)
                    break
                case byte.VRUM_CONFIG_ACK_OP:
                    result = CONFIG_ACK_OP(serial_port[0], opcode)
                    if result is True:
                        CONFIG_REQ(serial_port[0])
                    else:
                        print("Packet Not Properly Received, Configuration Not Updated!")
                    break
                case byte.VRUM_ANALOG_OP:
                    result = ANALOG_OP(serial_port[0], opcode)
                    if result is True:
                        commands.change_led(result, 0)
                        print("Request to activate the analog board has been received!")
                    elif result is False:
                        commands.change_led(result, 0)
                        print("Request to deactivate the analog board has been received!")
                    else:
                        print("Failure to read data!")
                    break
                case byte.VRUM_SCALAR1_OP:
                    result = SCALAR1_OP(serial_port[0], opcode)
                    if result is True:
                        commands.change_led(result, 1)
                        print("Request to activate scalar board no.1 has been received!")
                    elif result is False:
                        commands.change_led(result, 1)
                        print("Request to deactivate scalar board no.1 has been received!")
                    else:
                        print("Failure to read data!")
                    break
                case byte.VRUM_SCALAR2_OP:
                    result = SCALAR2_OP(serial_port[0], opcode)
                    if result is True:
                        commands.change_led(result, 2)
                        print("Request to activate scalar board no.2 has been received!")
                    elif result is False:
                        commands.change_led(result, 2)
                        print("Request to deactivate scalar board no.2 has been received!")
                    else:
                        print("Failure to read data!")
                    break
                case byte.VRUM_STAR_TRACK1_OP:
                    result = STAR_TRACK1_OP(serial_port[0], opcode)
                    if result is True:
                        commands.change_led(result, 3)
                        print("Request to activate star tracker no.1 has been received!")
                    elif result is False:
                        commands.change_led(result, 3)
                        print("Request to deactivate star tracker no.1 has been received!")
                    else:
                        print("Failure to read data!")
                    break
                case byte.VRUM_STAR_TRACK2_OP:
                    result = STAR_TRACK2_OP(serial_port[0], opcode)
                    if result is True:
                        commands.change_led(result, 4)
                        print("Request to activate star tracker no.2 has been received!")
                    elif result is False:
                        commands.change_led(result, 4)
                        print("Request to deactivate star tracker no.2 has been received!")
                    else:
                        print("Failure to read data!")
                    break
                case byte.VRUM_TIME_ACK_OP:
                    result = TIME_ACK_OP(serial_port[0], opcode)
                    if result is True:
                        pass
                    elif result is False:
                        print("Failed to receive time of tone acknowledge!")
                    else:
                        print("Failed to receive time of tone acknowledge!")
                    break
                case byte.VRUM_SCIENCE_STREAM_OP:
                    result = SCIENCE_STREAM_OP(serial_port[0], opcode)
                    if result is True:
                        pass
                    elif result is False:
                        pass
                    else:
                        print("Failure to read data!")
                    break
                case _:
                    print("No Corresponding Operational Code Found... Data Not Interpreted!")
                    break


""" always searches for data in bus and locks sending until the data is received """
def uart_driver():
    if serial_port[0] is None:
        print("No Connection Established... Data Will Not Be Transmitted or Received!")
    else:
        while True:
            if serial_port[0].in_waiting > 0:
                receive_data()
