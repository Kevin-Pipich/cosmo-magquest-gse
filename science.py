"""
This module houses all functions that relate to the science packet and magnetometer plots. All science data processing
will be handled in this module.
"""
# IMPORTED MODULES
from variables import *
# GUI modules
import customtkinter as ctk
from tkinter import TOP, NORMAL, DISABLED
# Threading modules
from threading import Thread
# File modules
from tkinter import filedialog
import os
import csv
# Time modules
from datetime import datetime
from time import gmtime, strftime, time
# Data processing modules
import numpy as np
from scipy import signal
# Image modules
from PIL import ImageTk, Image


""" organizes science packet into usable data """
def update_science(science):
    packet_data_length = int.from_bytes(science[4:5], "big")
    """ Time Data """
    time_since_1980 = int.from_bytes(science[7:10], "big")  # 2 bytes big endian

    # Determine the time between the epoch and the day GPS was stirred to UTC
    d1 = datetime(1970, 1, 1, 0, 0, 0)
    d2 = datetime(1980, 1, 6, 0, 0, 0)

    current_time = strftime("%A, %B %d, %Y %H:%M:%S", gmtime(time_since_1980 + (d2 - d1).total_seconds()))

    # save time from GPS
    Science_Time.append(current_time)

    """ Nano-Star Tracker 1 Data """
    # Attitude Quaternion
    Beta_0 = int.from_bytes(science[11:14], "big")
    Beta_1 = int.from_bytes(science[15:18], "big")
    Beta_2 = int.from_bytes(science[19:22], "big")
    Beta_3 = int.from_bytes(science[23:26], "big")

    attitude_quaternion = [Beta_0, Beta_1, Beta_2, Beta_3]

    # Angular Velocity
    ang_vel_1 = int.from_bytes(science[27:28], "big")
    ang_vel_2 = int.from_bytes(science[29:30], "big")
    ang_vel_3 = int.from_bytes(science[31:32], "big")

    angular_velocity = [ang_vel_1, ang_vel_2, ang_vel_3]

    tracker_right_ascension = int.from_bytes(science[33:34], "big")
    declination = int.from_bytes(science[35:36], "big")
    tracker_roll = int.from_bytes(science[37:38], "big")

    # Attitude Covariance
    COV_1 = int.from_bytes(science[39:42], "big")
    COV_2 = int.from_bytes(science[43:46], "big")
    COV_3 = int.from_bytes(science[47:50], "big")
    COV_4 = int.from_bytes(science[51:54], "big")
    COV_5 = int.from_bytes(science[55:58], "big")
    COV_6 = int.from_bytes(science[59:62], "big")

    attitude_covariance = [COV_1, COV_2, COV_3, COV_4, COV_5, COV_6]

    nano_star_tracker_1_data = [attitude_quaternion, angular_velocity, tracker_right_ascension, declination,
                                tracker_roll, attitude_covariance]
    # save data from NST 1 - in form specified as in TAB-PLD-002 VRuM FSW Specifications
    NST_1.append(nano_star_tracker_1_data)

    """ Nano-Star Tracker 2 Data """
    # Attitude Quaternion
    Beta_0 = int.from_bytes(science[63:66], "big")
    Beta_1 = int.from_bytes(science[67:70], "big")
    Beta_2 = int.from_bytes(science[71:74], "big")
    Beta_3 = int.from_bytes(science[75:78], "big")

    attitude_quaternion = [Beta_0, Beta_1, Beta_2, Beta_3]

    # Angular Velocity
    ang_vel_1 = int.from_bytes(science[79:80], "big")
    ang_vel_2 = int.from_bytes(science[81:82], "big")
    ang_vel_3 = int.from_bytes(science[83:84], "big")

    angular_velocity = [ang_vel_1, ang_vel_2, ang_vel_3]

    tracker_right_ascension = int.from_bytes(science[85:86], "big")
    declination = int.from_bytes(science[87:88], "big")
    tracker_roll = int.from_bytes(science[89:90], "big")

    # Attitude Covariance
    COV_1 = int.from_bytes(science[91:94], "big")
    COV_2 = int.from_bytes(science[95:98], "big")
    COV_3 = int.from_bytes(science[99:102], "big")
    COV_4 = int.from_bytes(science[103:106], "big")
    COV_5 = int.from_bytes(science[107:110], "big")
    COV_6 = int.from_bytes(science[111:114], "big")

    attitude_covariance = [COV_1, COV_2, COV_3, COV_4, COV_5, COV_6]

    nano_star_tracker_2_data = [attitude_quaternion, angular_velocity, tracker_right_ascension, declination,
                                tracker_roll, attitude_covariance]
    # save data from NST 2 - in form specified as in TAB-PLD-002 VRuM FSW Specifications
    NST_2.append(nano_star_tracker_2_data)

    """ Scalar Magnetometer Data and State """
    flag = False
    for i in range(118, packet_data_length, 4):
        Raw_Scalar_Magnetometer_Data.append(int.from_bytes(science[i:i + 3], "big"))  # Reads 4 bytes of mag out
        Raw_Scalar_Magnetometer_State.append(int.from_bytes(science[i + 4], "big"))  # Reads 1 byte of state
        if Raw_Scalar_Magnetometer_State[-1] != Raw_Scalar_Magnetometer_State[-2]:
            t3 = Thread(target=update_state)
            t3.daemon = True
            t3.start()
            if i > 118:
                flag = True
    Scalar_Magnetometer_Data.append(np.mean(Raw_Scalar_Magnetometer_Data[-100:]))  # average of all the raw scalar data
    State_Change.append(flag)

    # Frequency domain representation
    dt = int(current_scalar_sample_rate[0].text[:-3])  # sample rate

    n = len(Raw_Scalar_Magnetometer_Data[-100:])  # take a fft of the 100 data points given each second
    fhat = np.fft.fft(Raw_Scalar_Magnetometer_Data[-100:], n)
    FFT_amp = fhat * np.conj(fhat) / n
    freq = (1 / (dt * n)) * np.arange(n)
    L = np.arange(1, np.floor(n / 2), dtype='int')

    PSD.append(FFT_amp[L].real)
    Freq.append(freq[L])

    Spec_data = np.ndarray((len(Raw_Scalar_Magnetometer_Data) - 1,), buffer=np.array(Raw_Scalar_Magnetometer_Data),
                           offset=np.int_().itemsize,
                           dtype=int)

    f, t, Sxx = signal.spectrogram(Spec_data, dt)

    Spec_f.append(f)
    Spec_t.append(t)
    Spec_Sxx.append(Sxx)

    # Save data to csv file if checked
    if write_checkbox[0].get() == 1:
        save_to_file()

    plot_science()


""" updates science plots live, time domain and frequency domain """
def plot_science():
    """ Time domain plot """
    # Rescale the voltage axes if necessary
    if max(Scalar_Magnetometer_Data) > magnetometer_limits[1]:
        magnetometer_limits[0:1] = [magnetometer_limits[0], max(Scalar_Magnetometer_Data) * 1.05]
        sci_axes[0].set_ylim(magnetometer_limits)
        sci_axes_background[0] = sci_fig[0].canvas.copy_from_bbox(sci_axes[0].bbox)
    if min(Scalar_Magnetometer_Data) < magnetometer_limits[0]:
        magnetometer_limits[0:1] = [min(Scalar_Magnetometer_Data) * 0.95, max(Scalar_Magnetometer_Data) * 1.05]
        sci_axes[0].set_ylim(magnetometer_limits)
        sci_axes_background[0] = sci_fig[0].canvas.copy_from_bbox(sci_axes[0].bbox)
    if (max(Scalar_Magnetometer_Data) - min(Scalar_Magnetometer_Data) * 2) < \
            (magnetometer_limits[1] - magnetometer_limits[0]) \
            and max(Scalar_Magnetometer_Data) != 0 and min(Scalar_Magnetometer_Data) != 0:
        magnetometer_limits[0:1] = [min(Scalar_Magnetometer_Data) * 0.95, max(Scalar_Magnetometer_Data) * 1.05]
        sci_axes[0].set_ylim(magnetometer_limits)
        sci_axes_background[0] = sci_fig[0].canvas.copy_from_bbox(sci_axes[0].bbox)

    if max(Scalar_Magnetometer_Data) == 0 and min(Scalar_Magnetometer_Data) == 0:
        sci_fig[0].canvas.restore_region(sci_axes_background[0])
    else:
        sci_fig[0].canvas.restore_region(sci_axes_background[0])
        artist_3[0].set_xdata(Science_Time[:][24:])
        artist_3[0].set_ydata(Scalar_Magnetometer_Data)

    """ Frequency Domain Plot """
    # Rescale the voltage axes if necessary
    if max(PSD[-1]) > fft_limits[1]:
        fft_limits[0:1] = [fft_limits[0], max(PSD[-1]) * 1.05]
        sci_axes[1].set_ylim(fft_limits)
        sci_axes_background[1] = sci_fig[1].canvas.copy_from_bbox(sci_axes[1].bbox)
    if min(PSD[-1]) < fft_limits[0]:
        fft_limits[0:1] = [min(PSD[-1]) * 0.95, max(PSD[-1]) * 1.05]
        sci_axes[1].set_ylim(fft_limits)
        sci_axes_background[1] = sci_fig[1].canvas.copy_from_bbox(sci_axes[1].bbox)
    if (max(PSD[-1]) - min(PSD[-1]) * 2) < \
            (fft_limits[1] - fft_limits[0]) \
            and max(PSD[-1]) != 0 and min(PSD[-1]) != 0:
        fft_limits[0:1] = [min(PSD[-1]) * 0.95, max(PSD[-1]) * 1.05]
        sci_axes[0].set_ylim(fft_limits)
        sci_axes_background[1] = sci_fig[1].canvas.copy_from_bbox(sci_axes[1].bbox)

    if max(PSD[-1]) == 0 and min(PSD[-1]) == 0:
        sci_fig[1].canvas.restore_region(sci_axes_background[1])
    else:
        sci_fig[1].canvas.restore_region(sci_axes_background[1])
        artist_3[1].set_xdata(Freq[-1])
        artist_3[1].set_ydata(PSD[-1])

    """ Magnetometer Spectrogram """
    sci_axes[2].clear()
    sci_axes[2].pcolormesh(Spec_t[-1], Spec_f[-1], Spec_Sxx[-1], shading='gouraud')
    sci_axes[2].set_ylabel("Frequency [Hz]")
    sci_axes[2].set_xlabel("Time [s]")
    sci_axes[2].set_title("Magnetometer Spectrogram")


""" updates the magnetometer state live """
def update_state():
    match Raw_Scalar_Magnetometer_State[-1]:
        case 3:
            state_label[0].configure(text="Warm Up")

            orange_img = ImageTk.PhotoImage(Image.open("orange_button.png").resize((100, 100)))
            led_image[0].configure(image=orange_img)
            led_image[0].image = orange_img
            return
        case 4:
            state_label.configure(text="Laser Lock\nScan")

            green_img = ImageTk.PhotoImage(Image.open("green_button.png").resize((100, 100)))
            led_image[0].configure(image=green_img)
            led_image[0].image = green_img
            return
        case 5:
            state_label.configure(text="Scan for\nMagnetic\nResonance")

            blue_img = ImageTk.PhotoImage(Image.open("blue_button.png").resize((100, 100)))
            led_image[0].configure(image=blue_img)
            led_image[0].image = blue_img
            return
        case 6:
            state_label.configure(text="Magnetic\nLock")

            blue_img = ImageTk.PhotoImage(Image.open("blue_button.png").resize((100, 100)))
            led_image[0].configure(image=blue_img)
            led_image[0].image = blue_img
        case _:
            pass


""" creates a new window displaying the live science data """
def new_science_display(Science):
    science_display.clear()
    science_display.append(True)

    def close_display():
        science_display.clear()
        science_display.append(False)
        sci_display_window.destroy()
        Science.display_button.state = NORMAL

    sci_display_window.clear()
    sci_display_window.append(ctk.CTkToplevel())
    sci_display_window.geometry("538x750")
    sci_display_window.title("Live Science Data")
    sci_display_window.resizable(False, False)
    sci_display_window.protocol("WM_DELETE_WINDOW", close_display)
    Science.display_button.state = DISABLED

    if Scalar_Magnetometer_Data[-1] != 0:
        update_science_display()
    else:
        label = ctk.CTkLabel(master=sci_display_window,
                             text="No Data to Display!")
        label.pack(side=TOP, expand=True)


""" updates values in the live science display """
def update_science_display():
    match Raw_Scalar_Magnetometer_State[-1]:
        case 3:
            current_state = "Warm Up"
        case 4:
            current_state = "Laser Lock Scan"
        case 5:
            current_state = "Scan for Magnetic Resonance"
        case 6:
            current_state = "Magnetic Lock"
        case _:
            current_state = "Off"

    label1 = ctk.CTkLabel(master=sci_display_window,
                          text="=============== Time ===============\n\n"
                               + str(Science_Time[-1]) + "\n\n" +
                               "=============== Magnetometer Data ===============" +
                               "\n\n" + "Current State: " + current_state + "\n\n" +
                               "Average Magnetic Field: " + str(Scalar_Magnetometer_Data[-1])
                               + " nT\n\n")
    label1.grid(row=0, column=0, columnspan=2)

    label2 = ctk.CTkLabel(master=sci_display_window,
                          text="=============== NST 1 ===============\n\n" +
                               "Attitude Quaternions\nβ\u2080: " + str(NST_1[-1][0][0]) + "\n\nβ\u2081: " +
                               str(NST_1[-1][0][1]) + "\n\nβ\u2082: " + str(NST_1[-1][0][2]) + "\n\nβ\u2083: " +
                               str(NST_1[-1][0][3]) + "\n\nAngular Velocity\nω\u2081: " + str(NST_1[-1][1][0])
                               + "\n\nω\u2082: " + str(NST_1[-1][1][1]) + "\n\nω\u2083: " + str(
                              NST_1[-1][1][2]) +
                               "\n\nTracker Right Ascension: " + str(NST_1[-1][2]) + "\n\nDeclination: " +
                               str(NST_1[-1][3]) + "\n\nTracker Roll: " + str(NST_1[-1][4]) +
                               "\n\nAttitude Covariance\nCOV 1: " + str(NST_1[-1][5][0]) + "\n\nCOV 2: "
                               + str(NST_1[-1][5][1]) + "\n\nCOV 3: " + str(NST_1[-1][5][2]) + "\n\nCOV 4: " +
                               str(NST_1[-1][5][3]) + "\n\nCOV 5: " + str(NST_1[-1][5][4]) + "\n\nCOV 6: " +
                               str(NST_1[-1][5][5]))
    label2.grid(row=1, column=0)

    label3 = ctk.CTkLabel(master=sci_display_window,
                          text="=============== NST 2 ===============\n\n" +
                               "Attitude Quaternions\nβ\u2080: " + str(NST_2[-1][0][0]) + "\n\nβ\u2081: " +
                               str(NST_2[-1][0][1]) + "\n\nβ\u2082: " + str(NST_2[-1][0][2]) + "\n\nβ\u2083: " +
                               str(NST_2[-1][0][3]) + "\n\nAngular Velocity\nω\u2081: " + str(NST_2[-1][1][0])
                               + "\n\nω\u2082: " + str(NST_2[-1][1][1]) + "\n\nω\u2083: " + str(
                              NST_2[-1][1][2]) +
                               "\n\nTracker Right Ascension: " + str(NST_2[-1][2]) + "\n\nDeclination: " +
                               str(NST_2[-1][3]) + "\n\nTracker Roll: " + str(NST_2[-1][4]) +
                               "\n\nAttitude Covariance\nCOV 1: " + str(NST_2[-1][5][0]) + "\n\nCOV 2: "
                               + str(NST_2[-1][5][1]) + "\n\nCOV 3: " + str(NST_2[-1][5][2]) + "\n\nCOV 4: " +
                               str(NST_2[-1][5][3]) + "\n\nCOV 5: " + str(NST_2[-1][5][4]) + "\n\nCOV 6: " +
                               str(NST_2[-1][5][5]))
    label3.grid(row=1, column=1)


""" saves all science data to a csv until user decides to save file or close GUI """
def save_to_file():
    points_saved[0].configure(text=str(points_saved[0].get() + 1))

    if points_saved[0].get() == "1":
        header = ['Timestamp', 'Magnetometer Output', 'Magnetometer State', 'β0 (NST 1)', 'β1 (NST 1)',
                  'β2 (NST 1)', 'β3 (NST 1)', 'ω1 (NST 1)', 'ω2 (NST 1)', 'ω3 (NST 1)',
                  'Tracker Right Ascension (NST 1)', 'Declination (NST 1)', 'Tracker Roll (NST 1)', 'COV1 (NST 1)',
                  'COV2 (NST 1)', 'COV3 (NST 1)', 'COV4 (NST 1)', 'COV5 (NST 1)', 'COV6 (NST 1)', 'β0 (NST 2)',
                  'β1 (NST 2)', 'β2 (NST 2)', 'β3 (NST 2)', 'ω1 (NST 2)', 'ω2 (NST 2)', 'ω3 (NST 2)',
                  'Tracker Right Ascension (NST 2)', 'Declination (NST 2)', 'Tracker Roll (NST 2)', 'COV1 (NST 2)',
                  'COV2 (NST 2)', 'COV3 (NST 2)', 'COV4 (NST 2)', 'COV5 (NST 2)', 'COV6 (NST 2)']
        filename = "Magnetometer_Data_" + strftime("%Y%m%d%H%M%S", gmtime(time())) + ".csv"

        open(filename, 'x')

        directory = filedialog.askdirectory()
        save_path = os.path.join(directory, filename)

        csvfile = open(save_path, 'w')
        # create a csv writer object
        sci_csvwriter.append(csv.writer(csvfile))

        # write the fields
        sci_csvwriter[0].writerow(header)

    row = [Science_Time[-1], Scalar_Magnetometer_Data[-1], Raw_Scalar_Magnetometer_State[-1], NST_1[-1][0][0],
           NST_1[-1][0][1], NST_1[-1][0][2], NST_1[-1][0][3], NST_1[-1][1][0], NST_1[-1][1][1], NST_1[-1][1][2],
           NST_1[-1][2], NST_1[-1][3], NST_1[-1][4], NST_1[-1][5][0], NST_1[-1][5][1], NST_1[-1][5][2],
           NST_1[-1][5][3], NST_1[-1][5][4], NST_1[-1][5][5], NST_2[-1][0][0], NST_2[-1][0][1], NST_2[-1][0][2],
           NST_2[-1][0][3], NST_2[-1][1][0], NST_2[-1][1][1], NST_2[-1][1][2], NST_2[-1][2], NST_2[-1][3],
           NST_2[-1][4], NST_2[-1][5][0], NST_2[-1][5][1], NST_2[-1][5][2], NST_2[-1][5][3], NST_2[-1][5][4],
           NST_2[-1][5][5]]
    sci_csvwriter[0].writerow(row)


""" saves csv file of science data """
def save_file():
    if points_saved[0].get() == "0":
        print("No Data Was Collected and Therefore, No Data Was Saved")
    else:
        print("Data Saved Successfully!")
    points_saved[0].configure(text="0")
    sci_csvwriter.clear()
    write_checkbox[0].deselect()
