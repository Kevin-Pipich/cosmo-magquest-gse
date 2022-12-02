"""
This module handles the configuration functions for the commands page. It also is responsible for requesting packets
from the PIC and changing the LED lights on the analog board control frame.
"""
# IMPORTED MODULES
from variables import *
from byte import CDH_CONFIG_OP, CDH_MAG_GAIN_CONFIG, ON, OFF
import communications
from send import SCIENCE_STREAM_CTRL, SCI_REQ
# GUI modules
import customtkinter as ctk
# Image modules
from PIL import ImageTk, Image

# -------------------------------------------CONFIGURATION FUNCTIONS-------------------------------------------------- #

""" takes in values from input boxes on GUI and sends a command to change frequencies and amplitudes """
def new_config():
    try:
        int(frequencies[0].get())
        int(frequencies[1].get())
        int(frequencies[2].get())
        values = True
    except ValueError:
        values = False
    if values:
        if (int(frequencies[0].get()) > 3900 or int(frequencies[1].get()) > 3900 or
                int(frequencies[2].get()) > 3900 or int(frequencies[0].get()) < 0 or
                int(frequencies[1].get()) < 0 or int(frequencies[2].get()) < 0):
            window = ctk.CTkToplevel()
            window.geometry("350x75")
            window.title("WARNING!")
            window.resizable(False, False)
            # create warning label
            label = ctk.CTkLabel(window, text="Coil frequencies must be greater than 0 Hz\n and less than 3900 Hz!"
                                              "\nPlease enter accepted values")
            label.pack(side="top", fill="both", expand=True)
        else:
            # retrieve all frequencies and amplitudes to be combined into a hex value
            freq_1_bytes = int(round((float(frequencies[0].get())) * 2 ** 28 / 16E6)).to_bytes(2, "little")
            freq_2_bytes = int(round((float(frequencies[1].get())) * 2 ** 28 / 16E6)).to_bytes(2, "little")
            freq_3_bytes = int(round((float(frequencies[2].get())) * 2 ** 28 / 16E6)).to_bytes(2, "little")

            amp_1_bytes = int(user_amplitudes[0].get()).to_bytes(1, "little")
            amp_2_bytes = int(user_amplitudes[1].get()).to_bytes(1, "little")
            amp_3_bytes = int(user_amplitudes[2].get()).to_bytes(1, "little")

            match int(scalar_values[0].get()):
                case 115200:
                    baud_bytes = b'\x00'
                case 230400:
                    baud_bytes = b'\x01'
                case 460800:
                    baud_bytes = b'\x02'
                case 921600:
                    baud_bytes = b'\x03'
                case _:
                    baud_bytes = b'\x00'
                    print("Baud rate could not be read, default to 115200...")

            match scalar_values[1].get():
                case "100 Hz":
                    sample_bytes = b'\x64'
                case "250 Hz":
                    sample_bytes = b'\xfa'
                case _:
                    sample_bytes = b'\x00'
                    print("Sample rate could not be read, default to 100 Hz...")

            # create string in order to build packet
            final_string = freq_1_bytes + freq_2_bytes + freq_3_bytes + amp_1_bytes + amp_2_bytes + amp_3_bytes + \
                           baud_bytes + sample_bytes
            communications.send_data(CDH_CONFIG_OP, final_string)
    else:
        window = ctk.CTkToplevel()
        window.geometry("300x75")
        window.title("WARNING!")
        window.resizable(False, False)
        # create warning label
        label = ctk.CTkLabel(window, text="Entry must be an integer value!\n Please enter an integer value before "
                                          "submitting")
        label.pack(side="top", fill="both", expand=True)


""" updates the current configuration box in the command GUI for the analog config """
def update_config(config):
    current_frequencies[0].configure(text=str(round(int.from_bytes(config[0:2], "little") * (16E6 / 2 ** 28)))
                                          + " Hz")

    current_amplitudes[0].configure(text=str(int(int.from_bytes(config[6:7], "big") * 100 / 127)) + "%")

    current_frequencies[1].configure(text=str(round(int.from_bytes(config[2:4], "little") * (16E6 / 2 ** 28)))
                                          + " Hz")

    current_amplitudes[1].configure(text=str(int(int.from_bytes(config[7:8], "big") * 100 / 127)) + "%")

    current_frequencies[2].configure(text=str(round(int.from_bytes(config[4:6], "little") * (16E6 / 2 ** 28)))
                                          + " Hz")

    current_amplitudes[2].configure(text=str(int(int.from_bytes(config[8:9], "big") * 100 / 127)) + "%")

    current_scalar_sample_rate[0].configure(text=str(config[10]) + " Hz")

    match config[9]:
        case 0:
            baud = "115200"
        case 1:
            baud = "230400"
        case 2:
            baud = "460800"
        case 3:
            baud = "921600"
        case _:
            baud = " "

    current_scalar_baud_rate[0].configure(text=baud)

    amplitude_bars[0].set(int(current_amplitudes[0].text[:-1]) / 100)
    amplitude_bars[1].set(int(current_amplitudes[1].text[:-1]) / 100)
    amplitude_bars[2].set(int(current_amplitudes[2].text[:-1]) / 100)


""" restores the configuration to the default """
def restore_default():
    frequencies[0].set("9")
    frequencies[1].set("16")
    frequencies[2].set("20")

    amplitudes[0].set(127)
    amplitudes[1].set(112)
    amplitudes[2].set(114)

    amplitude_labels[0].configure(text=str(int(127 * 100 / 127)) + " %")
    amplitude_labels[1].configure(text=str(int(112 * 100 / 127)) + " %")
    amplitude_labels[2].configure(text=str(int(114 * 100 / 127)) + " %")

    scalar_values[0].set("115200")
    scalar_values[1].set("100 Hz")

    new_config()


""" changes the label for amplitude of the specified coil """
def change_amp_1(value):
    amplitude_labels[0].configure(text=str(int(value * 100 / 127)) + " %")


""" changes the label for amplitude of the specified coil """
def change_amp_2(value):
    amplitude_labels[1].configure(text=str(int(value * 100 / 127)) + " %")


""" changes the label for amplitude of the specified coil """
def change_amp_3(value):
    amplitude_labels[2].configure(text=str(int(value * 100 / 127)) + " %")


""" takes in values from input boxes in the GUI and sends a new gain configuration to be sent to the magnetometer"""
def new_gain():
    try:
        int(gain[0].get())
        value = True
    except ValueError:
        value = False
    if value:
        if int(gain[0].get()) > 65535 or int(gain[0].get()) < 0:
            window = ctk.CTkToplevel()
            window.geometry("350x75")
            window.title("WARNING!")
            window.resizable(False, False)
            # create warning label
            label = ctk.CTkLabel(window, text="Gain value must be greater than 0 \n and less than 65535!"
                                              "\nPlease enter accepted values")
            label.pack(side="top", fill="both", expand=True)
        else:
            gain_bytes = int(round(float(gain[0].get()))).to_bytes(2, "little")
            communications.send_data(CDH_MAG_GAIN_CONFIG, gain_bytes)
    else:
        window = ctk.CTkToplevel()
        window.geometry("300x75")
        window.title("WARNING!")
        window.resizable(False, False)
        # create warning label
        label = ctk.CTkLabel(window, text="Entry must be an integer value!\n Please enter an integer value before "
                                          "submitting")
        label.pack(side="top", fill="both", expand=True)


# ------------------------------------------------PACKET REQUESTS----------------------------------------------------- #

""" requests a science packet from the PIC """
def request_science():
    if serial_port[0] is None:
        print("No Connection Established... Data Will Not Be Transmitted or Received!")
    else:
        SCI_REQ(serial_port[0])


""" enables/disables the ability to stream science data """
def stream_science():
    if serial_port[-1] is None:
        print("No Connection Established... Data Will Not Be Transmitted or Received!")
    else:
        match stream_science_checkbox[0].get():
            case 1:
                SCIENCE_STREAM_CTRL(serial_port[-1], ON)
                print("Science data now streaming")
            case 0:
                SCIENCE_STREAM_CTRL(serial_port[-1], OFF)
                print("Science data no longer streaming")


# --------------------------------------------------AESTHETICS-------------------------------------------------------- #

""" changes the LED for the boards based on their operation state (on/ off) """
def change_led(result, light):
    if result:
        img = ImageTk.PhotoImage(Image.open("green_button.png").resize((65, 65)))  # green light = ON
    else:
        img = ImageTk.PhotoImage(Image.open("red_button.png").resize((65, 65)))  # red light = OFF
    board_led[light].configure(image=img)
    board_led[light].image = img
