"""
This module finds all the ports that are available on the specified device and connects to the correct one. If the
user requests a new port, these functions will also handel switching the com ports
"""
# IMPORTED MODULES
from variables import serial_port, port_flag
from communications import scheduler, uart_driver
from threading import Thread
# Serial modules
import serial.tools.list_ports
import serial
# GUI modules
import customtkinter as ctk
from tkinter import DISABLED, NORMAL, StringVar


# -------------------------------------------FIND SERIAL PORT--------------------------------------------------------- #

""" gets all the ports on the device """
def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


""" return a list of all the ports """
def get_all_ports():
    # Find all ports
    portsFound = get_ports()

    # Number of found ports
    numConnection = len(portsFound)

    # Create a list of ports
    ports = []

    # Loop through all found ports
    for i in range(0, numConnection):
        port = portsFound[i]
        # strPort = str(port)
        #
        # # Find specific port that is being looked for (must be wired connection)
        # if 'Serial' in strPort and 'Bluetooth' not in strPort:
        #     splitPort = strPort.split(' ')
        #     ports.append(splitPort[0])
        ports.append(str(port))

    if not ports:
        ports.append("No Available Ports")

    return ports


""" find the com port to be used """
def findCOM(portsFound):
    # Sets default to no ports found
    commPort = 'None'
    # Number of found ports
    numConnection = len(portsFound)

    # Loop through all found ports
    for i in range(0, numConnection):
        port = portsFound[i]
        strPort = str(port)

        # Find specific port that is being looked for
        if 'Serial' in strPort and 'Bluetooth' not in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort


""" connect to the com port that is found in findCOM """
def Connect_to_Port():
    connectPort = findCOM(get_ports())

    # If a port is found, create the serial port connection
    if connectPort != 'None':
        ser = serial.Serial(connectPort, baudrate=115200, timeout=1)
        print('Connected to ' + connectPort)
        port_flag.clear()
        port_flag.append(True)
        return ser

    else:
        print('Connection Issue!')
        return None


# --------------------------------------CHANGE SERIAL PORT/ GET PROPERTIES-------------------------------------------- #

""" connects to a new port (This function has given problems in the past // frankly it is not used often and has
not been properly tested) """
def new_port(Commands):
    def close_display():
        com_window.destroy()
        Commands.change_com.state = NORMAL

    def scan_for_ports():
        ports = get_all_ports()
        counter = 0
        for i in range(0, len(ports)):
            button = ctk.CTkButton(master=port_frame,
                                   text=ports[i],
                                   fg_color="#1a1a1a",
                                   corner_radius=0,
                                   command=lambda idx=counter: change_port(idx, ports))
            button.grid(row=counter, column=0, sticky="new", padx=10, pady=5)
            counter += 1

    def change_port(idx, ports):
        if ports[idx].split(' ')[0][:3] == "COM":
            text_var.set("Selected COM Port: " + ports[idx].split(' ')[0])
            submit.state = NORMAL

    def new_port_settings():
        serial_port.clear()
        serial_port.append(serial.Serial(text_var.get()[-4:], baudrate=int(baud.get()), timeout=1))
        print("Now Connected to " + text_var.get()[-4:])
        submit.state = DISABLED
        properties = get_serial_properties(serial_port[0])
        Commands.connection_label.configure(text=serial_name(serial_port[0]))

        Commands.baud_rate_label.configure(text="Rate: " + properties[0])

        Commands.byte_size_label.configure(text="Byte Size: " + properties[1])

        Commands.parity_label.configure(text="Parity: " + properties[2])

        Commands.stop_bits_label.configure(text="Stop Bits: " + properties[3])

        t1 = Thread(target=scheduler)
        t2 = Thread(target=uart_driver)

        t1.daemon = True
        t2.daemon = True

        t1.start()
        t2.start()

    com_window = ctk.CTkToplevel()
    com_window.geometry("550x365")
    com_window.title("Change COM Port")
    com_window.resizable(False, False)
    com_window.protocol("WM_DELETE_WINDOW", close_display)
    Commands.change_com.state = DISABLED

    """ Create frames for display and commands """
    com_window.rowconfigure(0, weight=15)
    com_window.rowconfigure(1, weight=1)

    com_window.columnconfigure(0, weight=1)

    port_frame = ctk.CTkFrame(master=com_window,
                              corner_radius=0)
    port_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=5)

    port_controls = ctk.CTkFrame(master=com_window,
                                 fg_color="#1a1a1a")
    port_controls.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)

    """ Add label to frame """
    port_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    port_frame.columnconfigure(0, weight=1)

    com_ports = ctk.CTkLabel(master=port_frame,
                             text=" ")
    com_ports.grid(row=0, column=0, sticky="nws", padx=5, pady=5)

    """ Add buttons to controls """
    port_controls.rowconfigure((0, 1, 2), weight=1)
    port_controls.columnconfigure((0, 1, 2, 3), weight=1)

    text_var = StringVar(value="Selected COM Port: None")

    selected_port = ctk.CTkLabel(master=port_controls,
                                 textvariable=text_var)
    selected_port.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    scan = ctk.CTkButton(master=port_controls,
                         text="Scan 🗘",
                         command=scan_for_ports)
    scan.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    baud = ctk.CTkOptionMenu(master=port_controls,
                             values=["115200"])
    baud.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    parity = ctk.CTkOptionMenu(master=port_controls,
                               values=["None"])
    parity.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

    stop = ctk.CTkOptionMenu(master=port_controls,
                             values=["1"])
    stop.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    submit = ctk.CTkButton(master=port_controls,
                           text="Change Port",
                           command=new_port_settings)
    submit.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

    submit.state = DISABLED


""" returns the serial port properties """
def get_serial_properties(ser):
    if ser is None:
        return ["Not Connected", "Not Connected", "Not Connected", "Not Connected"]
    else:
        baud_rate = str(ser.baudrate) + " bits per second"
        byte_size = str(ser.bytesize) + " bits"
        parity_bit = str(ser.parity)
        stop_bit = str(ser.stopbits) + " bit(s)"
        return [baud_rate, byte_size, parity_bit, stop_bit]


""" returns the serial port name """
def serial_name(ser):
    if ser is None:
        return "Not Connected to a Port!"
    else:
        return "Connected to " + ser.name
