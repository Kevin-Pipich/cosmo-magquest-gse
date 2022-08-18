import customtkinter as ctk
from variables import *
from tkinter import NORMAL, DISABLED, TOP, BOTH

""" [CURRENTLY DISABLED] Checks to ensure that voltages and currents are at safe levels, sends warning if not """
def safety_check(Voltage_List, Current_List, Temperature_List):
    names = ["Analog Board Rail", "Digital Board Rail", "Housekeeping Sensor Rail", "Star Tracker Rail",
             "Scalar Boards Rail", "Scalar Board No.1 Ch.1", "Scalar Board No.1 Ch.2", "Scalar Board No.1 Ch.3",
             "Scalar Board No.2 Ch.1", "Scalar Board No.2 Ch.2", "Scalar Board No.2 Ch.3", "5V Regulator",
             "3.3V Regulator", "Scalar Board No.1", "Scalar Board No.2"]
    safe_voltage = [5.1, 12.1, 3.4, 5.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1, 12.1]
    safe_current = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
    safe_temperature = [90, 90, 90, 90]

    for i in range(0, len(Voltage_List)):
        if Voltage_List[i][-1] >= safe_voltage[i]:
            warning_window = ctk.CTkToplevel()
            warning_window.geometry("365x200")
            warning_window.title("WARNING!")
            warning_window.resizable(False, False)

            warning_label = ctk.CTkLabel(master=warning_window,
                                         text="The Voltage of the " + names[i] + " Has Exceeded \n the Acceptable"
                                                                                 " Value!!! \n Live value: " +
                                              str(Voltage_List[i][-1]) + " V")
            warning_label.pack(side="top", fill="both", expand=True)
        if Current_List[i][-1] >= safe_current[i]:
            warning_window = ctk.CTkToplevel()
            warning_window.geometry("365x200")
            warning_window.title("WARNING!")
            warning_window.resizable(False, False)

            warning_label = ctk.CTkLabel(master=warning_window,
                                         text="The Current of the " + names[i] + " Has Exceeded \n the Acceptable"
                                                                                 " Value!!! \n Live value: " +
                                              str(Current_List[i][-1]) + " mA")
            warning_label.pack(side="top", fill="both", expand=True)

    for i in range(0, len(Temperature_List)):
        if Temperature_List[i][-1] >= safe_temperature[i]:
            warning_window = ctk.CTkToplevel()
            warning_window.geometry("365x200")
            warning_window.title("WARNING!")
            warning_window.resizable(False, False)

            warning_label = ctk.CTkLabel(master=warning_window,
                                         text="The Temperature of the " + names[i + 11] +
                                              " Has Exceeded the Acceptable Value!!! \n Live value: " +
                                              str(Temperature_List[i][-1]) + " C")
            warning_label.pack(side="top", fill="both", expand=True)


""" updates the values of each housekeeping value """
def update_housekeeping(housekeeping_packet):

    HK_data_points.popleft()
    HK_data_points.append(int(HK_data_points[-1] + 1))

    # ================= Housekeeping Values ================= #

    AB_voltage.popleft()
    AB_current.popleft()
    AB_current.append(int.from_bytes(housekeeping_packet[0:2], "little") * 4)
    AB_voltage.append(int.from_bytes(housekeeping_packet[2:4], "little") / 1000)

    DB_voltage.popleft()
    DB_current.popleft()
    DB_current.append(int.from_bytes(housekeeping_packet[4:6], "little") * 4)
    DB_voltage.append(int.from_bytes(housekeeping_packet[6:8], "little") / 1000)

    HK_voltage.popleft()
    HK_current.popleft()
    HK_current.append(int.from_bytes(housekeeping_packet[8:10], "little") * 4)
    HK_voltage.append(int.from_bytes(housekeeping_packet[10:12], "little") / 1000)

    ST_voltage.popleft()
    ST_current.popleft()
    ST_current.append(int.from_bytes(housekeeping_packet[12:14], "little") * 4)
    ST_voltage.append(int.from_bytes(housekeeping_packet[14:16], "little") / 1000)

    SB_voltage.popleft()
    SB_current.popleft()
    SB_current.append(int.from_bytes(housekeeping_packet[16:18], "little") * 4)
    SB_voltage.append(int.from_bytes(housekeeping_packet[18:20], "little") / 1000)

    SBN1C1_voltage.popleft()
    SBN1C1_current.popleft()
    SBN1C1_current.append(int.from_bytes(housekeeping_packet[20:22], "little") * 4)
    SBN1C1_voltage.append(int.from_bytes(housekeeping_packet[22:24], "little") / 1000)

    SBN1C2_voltage.popleft()
    SBN1C2_current.popleft()
    SBN1C2_current.append(int.from_bytes(housekeeping_packet[24:26], "little") * 4)
    SBN1C2_voltage.append(int.from_bytes(housekeeping_packet[26:28], "little") / 1000)

    SBN1C3_voltage.popleft()
    SBN1C3_current.popleft()
    SBN1C3_current.append(int.from_bytes(housekeeping_packet[28:30], "little") * 4)
    SBN1C3_voltage.append(int.from_bytes(housekeeping_packet[30:32], "little") / 1000)

    SBN2C1_voltage.popleft()
    SBN2C1_current.popleft()
    SBN2C1_current.append(int.from_bytes(housekeeping_packet[32:34], "little") * 4)
    SBN2C1_voltage.append(int.from_bytes(housekeeping_packet[34:36], "little") / 1000)

    SBN2C2_voltage.popleft()
    SBN2C2_current.popleft()
    SBN2C2_current.append(int.from_bytes(housekeeping_packet[36:38], "little") * 4)
    SBN2C2_voltage.append(int.from_bytes(housekeeping_packet[38:40], "little") / 1000)

    SBN2C3_voltage.popleft()
    SBN2C3_current.popleft()
    SBN2C3_current.append(int.from_bytes(housekeeping_packet[40:42], "little") * 4)
    SBN2C3_voltage.append(int.from_bytes(housekeeping_packet[42:44], "little") / 1000)

    REG5V_temp.popleft()
    REG5V_temp.append(int.from_bytes(housekeeping_packet[44:46], "little") * 0.0625)

    REG3V3_temp.popleft()
    REG3V3_temp.append(int.from_bytes(housekeeping_packet[46:48], "little") * 0.0625)

    SB1_temp.popleft()
    SB1_temp.append(int.from_bytes(housekeeping_packet[48:50], "little") * 0.0625)

    SB2_temp.popleft()
    SB2_temp.append(int.from_bytes(housekeeping_packet[50:52], "little") * 0.0625)

    Voltage_List = [AB_voltage, DB_voltage, HK_voltage, ST_voltage, SB_voltage, SBN1C1_voltage, SBN1C2_voltage,
                    SBN1C3_voltage, SBN2C1_voltage, SBN2C2_voltage, SBN2C3_voltage]
    Current_List = [AB_current, DB_current, HK_current, ST_current, SB_current, SBN1C1_current, SBN1C2_current,
                    SBN1C3_current, SBN2C1_current, SBN2C2_current, SBN2C3_current]
    Temperature_List = [REG5V_temp, REG3V3_temp, SB1_temp, SB2_temp]

    # ================= Calibration Values ================= #

    COIL1_AMP.popleft()
    COIL1_AMP.append(int.from_bytes(housekeeping_packet[52:54], "little") * (3.3 / 4095) * 5)

    COIL1_OFFSET.popleft()
    COIL1_OFFSET.append(int.from_bytes(housekeeping_packet[54:56], "little") * ((3.3 / 4095) - 1.65) * 5)

    COIL2_AMP.popleft()
    COIL2_AMP.append(int.from_bytes(housekeeping_packet[56:58], "little") * (3.3 / 4095) * 5)

    COIL2_OFFSET.popleft()
    COIL2_OFFSET.append(int.from_bytes(housekeeping_packet[58:60], "little") * ((3.3 / 4095) - 1.65) * 5)

    COIL3_AMP.popleft()
    COIL3_AMP.append(int.from_bytes(housekeeping_packet[60:62], "little") * (3.3 / 4095) * 5)

    COIL3_OFFSET.popleft()
    COIL3_OFFSET.append(int.from_bytes(housekeeping_packet[62:64], "little") * ((3.3 / 4095) - 1.65) * 5)

    VRUM_TEMP_1.popleft()
    VRUM_TEMP_1.append((int.from_bytes(housekeeping_packet[64:66], "little") * 0.282) - 577.7)

    VRUM_TEMP_2.popleft()
    VRUM_TEMP_2.append((int.from_bytes(housekeeping_packet[66:68], "little") * 0.282) - 577.7)

    VRUM_TEMP_3.popleft()
    VRUM_TEMP_3.append((int.from_bytes(housekeeping_packet[68:70], "little") * 0.282) - 577.7)

    VRUM_TEMP_4.popleft()
    VRUM_TEMP_4.append((int.from_bytes(housekeeping_packet[70:72], "little") * 0.282) - 577.7)

    Offset_List = [COIL1_OFFSET, COIL2_OFFSET, COIL3_OFFSET]
    Amplitude_List = [COIL1_AMP, COIL2_AMP, COIL3_AMP]

    # ================= Error Flags ================= #

    ERROR_REGISTER_0.popleft()
    ERROR_REGISTER_0.append(int.from_bytes(housekeeping_packet[72:76], "little"))

    ERROR_REGISTER_1.popleft()
    ERROR_REGISTER_1.append(int.from_bytes(housekeeping_packet[72:76], "little"))

    # self.safety_check(Voltage_List, Current_List, Temperature_List)

    plot_housekeeping(Voltage_List, Current_List, Temperature_List, Offset_List, Amplitude_List)


""" updates housekeeping plots live """
def plot_housekeeping(Voltage_List, Current_List, Temperature_List, Offset_List, Amplitude_List):

    # Updates all the figures which were already created
    for i in range(0, len(fig)):
        if i < 11:
            rescale_plots(Voltage_List, i, 1)
            rescale_plots(Current_List, i, 2)
        elif 11 <= i < 15:
            rescale_plots(Temperature_List, i-11, 3)
        else:
            rescale_plots(Offset_List, i, 4)
            rescale_plots(Amplitude_List, i-15, 5)

        fig[i].tight_layout()
        fig[i].canvas.draw()
        fig[i].canvas.flush_events()

    # Updates the error flags
    update_error()


""" rescale the plots when max or min values extend beyond the limits """
def rescale_plots(List, idx, limits):
    match limits:
        case 1:  # voltage limits
            if max(List[idx]) > voltage_limits[idx][1]:
                max_limit = max(List) * 1.05
                min_limit = voltage_limits[idx][0]

            elif min(List[idx]) < voltage_limits[idx][0]:
                min_limit = min(List) * 0.95
                max_limit = voltage_limits[idx][1]

            elif (max(List[idx]) - min(List[idx]) * 2) < (voltage_limits[idx][1] - voltage_limits[idx][0]) \
                    and max(List[idx]) != 0 and min(List[idx]) != 0:
                max_limit = max(List) * 1.05
                min_limit = min(List) * 0.95

            else:
                min_limit = voltage_limits[idx][0]
                max_limit = voltage_limits[idx][1]

            voltage_limits[idx] = [min_limit, max_limit]
            axes[idx].set_ylim(voltage_limits[idx])
            axes_background[idx] = fig[idx].canvas.copy_from_bbox(axes[idx].bbox)

            if max(List[idx]) == 0 and min(List[idx]) == 0:
                fig[idx].canvas.restore_region(axes_background[idx])
            else:
                fig[idx].canvas.restore_region(axes_background[idx])
                artist_1[idx].set_xdata(HK_x_values)
                artist_1[idx].set_ydata(List[idx])

        case 2:  # current limits
            if max(List[idx]) > current_limits[idx][1]:
                max_limit = max(List) * 1.05
                min_limit = current_limits[idx][0]

            elif min(List[idx]) < current_limits[idx][0]:
                min_limit = min(List) * 0.95
                max_limit = current_limits[idx][1]

            elif (max(List[idx]) - min(List[idx]) * 2) < (current_limits[idx][1] - current_limits[idx][0]) \
                    and max(List[idx]) != 0 and min(List[idx]) != 0:
                max_limit = max(List) * 1.05
                min_limit = min(List) * 0.95

            else:
                min_limit = current_limits[idx][0]
                max_limit = current_limits[idx][1]

            current_limits[idx] = [min_limit, max_limit]
            axes_twins[idx].set_ylim(current_limits[idx])
            axes_twins_background[idx] = fig[idx].canvas.copy_from_bbox(axes_twins[idx].bbox)

            if max(List[idx]) == 0 and min(List[idx]) == 0:
                fig[idx].canvas.restore_region(axes_twins_background[idx])
            else:
                fig[idx].canvas.restore_region(axes_twins_background[idx])
                artist_2[idx].set_xdata(HK_x_values)
                artist_2[idx].set_ydata(List[idx])

        case 3:  # temp limits
            if max(List[idx]) > temp_limits[idx][1]:
                max_limit = max(List[idx]) * 1.05
                min_limit = temp_limits[idx][0]

            elif min(List[idx]) < temp_limits[idx][0]:
                min_limit = min(List[idx]) * 0.95
                max_limit = temp_limits[idx][1]

            elif (max(List[idx]) - min(List[idx]) * 2) < (temp_limits[idx][1] - temp_limits[idx][0]) \
                    and max(List[idx]) != 0 and min(List[idx]) != 0:
                max_limit = max(List[idx]) * 1.05
                min_limit = min(List[idx]) * 0.95

            else:
                min_limit = temp_limits[idx][0]
                max_limit = temp_limits[idx][1]

            temp_limits[idx] = [min_limit, max_limit]
            axes[idx+11].set_ylim(temp_limits[idx])
            axes_background[idx+11] = fig[idx+11].canvas.copy_from_bbox(axes[idx+11].bbox)

            if max(List[idx]) == 0 and min(List[idx]) == 0:
                fig[idx+11].canvas.restore_region(axes_background[idx+11])
            else:
                fig[idx+11].canvas.restore_region(axes_background[idx+11])
                artist_1[idx+11].set_xdata(HK_x_values)
                artist_1[idx+11].set_ydata(List[idx+11])

        case 4:  # offset limits
            if max(List[idx]) > offset_limits[idx][1]:
                max_limit = max(List) * 1.05
                min_limit = offset_limits[idx][0]

            elif min(List[idx]) < offset_limits[idx][0]:
                min_limit = min(List) * 0.95
                max_limit = offset_limits[idx][1]

            elif (max(List[idx]) - min(List[idx]) * 2) < (offset_limits[idx][1] - offset_limits[idx][0]) \
                    and max(List[idx]) != 0 and min(List[idx]) != 0:
                max_limit = max(List) * 1.05
                min_limit = min(List) * 0.95

            else:
                min_limit = offset_limits[idx][0]
                max_limit = offset_limits[idx][1]

            offset_limits[idx] = [min_limit, max_limit]
            axes[idx+15].set_ylim(offset_limits[idx])
            axes_background[idx+15] = fig[idx+15].canvas.copy_from_bbox(axes[idx+15].bbox)

            if max(List[idx]) == 0 and min(List[idx]) == 0:
                fig[idx+15].canvas.restore_region(axes_background[idx+15])
            else:
                fig[idx+15].canvas.restore_region(axes_background[idx+15])
                artist_1[idx+15].set_xdata(HK_x_values)
                artist_1[idx+15].set_ydata(List[idx])

        case 5:  # amplitude limits
            if max(List[idx]) > amplitude_limits[idx][1]:
                max_limit = max(List) * 1.05
                min_limit = amplitude_limits[idx][0]

            elif min(List[idx]) < amplitude_limits[idx][0]:
                min_limit = min(List) * 0.95
                max_limit = amplitude_limits[idx][1]

            elif (max(List[idx]) - min(List[idx]) * 2) < (amplitude_limits[idx][1] - amplitude_limits[idx][0]) \
                    and max(List[idx]) != 0 and min(List[idx]) != 0:
                max_limit = max(List) * 1.05
                min_limit = min(List) * 0.95

            else:
                min_limit = amplitude_limits[idx][0]
                max_limit = amplitude_limits[idx][1]

            amplitude_limits[idx] = [min_limit, max_limit]
            axes_twins[idx+11].set_ylim(amplitude_limits[idx])
            axes_twins_background[idx+11] = fig[idx+15].canvas.copy_from_bbox(axes_twins[idx+11].bbox)

            if max(List[idx]) == 0 and min(List[idx]) == 0:
                fig[idx+15].canvas.restore_region(axes_twins_background[idx+11])
            else:
                fig[idx+15].canvas.restore_region(axes_twins_background[idx+11])
                artist_2[idx+11].set_xdata(HK_x_values)
                artist_2[idx+11].set_ydata(List[idx])


""" creates a new window displaying the live housekeeping data """
def new_housekeeping_display(Housekeeping):
    housekeeping_display.pop(True)

    def close_display():
        housekeeping_display.pop(False)
        hk_display_window.destroy()
        Housekeeping.display_button.state = NORMAL

    hk_display_window = ctk.CTkToplevel()
    hk_display_window.geometry("365x750")
    hk_display_window.title("Live Housekeeping Data")
    hk_display_window.resizable(False, False)
    hk_display_window.protocol("WM_DELETE_WINDOW", close_display)
    Housekeeping.display_button.state = DISABLED
    update_housekeeping_display(hk_display_window)


""" updates the values in the live housekeeping data display """
def update_housekeeping_display(hk_display_window):
    label = ctk.CTkLabel(hk_display_window, text="Data Point " + str(int(HK_data_points[-1])) + "\n\n"
                                                 + "============ Rail Voltage/ Currents ============" + "\n\n"
                                                 + "+5V Rail Analog Board Voltage: " + str(
        AB_voltage[-1]) + " V" + "\n"
                                 "+5V Rail Analog Board Current: " + str(AB_current[-1]) + " mA" + "\n\n"
                                                 + "12V Rail Digital Board Voltage: " + str(
        DB_voltage[-1]) + " V" + "\n"
                                                 + "12V Rail Digital Board Current: " + str(
        DB_current[-1]) + " mA" + "\n\n"
                                                 + "3.3V Rail Housekeeping Sensors Voltage: " + str(
        HK_voltage[-1]) + " V" + "\n"
                                                 + "3.3V Rail Housekeeping Sensors Current: " + str(
        HK_current[-1]) + " mA" + "\n\n"
                                                 + "5VST Rail Star Trackers Voltage: " + str(
        ST_voltage[-1]) + " V" + "\n"
                                                 + "5VST Rail Star Trackers Current: " + str(
        ST_current[-1]) + " mA" + "\n\n"
                                                 + "12VS Rail Scalar Board Voltage: " + str(
        SB_voltage[-1]) + " V" + "\n"
                                                 + "12VS Rail Scalar Board Current: " + str(
        SB_current[-1]) + " mA" + "\n\n"
                                                 + "========== Scalar Boards Voltage/ Currents ==========" + "\n\n"
                                                 + "Scalar Board No.1 Ch.1 Voltage: " + str(
        SBN1C1_voltage[-1]) + " V" + "\n"
                                                 + "Scalar Board No.1 Ch.1 Current: " + str(
        SBN1C1_current[-1]) + " mA" + "\n\n"
                                                 + "Scalar Board No.1 Ch.2 Voltage: " + str(
        SBN1C2_voltage[-1]) + " V" + "\n"
                                                 + "Scalar Board No.1 Ch.2 Current: " + str(
        SBN1C2_current[-1]) + " mA" + "\n\n"
                                                 + "Scalar Board No.1 Ch.3 Voltage: " + str(
        SBN1C3_voltage[-1]) + " V" + "\n"
                                                 + "Scalar Board No.1 Ch.3 Current: " + str(
        SBN1C3_current[-1]) + " mA" + "\n\n"
                                                 + "Scalar Board No.2 Ch.1 Voltage: " + str(
        SBN2C1_voltage[-1]) + " V" + "\n"
                                                 + "Scalar Board No.2 Ch.1 Current: " + str(
        SBN2C1_current[-1]) + " mA" + "\n\n"
                                                 + "Scalar Board No.2 Ch.2 Voltage: " + str(
        SBN2C2_voltage[-1]) + " V" + "\n"
                                                 + "Scalar Board No.2 Ch.2 Current: " + str(
        SBN2C2_current[-1]) + " mA" + "\n\n"
                                                 + "Scalar Board No.2 Ch.3 Voltage: " + str(
        SBN2C3_voltage[-1]) + " V" + "\n"
                                                 + "Scalar Board No.2 Ch.3 Current: " + str(
        SBN2C3_current[-1]) + " mA" + "\n\n"
                                                 + "================ Temperature Values ================" + "\n\n"
                                                 + "Temperature at +/-5V Regulator: " + str(
        REG5V_temp[-1]) + " C" + "\n\n"
                                                 + "Temperature at 3.3V Regulator: " + str(
        REG3V3_temp[-1]) + " C" + "\n\n"
                                                 + "Temperature at Scalar Board No.1: " + str(
        SB1_temp[-1]) + " C" + "\n\n"
                                                 + "Temperature at Scalar Board No.2: " + str(
        SB2_temp[-1]) + " C" + "\n\n")
    label.grid(row=0, column=0)


def update_error():
    # Create the Error List
    Error_List = []
    e0 = bin(ERROR_REGISTER_0[-1])[2:]
    e1 = bin(ERROR_REGISTER_1[-1])[2:]

    # CDH Comm Task Status
    match int(e0[:4], 2):
        case 0:
            CDH_Comm_State = "OK"
        case 1:
            CDH_Comm_State = "UART RX Error"
        case 2:
            CDH_Comm_State = "Timeout Error"
        case 3:
            CDH_Comm_State = "Error in Sync"
        case 4:
            CDH_Comm_State = "Error in Find Opcode"
        case 5:
            CDH_Comm_State = "Error Buffer Overflow"
        case 6:
            CDH_Comm_State = "Error CRC Fail"
        case 7:
            CDH_Comm_State = "Error Callback Null"
        case 8:
            CDH_Comm_State = "UART TX Error"
        case 9:
            CDH_Comm_State = "Error Unknown"
        case _:
            CDH_Comm_State = "Incorrect Value"
            print("Incorrect Error for CDH Comm State Machine")

    Error_List.append(CDH_Comm_State)

    # Housekeeping Task Status (HK Sensors Configuration Status)
    Error_List.append([e0[4] == "1", "INA No.1 (Digital Board) configuration"])
    Error_List.append([e0[5] == "1", "INA No.2 (Digital Board) configuration"])
    Error_List.append([e0[6] == "1", "INA (Scalar Board No.1) configuration"])
    Error_List.append([e0[7] == "1", "INA (Scalar Board No.2) configuration"])
    Error_List.append([e0[8] == "1", "TMP No.1 (Digital Board) configuration"])
    Error_List.append([e0[9] == "1", "TMP No.2 (Digital Board) configuration"])
    Error_List.append([e0[10] == "1", "TMP (Scalar Board No.2) configuration"])
    Error_List.append([e0[11] == "1", "TMP (Scalar Board No.2) configuration"])

    # Housekeeping Task Status (HK Sensor Poll Status)
    Error_List.append([e0[12] == "1", "INA No.1 (Digital Board) polling"])
    Error_List.append([e0[13] == "1", "INA No.2 (Digital Board) polling"])
    Error_List.append([e0[14] == "1", "INA (Scalar Board No.1) polling"])
    Error_List.append([e0[15] == "1", "INA (Scalar Board No.2) polling"])
    Error_List.append([e0[16] == "1", "TMP No.1 (Digital Board) polling"])
    Error_List.append([e0[17] == "1", "TMP No.2 (Digital Board) polling"])
    Error_List.append([e0[18] == "1", "TMP (Scalar Board No.2) polling"])
    Error_List.append([e0[19] == "1", "TMP (Scalar Board No.2) polling"])

    # Coil Control Task Status (Coil Drivers Configuration Status)
    Error_List.append([e0[20] == "1", "WaveGen No.1 (Analog Board) configuration"])
    Error_List.append([e0[21] == "1", "WaveGen No.2 (Analog Board) configuration"])
    Error_List.append([e0[22] == "1", "WaveGen No.3 (Analog Board) configuration"])
    Error_List.append([e0[23] == "1", "DigPot No.1 (Analog Board) configuration"])
    Error_List.append([e0[24] == "1", "DigPot No.2 (Analog Board) configuration"])
    Error_List.append([e0[25] == "1", "DigPot No.3 (Analog Board) configuration"])

    # Coil Control Task Status (Coil Drivers Control Status)
    Error_List.append([e0[26] == "1", "WaveGen No.1 (Analog Board) control"])
    Error_List.append([e0[27] == "1", "WaveGen No.2 (Analog Board) control"])
    Error_List.append([e0[28] == "1", "WaveGen No.3 (Analog Board) control"])
    Error_List.append([e0[29] == "1", "DigPot No.1 (Analog Board) control"])
    Error_List.append([e0[30] == "1", "DigPot No.2 (Analog Board) control"])
    Error_List.append([e0[31] == "1", "DigPot No.3 (Analog Board) control"])

    # Science Task Status (Science Instruments Configuration Status)
    Error_List.append([e1[0] == "1", "Scalar Board No.1 configuration"])
    Error_List.append([e1[1] == "1", "Scalar Board No.2 configuration"])
    Error_List.append([e1[2] == "1", "Star Tracker No.1 configuration"])
    Error_List.append([e1[3] == "1", "Star Tracker No.2 configuration"])

    # Science Task Status (Science Instruments Read Status)
    Error_List.append([e1[4] == "1", "Scalar Board No.1 read"])
    Error_List.append([e1[5] == "1", "Scalar Board No.2 read"])
    Error_List.append([e1[6] == "1", "Star Tracker No.1 read"])
    Error_List.append([e1[7] == "1", "Star Tracker No.2 read"])

    process_error(Error_List)


def process_error(Error_List):
    if Error_List[0] == "OK":
        color = "green"
    else:
        color = "darkred"
    self.frames[Housekeeping].error_grid[0].configure(text="CDH Comm Task State: " + Error_List[0],
                                                      fg_color=color)
    for i in range(1, len(Error_List)):
        if Error_List[i][0] is True:
            color = "green"
            text = "✓"
        else:
            color = "darkred"
            text = "❌"
        self.frames[Housekeeping].error_grid[i - 1].configure(text=text, fg_color=color)


def see_error(num):
    try:
        # if Error_List[num + 1][0] is True:
        #     error = " success!"
        # else:
        #     error = " fail!"
        # error_type = Error_List[num + 1][1]

        error_type = "There is no error number " + str(num) + "\n"
        error = "This is a test!"

        def close_display():
            error_window.destroy()
            for i in range(0, len(self.frames[Housekeeping].error_grid)):
                self.frames[Housekeeping].error_grid[i].state = NORMAL

        error_window = ctk.CTkToplevel()
        error_window.geometry("350x150")
        error_window.title("Error Message")
        error_window.resizable(False, False)
        error_window.protocol("WM_DELETE_WINDOW", close_display)
        for i in range(0, len(self.frames[Housekeeping].error_grid)):
            self.frames[Housekeeping].error_grid[i].state = DISABLED

        error_label = ctk.CTkLabel(master=error_window,
                                   text=error_type + error)
        error_label.pack(side=TOP, fill=BOTH, expand=True)

    except NameError:
        print("excepted")