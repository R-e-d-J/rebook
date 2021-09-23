"""Frame module for ReBook application"""

from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import asyncio
import json
import os
import webbrowser
from PIL import Image, ImageTk

import tools
import app.constant as cst


class MainFrame(ttk.Frame):
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-statements

    """MainFrame for ReBook Application"""

    def __init__(self, app, k2pdfopt_path):
        super().__init__(app)
        self.root = app  # root of tkinter

        self.half_width_screen = int(self.root.width / 2) - 60

        self.k2pdfopt_path = k2pdfopt_path
        self.k2pdfopt_command_args = {}
        self.custom_preset_file_path = "rebook_preset.json"

        self.strvar_device = tk.StringVar()
        self.strvar_screen_unit = tk.StringVar()
        self.strvar_command_args = tk.StringVar()
        self.strvar_conversion_mode = tk.StringVar()
        self.strvar_input_file_path = tk.StringVar()
        self.strvar_output_file_path = tk.StringVar()
        self.strvar_device_screen_width = tk.StringVar()
        self.strvar_device_screen_height = tk.StringVar()
        self.strvar_current_preview_page_num = tk.StringVar()

        # Crop Maring
        self.is_cropmargin_checked = tk.BooleanVar()
        self.strvar_top_cropmargin = tk.StringVar()
        self.strvar_left_cropmargin = tk.StringVar()
        self.strvar_width_cropmargin = tk.StringVar()
        self.strvar_height_cropmargin = tk.StringVar()
        self.strvar_crop_page_range = tk.StringVar()

        # cropbox 1
        self.is_cropbox_checked_1 = tk.BooleanVar()
        self.strvar_left_cropbox_1 = tk.StringVar()
        self.strvar_top_cropbox_1 = tk.StringVar()
        self.strvar_width_cropbox_1 = tk.StringVar()
        self.strvar_height_cropbox_1 = tk.StringVar()
        self.strvar_page_range_cropbox_1 = tk.StringVar()

        # cropbox 2
        self.is_cropbox_checked_2 = tk.BooleanVar()
        self.strvar_left_cropbox_2 = tk.StringVar()
        self.strvar_top_cropbox_2 = tk.StringVar()
        self.strvar_width_cropbox_2 = tk.StringVar()
        self.strvar_height_cropbox_2 = tk.StringVar()
        self.strvar_page_range_cropbox_2 = tk.StringVar()

        # cropbox 3
        self.is_cropbox_checked_3 = tk.BooleanVar()
        self.strvar_left_cropbox_3 = tk.StringVar()
        self.strvar_top_cropbox_3 = tk.StringVar()
        self.strvar_width_cropbox_3 = tk.StringVar()
        self.strvar_height_cropbox_3 = tk.StringVar()
        self.strvar_page_range_cropbox_3 = tk.StringVar()

        # cropbox 4
        self.is_cropbox_checked_4 = tk.BooleanVar()
        self.strvar_left_cropbox_4 = tk.StringVar()
        self.strvar_top_cropbox_4 = tk.StringVar()
        self.strvar_width_cropbox_4 = tk.StringVar()
        self.strvar_height_cropbox_4 = tk.StringVar()
        self.strvar_page_range_cropbox_4 = tk.StringVar()

        # cropbox 5
        self.is_cropbox_checked_5 = tk.BooleanVar()
        self.strvar_left_cropbox_5 = tk.StringVar()
        self.strvar_top_cropbox_5 = tk.StringVar()
        self.strvar_width_cropbox_5 = tk.StringVar()
        self.strvar_height_cropbox_5 = tk.StringVar()
        self.strvar_page_range_cropbox_5 = tk.StringVar()

        self.is_dpi_checked = tk.BooleanVar()
        self.strvar_device_screen_dpi = tk.StringVar()

        self.is_landscape_checked = tk.BooleanVar()
        self.strvar_landscape_pages = tk.StringVar()  # 1,3,5-10

        self.is_column_num_checked = tk.BooleanVar()
        self.strvar_column_num = tk.StringVar()

        self.is_smart_linebreak_checked = tk.BooleanVar()  # -ws 0.01~10
        self.strvar_linebreak_space = tk.StringVar()

        self.is_fixed_font_size_checked = tk.BooleanVar()
        self.strvar_fixed_font_size = tk.StringVar()

        self.strvar_page_numbers = tk.StringVar()

        self.is_resolution_multipler_checked = tk.BooleanVar()
        self.strvar_resolution_multiplier = tk.StringVar()

        self.is_auto_crop_checked = tk.BooleanVar()
        self.strvar_auto_crop = tk.StringVar()

        self.is_break_page_checked = tk.BooleanVar()
        self.is_native_pdf_checked = tk.BooleanVar()
        self.is_coloroutput_checked = tk.BooleanVar()
        self.is_reflow_text_checked = tk.BooleanVar()
        self.is_fast_preview_checked = tk.BooleanVar()
        self.is_avoid_overlap_checked = tk.BooleanVar()
        self.is_right_to_left_checked = tk.BooleanVar()
        self.is_autostraighten_checked = tk.BooleanVar()
        self.is_markedup_source_checked = tk.BooleanVar()
        self.is_erase_vertical_line_checked = tk.BooleanVar()
        self.is_ignore_small_defects_checked = tk.BooleanVar()
        self.is_erase_horizontal_line_checked = tk.BooleanVar()
        self.is_ghostscript_postprocessing_checked = tk.BooleanVar()

        # Tesseract
        self.is_tesseract_checked = tk.BooleanVar()
        self.strvar_tesseract_cpu_percentage = tk.StringVar()
        self.is_tesseract_fast_checked = tk.BooleanVar()
        self.strvar_tesseract_detection = tk.StringVar()
        self.strvar_tesseract_language = tk.StringVar()

        # Advanced options
        self.is_minimum_column_gap_checked = tk.BooleanVar()
        self.strvar_min_column_gap_width = tk.StringVar()

        self.is_max_gap_between_column_checked = tk.BooleanVar()
        self.strvar_max_gap_between_column = tk.StringVar()

        self.is_column_gap_range_checked = tk.BooleanVar()
        self.strvar_column_gap_range = tk.StringVar()

        self.is_minimum_column_height_checked = tk.BooleanVar()
        self.strvar_minimum_column_height = tk.StringVar()

        self.is_column_offset_maximum_checked = tk.BooleanVar()
        self.strvar_column_offset_maximum = tk.StringVar()

        self.is_min_height_blank_between_regions_checked = tk.BooleanVar()
        self.strvar_min_height_blank_between_regions = tk.StringVar()

        self.is_threshold_detecting_gaps_between_column_checked = tk.BooleanVar()
        self.strvar_threshold_detecting_gaps_between_column = tk.StringVar()

        self.is_threshold_detecting_gaps_between_rows_checked = tk.BooleanVar()
        self.strvar_threshold_detecting_gaps_between_rows = tk.StringVar()

        self.is_threshold_detecting_gaps_between_words_checked = tk.BooleanVar()
        self.strvar_threshold_detecting_gaps_between_words = tk.StringVar()

        self.is_text_only_checked = tk.BooleanVar()

        self.default_var_map = {
            cst.DEVICE_ARG_NAME: ["Kindle Paperwhite 3"],
            cst.SCREEN_UNIT_PREFIX: ["Pixels"],
            cst.DEVICE_WIDTH_ARG_NAME: ["560"],
            cst.DEVICE_HEIGHT_ARG_NAME: ["735"],
            cst.CONVERSION_MODE_ARG_NAME: ["Default"],
            cst.OUTPUT_PATH_ARG_NAME: [""],
            cst.COLUMN_NUM_ARG_NAME: [False, "2"],
            cst.RESOLUTION_MULTIPLIER_ARG_NAME: [False, "1.0"],
            cst.CROPMARGIN_ARG_NAME: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
            ],
            cst.CROPBOX_1_ARG_NAME: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            cst.CROPBOX_2_ARG_NAME: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            cst.CROPBOX_3_ARG_NAME: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            cst.CROPBOX_4_ARG_NAME: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            cst.CROPBOX_5_ARG_NAME: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            cst.DPI_ARG_NAME: [False, "167"],
            cst.PAGE_NUM_ARG_NAME: [""],
            cst.FIXED_FONT_SIZE_ARG_NAME: [False, "12"],
            cst.LANDSCAPE_ARG_NAME: [False, ""],
            cst.LINEBREAK_ARG_NAME: [True, "0.200"],
            cst.AUTO_STRAIGNTEN_ARG_NAME: [False],
            cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME: [False, False],
            cst.COLOR_OUTPUT_ARG_NAME: [False],
            cst.NATIVE_PDF_ARG_NAME: [False],
            cst.RIGHT_TO_LEFT_ARG_NAME: [False],
            cst.POST_GS_ARG_NAME: [False],
            cst.MARKED_SOURCE_ARG_NAME: [True],
            cst.REFLOW_TEXT_ARG_NAME: [True],
            cst.ERASE_VERTICAL_LINE_ARG_NAME: [True],
            cst.ERASE_HORIZONTAL_LINE_ARG_NAME: [True],
            cst.FAST_PREVIEW_ARG_NAME: [True],
            cst.IGN_SMALL_DEFECTS_ARG_NAME: [False],
            cst.AUTO_CROP_ARG_NAME: [False, "0.1"],
            cst.OCR_ARG_NAME: [False, "50"],
            cst.OCR_CPU_ARG_NAME: [False, "50"],
            cst.TESSERACT_LANGUAGE_ARG_NAME: ["English"],
            cst.TESSERACT_FAST_ARG_NAME: [False],
            cst.TESSERACT_DETECTION_ARG_NAME: ["line"],
            cst.MIN_COLUMN_GAP_WIDTH_ARG_NAME: [False, "0.1"],
            cst.MAX_GAP_BETWEEN_COLUMN_ARG_NAME: [False, "1.5"],
            cst.COLUMN_GAP_RANGE_ARG_NAME: [False, "0.33"],
            cst.MINIMUM_COLUMN_HEIGHT_ARG_NAME: [False, "1.5"],
            cst.COLUMN_OFFSET_MAXIMUM_ARG_NAME: [False, "0.3"],
            cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_ARG_NAME: [False, "0.014"],
            cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_ARG_NAME: [False, "0.005"],
            cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_ARG_NAME: [False, "0.006"],
            cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_ARG_NAME: [False, "0.0015"],
            cst.TEXT_ONLY_OUTPUT_ARG_NAME: [False],
            cst.PREVIEW_OUTPUT_ARG_NAME: [],
        }

        self.arg_var_map = {
            cst.DEVICE_ARG_NAME: [self.strvar_device],
            cst.SCREEN_UNIT_PREFIX: [self.strvar_screen_unit],
            cst.DEVICE_WIDTH_ARG_NAME: [self.strvar_device_screen_width],
            cst.DEVICE_HEIGHT_ARG_NAME: [self.strvar_device_screen_height],
            cst.CONVERSION_MODE_ARG_NAME: [self.strvar_conversion_mode],
            cst.OUTPUT_PATH_ARG_NAME: [self.strvar_output_file_path],
            cst.COLUMN_NUM_ARG_NAME: [
                self.is_column_num_checked,
                self.strvar_column_num,
            ],
            cst.RESOLUTION_MULTIPLIER_ARG_NAME: [
                self.is_resolution_multipler_checked,
                self.strvar_resolution_multiplier,
            ],
            cst.CROPMARGIN_ARG_NAME: [
                self.is_cropmargin_checked,
                self.strvar_left_cropmargin,
                self.strvar_top_cropmargin,
                self.strvar_width_cropmargin,
                self.strvar_height_cropmargin,
            ],
            cst.CROPBOX_1_ARG_NAME: [
                self.is_cropbox_checked_1,
                self.strvar_left_cropbox_1,
                self.strvar_top_cropbox_1,
                self.strvar_width_cropbox_1,
                self.strvar_height_cropbox_1,
                self.strvar_page_range_cropbox_1,
            ],
            cst.CROPBOX_2_ARG_NAME: [
                self.is_cropbox_checked_2,
                self.strvar_left_cropbox_2,
                self.strvar_top_cropbox_2,
                self.strvar_width_cropbox_2,
                self.strvar_height_cropbox_2,
                self.strvar_page_range_cropbox_2,
            ],
            cst.CROPBOX_3_ARG_NAME: [
                self.is_cropbox_checked_3,
                self.strvar_left_cropbox_3,
                self.strvar_top_cropbox_3,
                self.strvar_width_cropbox_3,
                self.strvar_height_cropbox_3,
                self.strvar_page_range_cropbox_3,
            ],
            cst.CROPBOX_4_ARG_NAME: [
                self.is_cropbox_checked_4,
                self.strvar_left_cropbox_4,
                self.strvar_top_cropbox_4,
                self.strvar_width_cropbox_4,
                self.strvar_height_cropbox_4,
                self.strvar_page_range_cropbox_4,
            ],
            cst.CROPBOX_5_ARG_NAME: [
                self.is_cropbox_checked_5,
                self.strvar_left_cropbox_5,
                self.strvar_top_cropbox_5,
                self.strvar_width_cropbox_5,
                self.strvar_height_cropbox_5,
                self.strvar_page_range_cropbox_5,
            ],
            cst.DPI_ARG_NAME: [
                self.is_dpi_checked,
                self.strvar_device_screen_dpi,
            ],
            cst.PAGE_NUM_ARG_NAME: [self.strvar_page_numbers],
            cst.FIXED_FONT_SIZE_ARG_NAME: [
                self.is_fixed_font_size_checked,
                self.strvar_fixed_font_size,
            ],
            cst.OCR_ARG_NAME: [
                self.is_tesseract_checked,
                self.strvar_tesseract_cpu_percentage,
            ],
            cst.OCR_CPU_ARG_NAME: [
                self.is_tesseract_checked,
                self.strvar_tesseract_cpu_percentage,
            ],
            cst.TESSERACT_LANGUAGE_ARG_NAME: [self.strvar_tesseract_language],
            cst.TESSERACT_FAST_ARG_NAME: [self.is_tesseract_fast_checked],
            cst.TESSERACT_DETECTION_ARG_NAME: [self.strvar_tesseract_detection],
            cst.LANDSCAPE_ARG_NAME: [
                self.is_landscape_checked,
                self.strvar_landscape_pages,
            ],
            cst.LINEBREAK_ARG_NAME: [
                self.is_smart_linebreak_checked,
                self.strvar_linebreak_space,
            ],
            cst.AUTO_STRAIGNTEN_ARG_NAME: [self.is_autostraighten_checked],
            cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME: [
                self.is_break_page_checked,
                self.is_avoid_overlap_checked,
            ],
            cst.COLOR_OUTPUT_ARG_NAME: [self.is_coloroutput_checked],
            cst.NATIVE_PDF_ARG_NAME: [self.is_native_pdf_checked],
            cst.RIGHT_TO_LEFT_ARG_NAME: [self.is_right_to_left_checked],
            cst.POST_GS_ARG_NAME: [self.is_ghostscript_postprocessing_checked],
            cst.MARKED_SOURCE_ARG_NAME: [self.is_markedup_source_checked],
            cst.REFLOW_TEXT_ARG_NAME: [self.is_reflow_text_checked],
            cst.ERASE_VERTICAL_LINE_ARG_NAME: [self.is_erase_vertical_line_checked],
            cst.ERASE_HORIZONTAL_LINE_ARG_NAME: [self.is_erase_horizontal_line_checked],
            cst.FAST_PREVIEW_ARG_NAME: [self.is_fast_preview_checked],
            cst.IGN_SMALL_DEFECTS_ARG_NAME: [self.is_ignore_small_defects_checked],
            cst.AUTO_CROP_ARG_NAME: [
                self.is_auto_crop_checked,
                self.strvar_auto_crop,
            ],
            cst.MIN_COLUMN_GAP_WIDTH_ARG_NAME: [
                self.is_minimum_column_gap_checked,
                self.strvar_min_column_gap_width,
            ],
            cst.MAX_GAP_BETWEEN_COLUMN_ARG_NAME: [
                self.is_max_gap_between_column_checked,
                self.strvar_max_gap_between_column,
            ],
            cst.COLUMN_GAP_RANGE_ARG_NAME: [
                self.is_column_gap_range_checked,
                self.strvar_column_gap_range,
            ],
            cst.MINIMUM_COLUMN_HEIGHT_ARG_NAME: [
                self.is_minimum_column_height_checked,
                self.strvar_minimum_column_height,
            ],
            cst.COLUMN_OFFSET_MAXIMUM_ARG_NAME: [
                self.is_column_offset_maximum_checked,
                self.strvar_column_offset_maximum,
            ],
            cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_ARG_NAME: [
                self.is_min_height_blank_between_regions_checked,
                self.strvar_min_height_blank_between_regions,
            ],
            cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_ARG_NAME: [
                self.is_threshold_detecting_gaps_between_column_checked,
                self.strvar_threshold_detecting_gaps_between_column,
            ],
            cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_ARG_NAME: [
                self.is_threshold_detecting_gaps_between_rows_checked,
                self.strvar_threshold_detecting_gaps_between_rows,
            ],
            cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_ARG_NAME: [
                self.is_threshold_detecting_gaps_between_words_checked,
                self.strvar_threshold_detecting_gaps_between_words,
            ],
            cst.TEXT_ONLY_OUTPUT_ARG_NAME: [self.is_text_only_checked],
            cst.PREVIEW_OUTPUT_ARG_NAME: [],
        }

        self.current_preview_page_index = 0
        self.background_process = None
        self.background_future = None

        labelframe_style = ttk.Style()
        labelframe_style.configure("TLabelframe.Label", font=("arial", 14, "bold"))

        self.create_menus()
        self.create_tabs()

        # Prepare to run
        self.thread_loop = asyncio.get_event_loop()
        run_loop_thread = Thread(
            target=self.start_loop, args=(self.thread_loop,), daemon=True
        )
        run_loop_thread.start()

        if not self.load_custom_preset():
            self.restore_default_values()

        self.log_string("Current directory : " + os.getcwd())

    def create_tabs(self):
        """Create 'Conversion' and 'Logs' ReBook's tabs"""
        self.notebook = ttk.Notebook(self.root)

        self.conversion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.conversion_tab, text="Conversion")

        self.advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_tab, text="Advanced")

        self.logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text="Logs")

        self.notebook.pack(expand=1, fill="both")

        self.tab_left_part = 0
        self.tab_right_part = 1

        self.__fill_conversion_tab()
        self.conversion_tab.columnconfigure(
            self.tab_right_part,
            weight=1,
        )
        self.conversion_tab.rowconfigure(
            self.conversion_tab_left_part_line_num,
            weight=1,
        )

        self.__fill_advanced_tab()
        self.__fill_logs_tab()

    def create_menus(self):
        """Create the menus for ReBook"""
        menu_bar = tk.Menu(self.root)
        self.root["menu"] = menu_bar

        # File menu
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label="File")
        menu_file.add_command(label="About", command=self.__menu_about_box)
        menu_file.add_command(label="Quit", command=self.root.quit)

        # Settings menu
        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_settings, label="Settings")
        menu_settings.add_command(
            label="Save current settings", command=self.__menu_save_preset
        )
        menu_settings.add_command(
            label="Load settings", command=self.__menu_open_preset_file
        )
        menu_settings.add_command(
            label="Reset settings to default", command=self.restore_default_values
        )

        # Help menu
        menu_help = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_help, label="Help")
        menu_help.add_command(
            label="K2pdfopt website helppage", command=self.__menu_open_helpwebpage
        )
        menu_help.add_command(
            label="K2pdfopt command line manual", command=self.__menu_open_cli_manual
        )

    def __menu_open_helpwebpage(self):
        """Menu `Webpage help`"""
        webbrowser.open("https://willus.com/k2pdfopt/help/")

    def __menu_open_cli_manual(self):
        """Menu `CLI help`"""
        webbrowser.open("https://www.willus.com/k2pdfopt/help/options.shtml")

    def __fill_left_side_of_conversion_tab(self):
        """Fill the left side of Conversion tab"""
        self.conversion_tab_left_part_line_num = -1
        self.__setup_file_frame()
        self.__setup_device_frame()
        self.__setup_margin_and_cropboxes_frame()
        self.__setup_parameters_frame()
        self.__setup_tesseract_frame()

    def __fill_right_side_of_conversion_tab(self):
        """Fill the right side of Conversion tab"""
        conversion_tab_right_part_line_num = -1
        conversion_tab_right_part_line_num = self.__draw_command_line_frame_on_tab(self.conversion_tab, self.tab_right_part, conversion_tab_right_part_line_num)
        self.__draw_action_frame_on_tab(self.conversion_tab, self.tab_right_part, conversion_tab_right_part_line_num)

    def __fill_conversion_tab(self):
        """Fill the Conversion tab"""
        self.__fill_left_side_of_conversion_tab()
        self.__fill_right_side_of_conversion_tab()

    def __fill_advanced_tab(self):
        """Fill the advanced tab"""
        self.__fill_left_side_of_advanced_tab()
        self.__fill_right_side_of_advanced_tab()

    def __fill_left_side_of_advanced_tab(self):
        """Fill the left part of advanced tab"""
        self.advanced_tab_left_part_line_num = -1
        self.__draw_advanced_option_frame()
        # self.__draw_more_cropboxes_frame()

    def __draw_advanced_option_frame(self):
        """Fill the advanced option tab"""
        self.advanced_tab_left_part_line_num += 1

        advanced_option_frame = ttk.Labelframe(
            self.advanced_tab,
            text="Advanced options",
            width=self.half_width_screen,
            height=300,
        )
        advanced_option_frame.grid(
            column=self.tab_left_part,
            row=self.advanced_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        advanced_option_frame.grid_propagate(False)
        self.__insert_advanced_option_field_into_frame(advanced_option_frame)

    def __insert_advanced_option_field_into_frame(self, frame):
        """Insert advanced option fields into a frame"""
        advanced_option_line_number = 0
        min_column_gap_width_label = ttk.Checkbutton(
            frame,
            text="Minimum column gap width",
            variable=self.is_minimum_column_gap_checked,
            command=self.gui_minimum_column_gap,
        )
        min_column_gap_width_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        min_column_gap_width = ttk.Spinbox(
            frame,
            from_=cst.MIN_COLUMN_GAP_WIDTH_MIN_VALUE,
            to=cst.MIN_COLUMN_GAP_WIDTH_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_min_column_gap_width,
            command=self.gui_minimum_column_gap,
            width=6,
        )
        min_column_gap_width.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        max_gap_between_column_label = ttk.Checkbutton(
            frame,
            text="Max allowed gap between columns",
            variable=self.is_max_gap_between_column_checked,
            command=self.gui_max_gap_between_column,
        )
        max_gap_between_column_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        max_gap_between_column = ttk.Spinbox(
            frame,
            from_=cst.MAX_GAP_BETWEEN_COLUMN_MIN_VALUE,
            to=cst.MAX_GAP_BETWEEN_COLUMN_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_max_gap_between_column,
            command=self.gui_max_gap_between_column,
            width=6,
        )
        max_gap_between_column.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        column_gap_range_label = ttk.Checkbutton(
            frame,
            text="Column-gap range",
            variable=self.is_column_gap_range_checked,
            command=self.gui_column_gap_range,
        )
        column_gap_range_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        column_gap_range = ttk.Spinbox(
            frame,
            from_=cst.COLUMN_GAP_RANGE_MIN_VALUE,
            to=cst.COLUMN_GAP_RANGE_MAX_VALUE,
            increment=0.01,
            textvariable=self.strvar_column_gap_range,
            command=self.gui_column_gap_range,
            width=6,
        )
        column_gap_range.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        minimum_column_height_label = ttk.Checkbutton(
            frame,
            text="Minimum column height",
            variable=self.is_minimum_column_height_checked,
            command=self.gui_minimum_column_height,
        )
        minimum_column_height_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        minimum_column_height = ttk.Spinbox(
            frame,
            from_=cst.MINIMUM_COLUMN_HEIGHT_MIN_VALUE,
            to=cst.MINIMUM_COLUMN_HEIGHT_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_minimum_column_height,
            command=self.gui_minimum_column_height,
            width=6,
        )
        minimum_column_height.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        column_offset_maximum_label = ttk.Checkbutton(
            frame,
            text="Column Offset Maximum",
            variable=self.is_column_offset_maximum_checked,
            command=self.gui_column_offset_maximum,
        )
        column_offset_maximum_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        column_offset_maximum = ttk.Spinbox(
            frame,
            from_=cst.COLUMN_OFFSET_MAXIMUM_MIN_VALUE,
            to=cst.COLUMN_OFFSET_MAXIMUM_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_column_offset_maximum,
            command=self.gui_column_offset_maximum,
            width=6,
        )
        column_offset_maximum.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        min_height_blank_between_regions_label = ttk.Checkbutton(
            frame,
            text="Min height of the blank area that separates regions",
            variable=self.is_min_height_blank_between_regions_checked,
            command=self.gui_min_height_blank_between_regions,
        )
        min_height_blank_between_regions_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        min_height_blank_between_regions = ttk.Spinbox(
            frame,
            from_=cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_MIN_VALUE,
            to=cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_MAX_VALUE,
            increment=0.001,
            textvariable=self.strvar_min_height_blank_between_regions,
            command=self.gui_min_height_blank_between_regions,
            width=6,
        )
        min_height_blank_between_regions.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        threshold_detecting_gaps_between_column_label = ttk.Checkbutton(
            frame,
            text="Threshold value for detecting column gaps",
            variable=self.is_threshold_detecting_gaps_between_column_checked,
            command=self.gui_threshold_detecting_gaps_between_column,
        )
        threshold_detecting_gaps_between_column_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        threshold_detecting_gaps_between_column = ttk.Spinbox(
            frame,
            from_=cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_MIN_VALUE,
            to=cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_MAX_VALUE,
            increment=0.001,
            textvariable=self.strvar_threshold_detecting_gaps_between_column,
            command=self.gui_threshold_detecting_gaps_between_column,
            width=6,
        )
        threshold_detecting_gaps_between_column.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        threshold_detecting_gaps_between_rows_label = ttk.Checkbutton(
            frame,
            text="Threshold value for detecting rows gaps",
            variable=self.is_threshold_detecting_gaps_between_rows_checked,
            command=self.gui_threshold_detecting_gaps_between_rows,
        )
        threshold_detecting_gaps_between_rows_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        threshold_detecting_gaps_between_rows = ttk.Spinbox(
            frame,
            from_=cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_MIN_VALUE,
            to=cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_MAX_VALUE,
            increment=0.001,
            textvariable=self.strvar_threshold_detecting_gaps_between_rows,
            command=self.gui_threshold_detecting_gaps_between_rows,
            width=6,
        )
        threshold_detecting_gaps_between_rows.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        threshold_detecting_gaps_between_words_label = ttk.Checkbutton(
            frame,
            text="Threshold value for detecting words gaps",
            variable=self.is_threshold_detecting_gaps_between_words_checked,
            command=self.gui_threshold_detecting_gaps_between_words,
        )
        threshold_detecting_gaps_between_words_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        threshold_detecting_gaps_between_words = ttk.Spinbox(
            frame,
            from_=cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_MIN_VALUE,
            to=cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_MAX_VALUE,
            increment=0.001,
            textvariable=self.strvar_threshold_detecting_gaps_between_words,
            command=self.gui_threshold_detecting_gaps_between_words,
            width=6,
        )
        threshold_detecting_gaps_between_words.grid(
            column=1,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        advanced_option_line_number += 1
        text_only_label = ttk.Checkbutton(
            frame,
            text="Text only",
            variable=self.is_text_only_checked,
            command=self.gui_text_only,
        )
        text_only_label.grid(
            column=0,
            row=advanced_option_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    # def __draw_more_cropboxes_frame(self):
    #     self.advanced_tab_left_part_line_num += 1

    #     self.more_cropboxes_frame = ttk.Labelframe(
    #         self.advanced_tab,
    #         text="More cropboxes",
    #         width=self.half_width_screen,
    #         height=300,
    #     )
    #     self.more_cropboxes_frame.grid(
    #         column=0,
    #         row=self.advanced_tab_left_part_line_num,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.more_cropboxes_frame.grid_propagate(False)

    #     more_cropboxes_line_number = 0

    #     self.cropbox_label = ttk.Label(
    #         self.more_cropboxes_frame,
    #         text="Crop Areas (in)",
    #     )
    #     self.cropbox_label.grid(
    #         column=0,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     cropaera_left_label = ttk.Label(
    #         self.more_cropboxes_frame,
    #         text="Left",
    #     )
    #     cropaera_left_label.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     cropaera_top_label = ttk.Label(
    #         self.more_cropboxes_frame,
    #         text="Top",
    #     )
    #     cropaera_top_label.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     cropaera_width_label = ttk.Label(
    #         self.more_cropboxes_frame,
    #         text="Width",
    #     )
    #     cropaera_width_label.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     cropaera_height_label = ttk.Label(
    #         self.more_cropboxes_frame,
    #         text="Height",
    #     )
    #     cropaera_height_label.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     cropaera_page_range_label = ttk.Label(
    #         self.more_cropboxes_frame,
    #         text="Page range",
    #         anchor=tk.CENTER,
    #     )
    #     cropaera_page_range_label.grid(
    #         column=6,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )

    #     more_cropboxes_line_number += 1
    #     self.cropbox_check_button_1 = ttk.Checkbutton(
    #         self.more_cropboxes_frame,
    #         variable=self.is_cropbox_checked_1,
    #         command=self.gui_cropbox1_margin,
    #     )
    #     self.cropbox_check_button_1.grid(
    #         column=1,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.left_cropbox1_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_left_cropbox_1,
    #         command=self.gui_cropbox1_margin,
    #         width=4,
    #     )
    #     self.left_cropbox1_spinbox.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.top_cropbox1_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_top_cropbox_1,
    #         command=self.gui_cropbox1_margin,
    #         width=4,
    #     )
    #     self.top_cropbox1_spinbox.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.width_cropbox1_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_width_cropbox_1,
    #         command=self.gui_cropbox1_margin,
    #         width=4,
    #     )
    #     self.width_cropbox1_spinbox.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.height_cropbox1_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_height_cropbox_1,
    #         command=self.gui_cropbox1_margin,
    #         width=4,
    #     )
    #     self.height_cropbox1_spinbox.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.cropbox1_page_range_entry = ttk.Entry(
    #         self.more_cropboxes_frame,
    #         textvariable=self.strvar_page_range_cropbox_1,
    #         validate="focusout",
    #         validatecommand=self.gui_cropbox1_margin,
    #         width=13,
    #     )
    #     self.cropbox1_page_range_entry.grid(
    #         column=6,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )

    #     more_cropboxes_line_number += 1
    #     self.cropbox_check_button_2 = ttk.Checkbutton(
    #         self.more_cropboxes_frame,
    #         variable=self.is_cropbox_checked_2,
    #         command=self.gui_cropbox2_margin,
    #     )
    #     self.cropbox_check_button_2.grid(
    #         column=1,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.left_cropbox2_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_left_cropbox_2,
    #         command=self.gui_cropbox2_margin,
    #         width=4,
    #     )
    #     self.left_cropbox2_spinbox.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.top_cropbox2_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_top_cropbox_2,
    #         command=self.gui_cropbox2_margin,
    #         width=4,
    #     )
    #     self.top_cropbox2_spinbox.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.width_cropbox2_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_width_cropbox_2,
    #         command=self.gui_cropbox2_margin,
    #         width=4,
    #     )
    #     self.width_cropbox2_spinbox.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.height_cropbox2_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_height_cropbox_2,
    #         command=self.gui_cropbox2_margin,
    #         width=4,
    #     )
    #     self.height_cropbox2_spinbox.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.cropbox2_page_range_entry = ttk.Entry(
    #         self.more_cropboxes_frame,
    #         textvariable=self.strvar_page_range_cropbox_2,
    #         validate="focusout",
    #         validatecommand=self.gui_cropbox2_margin,
    #         width=13,
    #     )
    #     self.cropbox2_page_range_entry.grid(
    #         column=6,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )

    #     more_cropboxes_line_number += 1
    #     self.cropbox_check_button_3 = ttk.Checkbutton(
    #         self.more_cropboxes_frame,
    #         variable=self.is_cropbox_checked_3,
    #         command=self.gui_cropbox3_margin,
    #     )
    #     self.cropbox_check_button_3.grid(
    #         column=1,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.left_cropbox3_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_left_cropbox_3,
    #         command=self.gui_cropbox3_margin,
    #         width=4,
    #     )
    #     self.left_cropbox3_spinbox.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.top_cropbox3_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_top_cropbox_3,
    #         command=self.gui_cropbox3_margin,
    #         width=4,
    #     )
    #     self.top_cropbox3_spinbox.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.width_cropbox3_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_width_cropbox_3,
    #         command=self.gui_cropbox3_margin,
    #         width=4,
    #     )
    #     self.width_cropbox3_spinbox.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.height_cropbox3_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_height_cropbox_3,
    #         command=self.gui_cropbox3_margin,
    #         width=4,
    #     )
    #     self.height_cropbox3_spinbox.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.cropbox3_page_range_entry = ttk.Entry(
    #         self.more_cropboxes_frame,
    #         textvariable=self.strvar_page_range_cropbox_3,
    #         validate="focusout",
    #         validatecommand=self.gui_cropbox3_margin,
    #         width=13,
    #     )
    #     self.cropbox3_page_range_entry.grid(
    #         column=6,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )

    #     more_cropboxes_line_number += 1
    #     self.cropbox_check_button_4 = ttk.Checkbutton(
    #         self.more_cropboxes_frame,
    #         variable=self.is_cropbox_checked_4,
    #         command=self.gui_cropbox4_margin,
    #     )
    #     self.cropbox_check_button_4.grid(
    #         column=1,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.left_cropbox4_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_left_cropbox_4,
    #         command=self.gui_cropbox4_margin,
    #         width=4,
    #     )
    #     self.left_cropbox4_spinbox.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.top_cropbox4_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_top_cropbox_4,
    #         command=self.gui_cropbox4_margin,
    #         width=4,
    #     )
    #     self.top_cropbox4_spinbox.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.width_cropbox4_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_width_cropbox_4,
    #         command=self.gui_cropbox4_margin,
    #         width=4,
    #     )
    #     self.width_cropbox4_spinbox.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.height_cropbox4_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_height_cropbox_4,
    #         command=self.gui_cropbox4_margin,
    #         width=4,
    #     )
    #     self.height_cropbox4_spinbox.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.cropbox4_page_range_entry = ttk.Entry(
    #         self.more_cropboxes_frame,
    #         textvariable=self.strvar_page_range_cropbox_4,
    #         validate="focusout",
    #         validatecommand=self.gui_cropbox4_margin,
    #         width=13,
    #     )
    #     self.cropbox4_page_range_entry.grid(
    #         column=6,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )

    #     more_cropboxes_line_number += 1
    #     self.cropbox_check_button_5 = ttk.Checkbutton(
    #         self.more_cropboxes_frame,
    #         variable=self.is_cropbox_checked_5,
    #         command=self.gui_cropbox5_margin,
    #     )
    #     self.cropbox_check_button_5.grid(
    #         column=1,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.left_cropbox5_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_left_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.left_cropbox5_spinbox.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.top_cropbox5_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_top_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.top_cropbox5_spinbox.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.width_cropbox5_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_width_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.width_cropbox5_spinbox.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.height_cropbox5_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_height_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.height_cropbox5_spinbox.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.cropbox5_page_range_entry = ttk.Entry(
    #         self.more_cropboxes_frame,
    #         textvariable=self.strvar_page_range_cropbox_5,
    #         validate="focusout",
    #         validatecommand=self.gui_cropbox5_margin,
    #         width=13,
    #     )
    #     self.cropbox5_page_range_entry.grid(
    #         column=6,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )

    #     more_cropboxes_line_number += 1
    #     cropbox_u_label = ttk.Label(self.more_cropboxes_frame, text="cboxu")
    #     cropbox_u_label.grid(
    #         column=0,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.cropboxe_u_check_button = ttk.Checkbutton(
    #         self.more_cropboxes_frame,
    #         variable=self.is_cropbox_checked_5,
    #         command=self.gui_cropbox5_margin,
    #     )
    #     self.cropboxe_u_check_button.grid(
    #         column=1,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.left_cropbox_u_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_left_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.left_cropbox_u_spinbox.grid(
    #         column=2,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.top_cropbox_u_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_top_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.top_cropbox_u_spinbox.grid(
    #         column=3,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.width_cropbox_u_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_width_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.width_cropbox_u_spinbox.grid(
    #         column=4,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     self.height_cropbox_u_spinbox = ttk.Spinbox(
    #         self.more_cropboxes_frame,
    #         from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
    #         to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
    #         increment=0.1,
    #         textvariable=self.strvar_height_cropbox_5,
    #         command=self.gui_cropbox5_margin,
    #         width=4,
    #     )
    #     self.height_cropbox_u_spinbox.grid(
    #         column=5,
    #         row=more_cropboxes_line_number,
    #         sticky=tk.N + tk.W,
    #         pady=cst.DEFAULT_PADY,
    #         padx=cst.DEFAULT_PADX,
    #     )
    #     # self.cropbox5_page_range_entry = ttk.Entry(
    #     #     self.more_cropboxes_frame,
    #     #     textvariable=self.strvar_page_range_cropbox_5,
    #     #     validate="focusout",
    #     #     validatecommand=self.gui_cropbox5_margin,
    #     #     width=13,
    #     # )
    #     # self.cropbox5_page_range_entry.grid(
    #     #     column=6,
    #     #     row=more_cropboxes_line_number,
    #     #     sticky=tk.N + tk.W,
    #     #     pady=cst.DEFAULT_PADY,
    #     #     padx=cst.DEFAULT_PADX,
    #     # )

    def __fill_right_side_of_advanced_tab(self):
        """Fill the right part of advanced tab"""
        self.advanced_tab_right_part_line_num = -1
        self.advanced_tab_right_part_line_num = self.__draw_command_line_frame_on_tab(self.advanced_tab, 1, self.advanced_tab_right_part_line_num)


    def __setup_file_frame(self):
        """Set up the file frame"""
        self.conversion_tab_left_part_line_num += 1

        file_frame = ttk.Labelframe(
            self.conversion_tab, text="Files", width=self.half_width_screen, height=78
        )
        file_frame.grid(
            column=self.tab_left_part,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        file_frame.grid_propagate(False)
        self.__insert_input_output_file_fields_into_frame(file_frame)

    def __insert_input_output_file_fields_into_frame(self, frame):
        """Insert the input and output file field into a"""
        file_frame_line_number = 0
        open_button = ttk.Button(
            frame, text="Input file", command=self.action_open_pdf_file
        )
        open_button.grid(
            column=0,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        self.input_path_entry = ttk.Entry(
            frame, textvariable=self.strvar_input_file_path, width=35
        )
        self.input_path_entry.grid(
            column=1,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        file_frame_line_number += 1
        output_folder_label = ttk.Button(
            frame,
            text="Output folder",
            command=self.action_choose_output_folder,
        )
        output_folder_label.grid(
            column=0,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        output_path_entry = ttk.Entry(
            frame, textvariable=self.strvar_output_file_path, width=40
        )
        output_path_entry.grid(
            column=1,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __setup_device_frame(self):
        """Set up the device frame"""
        self.conversion_tab_left_part_line_num += 1

        device_frame = ttk.Labelframe(
            self.conversion_tab, text="Device", width=self.half_width_screen, height=80
        )
        device_frame.grid(
            column=self.tab_left_part,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        device_frame.grid_propagate(False)
        self.__insert_device_fields_into_frame(device_frame)

    def __insert_device_fields_into_frame(self, frame):
        """Insert the device fields into a frame"""
        device_frame_line_number = 0
        device_label = ttk.Label(frame, text="Device")
        device_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        self.device_combobox = ttk.Combobox(
            frame, textvariable=self.strvar_device, width=25
        )
        self.device_combobox["values"] = list(cst.DEVICE_CHOICE_MAP.values())
        self.device_combobox.current(0)
        self.device_combobox.bind("<<ComboboxSelected>>", self.gui_device_unit_cbox)
        self.device_combobox.grid(
            column=1,
            columnspan=3,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        unit_label = ttk.Label(frame, text="Unit")
        unit_label.grid(
            column=4,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        self.unit_combobox = ttk.Combobox(
            frame, textvariable=self.strvar_screen_unit, width=20
        )
        self.unit_combobox["values"] = list(cst.UNIT_CHOICE_MAP.values())
        self.unit_combobox.current(0)
        self.unit_combobox.bind("<<ComboboxSelected>>", self.gui_device_unit_cbox)
        self.unit_combobox.grid(
            column=5,
            columnspan=3,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        device_frame_line_number += 1
        device_width_label = ttk.Label(frame, text="Width")
        device_width_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        device_width_spinbox = ttk.Spinbox(
            frame,
            from_=cst.DEVICE_WIDTH_MIN_VALUE,
            to=cst.DEVICE_WIDTH_MAX_VALUE,
            increment=1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        device_width_spinbox.grid(
            column=1,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        device_height_label = ttk.Label(frame, text="Height")
        device_height_label.grid(
            column=2,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        device_height_spinbox = ttk.Spinbox(
            frame,
            from_=cst.DEVICE_HEIGHT_MIN_VALUE,
            to=cst.DEVICE_HEIGHT_MAX_VALUE,
            increment=1,
            textvariable=self.strvar_device_screen_height,
            command=self.gui_width_height,
            width=6,
        )
        device_height_spinbox.grid(
            column=3,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        dpi_check_button = ttk.Checkbutton(
            frame,
            text="DPI",
            variable=self.is_dpi_checked,
            command=self.gui_dpi,
        )
        dpi_check_button.grid(
            column=4,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        device_dpi_spinbox = ttk.Spinbox(
            frame,
            from_=cst.DEVICE_DPI_MIN_VALUE,
            to=cst.DEVICE_DPI_MAX_VALUE,
            increment=1,
            textvariable=self.strvar_device_screen_dpi,
            command=self.gui_dpi,
            width=6,
        )
        device_dpi_spinbox.grid(
            column=5,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __setup_margin_and_cropboxes_frame(self):
        """Set up the cropbax and margin frame"""
        self.conversion_tab_left_part_line_num += 1

        margin_and_cropboxes_frame = ttk.Labelframe(
            self.conversion_tab,
            text="Margin & cropboxes",
            width=self.half_width_screen,
            height=223,
        )
        margin_and_cropboxes_frame.grid(
            column=self.tab_left_part,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        margin_and_cropboxes_frame.grid_propagate(False)
        self.__insert_margin_and_cropboxes_field_into_frame(margin_and_cropboxes_frame)

    def __insert_margin_and_cropboxes_field_into_frame(self, frame):
        """Insert margin and cropboxes field into a frame."""
        margin_and_cropboxes_frame_line_number = 0
        cropmargin_label = ttk.Label(
            frame,
            text="Crop Margins (in)",
        )
        cropmargin_label.grid(
            column=0,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropmargin_check_button = ttk.Checkbutton(
            frame,
            variable=self.is_cropmargin_checked,
            command=self.gui_crop_margin,
        )
        cropmargin_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        left_cropmargin_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_left_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        left_cropmargin_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        top_cropmargin_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_top_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        top_cropmargin_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        width_cropmargin_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_width_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        width_cropmargin_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        height_cropmargin_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_height_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        height_cropmargin_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropmargin_label = ttk.Label(
            frame,
            text="(left, top, right, bottom)",
        )
        cropmargin_label.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        margin_and_cropboxes_frame_line_number += 1
        whitespace_label = ttk.Label(frame, text="")
        whitespace_label.grid(column=1, row=margin_and_cropboxes_frame_line_number)

        margin_and_cropboxes_frame_line_number += 1
        cropbox_label = ttk.Label(
            frame,
            text="Crop Areas (in)",
        )
        cropbox_label.grid(
            column=0,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropaera_left_label = ttk.Label(
            frame,
            text="Left",
        )
        cropaera_left_label.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropaera_top_label = ttk.Label(
            frame,
            text="Top",
        )
        cropaera_top_label.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropaera_width_label = ttk.Label(
            frame,
            text="Width",
        )
        cropaera_width_label.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropaera_height_label = ttk.Label(
            frame,
            text="Height",
        )
        cropaera_height_label.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropaera_page_range_label = ttk.Label(
            frame,
            text="Page range",
            anchor=tk.CENTER,
        )
        cropaera_page_range_label.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        margin_and_cropboxes_frame_line_number += 1
        cropbox_check_button_1 = ttk.Checkbutton(
            frame,
            variable=self.is_cropbox_checked_1,
            command=lambda : self.ui_cropbox_margin(1),
        )
        cropbox_check_button_1.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        left_cropbox1_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_1,
            command=lambda : self.ui_cropbox_margin(1),
            width=4,
        )
        left_cropbox1_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        top_cropbox1_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_1,
            command=lambda : self.ui_cropbox_margin(1),
            width=4,
        )
        top_cropbox1_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        width_cropbox1_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_1,
            command=lambda : self.ui_cropbox_margin(1),
            width=4,
        )
        width_cropbox1_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        height_cropbox1_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_1,
            command=lambda : self.ui_cropbox_margin(1),
            width=4,
        )
        height_cropbox1_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropbox1_page_range_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_page_range_cropbox_1,
            validate="focusout",
            validatecommand=lambda : self.ui_cropbox_margin(1),
            width=13,
        )
        cropbox1_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        margin_and_cropboxes_frame_line_number += 1
        cropbox_check_button_2 = ttk.Checkbutton(
            frame,
            variable=self.is_cropbox_checked_2,
            command=lambda : self.ui_cropbox_margin(2),
        )
        cropbox_check_button_2.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        left_cropbox2_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_2,
            command=lambda : self.ui_cropbox_margin(2),
            width=4,
        )
        left_cropbox2_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        top_cropbox2_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_2,
            command=lambda : self.ui_cropbox_margin(2),
            width=4,
        )
        top_cropbox2_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        width_cropbox2_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_2,
            command=lambda : self.ui_cropbox_margin(2),
            width=4,
        )
        width_cropbox2_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        height_cropbox2_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_2,
            command=lambda : self.ui_cropbox_margin(2),
            width=4,
        )
        height_cropbox2_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropbox2_page_range_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_page_range_cropbox_2,
            validate="focusout",
            validatecommand=lambda : self.ui_cropbox_margin(2),
            width=13,
        )
        cropbox2_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        margin_and_cropboxes_frame_line_number += 1
        cropbox_check_button_3 = ttk.Checkbutton(
            frame,
            variable=self.is_cropbox_checked_3,
            command=lambda : self.ui_cropbox_margin(3),
        )
        cropbox_check_button_3.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        left_cropbox3_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_3,
            command=lambda : self.ui_cropbox_margin(3),
            width=4,
        )
        left_cropbox3_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        top_cropbox3_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_3,
            command=lambda : self.ui_cropbox_margin(3),
            width=4,
        )
        top_cropbox3_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        width_cropbox3_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_3,
            command=lambda : self.ui_cropbox_margin(3),
            width=4,
        )
        width_cropbox3_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        height_cropbox3_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_3,
            command=lambda : self.ui_cropbox_margin(3),
            width=4,
        )
        height_cropbox3_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropbox3_page_range_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_page_range_cropbox_3,
            validate="focusout",
            validatecommand=lambda : self.ui_cropbox_margin(3),
            width=13,
        )
        cropbox3_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        margin_and_cropboxes_frame_line_number += 1
        cropbox_check_button_4 = ttk.Checkbutton(
            frame,
            variable=self.is_cropbox_checked_4,
            command=lambda : self.ui_cropbox_margin(4),
        )
        cropbox_check_button_4.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        left_cropbox4_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_4,
            command=lambda : self.ui_cropbox_margin(4),
            width=4,
        )
        left_cropbox4_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        top_cropbox4_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_4,
            command=lambda : self.ui_cropbox_margin(4),
            width=4,
        )
        top_cropbox4_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        width_cropbox4_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_4,
            command=lambda : self.ui_cropbox_margin(4),
            width=4,
        )
        width_cropbox4_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        height_cropbox4_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_4,
            command=lambda : self.ui_cropbox_margin(4),
            width=4,
        )
        height_cropbox4_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropbox4_page_range_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_page_range_cropbox_4,
            validate="focusout",
            validatecommand=lambda : self.ui_cropbox_margin(4),
            width=13,
        )
        cropbox4_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        margin_and_cropboxes_frame_line_number += 1
        cropbox_check_button_5 = ttk.Checkbutton(
            frame,
            variable=self.is_cropbox_checked_5,
            command=lambda : self.ui_cropbox_margin(5),
        )
        cropbox_check_button_5.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        left_cropbox5_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_5,
            command=lambda : self.ui_cropbox_margin(5),
            width=4,
        )
        left_cropbox5_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        top_cropbox5_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_5,
            command=lambda : self.ui_cropbox_margin(5),
            width=4,
        )
        top_cropbox5_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        width_cropbox5_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_5,
            command=lambda : self.ui_cropbox_margin(5),
            width=4,
        )
        width_cropbox5_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        height_cropbox5_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MARGIN_AND_CROP_AREAS_MIN_VALUE,
            to=cst.MARGIN_AND_CROP_AREAS_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_5,
            command=lambda : self.ui_cropbox_margin(5),
            width=4,
        )
        height_cropbox5_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        cropbox5_page_range_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_page_range_cropbox_5,
            validate="focusout",
            validatecommand=lambda : self.ui_cropbox_margin(5),
            width=13,
        )
        cropbox5_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __setup_parameters_frame(self):
        """Draw the parameters frame and its widgets"""
        self.conversion_tab_left_part_line_num += 1

        parameters_frame = ttk.Labelframe(
            self.conversion_tab,
            text="Parameters & options",
            width=self.half_width_screen,
            height=290,
        )
        parameters_frame.grid(
            column=self.tab_left_part,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        parameters_frame.grid_propagate(False)
        self.__insert_paramaters_field_into_frame(parameters_frame)

    def __insert_paramaters_field_into_frame(self, frame):
        """Insert parameters fields into a frame"""
        parameters_frame_line_number = 0

        conversion_mode_label = ttk.Label(frame, text="Conversion Mode")
        conversion_mode_label.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        self.mode_combobox = ttk.Combobox(
            frame, textvariable=self.strvar_conversion_mode, width=10
        )
        self.mode_combobox["values"] = list(cst.MODE_CHOICE_MAP.values())
        self.mode_combobox.current(0)
        self.mode_combobox.bind("<<ComboboxSelected>>", self.gui_mode_cbox)
        self.mode_combobox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        page_number_label = ttk.Label(frame, text="Pages to Convert")
        page_number_label.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        page_number_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_page_numbers,
            validate="focusout",
            validatecommand=self.validate_and_update_page_nums,
            width=13,
        )
        page_number_entry.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        max_column_check_button = ttk.Checkbutton(
            frame,
            text="Maximum Columns",
            variable=self.is_column_num_checked,
            command=self.gui_column_num,
        )
        max_column_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        max_column_spinbox = ttk.Spinbox(
            frame,
            from_=cst.MAX_COLUMN_MIN_VALUE,
            to=cst.MAX_COLUMN_MAX_VALUE,
            increment=1,
            textvariable=self.strvar_column_num,
            command=self.gui_column_num,
            width=4,
        )
        max_column_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        landscape_check_button = ttk.Checkbutton(
            frame,
            text="Output in Landscape",
            variable=self.is_landscape_checked,
            command=self.gui_validate_landscape,
        )
        landscape_check_button.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        landscapepage_number_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_landscape_pages,
            validate="focusout",
            validatecommand=self.gui_validate_landscape,
            width=13,
        )
        landscapepage_number_entry.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        resolution_check_button = ttk.Checkbutton(
            frame,
            text="Document Resolution Factor",
            variable=self.is_resolution_multipler_checked,
            command=self.gui_document_resolution_multipler,
        )
        resolution_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        resolution_spinbox = ttk.Spinbox(
            frame,
            from_=cst.DOCUMENT_RESOLUTION_FACTOR_MIN_VALUE,
            to=cst.DOCUMENT_RESOLUTION_FACTOR_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_resolution_multiplier,
            command=self.gui_document_resolution_multipler,
            width=4,
        )
        resolution_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        fixed_font_size_check_button = ttk.Checkbutton(
            frame,
            text="Fixed Output Font Size",
            variable=self.is_fixed_font_size_checked,
            command=self.gui_fixed_font_size,
        )
        fixed_font_size_check_button.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        fixed_font_size_spinbox = ttk.Spinbox(
            frame,
            from_=cst.FIXED_FONT_SIZE_MIN_VALUE,
            to=cst.FIXED_FONT_SIZE_MAX_VALUE,
            increment=1,
            textvariable=self.strvar_fixed_font_size,
            command=self.gui_fixed_font_size,
            width=4,
        )
        fixed_font_size_spinbox.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        smart_line_break_check_button = ttk.Checkbutton(
            frame,
            text="Smart Line Breaks",
            variable=self.is_smart_linebreak_checked,
            command=self.gui_line_break,
        )
        smart_line_break_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        smart_line_break_spinbox = ttk.Spinbox(
            frame,
            from_=cst.SMART_LINE_BREAK_MIN_VALUE,
            to=cst.SMART_LINE_BREAK_MAX_VALUE,
            increment=0.01,
            textvariable=self.strvar_linebreak_space,
            command=self.gui_line_break,
            width=5,
        )
        smart_line_break_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        autocrop_check_button = ttk.Checkbutton(
            frame,
            text="Auto-Crop",
            variable=self.is_auto_crop_checked,
            command=self.gui_auto_crop,
        )
        autocrop_check_button.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        autocrop_spinbox = ttk.Spinbox(
            frame,
            from_=cst.AUTO_CROP_MIN_VALUE,
            to=cst.AUTO_CROP_MAX_VALUE,
            increment=0.1,
            textvariable=self.strvar_auto_crop,
            command=self.gui_auto_crop,
            width=5,
        )
        autocrop_spinbox.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        option_frame_left_part_col_num = 0
        parameters_frame_line_number += 1
        save_parameters_frame_line_number = parameters_frame_line_number

        autostraighten_check_button = ttk.Checkbutton(
            frame,
            text="Autostraighten",
            variable=self.is_autostraighten_checked,
            command=self.gui_auto_straighten,
        )
        autostraighten_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        break_after_source_page_check_button = ttk.Checkbutton(
            frame,
            text="Break after each source page",
            variable=self.is_break_page_checked,
            command=self.gui_break_page,
        )
        break_after_source_page_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        color_output_check_button = ttk.Checkbutton(
            frame,
            text="Color Output",
            variable=self.is_coloroutput_checked,
            command=self.gui_color_output,
        )
        color_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        native_pdf_output_check_button = ttk.Checkbutton(
            frame,
            text="Native PDF output",
            variable=self.is_native_pdf_checked,
            command=self.gui_native_pdf,
        )
        native_pdf_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        avoid_text_overlap_check_button = ttk.Checkbutton(
            frame,
            text="Avoid text selection overlap",
            variable=self.is_avoid_overlap_checked,
            command=self.gui_avoid_text_selection_overlap,
        )
        avoid_text_overlap_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        post_process_ghostscript_check_button = ttk.Checkbutton(
            frame,
            text="Post process w/GhostScript",
            variable=self.is_ghostscript_postprocessing_checked,
            command=self.gui_post_gs,
        )
        post_process_ghostscript_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        generate_markup_source_check_button = ttk.Checkbutton(
            frame,
            text="Generate marked-up source",
            variable=self.is_markedup_source_checked,
            command=self.gui_marked_source,
        )
        generate_markup_source_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        option_frame_right_part_col_num = 2
        parameters_frame_line_number = save_parameters_frame_line_number

        reflow_text_check_button = ttk.Checkbutton(
            frame,
            text="Re-flow text",
            variable=self.is_reflow_text_checked,
            command=self.gui_reflow_text,
        )
        reflow_text_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        erase_vline_check_button = ttk.Checkbutton(
            frame,
            text="Erase vertical lines",
            variable=self.is_erase_vertical_line_checked,
            command=self.gui_erase_vertical_line,
        )
        erase_vline_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        erase_hline_check_button = ttk.Checkbutton(
            frame,
            text="Erase horizontal lines",
            variable=self.is_erase_horizontal_line_checked,
            command=self.gui_erase_horizontal_line,
        )
        erase_hline_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        fast_preview_check_button = ttk.Checkbutton(
            frame,
            text="Fast preview",
            variable=self.is_fast_preview_checked,
            command=self.gui_fast_preview,
        )
        fast_preview_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        right_to_left_check_button = ttk.Checkbutton(
            frame,
            text="Right-to-left text",
            variable=self.is_right_to_left_checked,
            command=self.gui_right_to_left,
        )
        right_to_left_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        parameters_frame_line_number += 1
        ignore_defect_check_button = ttk.Checkbutton(
            frame,
            text="Ignore small defects",
            variable=self.is_ignore_small_defects_checked,
            command=self.gui_ignore_small_defect,
        )
        ignore_defect_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __setup_tesseract_frame(self):
        """Set up the tesseract options frame and draw its widgets"""
        self.conversion_tab_left_part_line_num += 1

        tesseract_frame = ttk.Labelframe(
            self.conversion_tab,
            text="Tesseract",
            width=self.half_width_screen,
            height=20,
        )
        tesseract_frame.grid(
            column=0,
            row=self.conversion_tab_left_part_line_num,
            # rowspan=3,
            sticky=tk.N + tk.S + tk.E + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        tesseract_frame.grid_propagate(False)
        self.__insert_tesseract_fields_into_frame(tesseract_frame)

    def __insert_tesseract_fields_into_frame(self, frame):
        """Insert tesseract/ocr field into a frame"""
        tesseract_frame_line_number = 1
        ocr_check_button = ttk.Checkbutton(
            frame,
            text="Tesseract (OCR)",
            variable=self.is_tesseract_checked,
            command=self.gui_ocr_and_cpu,
        )
        ocr_check_button.grid(
            column=0,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        ocr_cpu_spinbox = ttk.Spinbox(
            frame,
            from_=cst.OCR_CPU_MIN_VALUE,
            to=cst.OCR_CPU_MAX_VALUE,
            increment=1,
            # text='CPU %',
            textvariable=self.strvar_tesseract_cpu_percentage,
            command=self.gui_ocr_and_cpu,
            width=4,
        )
        ocr_cpu_spinbox.grid(
            column=1,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        tesseract_fast_check_button = ttk.Checkbutton(
            frame,
            text="Fast",
            variable=self.is_tesseract_fast_checked,
            command=self.gui_tesseract_fast,
        )
        tesseract_fast_check_button.grid(
            column=2,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        tesseract_frame_line_number += 1
        tesseract_language_label = ttk.Label(frame, text="Language")
        tesseract_language_label.grid(
            column=0,
            row=tesseract_frame_line_number,
            rowspan=2,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        self.tesseract_language = ttk.Combobox(
            frame, textvariable=self.strvar_tesseract_language, width=22
        )
        self.tesseract_language["values"] = list(cst.LANGUAGE_MAP.values())
        self.tesseract_language.current(24)
        self.tesseract_language.bind(
            "<<ComboboxSelected>>", self.gui_tesseract_language_cbox
        )
        self.tesseract_language.grid(
            column=1,
            row=tesseract_frame_line_number,
            columnspan=2,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        tesseract_frame_line_number += 1
        ocr_detection_label = ttk.Label(frame, text="OCR Detection")
        ocr_detection_label.grid(
            column=0,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        self.ocr_detection_combobox = ttk.Combobox(
            frame, textvariable=self.strvar_tesseract_detection, width=25
        )
        self.ocr_detection_combobox["values"] = list(cst.OCRD_MAP.values())
        self.ocr_detection_combobox.current(0)
        self.ocr_detection_combobox.bind(
            "<<ComboboxSelected>>", self.gui_tesseract_detection_cbox
        )
        self.ocr_detection_combobox.grid(
            column=1,
            columnspan=3,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __draw_action_frame_on_tab(self, tab, column, line):
        """Set up the action frame and draw its widgets"""
        line += 1

        action_frame = ttk.Labelframe(tab, text="Actions")
        action_frame.grid(
            column=column,
            row=line,
            rowspan=4,
            sticky=tk.N + tk.S + tk.E + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        action_frame_line_num = self.__insert_action_fields_into_frame(action_frame)
        action_frame.columnconfigure(1, weight=1)
        action_frame.rowconfigure(action_frame_line_num, weight=1)

    def __insert_action_fields_into_frame(self, frame):
        """Insert action fields into a frame"""
        action_frame_line_num = 0
        preview_button = ttk.Button(
            frame, text="Preview", command=self.action_preview_current_page
        )
        preview_button.grid(
            column=0,
            row=action_frame_line_num,
            columnspan=2,
        )
        convert_button = ttk.Button(
            frame, text="Convert", command=self.action_convert_pdf
        )
        convert_button.grid(
            column=2,
            row=action_frame_line_num,
        )
        abort_button = ttk.Button(
            frame,
            text="Abort",
            command=self.action_abort_conversion,
        )
        abort_button.grid(
            column=3,
            row=action_frame_line_num,
            columnspan=2,
        )

        action_frame_of_conversion_tab_column_num = 0
        action_frame_line_num += 1

        first_button = ttk.Button(
            frame, text="<<", command=self.action_ten_page_up
        )
        first_button.grid(
            column=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        action_frame_of_conversion_tab_column_num += 1

        previous_button = ttk.Button(
            frame, text="<", command=self.action_page_up
        )
        previous_button.grid(
            column=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        action_frame_of_conversion_tab_column_num += 1
        current_preview_page_number_entry = ttk.Entry(
            frame,
            textvariable=self.strvar_current_preview_page_num,
            width=30,
            justify='center',
        )
        current_preview_page_number_entry.grid(
            column=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        action_frame_of_conversion_tab_column_num += 1
        next_button = ttk.Button(
            frame, text=">", command=self.action_page_down
        )
        next_button.grid(
            column=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        action_frame_of_conversion_tab_column_num += 1

        last_button = ttk.Button(
            frame, text=">>", command=self.action_ten_page_down
        )
        last_button.grid(
            column=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

        action_frame_of_conversion_tab_column_num += 1
        action_frame_line_num += 1

        self.preview_canvas = tk.Canvas(frame, bd=0)
        self.preview_canvas.grid(
            column=0,
            columnspan=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.S + tk.E + tk.W,
        )

        x_scrollbar = ttk.Scrollbar(
            frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview
        )
        x_scrollbar.grid(
            column=0,
            row=action_frame_line_num + 1,
            columnspan=action_frame_of_conversion_tab_column_num,
            sticky=tk.E + tk.W,
        )

        y_scrollbar = ttk.Scrollbar(
            frame, command=self.preview_canvas.yview
        )
        y_scrollbar.grid(
            column=action_frame_of_conversion_tab_column_num,
            row=action_frame_line_num,
            sticky=tk.N + tk.S,
        )

        self.preview_canvas.configure(xscrollcommand=x_scrollbar.set)
        self.preview_canvas.configure(yscrollcommand=y_scrollbar.set)
        self.preview_canvas.bind("<MouseWheel>", self.yscroll_canvas)
        self.preview_canvas.bind("<Shift-MouseWheel>", self.xscroll_canvas)
        return action_frame_line_num

    def __fill_logs_tab(self):
        """Fill the Log tab with widget"""
        stdout_frame = ttk.Labelframe(self.logs_tab, text="k2pdfopt STDOUT:")
        stdout_frame.pack(expand=1, fill="both")
        stdout_frame.columnconfigure(0, weight=1)
        stdout_frame.rowconfigure(1, weight=1)

        self.stdout_text = scrolledtext.ScrolledText(
            stdout_frame, state=tk.DISABLED, wrap="word"
        )
        self.stdout_text.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.clear_button = ttk.Button(
            stdout_frame, text="Clear", command=self.__clear_logs
        )
        self.clear_button.grid(
            column=0,
            row=1,
            sticky=tk.N + tk.E,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __draw_command_line_frame_on_tab(self, tab, column, line):
        """Set up the `command line` frame and draw its widgets"""
        line += 1

        information_frame = ttk.Labelframe(
            tab, text="Command-line Options"
        )
        information_frame.grid(
            column=column,
            row=line,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )
        self.__insert_command_line_field_into_frame(information_frame)
        return line

    def __insert_command_line_field_into_frame(self, frame):
        """Insert the command-line fields into a frame."""
        command_arguments_entry = ttk.Entry(
            frame, textvariable=self.strvar_command_args, width=76
        )
        command_arguments_entry.bind("<Button-1>", self.gui_cmd_args)
        command_arguments_entry.grid(
            column=0,
            row=0,
            sticky=tk.N + tk.W,
            pady=cst.DEFAULT_PADY,
            padx=cst.DEFAULT_PADX,
        )

    def __initialize(self):
        """Simulate a click on every field : execute all the binded method

        TODO:
            - rename `validate_and_update_page_nums` to `gui_validate_and_update_page_nums`
            - for i in range (1,10) self.ui_cropbox_margin(i)
        """
        for method_name in [x for x in dir(self.__class__) if x.startswith("gui_")]:
            getattr(self, method_name)()
        self.validate_and_update_page_nums()

    def __initialize_vars(self, dict_vars):
        """Initialize variables from a dictionnary and build the associated command line"""
        for key, value in dict_vars.items():
            for i in range(len(value)):
                self.arg_var_map[key][i].set(value[i])
        self.__initialize()
        self.__update_command_argument_entry_strvar()

    # Command management methods
    def __remove_command_argument(self, arg_key):
        """Removing argument from k2pdfopt command line"""
        self.k2pdfopt_command_args.pop(arg_key, None)
        self.__update_command_argument_entry_strvar()

    def __add_or_update_command_argument(self, arg_key, arg_value):
        """Add or update argument to k2pdfopt command line"""
        self.k2pdfopt_command_args[arg_key] = arg_value
        self.__update_command_argument_entry_strvar()

    def __update_command_argument_entry_strvar(self):
        """Update command-line"""
        self.strvar_command_args.set(self.generate_command_argument_string())

    def generate_command_argument_string(self):
        """Transforms the dictionary `k2pdfopt_command_args` into a command line arguments list.

        Remarks: at the end, the chosen argument are completed by `mandatory` arguments
                ('-a- -ui- -x').
        """

        device_arg = self.k2pdfopt_command_args.pop(cst.DEVICE_ARG_NAME, None)
        if device_arg is None:
            width_arg = self.k2pdfopt_command_args.pop(cst.DEVICE_WIDTH_ARG_NAME, None)
            height_arg = self.k2pdfopt_command_args.pop(
                cst.DEVICE_HEIGHT_ARG_NAME, None
            )

        mode_arg = self.k2pdfopt_command_args.pop(cst.CONVERSION_MODE_ARG_NAME, None)
        if mode_arg is not None:
            arg_list = [mode_arg] + list(self.k2pdfopt_command_args.values())
            self.k2pdfopt_command_args[cst.CONVERSION_MODE_ARG_NAME] = mode_arg
        else:
            arg_list = list(self.k2pdfopt_command_args.values())

        if device_arg is not None:
            arg_list.append(device_arg)
            self.k2pdfopt_command_args[cst.DEVICE_ARG_NAME] = device_arg
        elif width_arg is not None and height_arg is not None:
            arg_list.append(width_arg)
            arg_list.append(height_arg)
            self.k2pdfopt_command_args[cst.DEVICE_WIDTH_ARG_NAME] = width_arg
            self.k2pdfopt_command_args[cst.DEVICE_HEIGHT_ARG_NAME] = height_arg

        arg_list.append("-a- -ui- -x")
        self.log_string("Generate Argument List: " + str(arg_list))
        cmd_arg_str = " ".join(arg_list)
        return cmd_arg_str

    def __menu_about_box(self):
        """Generate About's menu"""
        about_message = """ReBook 2 ßeta

                TclTk GUI for k2pdfopt
                Largely based on
                Pu Wang's rebook.

                The source code can be found at:
                 - rebook: http://github.com/pwang7/rebook/
                 - ReBook2: https://github.com/R-e-d-J/rebook/"""

        messagebox.showinfo(message=about_message)

    def action_open_pdf_file(self):
        """Select a PDF/DJVU file and generate output path"""
        supported_formats = [("PDF files", "*.pdf"), ("DJVU files", "*.djvu")]
        filename = filedialog.askopenfilename(
            filetypes=supported_formats,
            title="Select your file",
        )
        if filename is not None and len(filename.strip()) > 0:
            self.strvar_input_file_path.set(filename)
            if self.strvar_output_file_path.get() == "":
                (base_path, file_ext) = os.path.splitext(filename)
                end = base_path.rfind("/")
                self.strvar_output_file_path.set(
                    base_path[0 : end + 1]
                )  #  + self.output_file_suffix + file_ext

    def action_choose_output_folder(self):
        """Choose the output folder (path)"""
        folder_path = filedialog.askdirectory(title="Select the output folder")
        if folder_path is not None and len(folder_path) > 0:
            if folder_path[-1] != "/":
                folder_path += "/"
            self.strvar_output_file_path.set(folder_path)

    def __menu_save_preset(self):
        """Save the current present into a json file for next use"""
        filename = filedialog.asksaveasfilename()
        if filename is not None and len(filename.strip()) > 0:
            filename += ".json"
            with open(filename, "w", encoding="UTF-8") as preset_file:
                dict_to_save = {}
                for key, value in self.arg_var_map.items():
                    if key != cst.OUTPUT_PATH_ARG_NAME:
                        dict_to_save[key] = [var.get() for var in value]
                json.dump(dict_to_save, preset_file)

    def __menu_open_preset_file(self):
        """Open and load custom preset file"""
        supported_formats = [
            ("JSON files", "*.json"),
        ]
        filename = filedialog.askopenfilename(
            filetypes=supported_formats,
            title="Select your preset file",
        )
        if filename is not None and len(filename.strip()) > 0:
            self.load_custom_preset(filename)

    def gui_device_unit_cbox(
        self, binded_event=None
    ):  # pylint: disable=unused-argument
        """Manage `Unit` option"""
        self.update_device_unit_width_height()

    def gui_width_height(self):
        """Manage `Width` and `Height` options"""
        self.update_device_unit_width_height()

    def update_device_unit_width_height(self):
        """Update the command-line information with device's unit, width and height"""
        if self.device_combobox.current() != 23:  # non-other type
            device_type = cst.DEVICE_ARGUMENT_MAP[self.device_combobox.current()]
            arg = cst.DEVICE_ARG_NAME + " " + device_type
            self.__add_or_update_command_argument(cst.DEVICE_ARG_NAME, arg)
            self.__remove_command_argument(cst.DEVICE_WIDTH_ARG_NAME)
            self.__remove_command_argument(cst.DEVICE_HEIGHT_ARG_NAME)
            self.strvar_device_screen_width.set(
                cst.DEVICE_WIDTH_HEIGHT_DPI_INFO[self.device_combobox.current()][0]
            )
            self.strvar_device_screen_height.set(
                cst.DEVICE_WIDTH_HEIGHT_DPI_INFO[self.device_combobox.current()][1]
            )
            self.strvar_device_screen_dpi.set(
                cst.DEVICE_WIDTH_HEIGHT_DPI_INFO[self.device_combobox.current()][2]
            )
        else:  # "Other type" chosen
            screen_unit = cst.UNIT_ARGUMENT_MAP[self.unit_combobox.current()]

            width = self.strvar_device_screen_width.get().strip()
            if tools.is_acceptable_number(
                width, "int", cst.DEVICE_WIDTH_MIN_VALUE, cst.DEVICE_WIDTH_MAX_VALUE
            ):
                width_arg = cst.DEVICE_WIDTH_ARG_NAME + " " + width + screen_unit
                self.__add_or_update_command_argument(
                    cst.DEVICE_WIDTH_ARG_NAME, width_arg
                )
            else:
                self.__remove_command_argument(cst.DEVICE_WIDTH_ARG_NAME)

            height = self.strvar_device_screen_height.get().strip()
            if tools.is_acceptable_number(
                width, "int", cst.DEVICE_HEIGHT_MIN_VALUE, cst.DEVICE_HEIGHT_MAX_VALUE
            ):
                height_arg = cst.DEVICE_HEIGHT_ARG_NAME + " " + height + screen_unit
                self.__add_or_update_command_argument(
                    cst.DEVICE_HEIGHT_ARG_NAME, height_arg
                )
            else:
                self.__remove_command_argument(cst.DEVICE_HEIGHT_ARG_NAME)

            self.__remove_command_argument(cst.DEVICE_ARG_NAME)

    def gui_mode_cbox(self, binded_event=None):  # pylint: disable=unused-argument
        """Manage `Mode` options"""
        conversion_mode = cst.MODE_ARGUMENT_MAP[self.mode_combobox.current()]
        arg = cst.CONVERSION_MODE_ARG_NAME + " " + conversion_mode
        self.__add_or_update_command_argument(cst.CONVERSION_MODE_ARG_NAME, arg)

    def gui_cmd_args(self, binded_event=None):  # pylint: disable=unused-argument
        """update the k2pdfopt command-line"""
        self.__update_command_argument_entry_strvar()

    def gui_column_num(self):
        """Manage `Max Column` options"""
        nb_column = self.strvar_column_num.get().strip()
        if self.is_column_num_checked.get() and tools.is_acceptable_number(
            nb_column, "int", cst.MAX_COLUMN_MIN_VALUE, cst.MAX_COLUMN_MIN_VALUE
        ):
            arg = cst.COLUMN_NUM_ARG_NAME + " " + nb_column
            self.__add_or_update_command_argument(cst.COLUMN_NUM_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.COLUMN_NUM_ARG_NAME)

    def gui_document_resolution_multipler(self):
        """Manage `Document Resolution Factor` options"""
        multiplier = self.strvar_resolution_multiplier.get().strip()
        if self.is_resolution_multipler_checked.get() and tools.is_acceptable_number(
            multiplier,
            "float",
            cst.DOCUMENT_RESOLUTION_FACTOR_MIN_VALUE,
            cst.DOCUMENT_RESOLUTION_FACTOR_MAX_VALUE,
        ):
            arg = cst.RESOLUTION_MULTIPLIER_ARG_NAME + " " + multiplier
            self.__add_or_update_command_argument(
                cst.RESOLUTION_MULTIPLIER_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.RESOLUTION_MULTIPLIER_ARG_NAME)

    def gui_crop_margin(self):
        """Manage `Crop Margin` option

        Remarks:
            - conflict with `Auto-Crop` option
            - conflict with `Cropboxes` options
        """

        if self.is_cropmargin_checked.get():
            self.is_auto_crop_checked.set(False)
            self.__remove_command_argument(cst.AUTO_CROP_ARG_NAME)
            self.__remove_cropboxes_argument()

            if len(self.strvar_left_cropmargin.get().strip()) > 0:
                arg = (
                    cst.CROP_MARGIN_LEFT_ARG_NAME
                    + " "
                    + self.strvar_left_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    cst.CROP_MARGIN_LEFT_ARG_NAME, arg
                )

            if len(self.strvar_top_cropmargin.get().strip()) > 0:
                arg = (
                    cst.CROP_MARGIN_TOP_ARG_NAME
                    + " "
                    + self.strvar_top_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(cst.CROP_MARGIN_TOP_ARG_NAME, arg)

            if len(self.strvar_width_cropmargin.get().strip()) > 0:
                arg = (
                    cst.CROP_MARGIN_RIGHT_ARG_NAME
                    + " "
                    + self.strvar_width_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    cst.CROP_MARGIN_RIGHT_ARG_NAME, arg
                )

            if len(self.strvar_height_cropmargin.get().strip()) > 0:
                arg = (
                    cst.CROP_MARGIN_BOTTOM_ARG_NAME
                    + " "
                    + self.strvar_height_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    cst.CROP_MARGIN_BOTTOM_ARG_NAME, arg
                )
        else:
            self.__remove_crop_margin_argument()

    def __remove_crop_margin_argument(self):
        self.is_cropmargin_checked.set(False)
        self.__remove_command_argument(cst.CROP_MARGIN_LEFT_ARG_NAME)
        self.__remove_command_argument(cst.CROP_MARGIN_TOP_ARG_NAME)
        self.__remove_command_argument(cst.CROP_MARGIN_RIGHT_ARG_NAME)
        self.__remove_command_argument(cst.CROP_MARGIN_BOTTOM_ARG_NAME)

    def ui_cropbox_margin(self, number):
        """Manage `Cropbox x` options"""
        page_range = getattr(self, "strvar_page_range_cropbox_" + str(number)).get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            getattr(self, "strvar_page_range_cropbox_" + str(number)).set("")
            messagebox.showerror(
                message="Invalide cropbox 1's page range. It should be like : 2-5e,3-7o,9-"
            )
            return

        if getattr(self, "is_cropbox_checked_" + str(number)).get():
            self.__remove_crop_margin_argument()
            self.is_auto_crop_checked.set(False)
            self.__remove_command_argument(cst.AUTO_CROP_ARG_NAME)

            cropbox_value = [
                getattr(self, "strvar_left_cropbox_" + str(number)).get(),
                getattr(self, "strvar_top_cropbox_" + str(number)).get(),
                getattr(self, "strvar_width_cropbox_" + str(number)).get(),
                getattr(self, "strvar_height_cropbox_" + str(number)).get(),
            ]
            arg = (
                cst.CROPBOX_ARG_NAME
                + page_range
                + " "
                + ",".join(map(str.strip, cropbox_value))
            )
            self.__add_or_update_command_argument(getattr(cst, "CROPBOX_" + str(number) + "_ARG_NAME"), arg)
        else:
            self.__remove_command_argument(getattr(cst, "CROPBOX_" + str(number) + "_ARG_NAME"))

    def gui_dpi(self):
        """Manage device's `DPI` option"""
        dpi_value = self.strvar_device_screen_dpi.get().strip()
        if self.is_dpi_checked.get() and tools.is_acceptable_number(
            dpi_value, "int", cst.DEVICE_DPI_MIN_VALUE, cst.DEVICE_DPI_MAX_VALUE
        ):
            arg = cst.DPI_ARG_NAME + " " + dpi_value
            self.__add_or_update_command_argument(cst.DPI_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.DPI_ARG_NAME)

    def validate_and_update_page_nums(self):
        """Update the command-line with page range if it's a valid range"""
        if len(
            self.strvar_page_numbers.get().strip()
        ) > 0 and not tools.check_page_nums(self.strvar_page_numbers.get().strip()):

            self.__remove_command_argument(cst.PAGE_NUM_ARG_NAME)
            self.strvar_page_numbers.set("")
            messagebox.showerror(
                message="Invalide Page Argument. It should be like: 2-5e,3-7o,9-"
            )
            return False

        if len(self.strvar_page_numbers.get().strip()) > 0:
            arg = cst.PAGE_NUM_ARG_NAME + " " + self.strvar_page_numbers.get().strip()
            self.__add_or_update_command_argument(cst.PAGE_NUM_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.PAGE_NUM_ARG_NAME)

        return True

    def gui_fixed_font_size(self):
        """Manage `Fixed output font size` option"""
        font_size = self.strvar_fixed_font_size.get().strip()
        if self.is_fixed_font_size_checked.get() and tools.is_acceptable_number(
            font_size,
            "int",
            cst.FIXED_FONT_SIZE_MIN_VALUE,
            cst.FIXED_FONT_SIZE_MAX_VALUE,
        ):
            arg = cst.FIXED_FONT_SIZE_ARG_NAME + " " + font_size
            self.__add_or_update_command_argument(cst.FIXED_FONT_SIZE_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.FIXED_FONT_SIZE_ARG_NAME)

    def __remove_tesseract_argument(self):
        self.__remove_command_argument(cst.OCR_ARG_NAME)
        self.__remove_command_argument(cst.OCR_CPU_ARG_NAME)
        self.__remove_command_argument(cst.TESSERACT_LANGUAGE_ARG_NAME)
        self.__remove_command_argument(cst.TESSERACT_FAST_ARG_NAME)
        self.__remove_command_argument(cst.TESSERACT_DETECTION_ARG_NAME)

    def __uncheck_cropboxes_checkbox(self):
        self.is_cropbox_checked_1.set(False)
        self.is_cropbox_checked_2.set(False)
        self.is_cropbox_checked_3.set(False)
        self.is_cropbox_checked_4.set(False)
        self.is_cropbox_checked_5.set(False)

    def __remove_cropboxes_argument(self):
        self.__uncheck_cropboxes_checkbox()
        self.__remove_command_argument(cst.CROPBOX_1_ARG_NAME)
        self.__remove_command_argument(cst.CROPBOX_2_ARG_NAME)
        self.__remove_command_argument(cst.CROPBOX_3_ARG_NAME)
        self.__remove_command_argument(cst.CROPBOX_4_ARG_NAME)
        self.__remove_command_argument(cst.CROPBOX_5_ARG_NAME)

    def gui_ocr_and_cpu(self):
        """OCR CPU pourcentage management

        Remarks:
            - ocr conflicts with native pdf
            - negtive integer means percentage
        """
        if self.is_tesseract_checked.get():
            self.is_native_pdf_checked.set(False)
            self.__remove_command_argument(cst.NATIVE_PDF_ARG_NAME)
            self.__add_or_update_command_argument(cst.OCR_ARG_NAME, cst.OCR_ARG_NAME)
            ocr_cpu_arg = (
                cst.OCR_CPU_ARG_NAME
                + " -"
                + self.strvar_tesseract_cpu_percentage.get().strip()
            )
            self.__add_or_update_command_argument(cst.OCR_CPU_ARG_NAME, ocr_cpu_arg)
            self.gui_tesseract_fast()
            self.gui_tesseract_language_cbox()
        else:
            self.__remove_tesseract_argument()

    def gui_tesseract_fast(self):
        """Manage `Fast` option for Tesseract"""
        if self.is_tesseract_fast_checked.get():
            self.gui_tesseract_language_cbox()
        else:
            self.__remove_command_argument(cst.TESSERACT_LANGUAGE_ARG_NAME)
            self.gui_tesseract_language_cbox()

    def gui_tesseract_language_cbox(
        self, binded_event=None
    ):  # pylint: disable=unused-argument
        """Manage the `language` option for Tesseract"""
        if self.is_tesseract_checked.get():
            language_arg = cst.LANGUAGE_ARGUMENT_MAP[self.tesseract_language.current()]
            arg = cst.TESSERACT_LANGUAGE_ARG_NAME + " " + language_arg
            if self.is_tesseract_fast_checked.get():
                arg += " " + cst.TESSERACT_FAST_ARG_NAME
            self.__add_or_update_command_argument(cst.TESSERACT_LANGUAGE_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.TESSERACT_LANGUAGE_ARG_NAME)

    def gui_tesseract_detection_cbox(
        self, binded_event=None
    ):  # pylint: disable=unused-argument
        """Manage `OCR Detection` option for Tesseract"""
        if self.is_tesseract_checked.get():
            detection_type = (
                cst.TESSERACT_DETECTION_ARG_NAME
                + " "
                + cst.OCRD_ARGUMENT_MAP[self.ocr_detection_combobox.current()]
            )
            self.__add_or_update_command_argument(
                cst.TESSERACT_DETECTION_ARG_NAME, detection_type
            )
        else:
            self.__remove_command_argument(cst.TESSERACT_DETECTION_ARG_NAME)

    def gui_validate_landscape(self):
        """Update the command-line with landscape (page range if valid range)"""
        page_range = self.strvar_landscape_pages.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            self.__remove_command_argument(cst.LANDSCAPE_ARG_NAME)
            self.strvar_landscape_pages.set("")
            messagebox.showerror(
                message="Invalide `Output in Landscape` Page Argument!"
            )
            return False

        if self.is_landscape_checked.get():
            arg = cst.LANDSCAPE_ARG_NAME
            if len(page_range) > 0:
                arg += page_range  # no space between -ls and page numbers
            self.__add_or_update_command_argument(cst.LANDSCAPE_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.LANDSCAPE_ARG_NAME)

        return True

    def gui_line_break(self):
        """Manage `Line Breack on eacht source page breack` option"""
        line_break = self.strvar_linebreak_space.get().strip()
        if self.is_smart_linebreak_checked.get() and tools.is_acceptable_number(
            line_break,
            "float",
            cst.SMART_LINE_BREAK_MIN_VALUE,
            cst.SMART_LINE_BREAK_MAX_VALUE,
        ):
            arg = cst.LINEBREAK_ARG_NAME + " " + str(line_break)
            self.__add_or_update_command_argument(cst.LINEBREAK_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.LINEBREAK_ARG_NAME)

    def gui_auto_straighten(self):
        """Manage `Auto Straighten` option"""
        if self.is_autostraighten_checked.get():
            self.__add_or_update_command_argument(
                cst.AUTO_STRAIGNTEN_ARG_NAME, cst.AUTO_STRAIGNTEN_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.AUTO_STRAIGNTEN_ARG_NAME)

    def gui_break_page(self):
        """Native PDF management

        Remarks : `break page` conflicts with `avoid overlap` since they are both -bp flag
        """
        if self.is_break_page_checked.get():
            self.is_avoid_overlap_checked.set(False)
            self.__remove_command_argument(cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME)
            self.__add_or_update_command_argument(
                cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME,
                cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME,
            )
        else:
            self.__remove_command_argument(cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME)

    def gui_color_output(self):
        """Manage `Color Output` option"""
        if self.is_coloroutput_checked.get():
            self.__add_or_update_command_argument(
                cst.COLOR_OUTPUT_ARG_NAME, cst.COLOR_OUTPUT_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.COLOR_OUTPUT_ARG_NAME)

    def gui_native_pdf(self):
        """Manage `Native PDF`option.

        Remarks: `native pdf` conflicts with 'ocr' and 'reflow text'
        """
        if self.is_native_pdf_checked.get():
            self.is_tesseract_checked.set(False)
            self.__remove_tesseract_argument()
            self.is_reflow_text_checked.set(False)
            self.__remove_command_argument(cst.REFLOW_TEXT_ARG_NAME)
            self.__add_or_update_command_argument(
                cst.NATIVE_PDF_ARG_NAME, cst.NATIVE_PDF_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.NATIVE_PDF_ARG_NAME)

    def gui_right_to_left(self):
        """Manage `Right to left` option"""
        if self.is_right_to_left_checked.get():
            self.__add_or_update_command_argument(
                cst.RIGHT_TO_LEFT_ARG_NAME, cst.RIGHT_TO_LEFT_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.RIGHT_TO_LEFT_ARG_NAME)

    def gui_post_gs(self):
        """Manage `post precessing with GhostScript` option"""
        if self.is_ghostscript_postprocessing_checked.get():
            self.__add_or_update_command_argument(
                cst.POST_GS_ARG_NAME, cst.POST_GS_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.POST_GS_ARG_NAME)

    def gui_marked_source(self):
        """Manage `Show Markup Source` option"""
        if self.is_markedup_source_checked.get():
            self.__add_or_update_command_argument(
                cst.MARKED_SOURCE_ARG_NAME, cst.MARKED_SOURCE_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.MARKED_SOURCE_ARG_NAME)

    def gui_reflow_text(self):
        """Manage `Re-Flow text` option

        Remarks: `reflow text` conflicts with `native pdf`
        """
        if self.is_reflow_text_checked.get():
            self.is_native_pdf_checked.set(False)
            self.__remove_command_argument(cst.NATIVE_PDF_ARG_NAME)
            arg = cst.REFLOW_TEXT_ARG_NAME + "+"
            self.__add_or_update_command_argument(cst.REFLOW_TEXT_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.REFLOW_TEXT_ARG_NAME)

    def gui_erase_vertical_line(self):
        """Manage `Erase vertical line` option"""
        if self.is_erase_vertical_line_checked.get():
            arg = cst.ERASE_VERTICAL_LINE_ARG_NAME + " 1"
            self.__add_or_update_command_argument(cst.ERASE_VERTICAL_LINE_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.ERASE_VERTICAL_LINE_ARG_NAME)

    def gui_fast_preview(self):
        """Manage fast preview option"""
        if self.is_fast_preview_checked.get():
            arg = cst.FAST_PREVIEW_ARG_NAME + " 0"
            self.__add_or_update_command_argument(cst.FAST_PREVIEW_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.FAST_PREVIEW_ARG_NAME)

    def gui_avoid_text_selection_overlap(self):
        """Manage `Avoid text selection overlap` option

        Remarks: avoid overlap conflicts with break page since they are both -bp flag
        """
        if self.is_avoid_overlap_checked.get():
            self.is_break_page_checked.set(False)
            self.__remove_command_argument(cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME)

            arg = cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME + " m"
            self.__add_or_update_command_argument(
                cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.BREAK_PAGE_AVOID_OVERLAP_ARG_NAME)

    def gui_ignore_small_defect(self):
        """Manage `ignore small defect` option"""
        if self.is_ignore_small_defects_checked.get():
            arg = cst.IGN_SMALL_DEFECTS_ARG_NAME + " 1.5"
            self.__add_or_update_command_argument(cst.IGN_SMALL_DEFECTS_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.IGN_SMALL_DEFECTS_ARG_NAME)

    def gui_erase_horizontal_line(self):
        """Manage `Erase horizontal line` option"""
        if self.is_erase_horizontal_line_checked.get():
            arg = cst.ERASE_HORIZONTAL_LINE_ARG_NAME + " 1"
            self.__add_or_update_command_argument(
                cst.ERASE_HORIZONTAL_LINE_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.ERASE_HORIZONTAL_LINE_ARG_NAME)

    def gui_auto_crop(self):
        """Manage `Auto-Crop` option.

        Remarks:
            - conflict with `crop margin`
            - conflict with `cropboxes`
        """
        auto_crop_value = self.strvar_auto_crop.get().strip()
        if self.is_auto_crop_checked.get() and tools.is_acceptable_number(auto_crop_value, "float", cst.AUTO_CROP_MIN_VALUE, cst.AUTO_CROP_MAX_VALUE):
            self.__remove_crop_margin_argument()
            self.__remove_cropboxes_argument()
            arg = cst.AUTO_CROP_ARG_NAME + ' ' + auto_crop_value
            self.__add_or_update_command_argument(cst.AUTO_CROP_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.AUTO_CROP_ARG_NAME)

    def gui_minimum_column_gap(self):
        """Manage `Minimum column gap` advanced option"""
        min_column_gap = self.strvar_min_column_gap_width.get().strip()
        if self.is_minimum_column_gap_checked.get() and tools.is_acceptable_number(
            min_column_gap,
            "float",
            cst.MIN_COLUMN_GAP_WIDTH_MIN_VALUE,
            cst.MIN_COLUMN_GAP_WIDTH_MAX_VALUE,
        ):
            arg = cst.MIN_COLUMN_GAP_WIDTH_ARG_NAME + " " + min_column_gap
            self.__add_or_update_command_argument(
                cst.MIN_COLUMN_GAP_WIDTH_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.MIN_COLUMN_GAP_WIDTH_ARG_NAME)

    def gui_max_gap_between_column(self):
        """Manage `Max allowed gap between columns` advanced option"""
        max_column_gap = self.strvar_max_gap_between_column.get().strip()
        if self.is_max_gap_between_column_checked.get() and tools.is_acceptable_number(
            max_column_gap,
            "float",
            cst.MAX_GAP_BETWEEN_COLUMN_MIN_VALUE,
            cst.MAX_GAP_BETWEEN_COLUMN_MAX_VALUE,
        ):
            arg = cst.MAX_GAP_BETWEEN_COLUMN_ARG_NAME + " " + max_column_gap
            self.__add_or_update_command_argument(
                cst.MAX_GAP_BETWEEN_COLUMN_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.MAX_GAP_BETWEEN_COLUMN_ARG_NAME)

    def gui_column_gap_range(self):
        """Manage `column gap range` advanced option"""
        column_gap_range = self.strvar_column_gap_range.get().strip()
        if self.is_column_gap_range_checked.get() and tools.is_acceptable_number(
            column_gap_range,
            "float",
            cst.COLUMN_GAP_RANGE_MIN_VALUE,
            cst.COLUMN_GAP_RANGE_MAX_VALUE,
        ):
            arg = cst.COLUMN_GAP_RANGE_ARG_NAME + " " + column_gap_range
            self.__add_or_update_command_argument(cst.COLUMN_GAP_RANGE_ARG_NAME, arg)
        else:
            self.__remove_command_argument(cst.COLUMN_GAP_RANGE_ARG_NAME)

    def gui_minimum_column_height(self):
        """Manage `minimum column height` advanced option"""
        min_column_height = self.strvar_minimum_column_height.get().strip()
        if self.is_minimum_column_height_checked.get() and tools.is_acceptable_number(
            min_column_height,
            "float",
            cst.MINIMUM_COLUMN_HEIGHT_MIN_VALUE,
            cst.MINIMUM_COLUMN_HEIGHT_MAX_VALUE,
        ):
            arg = cst.MINIMUM_COLUMN_HEIGHT_ARG_NAME + " " + min_column_height
            self.__add_or_update_command_argument(
                cst.MINIMUM_COLUMN_HEIGHT_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.MINIMUM_COLUMN_HEIGHT_ARG_NAME)

    def gui_column_offset_maximum(self):
        """Manage `column offset maximum` advanced option"""
        column_offset_max = self.strvar_column_offset_maximum.get().strip()
        if self.is_column_offset_maximum_checked.get() and tools.is_acceptable_number(
            column_offset_max,
            "float",
            cst.COLUMN_OFFSET_MAXIMUM_MIN_VALUE,
            cst.COLUMN_OFFSET_MAXIMUM_MAX_VALUE,
        ):
            arg = cst.COLUMN_OFFSET_MAXIMUM_ARG_NAME + " " + column_offset_max
            self.__add_or_update_command_argument(
                cst.COLUMN_OFFSET_MAXIMUM_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(cst.COLUMN_OFFSET_MAXIMUM_ARG_NAME)

    def gui_min_height_blank_between_regions(self):
        """ Manage the `min height of the blank area that separates regions` advanced option """
        min_height_blank_between_regions = (
            self.strvar_min_height_blank_between_regions.get().strip()
        )
        if (
            self.is_min_height_blank_between_regions_checked.get()
            and tools.is_acceptable_number(
                min_height_blank_between_regions,
                "float",
                cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_MIN_VALUE,
                cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_MAX_VALUE,
            )
        ):
            arg = (
                cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_ARG_NAME
                + " "
                + min_height_blank_between_regions
            )
            self.__add_or_update_command_argument(
                cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(
                cst.MIN_HEIGHT_BLANK_BETWEEN_REGIONS_ARG_NAME
            )

    def gui_threshold_detecting_gaps_between_column(self):
        """Manage `Threshold value for detecting column gaps` advanced option """
        threshold = self.strvar_threshold_detecting_gaps_between_column.get().strip()
        if (
            self.is_threshold_detecting_gaps_between_column_checked.get()
            and tools.is_acceptable_number(
                threshold,
                "float",
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_MIN_VALUE,
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_MAX_VALUE,
            )
        ):
            arg = cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_ARG_NAME + " " + threshold
            self.__add_or_update_command_argument(
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_COLUMN_ARG_NAME
            )

    def gui_threshold_detecting_gaps_between_rows(self):
        """Manage the `threshold value for detecting gaps between rows` advanced option """
        threshold = self.strvar_threshold_detecting_gaps_between_rows.get().strip()
        if (
            self.is_threshold_detecting_gaps_between_rows_checked.get()
            and tools.is_acceptable_number(
                threshold,
                "float",
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_MIN_VALUE,
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_MAX_VALUE,
            )
        ):
            arg = cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_ARG_NAME + " " + threshold
            self.__add_or_update_command_argument(
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_ROWS_ARG_NAME
            )

    def gui_threshold_detecting_gaps_between_words(self):
        """Manage the `threshold for detecting word gaps` advanced option """
        threshold = self.strvar_threshold_detecting_gaps_between_words.get().strip()
        if (
            self.is_threshold_detecting_gaps_between_words_checked.get()
            and tools.is_acceptable_number(
                threshold,
                "float",
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_MIN_VALUE,
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_MAX_VALUE,
            )
        ):
            arg = cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_ARG_NAME + " " + threshold
            self.__add_or_update_command_argument(
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_ARG_NAME, arg
            )
        else:
            self.__remove_command_argument(
                cst.THRESHOLD_DETECTING_GAPS_BETWEEN_WORDS_ARG_NAME
            )

    def gui_text_only(self):
        """Manage the `text only` advanced option"""
        if self.is_text_only_checked.get():
            self.__add_or_update_command_argument(
                cst.TEXT_ONLY_OUTPUT_ARG_NAME, cst.TEXT_ONLY_OUTPUT_ARG_NAME
            )
        else:
            self.__remove_command_argument(cst.TEXT_ONLY_OUTPUT_ARG_NAME)

    def __remove_preview_image_and_clear_canvas(self):
        """Remove the preview image and clear the preview canevas"""
        if os.path.exists(cst.PREVIEW_IMAGE_PATH):
            os.remove(cst.PREVIEW_IMAGE_PATH)
        self.preview_canvas.delete(tk.ALL)
        self.canvas_image_tag = None

    def load_preview_image(self, img_path, preview_page_index):
        """Load the preview image into the preview canevas"""
        if os.path.exists(img_path):
            image = Image.open(img_path)
            image = image.resize(
                (int(self.root.width / 2), int((self.root.width / 2) * 1.4143)),
                Image.ANTIALIAS,
            )
            self.preview_image = ImageTk.PhotoImage(image)
            self.canvas_image_tag = self.preview_canvas.create_image(
                (0, 0),
                anchor=tk.NW,
                image=self.preview_image,
                tags="preview",
            )
            self.preview_canvas.config(
                scrollregion=(
                    0,
                    0,
                    self.preview_image.width(),
                    self.preview_image.height(),
                ),
            )
            self.strvar_current_preview_page_num.set("Page: " + str(preview_page_index))
        else:
            self.strvar_current_preview_page_num.set(
                "No Page: " + str(preview_page_index)
            )

    def __generate_one_preview_image(self, preview_page_index):
        """Generate the images previews"""
        if not self.__pdf_conversion_is_done():
            return

        if not os.path.exists(self.strvar_input_file_path.get().strip()):
            messagebox.showerror(
                message=(
                    "Failed to Find Input PDF File to convert for Preview: %s"
                    % self.strvar_input_file_path.get().strip()
                ),
            )
            return

        self.__remove_preview_image_and_clear_canvas()
        output_arg = " ".join([cst.PREVIEW_OUTPUT_ARG_NAME, str(preview_page_index)])
        self.background_future = self.convert_pdf_file(output_arg)
        self.strvar_current_preview_page_num.set("Preview Generating...")

        def preview_image_future(bgf):
            self.load_preview_image(cst.PREVIEW_IMAGE_PATH, preview_page_index)
            self.log_string(
                "Preview generation for page %d finished" % preview_page_index
            )

        self.background_future.add_done_callback(preview_image_future)

    def action_abort_conversion(self):
        """Abord the process of the preview/conversion"""
        if self.background_future is not None:
            self.background_future.cancel()
        if (
            self.background_process is not None
            and self.background_process.returncode is None
        ):
            self.background_process.terminate()

    def action_convert_pdf(self):
        """Convert the input PDF/DJVU file"""
        if not self.__pdf_conversion_is_done():
            return
        pdf_output_arg = (
            cst.OUTPUT_PATH_ARG_NAME + " %s" + cst.OUTPUT_FILE_SUFFIX
        )  # + ".pdf"
        self.background_future = self.convert_pdf_file(pdf_output_arg)

    def action_preview_current_page(self):
        """(Re)Generate preview for the current page index"""
        self.current_preview_page_index = max(self.current_preview_page_index, 1)
        self.__generate_one_preview_image(self.current_preview_page_index)

    def action_ten_page_up(self):
        """Generate preview of the 10th previous page"""
        self.current_preview_page_index = max(self.current_preview_page_index - 10, 1)
        self.__generate_one_preview_image(self.current_preview_page_index)

    def action_page_up(self):
        """Generate preview of the previous page"""
        if self.current_preview_page_index > 1:
            self.current_preview_page_index -= 1
        self.__generate_one_preview_image(self.current_preview_page_index)

    def action_page_down(self):
        """Generate preview of the next page"""
        self.current_preview_page_index += 1
        self.__generate_one_preview_image(self.current_preview_page_index)

    def action_ten_page_down(self):
        """Generate preview of the 10th next page"""
        self.current_preview_page_index += 10
        self.__generate_one_preview_image(self.current_preview_page_index)

    def yscroll_canvas(self, event):
        """Y Scrollbar for the preview canevas"""
        self.preview_canvas.yview_scroll(-1 * event.delta, "units")

    def xscroll_canvas(self, event):
        """X Scrollbar for the preview canevas"""
        self.preview_canvas.xview_scroll(-1 * event.delta, "units")

    def __pdf_conversion_is_done(self):
        """Check if the PDF conversion is already done or not"""
        if (self.background_future is None) or (self.background_future.done()):
            if (self.background_process is None) or (
                self.background_process.returncode is not None
            ):
                return True

        messagebox.showerror(
            message="Background Conversion Not Finished Yet! Please Wait..."
        )
        return False

    def start_loop(self, loop):
        """Loop for asyncio"""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def convert_pdf_file(self, output_arg):
        """Conversion of the selected PDF file with chosen options"""

        async def async_run_cmd_and_log(exec_cmd):
            executed = exec_cmd.strip()

            def log_bytes(log_btyes):
                self.log_string(log_btyes.decode("utf-8"))

            self.log_string(executed)

            process = await asyncio.create_subprocess_shell(
                executed,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self.background_process = process

            while True:
                line = await process.stdout.readline()
                log_bytes(line)

                if not line:
                    break

                if line == "" and process.returncode is not None:
                    break

        input_pdf_path = self.strvar_input_file_path.get().strip()

        # in case the file name contains space
        if " " in input_pdf_path:
            input_pdf_path = '"' + input_pdf_path + '"'

        executed = " ".join(
            [
                self.k2pdfopt_path,
                input_pdf_path,
                output_arg,
                self.generate_command_argument_string(),
            ]
        )
        future = asyncio.run_coroutine_threadsafe(
            async_run_cmd_and_log(executed), self.thread_loop
        )

        return future

    def log_string(self, str_line):
        """Write a line into the log textbox"""
        log_content = str_line.strip()

        if len(log_content) > 0:
            self.stdout_text.config(state=tk.NORMAL)
            self.stdout_text.insert(tk.END, log_content + "\n")
            self.stdout_text.config(state=tk.DISABLED)

    def __clear_logs(self):
        """Clear the logs textbox"""
        self.stdout_text.config(state=tk.NORMAL)
        self.stdout_text.delete(1.0, tk.END)
        self.stdout_text.config(state=tk.DISABLED)

    def load_custom_preset(self, json_path_file=None):
        """Load a JSON file with user custom preset

        Remarks: there is more than ONE custom preset si the second IF must be refactored.
        """
        if json_path_file is None:
            json_path_file = self.custom_preset_file_path
        if os.path.exists(json_path_file):
            with open(json_path_file, encoding="UTF-8") as preset_file:
                dict_to_load = json.load(preset_file)

                if dict_to_load:
                    self.__initialize_vars(dict_to_load)
                    return True

        return False

    def restore_default_values(self):
        """Clear logs, preview and reset all the default values"""
        for attribute, value in self.__dict__.items():
            if isinstance(value, tk.StringVar) and attribute.startswith("strvar_"):
                value.set("")
            if (
                isinstance(value, tk.BooleanVar)
                and attribute.startswith("is_")
                and attribute.endswith("_checked")
            ):
                value.set(False)
            if isinstance(value, ttk.Combobox) and attribute.endswith("_combobox"):
                value.current(0)

        self.__clear_logs()
        self.__remove_preview_image_and_clear_canvas()
        self.__initialize_vars(self.default_var_map)
