"""
This module defines and preallocates memory to all variables that are used between all the files
"""

from collections import deque
from numpy import zeros

# -----------------------------------------------DEFINE DEQUE SIZE-----------------------------------------------------#

deque_size = 24  # set deque size (6 = 1 min of data)
sci_deque_size = 60  # set science deque size (1 = 1 second of data)

# ----------------------------------------VOLTAGE AND CURRENT PREALLOCATION--------------------------------------------#

""" Housekeeping x-axis """
HK_x_values = deque([x for x in range(0, deque_size)])

""" Data points """
# Initialize the data point deque
HK_data_points = deque(zeros(deque_size))

"""+5V Analog Board Graph"""
# Initialize the 2 variables to be plotted
AB_voltage = deque(zeros(deque_size))
AB_current = deque(zeros(deque_size))

"""12V Digital Board Graph"""
# Initialize the 2 variables to be plotted
DB_voltage = deque(zeros(deque_size))
DB_current = deque(zeros(deque_size))

"""3.3V Housekeeping Sensors Graph"""
# Initialize the 2 variables to be plotted
HK_voltage = deque(zeros(deque_size))
HK_current = deque(zeros(deque_size))

"""5VST Star Trackers Graph"""
# Initialize the 2 variables to be plotted
ST_voltage = deque(zeros(deque_size))
ST_current = deque(zeros(deque_size))

"""12VS Rail for Scalar Boards Graph"""
# Initialize the 2 variables to be plotted
SB_voltage = deque(zeros(deque_size))
SB_current = deque(zeros(deque_size))

"""Scalar Boards No.1 Ch.1 Graph"""
# Initialize the 2 variables to be plotted
SBN1C1_voltage = deque(zeros(deque_size))
SBN1C1_current = deque(zeros(deque_size))

"""Scalar Boards No.1 Ch.2 Graph"""
# Initialize the 2 variables to be plotted
SBN1C2_voltage = deque(zeros(deque_size))
SBN1C2_current = deque(zeros(deque_size))

"""Scalar Boards No.1 Ch.3 Graph"""
# Initialize the 2 variables to be plotted
SBN1C3_voltage = deque(zeros(deque_size))
SBN1C3_current = deque(zeros(deque_size))

"""Scalar Boards No.2 Ch.1 Graph"""
# Initialize the 2 variables to be plotted
SBN2C1_voltage = deque(zeros(deque_size))
SBN2C1_current = deque(zeros(deque_size))

"""Scalar Boards No.2 Ch.2 Graph"""
# Initialize the 2 variables to be plotted
SBN2C2_voltage = deque(zeros(deque_size))
SBN2C2_current = deque(zeros(deque_size))

"""Scalar Boards No.2 Ch.3 Graph"""
# Initialize the 2 variables to be plotted
SBN2C3_voltage = deque(zeros(deque_size))
SBN2C3_current = deque(zeros(deque_size))

# ------------------------------------TEMPERATURE VISUALIZATION PREALLOCATION------------------------------------------#

"""+/-5V Regulator"""
# Initialize variable to be plotted
REG5V_temp = deque(zeros(deque_size))

"""3.3V Regulator"""
# Initialize variable to be plotted
REG3V3_temp = deque(zeros(deque_size))

"""Scalar Board 1"""
# Initialize variable to be plotted
SB1_temp = deque(zeros(deque_size))

"""Scalar Board 2"""
# Initialize variable to be plotted
SB2_temp = deque(zeros(deque_size))

# ---------------------------------------------CALIBRATION VARIABLES---------------------------------------------------#

""" Coil 1 Offset and Amplitude """
COIL1_AMP = deque(zeros(deque_size))
COIL1_OFFSET = deque(zeros(deque_size))

""" Coil 2 Offset and Amplitude """
COIL2_AMP = deque(zeros(deque_size))
COIL2_OFFSET = deque(zeros(deque_size))

""" Coil 3 Offset and Amplitude """
COIL3_AMP = deque(zeros(deque_size))
COIL3_OFFSET = deque(zeros(deque_size))

""" VRuM Temperatures """
VRUM_TEMP_1 = deque(zeros(deque_size))
VRUM_TEMP_2 = deque(zeros(deque_size))
VRUM_TEMP_3 = deque(zeros(deque_size))
VRUM_TEMP_4 = deque(zeros(deque_size))

# ---------------------------------------------SCALE LIMITS VARIABLES--------------------------------------------------#

""" Housekeeping Plots Limits """
voltage_limits = [[0, 5.5], [0, 12.5], [0, 3.8], [0, 5.5], [0, 12.5], [0, 12.5], [0, 12.5], [0, 12.5],
                          [0, 12.5], [0, 12.5], [0, 12.5]]
current_limits = [[0, 275], [0, 275], [0, 275], [0, 275], [0, 275], [0, 275], [0, 275], [0, 275], [0, 275],
                  [0, 275], [0, 275]]
temp_limits = [[0, 35], [0, 35], [0, 35], [0, 35]]

""" Calibration Plots Limits """
offset_limits = [[0, 30], [0, 30], [0, 30]]
amplitude_limits = [[0, 30], [0, 30], [0, 30]]

""" Science Plots Limits """
magnetometer_limits = [0, 10]
fft_limits = [0, 10]

# ---------------------------------------------FIGURE & AXES VARIABLES-------------------------------------------------#

""" Housekeeping Page Plots """
fig = []

axes = []
axes_background = []

axes_twins = []
axes_twins_background = []

plot_names = ["+5V Rail Analog Board", "12V Rail Digital Board", "3.3V Rail HK Sensors",
                      "5VST Rail Star Trackers", "12VS Rail Scalar Boards", "Scalar Board No.1 Ch.1",
                      "Scalar Board No.1 Ch.2", "Scalar Board No.1 Ch.3", "Scalar Board No.2 Ch.1",
                      "Scalar Board No.2 Ch.2", "Scalar Board No.2 Ch.3", "Temperature at ±5V Regulator",
                      "Temperature at 3.3V Regulator", "Temperature at Scalar Board No.1",
                      "Temperature at Scalar Board No.2", "Coil 1", "Coil 2", "Coil 3"]

artist_1 = []
artist_2 = []

""" Science Page Plots """
sci_fig = []

sci_axes = []
sci_axes_background = []

sci_plot_names = ["Magnetometer Data Time Domain", "Magnetometer Data Frequency Domain",
                  "Magnetometer Spectrogram"]

artist_3 = []


# -------------------------------------------------ERROR FLAGS---------------------------------------------------------#

""" Error Flags """
ERROR_REGISTER_0 = deque(zeros(deque_size))
ERROR_REGISTER_1 = deque(zeros(deque_size))

# ---------------------------------------SCIENCE DATA/STATE PREALLOCATION----------------------------------------------#

# Time expressed in GPS time
Science_Time = deque(zeros(sci_deque_size))

NST_1 = deque(zeros(sci_deque_size))
NST_2 = deque(zeros(sci_deque_size))

Raw_Scalar_Magnetometer_Data = deque(zeros(1025))
Raw_Scalar_Magnetometer_State = deque(zeros(100))

State_Colors = deque(zeros(sci_deque_size))
segments = deque(zeros(sci_deque_size))

Scalar_Magnetometer_Data = deque(zeros(sci_deque_size))
PSD = deque(zeros(sci_deque_size))
Freq = deque(zeros(sci_deque_size))
State_Change = deque(zeros(sci_deque_size))

Spec_f = deque(zeros(sci_deque_size))
Spec_t = deque(zeros(sci_deque_size))
Spec_Sxx = deque(zeros(sci_deque_size))

# ---------------------------------------------DISPLAY WINDOWS & FRAMES------------------------------------------------#
housekeeping_display = deque([False])
science_display = deque([False])
