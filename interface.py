"""
This module contains the creation of the GUI. interface.py handles the creation of all objects (plots, buttons, sliders,
etc.) to be placed within the GUI.
"""
# IMPORTED MODULES
from variables import *
from byte import *
import port
import housekeeping
import commands
import science
import communications
import hidden
# GUI modules
import customtkinter as ctk
from tkinter.ttk import Notebook, Style
import tkinter.messagebox
# Plot modules
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
# Image modules
from PIL import ImageTk, Image
# System management modules
import threading
import sys

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    """
    The 'App' class is the GUI driver. 'App' handles the transitions between tabs. This class also initializes
    serial port communications and is responsible for handling data after it is received through the serial bus and
    processed in "Commands.py". 'App' also handles plotting data to figures that are created within the other classes.
    """

    WIDTH = 1920
    HEIGHT = 1080

    power = True  # must be true in order to send/receive commands

    exit = threading.Event()

    serial_port.append(port.Connect_to_Port())

    def __init__(self, *args, **kwargs):
        # __init__ function for class CTk
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title("COSMO Interface")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Housekeeping, Commands, Science):
            frame = F(container, self)

            # initializing frame of that object from
            # Housekeeping, Commands, Science respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Housekeeping)  # default page that is shown

    def show_frame(self, cont):
        """
        displays the current frame passed as parameter
        """

        frame = self.frames[cont]
        frame.tkraise()

    def on_closing(self):
        """
        closes all the tabs/ windows/ threads when either the 'close' button or the 'x' button is hit
        """
        self.power = False
        self.exit.set()
        if int(points_saved[0].text) != 0:
            science.save_file()
        sys.exit()


class Housekeeping(ctk.CTkFrame):
    """
    The 'Housekeeping' page consists of 15 plots (11 with 2 y-axes for voltage and current visualization and 4 with
    temperature visualization) as well as options to save housekeeping data and display live housekeeping values.
    """
    FIG_WIDTH = 5.5
    FIG_HEIGHT = 4.5
    DPI = 50

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self,
                                       width=180,
                                       corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.img = ImageTk.PhotoImage(Image.open("cosmo-logo.png").resize((180, 180)))
        self.logo = ctk.CTkLabel(master=self.frame_left, image=self.img)
        self.logo.grid(row=0, column=0, pady=5, padx=5)

        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                    text="Housekeeping Page",
                                    text_font=("Roboto Medium", -20))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.housekeeping_button = ctk.CTkButton(master=self.frame_left,
                                                 text="Housekeeping",
                                                 fg_color=("gray75", "gray30"))
        self.housekeeping_button.grid(row=2, column=0, pady=10, padx=20)

        self.command_button = ctk.CTkButton(master=self.frame_left,
                                            text="Commands",
                                            fg_color=("gray75", "gray30"),
                                            command=lambda: controller.show_frame(Commands))
        self.command_button.grid(row=3, column=0, pady=10, padx=20)

        self.science_button = ctk.CTkButton(master=self.frame_left,
                                            text="Science",
                                            fg_color=("gray75", "gray30"),
                                            command=lambda: controller.show_frame(Science))
        self.science_button.grid(row=4, column=0, pady=10, padx=20)

        self.button_3 = ctk.CTkButton(master=self.frame_left,
                                      text="Save Data to .csv",
                                      fg_color=("gray75", "gray30"),
                                      command=housekeeping.save_data)
        self.button_3.grid(row=6, column=0, pady=10, padx=20)

        self.display_button = ctk.CTkButton(master=self.frame_left,
                                            text="Display HK Data",
                                            fg_color=("gray75", "gray30"),
                                            command=lambda H=self: housekeeping.new_housekeeping_display(H))
        self.display_button.grid(row=7, column=0, pady=10, padx=20)

        self.close_button = ctk.CTkButton(master=self.frame_left,
                                          text="Close",
                                          command=lambda: controller.on_closing())
        self.close_button.grid(row=9, column=0, pady=10, padx=20)

        # ============ frame_right ============

        s = Style()
        s.theme_use('default')
        s.layout("TNotebook", [])
        s.configure('TNotebook', background="#333333")
        s.configure('TNotebook.Tab', background="#616161")
        s.map("TNotebook.Tab", background=[("selected", "#395e9c")])
        s.configure("TNotebook", focuscolor=s.configure(".")["background"])

        tabControl = Notebook(self.frame_right)

        # configure grid layout (3x7)
        self.frame_right.rowconfigure(0, weight=1)
        self.frame_right.columnconfigure(0, weight=1)

        self.frame_info = ctk.CTkFrame(master=tabControl)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=8, pady=10, padx=20, sticky="nsew")

        tabControl.add(self.frame_info, text="Housekeeping")

        self.cal_error = ctk.CTkFrame(master=tabControl)
        tabControl.add(self.cal_error, text="Calibration & Error Flags")

        tabControl.grid(row=0, column=0, sticky="nsew")

        # ============ Housekeeping Tab ============

        # configure grid layout (4x4)
        self.frame_info.rowconfigure([1, 2, 3, 4], weight=1)
        self.frame_info.columnconfigure([0, 1, 2, 3], weight=1)

        self.label_info_1 = ctk.CTkLabel(master=self.frame_info,
                                         text="Current and Voltage for All Boards",
                                         height=25,
                                         fg_color=("white", "gray38"),
                                         justify=tkinter.LEFT,
                                         corner_radius=8)
        self.label_info_1.grid(column=0, row=0, columnspan=3, sticky="nwe", padx=15, pady=15)

        """ Create all housekeeping figures with two axes (one for voltage, one for current). Place the figures in
        grid and configure the layout for all graphs """
        self.figure_1 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_1 = self.figure_1.add_subplot(111)
        self.ax_twin_1 = self.ax_1.twinx()
        self.canvas_1 = FigureCanvasTkAgg(self.figure_1, master=self.frame_info)
        self.canvas_1.draw()
        self.canvas_1.get_tk_widget().grid(row=1, column=0, sticky="ew", padx=15, pady=5)

        self.figure_2 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_2 = self.figure_2.add_subplot(111)
        self.ax_twin_2 = self.ax_2.twinx()
        self.canvas_2 = FigureCanvasTkAgg(self.figure_2, master=self.frame_info)
        self.canvas_2.draw()
        self.canvas_2.get_tk_widget().grid(row=2, column=0, sticky="ew", padx=15, pady=5)

        self.figure_3 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_3 = self.figure_3.add_subplot(111)
        self.ax_twin_3 = self.ax_3.twinx()
        self.canvas_3 = FigureCanvasTkAgg(self.figure_3, master=self.frame_info)
        self.canvas_3.draw()
        self.canvas_3.get_tk_widget().grid(row=3, column=0, sticky="ew", padx=15, pady=5)

        self.figure_4 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_4 = self.figure_4.add_subplot(111)
        self.ax_twin_4 = self.ax_4.twinx()
        self.canvas_4 = FigureCanvasTkAgg(self.figure_4, master=self.frame_info)
        self.canvas_4.draw()
        self.canvas_4.get_tk_widget().grid(row=4, column=0, sticky="ew", padx=15, pady=5)

        self.figure_5 = Figure(figsize=(Housekeeping.FIG_WIDTH + 4, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_5 = self.figure_5.add_subplot(111)
        self.ax_twin_5 = self.ax_5.twinx()
        self.canvas_5 = FigureCanvasTkAgg(self.figure_5, master=self.frame_info)
        self.canvas_5.draw()
        self.canvas_5.get_tk_widget().grid(row=1, column=1, columnspan=2, sticky="ns", padx=15, pady=5)

        self.figure_6 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_6 = self.figure_6.add_subplot(111)
        self.ax_twin_6 = self.ax_6.twinx()
        self.canvas_6 = FigureCanvasTkAgg(self.figure_6, master=self.frame_info)
        self.canvas_6.draw()
        self.canvas_6.get_tk_widget().grid(row=2, column=1, sticky="ew", padx=15, pady=5)

        self.figure_7 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_7 = self.figure_7.add_subplot(111)
        self.ax_twin_7 = self.ax_7.twinx()
        self.canvas_7 = FigureCanvasTkAgg(self.figure_7, master=self.frame_info)
        self.canvas_7.draw()
        self.canvas_7.get_tk_widget().grid(row=3, column=1, sticky="ew", padx=15, pady=5)

        self.figure_8 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_8 = self.figure_8.add_subplot(111)
        self.ax_twin_8 = self.ax_8.twinx()
        self.canvas_8 = FigureCanvasTkAgg(self.figure_8, master=self.frame_info)
        self.canvas_8.draw()
        self.canvas_8.get_tk_widget().grid(row=4, column=1, sticky="ew", padx=15, pady=5)

        self.figure_9 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_9 = self.figure_9.add_subplot(111)
        self.ax_twin_9 = self.ax_9.twinx()
        self.canvas_9 = FigureCanvasTkAgg(self.figure_9, master=self.frame_info)
        self.canvas_9.draw()
        self.canvas_9.get_tk_widget().grid(row=2, column=2, sticky="ew", padx=15, pady=5)

        self.figure_10 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_10 = self.figure_10.add_subplot(111)
        self.ax_twin_10 = self.ax_10.twinx()
        self.canvas_10 = FigureCanvasTkAgg(self.figure_10, master=self.frame_info)
        self.canvas_10.draw()
        self.canvas_10.get_tk_widget().grid(row=3, column=2, sticky="ew", padx=15, pady=5)

        self.figure_11 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_11 = self.figure_11.add_subplot(111)
        self.ax_twin_11 = self.ax_11.twinx()
        self.canvas_11 = FigureCanvasTkAgg(self.figure_11, master=self.frame_info)
        self.canvas_11.draw()
        self.canvas_11.get_tk_widget().grid(row=4, column=2, sticky="ew", padx=15, pady=5)

        self.label_info_2 = ctk.CTkLabel(master=self.frame_info,
                                         text="Temperature Readings",
                                         height=25,
                                         fg_color=("white", "gray38"),
                                         justify=tkinter.LEFT,
                                         corner_radius=8)
        self.label_info_2.grid(column=3, row=0, columnspan=1, sticky="nwe", padx=15, pady=15)

        self.figure_12 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_12 = self.figure_12.add_subplot(111)
        self.canvas_12 = FigureCanvasTkAgg(self.figure_12, master=self.frame_info)
        self.canvas_12.draw()
        self.canvas_12.get_tk_widget().grid(row=1, column=3, sticky="ew", padx=15, pady=5)

        self.figure_13 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_13 = self.figure_13.add_subplot(111)
        self.canvas_13 = FigureCanvasTkAgg(self.figure_13, master=self.frame_info)
        self.canvas_13.draw()
        self.canvas_13.get_tk_widget().grid(row=2, column=3, sticky="ew", padx=15, pady=5)

        self.figure_14 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_14 = self.figure_14.add_subplot(111)
        self.canvas_14 = FigureCanvasTkAgg(self.figure_14, master=self.frame_info)
        self.canvas_14.draw()
        self.canvas_14.get_tk_widget().grid(row=3, column=3, sticky="ew", padx=15, pady=5)

        self.figure_15 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_15 = self.figure_15.add_subplot(111)
        self.canvas_15 = FigureCanvasTkAgg(self.figure_15, master=self.frame_info)
        self.canvas_15.draw()
        self.canvas_15.get_tk_widget().grid(row=4, column=3, sticky="ew", padx=15, pady=5)

        # ============ Calibration and Error Flag Tab =============

        self.cal_error.rowconfigure((0, 1, 2, 3), weight=1)
        self.cal_error.columnconfigure(0, weight=10, minsize=750)
        self.cal_error.columnconfigure(1, weight=1)

        self.cal_label = ctk.CTkLabel(master=self.cal_error,
                                      text="Calibration Plots",
                                      height=25,
                                      fg_color=("white", "gray38"),
                                      justify=tkinter.LEFT,
                                      corner_radius=8)
        self.cal_label.grid(row=0, column=0, sticky="ew", padx=15, pady=5)

        self.figure_16 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_16 = self.figure_16.add_subplot(111)
        self.ax_twin_12 = self.ax_16.twinx()
        self.canvas_16 = FigureCanvasTkAgg(self.figure_16, master=self.cal_error)
        self.canvas_16.draw()
        self.canvas_16.get_tk_widget().grid(row=1, column=0, sticky="ew", padx=15, pady=5)

        self.figure_17 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_17 = self.figure_17.add_subplot(111)
        self.ax_twin_13 = self.ax_17.twinx()
        self.canvas_17 = FigureCanvasTkAgg(self.figure_17, master=self.cal_error)
        self.canvas_17.draw()
        self.canvas_17.get_tk_widget().grid(row=2, column=0, sticky="ew", padx=15, pady=5)

        self.figure_18 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=Housekeeping.DPI)
        self.ax_18 = self.figure_18.add_subplot(111)
        self.ax_twin_14 = self.ax_18.twinx()
        self.canvas_18 = FigureCanvasTkAgg(self.figure_18, master=self.cal_error)
        self.canvas_18.draw()
        self.canvas_18.get_tk_widget().grid(row=3, column=0, sticky="ew", padx=15, pady=5)

        self.error_frame = ctk.CTkFrame(master=self.cal_error, fg_color="#292929")
        self.error_frame.grid(row=1, rowspan=3, column=1, sticky="nsew", padx=15, pady=15)

        self.error_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.error_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.error_label = ctk.CTkLabel(master=self.cal_error,
                                        text="Error Flags",
                                        height=25,
                                        fg_color=("white", "gray38"),
                                        justify=tkinter.LEFT,
                                        corner_radius=8)
        self.error_label.grid(row=0, column=1, sticky="ew", padx=15, pady=15)

        self.CDH_Comm_State = ctk.CTkLabel(master=self.error_frame,
                                           text="CDH Comm Task Status: Start Up",
                                           fg_color="orange",
                                           height=40)
        self.CDH_Comm_State.grid(row=9, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        error_grid.append(self.CDH_Comm_State)

        counter = 0
        for i in range(0, 9):
            for j in range(0, 4):
                button = ctk.CTkButton(master=self.error_frame,
                                       fg_color="orange",
                                       hover_color="black",
                                       text="Start Up",
                                       text_font=("Kanit", -10),
                                       command=lambda idx=counter: housekeeping.see_error(idx))
                button.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                error_grid.append(button)
                counter += 1

        # ============ Save all Figures/Axes =============

        fig.extend([self.figure_1, self.figure_2, self.figure_3, self.figure_4, self.figure_5, self.figure_6,
                    self.figure_7, self.figure_8, self.figure_9, self.figure_10, self.figure_11, self.figure_12,
                    self.figure_13, self.figure_14, self.figure_15, self.figure_16, self.figure_17, self.figure_18])

        axes.extend([self.ax_1, self.ax_2, self.ax_3, self.ax_4, self.ax_5, self.ax_6, self.ax_7, self.ax_8,
                     self.ax_9, self.ax_10, self.ax_11, self.ax_12, self.ax_13, self.ax_14, self.ax_15, self.ax_16,
                     self.ax_17, self.ax_18])

        axes_twins.extend([self.ax_twin_1, self.ax_twin_2, self.ax_twin_3, self.ax_twin_4, self.ax_twin_5,
                           self.ax_twin_6, self.ax_twin_7, self.ax_twin_8, self.ax_twin_9, self.ax_twin_10,
                           self.ax_twin_11, self.ax_twin_12, self.ax_twin_13, self.ax_twin_14])

        """ Save the background of each figure for faster updating when data is received from the serial port """
        for i in range(0, len(axes)):
            axes[i].patch.set_color("black")
            fig[i].set_facecolor("dimgrey")
            axes[i].set_title(plot_names[i])
            axes[i].set_xlim(0, deque_size)
            if i < 11:
                axes[i].set_ylim(voltage_limits[i])
                axes[i].set_ylabel("Voltage [V]", color='white')
            elif 11 <= i < 15:
                axes[i].set_ylim(temp_limits[i - 11])
                axes[i].set_ylabel("Temperature [C]", color='red')
            else:
                axes[i].set_ylim(offset_limits[i - 15])
                axes[i].set_ylabel("Current DC Offset [mA]", color='white')
            axes_background.append(fig[i].canvas.copy_from_bbox(axes[i].bbox))
            axes[i].get_xaxis().set_visible(False)
            fig[i].tight_layout()

        for i in range(0, len(axes_twins)):
            if i < 11:
                axes_twins[i].set_xlim(0, deque_size)
                axes_twins[i].set_ylim(current_limits[i])
                axes_twins[i].set_ylabel("Current [mA]", color='blue')
                axes_twins_background.append(fig[i].canvas.copy_from_bbox(axes_twins[i].bbox))
            else:
                axes_twins[i].set_xlim(0, deque_size)
                axes_twins[i].set_ylim(amplitude_limits[i - 11])
                axes_twins[i].set_ylabel("Current Amplitude [mA]", color='blue')
                axes_twins_background.append(fig[i + 4].canvas.copy_from_bbox(axes_twins[i].bbox))

        """ Create artists for updating figure when new data is received """
        artist_1.extend([axes[0].plot([], [], color='white')[0],
                        axes[1].plot([], [], color='white')[0],
                        axes[2].plot([], [], color='white')[0],
                        axes[3].plot([], [], color='white')[0],
                        axes[4].plot([], [], color='white')[0],
                        axes[5].plot([], [], color='white')[0],
                        axes[6].plot([], [], color='white')[0],
                        axes[7].plot([], [], color='white')[0],
                        axes[8].plot([], [], color='white')[0],
                        axes[9].plot([], [], color='white')[0],
                        axes[10].plot([], [], color='white')[0],
                        axes[11].plot([], [], color='red')[0],
                        axes[12].plot([], [], color='red')[0],
                        axes[13].plot([], [], color='red')[0],
                        axes[14].plot([], [], color='red')[0],
                        axes[15].plot([], [], color='white')[0],
                        axes[16].plot([], [], color='white')[0],
                        axes[17].plot([], [], color='white')[0]])

        artist_2.extend([axes_twins[0].plot([], [], color='blue')[0],
                        axes_twins[1].plot([], [], color='blue')[0],
                        axes_twins[2].plot([], [], color='blue')[0],
                        axes_twins[3].plot([], [], color='blue')[0],
                        axes_twins[4].plot([], [], color='blue')[0],
                        axes_twins[5].plot([], [], color='blue')[0],
                        axes_twins[6].plot([], [], color='blue')[0],
                        axes_twins[7].plot([], [], color='blue')[0],
                        axes_twins[8].plot([], [], color='blue')[0],
                        axes_twins[9].plot([], [], color='blue')[0],
                        axes_twins[10].plot([], [], color='blue')[0],
                        axes_twins[11].plot([], [], color='blue')[0],
                        axes_twins[12].plot([], [], color='blue')[0],
                        axes_twins[13].plot([], [], color='blue')[0]])


class Commands(ctk.CTkFrame):
    """
    The 'Commands' page is responsible for visualizing the commands that the user is capable of sending to the PIC,
    this page has sections for board control, configuration control, and serial port control. It also has a section to
    display the current configuration
    """

    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self,
                                       width=180,
                                       corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.img = ImageTk.PhotoImage(Image.open("cosmo-logo.png").resize((180, 180)))
        self.logo = ctk.CTkLabel(master=self.frame_left, image=self.img)
        self.logo.grid(row=0, column=0, pady=5, padx=5)

        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                    text="Command Page",
                                    text_font=("Roboto Medium", -20))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.housekeeping_button = ctk.CTkButton(master=self.frame_left,
                                                 text="Housekeeping",
                                                 fg_color=("gray75", "gray30"),
                                                 command=lambda: controller.show_frame(Housekeeping))
        self.housekeeping_button.grid(row=2, column=0, pady=10, padx=20)

        self.command_button = ctk.CTkButton(master=self.frame_left,
                                            text="Commands",
                                            fg_color=("gray75", "gray30"))
        self.command_button.grid(row=3, column=0, pady=10, padx=20)

        self.science_button = ctk.CTkButton(master=self.frame_left,
                                            text="Science",
                                            fg_color=("gray75", "gray30"),
                                            command=lambda: controller.show_frame(Science))
        self.science_button.grid(row=4, column=0, pady=10, padx=20)

        self.close_button = ctk.CTkButton(master=self.frame_left,
                                          text="Close",
                                          command=lambda: controller.on_closing())
        self.close_button.grid(row=9, column=0, pady=10, padx=20)

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(1, weight=25)
        self.frame_right.columnconfigure(3, weight=1)

        self.Board_CTRL = ctk.CTkFrame(master=self.frame_right)
        self.Board_CTRL.grid(row=0, column=0, rowspan=8, pady=20, padx=20, sticky="nsew")

        self.Config_CTRL = ctk.CTkFrame(master=self.frame_right)
        self.Config_CTRL.grid(row=0, column=1, rowspan=4, pady=20, padx=20, sticky="nsew")

        self.Current_Config = ctk.CTkFrame(master=self.frame_right)
        self.Current_Config.grid(row=4, column=1, rowspan=4, pady=20, padx=20, sticky="nsew")

        self.Serial_Config = ctk.CTkFrame(master=self.frame_right)
        self.Serial_Config.grid(row=1, column=2, rowspan=7, pady=20, padx=20, sticky="nsew")

        self.Serial_Settings = ctk.CTkFrame(master=self.frame_right)
        self.Serial_Settings.grid(row=0, column=2, rowspan=1, pady=20, padx=20, sticky="nsew")

        # ============ BOARD ON/OFF CONTROL ============

        # configure grid layout (17x2)
        self.Board_CTRL.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), weight=1)
        self.Board_CTRL.columnconfigure((0, 1), weight=1)

        # Analog Board Control
        self.analog_board_ctrl = ctk.CTkLabel(master=self.Board_CTRL,
                                              text="Analog Board Control",
                                              height=50,
                                              fg_color=("white", "gray38"),
                                              justify=tkinter.LEFT,
                                              corner_radius=8)
        self.analog_board_ctrl.grid(column=0, row=1, columnspan=2, sticky="nwe", padx=15, pady=15)

        self.analog_on_off = tkinter.IntVar(value=1)

        analog_img = ImageTk.PhotoImage(Image.open("green_button.png").resize((65, 65)))
        self.analog_led = ctk.CTkLabel(master=self.Board_CTRL, image=analog_img)
        self.analog_led.image = analog_img
        self.analog_led.grid(row=2, rowspan=2, column=0, sticky="n", padx=5, pady=5)

        self.analog_on = ctk.CTkRadioButton(master=self.Board_CTRL,
                                            text="on",
                                            variable=self.analog_on_off,
                                            value=1,
                                            command=lambda: communications.send_data(CDH_ANALOG_CTRL, ON))
        self.analog_on.grid(row=2, column=1, sticky="nswe", padx=5, pady=5)

        self.analog_off = ctk.CTkRadioButton(master=self.Board_CTRL,
                                             text="off",
                                             variable=self.analog_on_off,
                                             value=0,
                                             command=lambda: communications.send_data(CDH_ANALOG_CTRL, OFF))
        self.analog_off.grid(row=3, column=1, sticky="nswe", padx=5, pady=5)

        # Scalar Board 1 Control
        self.scalar_board_1_ctrl = ctk.CTkLabel(master=self.Board_CTRL,
                                                text="Scalar Board No.1 Control",
                                                height=50,
                                                fg_color=("white", "gray38"),
                                                justify=tkinter.LEFT,
                                                corner_radius=8)
        self.scalar_board_1_ctrl.grid(column=0, row=4, columnspan=2, sticky="nwe", padx=15, pady=15)

        self.sb1_on_off = tkinter.IntVar(value=0)

        sb1_img = ImageTk.PhotoImage(Image.open("red_button.png").resize((65, 65)))
        self.sb1_led = ctk.CTkLabel(master=self.Board_CTRL, image=sb1_img)
        self.sb1_led.image = sb1_img
        self.sb1_led.grid(row=5, rowspan=2, column=0, sticky="n", padx=5, pady=5)

        self.sb1_on = ctk.CTkRadioButton(master=self.Board_CTRL,
                                         text="on",
                                         variable=self.sb1_on_off,
                                         value=1,
                                         command=lambda: communications.send_data(CDH_SCALAR1_CTRL, ON))
        self.sb1_on.grid(row=5, column=1, sticky="nswe", padx=5, pady=5)

        self.sb1_off = ctk.CTkRadioButton(master=self.Board_CTRL,
                                          text="off",
                                          variable=self.sb1_on_off,
                                          value=0,
                                          command=lambda: communications.send_data(CDH_SCALAR1_CTRL, OFF))
        self.sb1_off.grid(row=6, column=1, sticky="nswe", padx=5, pady=5)

        # Scalar Board 2 Control
        self.scalar_board_2_ctrl = ctk.CTkLabel(master=self.Board_CTRL,
                                                text="Scalar Board No.2 Control",
                                                height=50,
                                                fg_color=("white", "gray38"),
                                                justify=tkinter.LEFT,
                                                corner_radius=8)
        self.scalar_board_2_ctrl.grid(column=0, row=7, columnspan=2, sticky="nwe", padx=15, pady=15)

        self.sb2_on_off = tkinter.IntVar(value=0)

        sb2_img = ImageTk.PhotoImage(Image.open("red_button.png").resize((65, 65)))
        self.sb2_led = ctk.CTkLabel(master=self.Board_CTRL, image=sb2_img)
        self.sb2_led.image = sb2_img
        self.sb2_led.grid(row=8, rowspan=2, column=0, sticky="n", padx=5, pady=5)

        self.sb2_on = ctk.CTkRadioButton(master=self.Board_CTRL,
                                         text="on",
                                         variable=self.sb2_on_off,
                                         value=1,
                                         command=lambda: communications.send_data(CDH_SCALAR2_CTRL, ON))
        self.sb2_on.grid(row=8, column=1, sticky="nswe", padx=5, pady=5)

        self.sb2_off = ctk.CTkRadioButton(master=self.Board_CTRL,
                                          text="off",
                                          variable=self.sb2_on_off,
                                          value=0,
                                          command=lambda: communications.send_data(CDH_SCALAR2_CTRL, OFF))
        self.sb2_off.grid(row=9, column=1, sticky="nswe", padx=5, pady=5)

        # Star Tracker 1 Control
        self.star_tracker_1_ctrl = ctk.CTkLabel(master=self.Board_CTRL,
                                                text="Star Tracker 1 Control",
                                                height=50,
                                                fg_color=("white", "gray38"),
                                                justify=tkinter.LEFT,
                                                corner_radius=8)
        self.star_tracker_1_ctrl.grid(column=0, row=10, columnspan=2, sticky="nwe", padx=15, pady=15)

        self.st1_on_off = tkinter.IntVar(value=0)

        st1_img = ImageTk.PhotoImage(Image.open("red_button.png").resize((65, 65)))
        self.st1_led = ctk.CTkLabel(master=self.Board_CTRL, image=st1_img)
        self.st1_led.image = st1_img
        self.st1_led.grid(row=11, rowspan=2, column=0, sticky="n", padx=5, pady=5)

        self.st1_on = ctk.CTkRadioButton(master=self.Board_CTRL,
                                         text="on",
                                         variable=self.st1_on_off,
                                         value=1,
                                         command=lambda: communications.send_data(CDH_STAR_TRACK1_CTRL, ON))
        self.st1_on.grid(row=11, column=1, sticky="nswe", padx=5, pady=5)

        self.st1_off = ctk.CTkRadioButton(master=self.Board_CTRL,
                                          text="off",
                                          variable=self.st1_on_off,
                                          value=0,
                                          command=lambda: communications.send_data(CDH_STAR_TRACK1_CTRL, OFF))
        self.st1_off.grid(row=12, column=1, sticky="nswe", padx=5, pady=5)

        # Star Tracker 2 Control
        self.star_tracker_2_ctrl = ctk.CTkLabel(master=self.Board_CTRL,
                                                text="Star Tracker 2 Control",
                                                height=50,
                                                fg_color=("white", "gray38"),
                                                justify=tkinter.LEFT,
                                                corner_radius=8)
        self.star_tracker_2_ctrl.grid(column=0, row=13, columnspan=2, sticky="nwe", padx=15, pady=15)

        self.st2_on_off = tkinter.IntVar(value=0)

        st2_img = ImageTk.PhotoImage(Image.open("red_button.png").resize((65, 65)))
        self.st2_led = ctk.CTkLabel(master=self.Board_CTRL, image=st2_img)
        self.st2_led.image = st2_img
        self.st2_led.grid(row=14, rowspan=2, column=0, sticky="n", padx=5, pady=5)

        self.st2_on = ctk.CTkRadioButton(master=self.Board_CTRL,
                                         text="on",
                                         variable=self.st2_on_off,
                                         value=1,
                                         command=lambda: communications.send_data(CDH_STAR_TRACK2_CTRL, ON))
        self.st2_on.grid(row=14, column=1, sticky="nswe", padx=5, pady=5)

        self.st2_off = ctk.CTkRadioButton(master=self.Board_CTRL,
                                          text="off",
                                          variable=self.st2_on_off,
                                          value=0,
                                          command=lambda: communications.send_data(CDH_STAR_TRACK2_CTRL, OFF))
        self.st2_off.grid(row=15, column=1, sticky="nswe", padx=5, pady=5)

        # ============ SAVE BOARD LEDs TO VARIABLE ============

        board_led.extend([self.analog_led, self.sb1_led, self.sb2_led, self.st1_led, self.st2_led])

        # ============ CONFIGURATION CONTROL ============

        # configure grid layout (2x2)
        self.Config_CTRL.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.Config_CTRL.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.config_ctrl_label = ctk.CTkLabel(master=self.Config_CTRL,
                                              text="Configuration Control",
                                              height=50,
                                              fg_color=("white", "gray38"),
                                              corner_radius=8)
        self.config_ctrl_label.grid(row=0, column=0, columnspan=6, sticky="ew", padx=60, pady=5)

        # Coil 1
        self.coil_1_label = ctk.CTkLabel(master=self.Config_CTRL,
                                         text="Coil 1",
                                         fg_color=("white", "#292929"),
                                         corner_radius=8)
        self.coil_1_label.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10)

        self.coil_1_frequency_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                   text="Frequency")
        self.coil_1_frequency_label.grid(row=2, column=0, sticky="ew")

        self.freq_1 = tkinter.StringVar()
        self.coil_1_frequency = ctk.CTkEntry(master=self.Config_CTRL,
                                             textvariable=self.freq_1,
                                             placeholder_text="Enter Coil 1 Frequency in Hz...",
                                             text_color="cornflowerblue")
        self.coil_1_frequency.grid(row=2, column=1, columnspan=2, sticky="ew", padx=30, pady=5)

        self.coil_1_amplitude_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                   text="Amplitude")
        self.coil_1_amplitude_label.grid(row=3, column=0, sticky="ew")

        self.amp_1 = tkinter.IntVar()
        self.amp_1_label = ctk.CTkLabel(master=self.Config_CTRL, text="100%")
        self.amp_1_label.grid(row=3, column=2)

        self.coil_1_amplitude = ctk.CTkSlider(master=self.Config_CTRL,
                                              variable=self.amp_1,
                                              from_=0,
                                              to=127,
                                              number_of_steps=127,
                                              command=commands.change_amp_1)
        self.coil_1_amplitude.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Coil 2
        self.coil_2_label = ctk.CTkLabel(master=self.Config_CTRL,
                                         text="Coil 2",
                                         fg_color=("white", "#292929"),
                                         corner_radius=8)
        self.coil_2_label.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10)

        self.coil_2_frequency_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                   text="Frequency")
        self.coil_2_frequency_label.grid(row=5, column=0, sticky="ew")

        self.freq_2 = tkinter.StringVar()
        self.coil_2_frequency = ctk.CTkEntry(master=self.Config_CTRL,
                                             textvariable=self.freq_2,
                                             placeholder_text="Enter Coil 2 Frequency in Hz...",
                                             text_color="cornflowerblue")
        self.coil_2_frequency.grid(row=5, column=1, columnspan=2, sticky="ew", padx=30, pady=5)

        self.coil_2_amplitude_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                   text="Amplitude")
        self.coil_2_amplitude_label.grid(row=6, column=0, sticky="ew")

        self.amp_2 = tkinter.IntVar()
        self.amp_2_label = ctk.CTkLabel(master=self.Config_CTRL, text="100%")
        self.amp_2_label.grid(row=6, column=2)

        self.coil_2_amplitude = ctk.CTkSlider(master=self.Config_CTRL,
                                              variable=self.amp_2,
                                              from_=0,
                                              to=127,
                                              number_of_steps=127,
                                              command=commands.change_amp_2)
        self.coil_2_amplitude.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        # Coil 3
        self.coil_3_label = ctk.CTkLabel(master=self.Config_CTRL,
                                         text="Coil 3",
                                         fg_color=("white", "#292929"),
                                         corner_radius=8)
        self.coil_3_label.grid(row=7, column=0, columnspan=3, sticky="ew", padx=10)

        self.coil_3_frequency_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                   text="Frequency")
        self.coil_3_frequency_label.grid(row=8, column=0, sticky="ew")

        self.freq_3 = tkinter.StringVar()
        self.coil_3_frequency = ctk.CTkEntry(master=self.Config_CTRL,
                                             textvariable=self.freq_3,
                                             placeholder_text="Enter Coil 3 Frequency in Hz...",
                                             text_color="cornflowerblue")
        self.coil_3_frequency.grid(row=8, column=1, columnspan=2, sticky="ew", padx=30, pady=5)

        self.coil_3_amplitude_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                   text="Amplitude")
        self.coil_3_amplitude_label.grid(row=9, column=0, sticky="ew")

        self.amp_3 = tkinter.IntVar()
        self.amp_3_label = ctk.CTkLabel(master=self.Config_CTRL, text="100%")
        self.amp_3_label.grid(row=9, column=2)

        self.coil_3_amplitude = ctk.CTkSlider(master=self.Config_CTRL,
                                              variable=self.amp_3,
                                              from_=0,
                                              to=127,
                                              number_of_steps=127,
                                              command=commands.change_amp_3)
        self.coil_3_amplitude.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

        # Scalar Sample Rate
        self.scalar_sample_label = ctk.CTkLabel(master=self.Config_CTRL,
                                                text="Scalar Sample Rate",
                                                fg_color=("white", "#292929"),
                                                corner_radius=8)
        self.scalar_sample_label.grid(row=1, column=3, columnspan=3, sticky="ew", padx=20)

        self.scalar_sample = ctk.CTkOptionMenu(master=self.Config_CTRL,
                                               values=["100 Hz", "250 Hz"])
        self.scalar_sample.grid(row=2, column=4, padx=5, pady=5)

        # Scalar Baud Rate
        self.scalar_baud_label = ctk.CTkLabel(master=self.Config_CTRL,
                                              text="Scalar Baud Rate",
                                              fg_color=("white", "#292929"),
                                              corner_radius=8)
        self.scalar_baud_label.grid(row=3, column=3, columnspan=3, sticky="ew", padx=20)

        self.scalar_baud = ctk.CTkOptionMenu(master=self.Config_CTRL,
                                             values=["115200", "230400", "460800", "921600"])
        self.scalar_baud.grid(row=4, column=4, padx=5, pady=5)

        # Submit Button
        self.config_submit = ctk.CTkButton(master=self.Config_CTRL,
                                           text="Submit Configuration",
                                           command=lambda: commands.new_config())
        self.config_submit.grid(row=10, column=0, columnspan=6, sticky="ew", pady=10, padx=125)

        # Default Settings
        self.coil_1_amplitude.set(127)
        self.coil_2_amplitude.set(127)
        self.coil_3_amplitude.set(127)

        # ============ CURRENT CONFIGURATION FRAME ============

        # configure grid layout (2x2)
        self.Current_Config.rowconfigure((0, 1), weight=1)
        self.Current_Config.columnconfigure((0, 1, 2), weight=1)

        self.current_config_label = ctk.CTkLabel(master=self.Current_Config,
                                                 text="Current Configuration",
                                                 height=50,
                                                 fg_color=("white", "gray38"),
                                                 corner_radius=8)
        self.current_config_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=60, pady=5)

        # ============ CURRENT CONFIGURATION FRAME 1 ============

        self.Current_Config_frame_1 = ctk.CTkFrame(master=self.Current_Config, fg_color=("#dbdbdb", "#333333"))
        self.Current_Config_frame_1.grid(row=1, column=0, padx=20, sticky="new")

        self.Current_Config_frame_1.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.Current_Config_frame_1.columnconfigure((0, 1), weight=1)

        # Coil 1

        self.coil_1 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                   text="Coil 1",
                                   height=20,
                                   fg_color=("white", "#292929"),
                                   corner_radius=8)
        self.coil_1.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        self.current_freq_1 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                           text="9 Hz",
                                           text_font=("Kanit", 20, "bold"),
                                           height=10)
        self.current_freq_1.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.amp_1_bar = ctk.CTkProgressBar(master=self.Current_Config_frame_1, height=20)
        self.amp_1_bar.set(1)
        self.amp_1_bar.grid(row=2, column=0)

        self.current_amp_1 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                          text="100%",
                                          text_font=("Kanit", 20, "bold"),
                                          height=10)
        self.current_amp_1.grid(row=2, column=1, sticky="ew")

        # Coil 2

        self.coil_2 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                   text="Coil 2",
                                   height=20,
                                   fg_color=("white", "#292929"),
                                   corner_radius=8)
        self.coil_2.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.current_freq_2 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                           text="16 Hz",
                                           text_font=("Kanit", 20, "bold"),
                                           height=10)
        self.current_freq_2.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.amp_2_bar = ctk.CTkProgressBar(master=self.Current_Config_frame_1, height=20)
        self.amp_2_bar.set(1)
        self.amp_2_bar.grid(row=5, column=0)

        self.current_amp_2 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                          text="100%",
                                          text_font=("Kanit", 20, "bold"),
                                          height=10)
        self.current_amp_2.grid(row=5, column=1, sticky="ew")

        # Coil 3

        self.coil_3 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                   text="Coil 3",
                                   height=20,
                                   fg_color=("white", "#292929"),
                                   corner_radius=8)
        self.coil_3.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.current_freq_3 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                           text="20 Hz",
                                           text_font=("Kanit", 20, "bold"),
                                           height=10)
        self.current_freq_3.grid(row=7, column=0, columnspan=2, sticky="ew")

        self.amp_3_bar = ctk.CTkProgressBar(master=self.Current_Config_frame_1, height=20)
        self.amp_3_bar.set(1)
        self.amp_3_bar.grid(row=8, column=0)

        self.current_amp_3 = ctk.CTkLabel(master=self.Current_Config_frame_1,
                                          text="100%",
                                          text_font=("Kanit", 20, "bold"),
                                          height=10)
        self.current_amp_3.grid(row=8, column=1, sticky="ew")

        # ============ CURRENT CONFIGURATION FRAME 2 ============

        self.Current_Config_frame_2 = ctk.CTkFrame(master=self.Current_Config, fg_color=("#dbdbdb", "#333333"))
        self.Current_Config_frame_2.grid(row=1, column=1, padx=20, sticky="new")

        self.Current_Config_frame_2.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.Current_Config_frame_2.columnconfigure(0, weight=2)

        self.current_scalar_sample_rate_label = ctk.CTkLabel(master=self.Current_Config_frame_2,
                                                             text="Scalar Sample Rate",
                                                             height=20,
                                                             fg_color=("white", "#292929"),
                                                             corner_radius=8)
        self.current_scalar_sample_rate_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        current_scalar_sample_rate.append(ctk.CTkLabel(master=self.Current_Config_frame_2,
                                                       text="100 Hz",
                                                       text_font=("Kanit", 20, "bold")))
        current_scalar_sample_rate[0].grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.current_scalar_baud_rate_label = ctk.CTkLabel(master=self.Current_Config_frame_2,
                                                           text="Scalar Baud Rate",
                                                           height=20,
                                                           fg_color=("white", "#292929"),
                                                           corner_radius=8)
        self.current_scalar_baud_rate_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        current_scalar_baud_rate.append(ctk.CTkLabel(master=self.Current_Config_frame_2,
                                                     text="115200",
                                                     text_font=("Kanit", 20, "bold")))
        current_scalar_baud_rate[0].grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        # ============ SERIAL PORT CONFIGURATION ============

        self.Serial_Config.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.Serial_Config.columnconfigure(0, weight=1)

        self.serial_label = ctk.CTkLabel(master=self.Serial_Config,
                                         text="Serial Port Configuration",
                                         fg_color=("white", "gray38"),
                                         corner_radius=8)
        self.serial_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)

        properties = port.get_serial_properties(serial_port[0])

        self.baud_rate_label = ctk.CTkLabel(master=self.Serial_Config,
                                            text="Rate: " + properties[0])
        self.baud_rate_label.grid(row=1, column=0, sticky="new")

        self.byte_size_label = ctk.CTkLabel(master=self.Serial_Config,
                                            text="Byte Size: " + properties[1])
        self.byte_size_label.grid(row=2, column=0, sticky="new")

        self.parity_label = ctk.CTkLabel(master=self.Serial_Config,
                                         text="Parity: " + properties[2])
        self.parity_label.grid(row=3, column=0, sticky="new")

        self.stop_bits_label = ctk.CTkLabel(master=self.Serial_Config,
                                            text="Stop Bits: " + properties[3])
        self.stop_bits_label.grid(row=4, column=0, sticky="new")

        self.packet_request = ctk.CTkLabel(master=self.Serial_Config,
                                           text="Science Requests",
                                           fg_color=("white", "gray38"),
                                           corner_radius=8)
        self.packet_request.grid(row=5, column=0, sticky="new", padx=10, pady=10)

        stream_science_checkbox.append(ctk.CTkCheckBox(master=self.Serial_Config,
                                                       text="Stream Science",
                                                       command=commands.stream_science))
        stream_science_checkbox[0].grid(row=6, column=0, sticky="new", padx=25, pady=10)

        self.sci_request = ctk.CTkButton(master=self.Serial_Config,
                                         text="Science Packet",
                                         command=commands.request_science)
        self.sci_request.grid(row=7, column=0, sticky="new", padx=25, pady=10)

        self.presets = ctk.CTkLabel(master=self.Serial_Config,
                                    text="Presets",
                                    fg_color=("white", "gray38"),
                                    corner_radius=8)
        self.presets.grid(row=8, column=0, sticky="new", padx=10, pady=10)

        self.default_config = ctk.CTkButton(master=self.Serial_Config,
                                            text="Default Configuration",
                                            command=commands.restore_default)
        self.default_config.grid(row=9, column=0, sticky="new", padx=25, pady=10)

        self.play_game = ctk.CTkButton(master=self.Serial_Config,
                                       text="Begin",
                                       command=lambda C=self: hidden.easter_egg(C))
        self.play_game.grid(row=10, column=0, sticky="new", padx=25, pady=10)

        # ============ SERIAL PORT SETTINGS ============

        self.Serial_Settings.rowconfigure((0, 1, 2), weight=1)
        self.Serial_Settings.columnconfigure(0, weight=1)

        self.connection_label = ctk.CTkLabel(master=self.Serial_Settings,
                                             text=port.serial_name(serial_port[0]),
                                             fg_color=("white", "gray38"),
                                             corner_radius=8)
        self.connection_label.grid(row=0, column=0, pady=5, padx=20)

        self.change_com = ctk.CTkButton(master=self.Serial_Settings,
                                        text="Change Port",
                                        command=lambda C=self: port.new_port(C))
        self.change_com.grid(row=1, column=0, padx=20, pady=5)

        # =========== APPEND OBJECTS TO VARIABLES ============
        current_frequencies.extend([self.current_freq_1, self.current_freq_2, self.current_freq_3])
        current_amplitudes.extend([self.current_amp_1, self.current_amp_2, self.current_amp_3])
        amplitude_bars.extend([self.amp_1_bar, self.amp_2_bar, self.amp_3_bar])

        frequencies.extend([self.freq_1, self.freq_2, self.freq_3])
        amplitudes.extend([self.amp_1, self.amp_2, self.amp_3])
        user_amplitudes.extend([self.coil_1_amplitude, self.coil_2_amplitude, self.coil_3_amplitude])
        amplitude_labels.extend([self.amp_1_label, self.amp_2_label, self.amp_3_label])
        scalar_values.extend([self.scalar_baud, self.scalar_sample])


class Science(ctk.CTkFrame):
    """
    The 'Science' page houses three graphs displaying a portion of the data received from science packets every second.
    It also displays the state of the magnetometer and offers options to save to a file as well as display live data, as
    well as displaying a spectrogram of the magnetometer data.
    """

    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self,
                                       width=180,
                                       corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.img = ImageTk.PhotoImage(Image.open("cosmo-logo.png").resize((180, 180)))
        self.logo = ctk.CTkLabel(master=self.frame_left, image=self.img)
        self.logo.grid(row=0, column=0, pady=5, padx=5)

        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                    text="Science Page",
                                    text_font=("Roboto Medium", -20))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.housekeeping_button = ctk.CTkButton(master=self.frame_left,
                                                 text="Housekeeping",
                                                 fg_color=("gray75", "gray30"),
                                                 command=lambda: controller.show_frame(Housekeeping))
        self.housekeeping_button.grid(row=2, column=0, pady=10, padx=20)

        self.command_button = ctk.CTkButton(master=self.frame_left,
                                            text="Commands",
                                            fg_color=("gray75", "gray30"),
                                            command=lambda: controller.show_frame(Commands))
        self.command_button.grid(row=3, column=0, pady=10, padx=20)

        self.science_button = ctk.CTkButton(master=self.frame_left,
                                            text="Science",
                                            fg_color=("gray75", "gray30"))
        self.science_button.grid(row=4, column=0, pady=10, padx=20)

        self.close_button = ctk.CTkButton(master=self.frame_left,
                                          text="Close",
                                          command=lambda: controller.on_closing())
        self.close_button.grid(row=9, column=0, pady=10, padx=20)

        # ============ frame_right ============

        s = Style()
        s.theme_use('default')
        s.layout("TNotebook", [])
        s.configure('TNotebook', background="#333333")
        s.configure('TNotebook.Tab', background="#616161")
        s.map("TNotebook.Tab", background=[("selected", "#395e9c")])
        s.configure("TNotebook", focuscolor=s.configure(".")["background"])

        tabControl = Notebook(self.frame_right)

        self.frame_right.rowconfigure(0, weight=1)
        self.frame_right.columnconfigure(0, weight=1)

        self.magnetometer_frame = ctk.CTkFrame(master=tabControl)
        tabControl.add(self.magnetometer_frame, text="Magnetometer Data/State")

        self.magnetometer_frame.rowconfigure(0, weight=1)
        self.magnetometer_frame.rowconfigure(1, weight=50, minsize=500)
        self.magnetometer_frame.columnconfigure(0, weight=1, minsize=350)
        self.magnetometer_frame.columnconfigure(1, weight=50)

        self.frame_options = ctk.CTkFrame(master=self.magnetometer_frame)
        self.frame_options.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.frame_sci_plot = ctk.CTkFrame(master=self.magnetometer_frame)
        self.frame_sci_plot.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=20)

        self.frame_state = ctk.CTkFrame(master=self.magnetometer_frame)
        self.frame_state.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.star_tracker_frame = ctk.CTkFrame(master=tabControl)
        tabControl.add(self.star_tracker_frame, text="Star Tracker Data")

        tabControl.grid(row=0, column=0, sticky="nsew")

        # ============ frame_options ============

        self.frame_options.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.frame_options.columnconfigure(0, weight=1)

        self.options_label = ctk.CTkLabel(master=self.frame_options,
                                          text="Save Science Data",
                                          height=50,
                                          fg_color=("white", "gray38"),
                                          justify=tkinter.LEFT,
                                          corner_radius=8)
        self.options_label.grid(row=0, column=0, sticky="ew", pady=5, padx=20)

        write_checkbox.append(ctk.CTkCheckBox(master=self.frame_options,
                                              text="Write to File"))
        write_checkbox[0].grid(row=1, column=0, sticky="s")

        self.number_saved = ctk.CTkLabel(master=self.frame_options,
                                         text="Data Points Saved",
                                         text_font=("Artico Condensed Light", -18),
                                         height=50)
        self.number_saved.grid(row=2, column=0, sticky="nsew", pady=5, padx=5)

        points_saved.append(ctk.CTkLabel(master=self.frame_options,
                                         text="0",
                                         text_font=("Kanit", -20, "bold"),
                                         fg_color=("white", "gray38"),
                                         corner_radius=8))
        points_saved[0].grid(row=3, column=0, sticky="ns")

        self.save_file = ctk.CTkButton(master=self.frame_options,
                                       text="Save File",
                                       command=lambda: science.save_file)
        self.save_file.grid(row=4, column=0, padx=5, pady=5)

        self.options_label = ctk.CTkLabel(master=self.frame_options,
                                          text="Science Options",
                                          height=50,
                                          fg_color=("white", "gray38"),
                                          justify=tkinter.LEFT,
                                          corner_radius=8)
        self.options_label.grid(row=5, column=0, sticky="ew", pady=5, padx=20)

        self.display_button = ctk.CTkButton(master=self.frame_options,
                                            text="Display Science Data",
                                            command=lambda S=self: science.new_science_display(S))
        self.display_button.grid(row=6, column=0, pady=5, padx=5)

        # ============ frame_sci_plot ============

        self.frame_sci_plot.rowconfigure((0, 1, 2), weight=1)
        self.frame_sci_plot.columnconfigure(0, weight=1)

        self.figure_1 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=50)
        self.ax_1 = self.figure_1.add_subplot(111)
        self.canvas_1 = FigureCanvasTkAgg(self.figure_1, master=self.frame_sci_plot)
        self.canvas_1.draw()
        self.canvas_1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.figure_2 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=50)
        self.ax_2 = self.figure_2.add_subplot(111)
        self.canvas_2 = FigureCanvasTkAgg(self.figure_2, master=self.frame_sci_plot)
        self.canvas_2.draw()
        self.canvas_2.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        self.figure_3 = Figure(figsize=(Housekeeping.FIG_WIDTH, Housekeeping.FIG_HEIGHT), dpi=50)
        self.ax_3 = self.figure_3.add_subplot(111)
        self.canvas_3 = FigureCanvasTkAgg(self.figure_3, master=self.frame_sci_plot)
        self.canvas_3.draw()
        self.canvas_3.get_tk_widget().grid(row=2, column=0, sticky="nsew", padx=15, pady=15)

        # ============ frame_state_plot ============

        self.frame_state.rowconfigure((0, 1), weight=1)
        self.frame_state.columnconfigure((0, 1), weight=1)

        self.state_frame_label = ctk.CTkLabel(master=self.frame_state,
                                              text="Magnetometer State",
                                              height=50,
                                              fg_color=("white", "gray38"),
                                              corner_radius=8)
        self.state_frame_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=5)

        black_img = ImageTk.PhotoImage(Image.open("black_button.png").resize((100, 100)))

        led_image.append(ctk.CTkLabel(master=self.frame_state, image=black_img))
        led_image[0].grid(row=1, column=0, sticky="nsew")

        self.state_led = ctk.CTkLabel(master=self.frame_state, image=black_img)
        self.state_led.image = black_img
        self.state_led.grid(row=1, column=0, sticky="nsew")

        self.state_label = ctk.CTkLabel(master=self.frame_state,
                                        text="OFF",
                                        text_font=("Kanit", -20, "bold"),
                                        height=50)
        self.state_label.grid(row=1, column=1)

        # =========== Save all figures to be updated ===========

        sci_fig.extend([self.figure_1, self.figure_2, self.figure_3])
        sci_axes.extend([self.ax_1, self.ax_2, self.ax_3])

        for i in range(0, len(sci_axes)):
            sci_axes[i].patch.set_color("black")
            sci_axes[i].set_title(sci_plot_names[i])
            sci_fig[i].set_facecolor("dimgrey")
            if i == 0:
                sci_axes[i].set_xlabel("Time [s]")
                sci_axes[i].set_ylabel("Magnitude of B-field [nT]")
            if i == 1:
                sci_axes[i].set_xlabel("Frequency [Hz]")
                sci_axes[i].set_ylabel("Amplitude of Spectral Components")
            if i == 2:
                sci_axes[i].set_xlabel("Time [s]")
                sci_axes[i].set_ylabel("Frequency [Hz]")
            sci_fig[i].tight_layout()
            sci_axes_background.append(sci_fig[i].canvas.copy_from_bbox(sci_axes[i].bbox))

        artist_3.extend([sci_axes[0].plot([], [], color='blue')[0],
                        sci_axes[1].plot([], [], color='blue')[0]])


if __name__ == "__main__":
    # -----------------------------------------------CREATE APP--------------------------------------------------------#

    app = App()

    # ----------------------------------------------- THREADING -------------------------------------------------------#

    t1 = threading.Thread(target=communications.scheduler, args=(app,))
    t2 = threading.Thread(target=communications.uart_driver)

    t1.daemon = True
    t2.daemon = True

    t2.start()
    t1.start()

    app.mainloop()
