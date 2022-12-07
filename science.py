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
from time import gmtime, strftime, time, mktime
# Data processing modules
import numpy as np
from scipy import signal
# Image modules
from PIL import ImageTk, Image

""" organizes science packet into usable data """
def update_science(science):
    if science is None:
        return

    packet_data_length = int.from_bytes(science[4:6], "big")
    """ Time Data """
    time_since_1980 = int.from_bytes(science[7:11], "big")  # 2 bytes big endian

    # Determine the time between the epoch and the day GPS was stirred to UTC
    d1 = datetime(1970, 1, 1, 0, 0, 0)
    d2 = datetime(1980, 1, 6, 0, 0, 0)

    current_time = mktime(gmtime(time_since_1980 + (d2 - d1).total_seconds()))
    # save time from GPS
    Science_Time.popleft()
    Science_Time.append(current_time)

    """ Nano-Star Tracker 1 Data """
    # Attitude Quaternion
    Beta_0 = int.from_bytes(science[11:15], "big")
    Beta_1 = int.from_bytes(science[15:19], "big")
    Beta_2 = int.from_bytes(science[19:23], "big")
    Beta_3 = int.from_bytes(science[23:27], "big")

    attitude_quaternion = [Beta_0, Beta_1, Beta_2, Beta_3]

    # Angular Velocity
    ang_vel_1 = int.from_bytes(science[27:29], "big")
    ang_vel_2 = int.from_bytes(science[29:31], "big")
    ang_vel_3 = int.from_bytes(science[31:33], "big")

    angular_velocity = [ang_vel_1, ang_vel_2, ang_vel_3]

    tracker_right_ascension = int.from_bytes(science[33:35], "big")
    declination = int.from_bytes(science[35:37], "big")
    tracker_roll = int.from_bytes(science[37:39], "big")

    # Attitude Covariance
    COV_1 = int.from_bytes(science[39:43], "big")
    COV_2 = int.from_bytes(science[43:47], "big")
    COV_3 = int.from_bytes(science[47:51], "big")
    COV_4 = int.from_bytes(science[51:55], "big")
    COV_5 = int.from_bytes(science[55:59], "big")
    COV_6 = int.from_bytes(science[59:63], "big")

    attitude_covariance = [COV_1, COV_2, COV_3, COV_4, COV_5, COV_6]

    # Tracker Status
    Operating_Mode = science[63]
    Star_ID_Step = science[64]
    Attitude_Status = science[65]
    Rate_Est_Status = science[66]

    tracker_status = [Operating_Mode, Star_ID_Step, Attitude_Status, Rate_Est_Status]

    nano_star_tracker_1_data = [attitude_quaternion, angular_velocity, tracker_right_ascension, declination,
                                tracker_roll, attitude_covariance, tracker_status]
    # save data from NST 1 - in form specified as in TAB-PLD-002 VRuM FSW Specifications
    NST_1.popleft()
    NST_1.append(nano_star_tracker_1_data)

    """ Nano-Star Tracker 2 Data """
    # Attitude Quaternion
    Beta_0 = int.from_bytes(science[67:71], "big")
    Beta_1 = int.from_bytes(science[71:75], "big")
    Beta_2 = int.from_bytes(science[75:79], "big")
    Beta_3 = int.from_bytes(science[79:83], "big")

    attitude_quaternion = [Beta_0, Beta_1, Beta_2, Beta_3]

    # Angular Velocity
    ang_vel_1 = int.from_bytes(science[83:85], "big")
    ang_vel_2 = int.from_bytes(science[85:87], "big")
    ang_vel_3 = int.from_bytes(science[87:89], "big")

    angular_velocity = [ang_vel_1, ang_vel_2, ang_vel_3]

    tracker_right_ascension = int.from_bytes(science[89:91], "big")
    declination = int.from_bytes(science[91:93], "big")
    tracker_roll = int.from_bytes(science[93:95], "big")

    # Attitude Covariance
    COV_1 = int.from_bytes(science[95:99], "big")
    COV_2 = int.from_bytes(science[99:103], "big")
    COV_3 = int.from_bytes(science[103:107], "big")
    COV_4 = int.from_bytes(science[107:111], "big")
    COV_5 = int.from_bytes(science[111:115], "big")
    COV_6 = int.from_bytes(science[115:119], "big")

    attitude_covariance = [COV_1, COV_2, COV_3, COV_4, COV_5, COV_6]

    # Tracker Status
    Operating_Mode = science[119]
    Star_ID_Step = science[120]
    Attitude_Status = science[121]
    Rate_Est_Status = science[122]

    tracker_status = [Operating_Mode, Star_ID_Step, Attitude_Status, Rate_Est_Status]

    nano_star_tracker_2_data = [attitude_quaternion, angular_velocity, tracker_right_ascension, declination,
                                tracker_roll, attitude_covariance, tracker_status]
    # save data from NST 2 - in form specified as in TAB-PLD-002 VRuM FSW Specifications
    NST_2.popleft()
    NST_2.append(nano_star_tracker_2_data)

    """ Scalar Magnetometer Data and State """
    flag = False
    for i in range(123, packet_data_length + 5, 5):
        Raw_Scalar_Magnetometer_Data.popleft()
        Magnetometer_Status.popleft()
        Mod8_Counter.popleft()
        CRC_Flag.popleft()

        Raw_Scalar_Magnetometer_Data.append(int.from_bytes(science[i:i + 4], "big"))  # Reads 4 bytes of mag out
        Raw_Scalar_Magnetometer_State = ("{:08b}".format(science[i + 4]))  # Reads 1 byte of state
        Magnetometer_Status.append(int(Raw_Scalar_Magnetometer_State[-4:], 2))  # Saves Magnetometer Status
        Mod8_Counter.append(int(Raw_Scalar_Magnetometer_State[:3], 2))  # Saves scalar "timestamp"
        CRC_Flag.append(Raw_Scalar_Magnetometer_State[3])  # Saves CRC flag

        # Confirm that the no packets were skipped
        if Mod8_Counter[-1] != Mod8_Counter[-2] + 1 and not (Mod8_Counter[-2] == 7 and Mod8_Counter[-1] == 0) and \
                not (Mod8_Counter[-2] == 0 and Mod8_Counter[-1] == 0) and i != 123:
            if Mod8_Counter[-2] > Mod8_Counter[-1]:
                skipped_packets = 7 - Mod8_Counter[-2] + Mod8_Counter[-1]
            else:
                skipped_packets = Mod8_Counter[-1] - Mod8_Counter[-2]
            print("Packet Skipped!\nNumber of Skipped Packets: " + str(int(skipped_packets)))

        # Confirm the CRC Flag is correct
        if int(CRC_Flag[-1]) != 1:
            crc_failure(False)
            print("Scalar Transmission of CRC Failed! Packet #" + str(int(((i-123)/5))+1))
        else:
            if sci_CRC_label[0].text == "No Connection!" or sci_CRC_label[0].text == "CRC Failed!":
                crc_failure(True)
            else:
                pass

        # Check if the status of the magnetometer has changed
        if Magnetometer_Status[-1] != Magnetometer_Status[-2]:
            t3 = Thread(target=update_state)
            t3.daemon = True
            t3.start()
            flag = True

        Magnetometer_State.popleft()
        Magnetometer_State.append(Magnetometer_Status[-1])

    mag_data = []
    for i in range(0, 100):
        mag_data.append(Raw_Scalar_Magnetometer_Data[-i] * 4e6/(pow(2, 32) - 1)/6.99583)
    Scalar_Magnetometer_Data.popleft()
    State_Change.popleft()
    Scalar_Magnetometer_Data.append(np.mean(mag_data))  # average of all the raw scalar data
    State_Change.append(flag)

    # Frequency domain representation
    dt = int(current_scalar_sample_rate[0].text[:-3])  # sample rate
    #
    # n = len(mag_data)  # take a fft of the 100 data points given each second
    # f_hat = np.fft.fft(mag_data, n)
    # FFT_amp = f_hat * np.conj(f_hat) / n
    # freq = (1 / (dt * n)) * np.arange(n)
    # L = np.arange(1, np.floor(n / 2), dtype='int')
    #
    # PSD.append(FFT_amp[L].real)
    # Freq.append(freq[L])

    fft = np.fft.fft(mag_data)
    fft = fft[range(int(len(fft)/2))]
    freq_fft = np.linspace(0, dt/2, len(fft))

    PSD.append(np.abs(fft)**2)
    Freq.append(freq_fft)

    # Save data to csv file if checked
    if write_checkbox[0].get() == 1:
        if num_saved[0].get() == "0":
            filename = "Magnetometer_Data_" + strftime("%Y%m%d%H%M%S", gmtime(time())) + ".csv"

            open(filename, 'x')

            directory = filedialog.askdirectory()
            save_path = os.path.join(directory, filename)

            csvfile = open(save_path, 'w')
            # create a csv writer object
            sci_csvwriter.append(csv.writer(csvfile))

            write_to_sci.append(True)
        if write_to_sci[0]:
            save_to_file()

    plot_science()
    # plot_attitude()
    # update_quality()

    Science_x_values.popleft()
    Science_x_values.append(Science_x_values[-1] + 1)


""" updates science plots live, time domain and frequency domain """
def plot_science():
    # Time domain plot
    rescale_plots(Scalar_Magnetometer_Data, Science_x_values, magnetometer_limits, artist_3[0], sci_fig[0], sci_axes[0],
                  sci_axes_background[0], 1.02, 0.98)

    # Frequency domain plot
    rescale_plots(PSD[-1][1:]/1e5, Freq[-1][1:], fft_limits, artist_3[1], sci_fig[1], sci_axes[1], sci_axes_background[1],
                  1.10, 0.90)

    # State plot
    artist_3[2].set_xdata(np.linspace(1, 100, 100))
    artist_3[2].set_ydata(Magnetometer_State)

    for i in range(0, len(sci_fig)):
        sci_fig[i].tight_layout()
        sci_fig[i].canvas.draw()
        sci_fig[i].canvas.flush_events()


""" updates the attitude plots live in time domain """
def plot_attitude():
    quaternions_NST1 = []
    quaternions_NST2 = []
    for idx in range(0, len(NST_1)):
        try:
            quaternions_NST1.extend([NST_1[idx][0][0], NST_1[idx][0][1], NST_1[idx][0][2], NST_1[idx][0][3]])
            quaternions_NST2.extend([NST_2[idx][0][0], NST_2[idx][0][1], NST_2[idx][0][2], NST_2[idx][0][3]])
        except IndexError or TypeError or ValueError:
            quaternions_NST1.extend([0, 0, 0, 0])
            quaternions_NST2.extend([0, 0, 0, 0])

    for idx in range(0, 4):
        rescale_plots(quaternions_NST1[idx::4], Science_x_values, NST1_limits[idx], artist_4[idx], tracker_fig[idx],
                      tracker_axes[idx], tracker_axes_background[idx], 1.05, 0.95)
        rescale_plots(quaternions_NST2[idx::4], Science_x_values, NST2_limits[idx], artist_4[idx+4], tracker_fig[idx],
                      tracker_axes_twins[idx], tracker_axes_twins_background[idx], 1.10, 0.90)


""" rescale the plots when max or min values extend beyond the limits """
def rescale_plots(Y_List, X_List, y_limits, artist, figure, axis, background, upper_tolerance, lower_tolerance):
    try:
        max_limit = None
        min_limit = None
        # y Limits
        if max(Y_List) > axis.get_ylim()[1] or (axis.get_ylim()[1] - max(Y_List)) >= (max(Y_List) * (1-upper_tolerance)):
            max_limit = max(Y_List) * upper_tolerance
        if min(Y_List) < axis.get_ylim()[0] or (min(Y_List) - axis.get_ylim()[0]) > (min(Y_List) * (1-upper_tolerance)):
            min_limit = min(Y_List) * lower_tolerance
        if max_limit is None:
            max_limit = axis.get_ylim()[1]
        if min_limit is None:
            min_limit = axis.get_ylim()[0]

        if min_limit != axis.get_ylim()[0] or max_limit != axis.get_ylim()[1]:
            limits = [min_limit, max_limit]
            axis.set_ylim(limits)
            background = figure.canvas.copy_from_bbox(axis.bbox)

        # x limits
        if min(X_List) != 0 or max(X_List) != 0:
            axis.set_xlim([min(X_List), max(X_List)])
            background = figure.canvas.copy_from_bbox(axis.bbox)
        else:
            pass

        axis.set_xlim([min(X_List), max(X_List)])
        background = figure.canvas.copy_from_bbox(axis.bbox)

        if max(Y_List) == 0 and min(Y_List) == 0:
            figure.canvas.restore_region(background)
        else:
            figure.canvas.restore_region(background)
            artist.set_xdata(X_List)
            artist.set_ydata(Y_List)
    except ValueError:
        figure.canvas.restore_region(background)
        artist.set_xdata(X_List)
        artist.set_ydata(Y_List)


""" updates the labels for the attitude quality """
def update_quality():
    OpMode_Status = [["IDLE", "red"], ["INITIALIZE", "blue"], ["STARID", "green"], ["TRACK", "green"],
                     ["PHOTO", "green"], ["CAL", "blue"]]
    StarID_Status = [["IDLE", "red"], ["INITIALIZE", "blue"], ["WAITING FOR IMAGE", "green"]]
    Attitude_Status = [["OK", "green"], ["PENDING", "blue"], ["BAD", "red"], ["TOO FEW STARS", "orange"],
                       ["QUEST FAILED", "red"], ["RESIDUALS TOO HIGH", "red"], ["", "red"], ["", "red"], ["", "red"],
                       ["", "red"], ["", "red"], ["", "red"], ["", "red"], ["", "red"], ["", "red"], ["", "red"],
                       ["", "red"], ["", "red"], ["", "red"], ["", "red"], ["", "red"], ["", "red"], ["", "red"],
                       ["", "red"], ["", "red"], ["RATE TOO HIGH", "red"]]
    Rate_Est_Status = [["OK", "green"], ["", "orange"], ["BAD", "red"]]

    Attitude_Quality_NST1[0].configure(text=OpMode_Status[NST_1[-1][6][0]][0],
                                       fg_color=OpMode_Status[NST_1[-1][6][0]][1])
    Attitude_Quality_NST1[1].configure(text=StarID_Status[NST_1[-1][6][1]][0],
                                       fg_color=StarID_Status[NST_1[-1][6][1]][1])
    Attitude_Quality_NST1[2].configure(text=Attitude_Status[NST_1[-1][6][2]][0],
                                       fg_color=Attitude_Status[NST_1[-1][6][2]][1])
    Attitude_Quality_NST1[3].configure(text=Rate_Est_Status[NST_1[-1][6][3]][0],
                                       fg_color=Rate_Est_Status[NST_1[-1][6][3]][1])

    Attitude_Quality_NST2[0].configure(text=OpMode_Status[NST_2[-1][6][0]][0],
                                       fg_color=OpMode_Status[NST_2[-1][6][0]][1])
    Attitude_Quality_NST2[1].configure(text=StarID_Status[NST_2[-1][6][1]][0],
                                       fg_color=StarID_Status[NST_2[-1][6][1]][1])
    Attitude_Quality_NST2[2].configure(text=Attitude_Status[NST_2[-1][6][2]][0],
                                       fg_color=Attitude_Status[NST_2[-1][6][2]][1])
    Attitude_Quality_NST2[3].configure(text=Rate_Est_Status[NST_2[-1][6][3]][0],
                                       fg_color=Rate_Est_Status[NST_2[-1][6][3]][1])


""" updates the magnetometer state live """
def update_state():
    match Magnetometer_Status[-1]:
        case 3:
            state_label[0].configure(text="Warm Up")

            orange_img = ImageTk.PhotoImage(Image.open("orange_button.png").resize((80, 80)))
            led_image[0].configure(image=orange_img)
            led_image[0].image = orange_img
            return
        case 4:
            state_label[0].configure(text="Laser Lock\nScan")

            green_img = ImageTk.PhotoImage(Image.open("green_button.png").resize((80, 80)))
            led_image[0].configure(image=green_img)
            led_image[0].image = green_img
            return
        case 5:
            state_label[0].configure(text="Scan for\nMagnetic\nResonance")

            blue_img = ImageTk.PhotoImage(Image.open("blue_button.png").resize((80, 80)))
            led_image[0].configure(image=blue_img)
            led_image[0].image = blue_img
            return
        case 6:
            state_label[0].configure(text="Magnetic Lock")

            blue_img = ImageTk.PhotoImage(Image.open("blue_button.png").resize((80, 80)))
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
        sci_display_window[0].destroy()
        Science.display_button.state = NORMAL

    sci_display_window.clear()
    sci_display_window.append(ctk.CTkToplevel())
    sci_display_window[0].geometry("538x750")
    sci_display_window[0].title("Live Science Data")
    sci_display_window[0].resizable(False, False)
    sci_display_window[0].protocol("WM_DELETE_WINDOW", close_display)
    Science.display_button.state = DISABLED

    if Scalar_Magnetometer_Data[-1] != 0:
        update_science_display()
    else:
        label = ctk.CTkLabel(master=sci_display_window[0],
                             text="No Data to Display!")
        label.pack(side=TOP, expand=True)


""" updates values in the live science display """
def update_science_display():
    match Magnetometer_Status[-1]:
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

    label1 = ctk.CTkLabel(master=sci_display_window[0],
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
                               + "\n\nω\u2082: " + str(NST_1[-1][1][1]) + "\n\nω\u2083: " + str(NST_1[-1][1][2]) +
                               "\n\nTracker Right Ascension: " + str(NST_1[-1][2]) + "\n\nDeclination: " +
                               str(NST_1[-1][3]) + "\n\nTracker Roll: " + str(NST_1[-1][4]) +
                               "\n\nAttitude Covariance\nCOV 1: " + str(NST_1[-1][5][0]) + "\n\nCOV 2: "
                               + str(NST_1[-1][5][1]) + "\n\nCOV 3: " + str(NST_1[-1][5][2]) + "\n\nCOV 4: " +
                               str(NST_1[-1][5][3]) + "\n\nCOV 5: " + str(NST_1[-1][5][4]) + "\n\nCOV 6: " +
                               str(NST_1[-1][5][5]) + "\n\nOp Mode: " + str(NST_1[-1][6][0]) + "\n\nStarID Step: " +
                               str(NST_1[-1][6][1]) + "\n\nAttitude Status: " + str(NST_1[-1][6][2]) +
                               "\n\nRate Est Status: " + str(NST_1[-1][6][3]))
    label2.grid(row=1, column=0)

    label3 = ctk.CTkLabel(master=sci_display_window,
                          text="=============== NST 2 ===============\n\n" +
                               "Attitude Quaternions\nβ\u2080: " + str(NST_2[-1][0][0]) + "\n\nβ\u2081: " +
                               str(NST_2[-1][0][1]) + "\n\nβ\u2082: " + str(NST_2[-1][0][2]) + "\n\nβ\u2083: " +
                               str(NST_2[-1][0][3]) + "\n\nAngular Velocity\nω\u2081: " + str(NST_2[-1][1][0])
                               + "\n\nω\u2082: " + str(NST_2[-1][1][1]) + "\n\nω\u2083: " + str(NST_2[-1][1][2]) +
                               "\n\nTracker Right Ascension: " + str(NST_2[-1][2]) + "\n\nDeclination: " +
                               str(NST_2[-1][3]) + "\n\nTracker Roll: " + str(NST_2[-1][4]) +
                               "\n\nAttitude Covariance\nCOV 1: " + str(NST_2[-1][5][0]) + "\n\nCOV 2: "
                               + str(NST_2[-1][5][1]) + "\n\nCOV 3: " + str(NST_2[-1][5][2]) + "\n\nCOV 4: " +
                               str(NST_2[-1][5][3]) + "\n\nCOV 5: " + str(NST_2[-1][5][4]) + "\n\nCOV 6: " +
                               str(NST_2[-1][5][5]) + "\n\nOp Mode: " + str(NST_2[-1][6][0]) + "\n\nStarID Step: " +
                               str(NST_2[-1][6][1]) + "\n\nAttitude Status: " + str(NST_2[-1][6][2]) +
                               "\n\nRate Est Status: " + str(NST_2[-1][6][3]))
    label3.grid(row=1, column=1)


""" saves all science data to a csv until user decides to save file or close GUI """
def save_to_file():
    num_saved[0].set(str(int(num_saved[0].get()) + 1))

    if num_saved[0].get() == "1":
        header = ['Timestamp [s]', 'Magnetometer Output [nT]', 'Magnetometer State', 'Beta0 (NST 1)', 'Beta1 (NST 1)',
                  'Beta2 (NST 1)', 'Beta3 (NST 1)', 'omega1 (NST 1)', 'omega2 (NST 1)', 'omega3 (NST 1)',
                  'Tracker Right Ascension (NST 1)', 'Declination (NST 1)', 'Tracker Roll (NST 1)', 'COV1 (NST 1)',
                  'COV2 (NST 1)', 'COV3 (NST 1)', 'COV4 (NST 1)', 'COV5 (NST 1)', 'COV6 (NST 1)', 'Op Mode (NST 1)',
                  'StarID Step (NST 1)', 'Attitude Status (NST 1)', 'Rate Est Status (NST 1)',
                  'Beta0 (NST 2)', 'Beta1 (NST 2)', 'Beta2 (NST 2)', 'Beta3 (NST 2)', 'omega1 (NST 2)',
                  'omega2 (NST 2)', 'omega3 (NST 2)', 'Tracker Right Ascension (NST 2)', 'Declination (NST 2)',
                  'Tracker Roll (NST 2)', 'COV1 (NST 2)', 'COV2 (NST 2)', 'COV3 (NST 2)', 'COV4 (NST 2)',
                  'COV5 (NST 2)', 'COV6 (NST 2)', 'Op Mode (NST 2)', 'StarID Step (NST 2)', 'Attitude Status (NST 2)',
                  'Rate Est Status (NST 2)']
        # write the fields
        sci_csvwriter[0].writerow(header)

    row = [Science_Time[-1], Scalar_Magnetometer_Data[-1], Magnetometer_Status[-1], NST_1[-1][0][0],
           NST_1[-1][0][1], NST_1[-1][0][2], NST_1[-1][0][3], NST_1[-1][1][0], NST_1[-1][1][1], NST_1[-1][1][2],
           NST_1[-1][2], NST_1[-1][3], NST_1[-1][4], NST_1[-1][5][0], NST_1[-1][5][1], NST_1[-1][5][2],
           NST_1[-1][5][3], NST_1[-1][5][4], NST_1[-1][5][5], NST_1[-1][6][0], NST_1[-1][6][1], NST_1[-1][6][2],
           NST_1[-1][6][3], NST_2[-1][0][0], NST_2[-1][0][1], NST_2[-1][0][2], NST_2[-1][0][3], NST_2[-1][1][0],
           NST_2[-1][1][1], NST_2[-1][1][2], NST_2[-1][2], NST_2[-1][3], NST_2[-1][4], NST_2[-1][5][0],
           NST_2[-1][5][1], NST_2[-1][5][2], NST_2[-1][5][3], NST_2[-1][5][4], NST_2[-1][5][5], NST_2[-1][6][0],
           NST_2[-1][6][1], NST_2[-1][6][2], NST_2[-1][6][3]]
    sci_csvwriter[0].writerow(row)


""" saves csv file of science data """
def save_file():
    if num_saved[0].get() == "0":
        print("No Data Was Collected and Therefore, No Data Was Saved")
    else:
        print("Data Saved Successfully!")
    num_saved[0].set("0")
    sci_csvwriter.clear()
    write_checkbox[0].deselect()


""" changes the CRC indicator on the science page """
def crc_failure(switch):
    if switch:
        green_img = ImageTk.PhotoImage(Image.open("green_button.png").resize((60, 60)))
        sci_CRC_image[0].configure(image=green_img)
        sci_CRC_image[0].image = green_img

        sci_CRC_label[0].configure(text="CRC Passed!")
    else:
        red_img = ImageTk.PhotoImage(Image.open("red_button.png").resize((60, 60)))
        sci_CRC_image[0].configure(image=red_img)
        sci_CRC_image[0].image = red_img

        sci_CRC_label[0].configure(text="CRC Failed!")
