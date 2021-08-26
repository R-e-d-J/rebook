from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
import asyncio
import json
import os
import webbrowser
from PIL import Image, ImageTk

import tools


class MainFrame(ttk.Frame):
    device_argument_map =   {
                                0: 'k2',
                                1: 'dx',
                                2: 'kpw',
                                3: 'kp2',
                                4: 'kp3',
                                5: 'kv',
                                6: 'ko2',
                                7: 'pb2',
                                8: 'nookst',
                                9: 'kbt',
                                10: 'kbg',
                                11: 'kghd',
                                12: 'kghdfs',
                                13: 'kbm',
                                14: 'kba',
                                15: 'kbhd',
                                16: 'kbh2o',
                                17: 'kbh2ofs',
                                18: 'kao',
                                19: 'nex7',
                                20: None,
                            }

    device_choice_map = {
                            0: 'Kindle 1-5',
                            1: 'Kindle DX',
                            2: 'Kindle Paperwhite',
                            3: 'Kindle Paperwhite 2',
                            4: 'Kindle Paperwhite 3',
                            5: 'Kindle Voyage/PW3+/Oasis',
                            6: 'Kindle Oasis 2',
                            7: 'Pocketbook Basic 2',
                            8: 'Nook Simple Touch',
                            9: 'Kobo Touch',
                            10: 'Kobo Glo',
                            11: 'Kobo Glo HD',
                            12: 'Kobo Glo HD Full Screen',
                            13: 'Kobo Mini',
                            14: 'Kobo Aura',
                            15: 'Kobo Aura HD',
                            16: 'Kobo H2O',
                            17: 'Kobo H2O Full Screen',
                            18: 'Kobo Aura One',
                            19: 'Nexus 7',
                            20: 'Other (specify width & height)',
                        }

    mode_argument_map = {
                            0: 'def',
                            1: 'copy',
                            2: 'fp',
                            3: 'fw',
                            4: '2col',
                            5: 'tm',
                            6: 'crop',
                            7: 'concat',
                        }

    mode_choice_map =   {
                            0: 'Default',
                            1: 'Copy',
                            2: 'Fit Page',
                            3: 'Fit Width',
                            4: '2 Columns',
                            5: 'Trim Margins',
                            6: 'Crop',
                            7: 'Concat'
                        }

    unit_argument_map = {
                            0: 'in',
                            1: 'cm',
                            2: 's',
                            3: 't',
                            4: 'p',
                            5: 'x',
                        }

    unit_choice_map =   {
                            0: 'Inches',
                            1: 'Centimeters',
                            2: 'Source Page Size',
                            3: 'Trimmed Source Region Size',
                            4: 'Pixels',
                            5: 'Relative to the OCR Text Layer',
                        }

    def __init__(self, app, k2pdfopt_path):
        super().__init__(app)
        self.root = app           # root of tkinter

        self.default_padx = 5
        self.default_pady = 0
        self.k2pdfopt_path = k2pdfopt_path
        self.k2pdfopt_cmd_args = {}
        self.custom_preset_file_path = 'rebook_preset.json'

        self.strvar_device = tk.StringVar()
        self.strvar_screen_unit = tk.StringVar()
        self.strvar_screen_width = tk.StringVar()
        self.strvar_screen_height = tk.StringVar()
        self.strvar_input_file_path = tk.StringVar()
        self.strvar_output_file_path = tk.StringVar()
        self.strvar_conversion_mode = tk.StringVar()
        
        self.strvar_command_args = tk.StringVar()
        self.strvar_current_preview_page_num = tk.StringVar()
        
        self.device_arg_name = '-dev'               # -dev <name>
        self.width_arg_name = '-w'                  # -w <width>[in|cm|s|t|p]
        self.height_arg_name = '-h'                 # -h <height>[in|cm|s|t|p|x]
        self.conversion_mode_arg_name = '-mode'     # -mode <mode>
        self.output_path_arg_name = '-o'            # -o <namefmt>
        self.output_pdf_suffix = '-output.pdf'
        self.screen_unit_prefix = '-screen_unit'

        # Parameters frame
        self.column_num_arg_name = '-col'            # -col <maxcol>
        self.resolution_multiplier_arg_name = '-dr'  # -dr <value>
        self.crop_margin_arg_name = '-cbox'          # -cbox[<pagelist>|u|-]
        self.crop_margin_left_arg_name = '-ml'
        self.crop_margin_top_arg_name = '-mt'
        self.crop_margin_right_arg_name = '-mr'
        self.crop_margin_bottom_arg_name = '-mb'
        self.dpi_arg_name = '-dpi'                   # -dpi <dpival>
        self.page_num_arg_name = '-p'                # -p <pagelist>
        self.fixed_font_size_arg_name = '-fs'        # -fs 0/-fs <font size>[+]
        self.ocr_arg_name = '-ocr'                   # -ocr-/-ocr t
        self.ocr_cpu_arg_name = '-nt'                # -nt -50/-nt <percentage>
        self.landscape_arg_name = '-ls'              # -ls[-][pagelist]
        self.linebreak_arg_name = '-ws'              # -ws <spacing>

        self.is_column_num_checked = tk.BooleanVar()
        self.is_resolution_multipler_checked = tk.BooleanVar()
        self.is_crop_margin_checked = tk.BooleanVar()
        self.is_dpi_checked = tk.BooleanVar()
        self.is_fixed_font_size_checked = tk.BooleanVar()
        self.is_ocr_cpu_limitation_checked = tk.BooleanVar()
        self.is_landscape_checked = tk.BooleanVar()
        self.is_smart_linebreak_checked = tk.BooleanVar()  # -ws 0.01~10

        self.strvar_column_num = tk.StringVar()
        self.strvar_resolution_multiplier = tk.StringVar()
        # self.strvar_crop_page_range = tk.StringVar()
        self.strvar_left_margin = tk.StringVar()
        self.strvar_top_margin = tk.StringVar()
        self.strvar_width_margin = tk.StringVar()
        self.strvar_height_margin = tk.StringVar()
        self.strvar_dpi = tk.StringVar()
        self.strvar_page_numbers = tk.StringVar()
        self.strvar_fixed_font_size = tk.StringVar()
        self.strvar_ocr_cpu_percentage = tk.StringVar()
        self.strvar_landscape_pages = tk.StringVar()      # 1,3,5-10
        self.strvar_linebreak_space = tk.StringVar()

        self.auto_straignten_arg_name = '-as'            # -as-/-as
        self.break_page_avoid_overlap_arg_name = '-bp'   # -bp-/-bp
        self.color_output_arg_name = '-c'                # -c-/-c
        self.native_pdf_arg_name = '-n'                  # -n-/-n
        self.right_to_left_arg_name = '-r'               # -r-/-r
        self.post_gs_arg_name = '-ppgs'                  # -ppgs-/-ppgs
        self.marked_source_arg_name = '-sm'              # -sm-/-sm
        self.reflow_text_arg_name = '-wrap'              # -wrap+/-wrap-
        self.erase_vertical_line_arg_name = '-evl'       # -evl 0/-evl 1
        self.erase_horizontal_line_arg_name = '-ehl'     # -ehl 0/-ehl 1
        self.fast_preview_arg_name = '-rt'               # -rt /-rt 0
        self.ign_small_defects_arg_name = '-de'          # -de 1.0/-de 1.5
        self.auto_crop_arg_name = '-ac'                  # -ac-/-ac

        self.is_autostraighten_checked = tk.BooleanVar()
        self.isBreakPage = tk.BooleanVar()
        self.is_coloroutput_checked = tk.BooleanVar()
        self.is_native_pdf_checked = tk.BooleanVar()
        self.is_right_to_left_checked = tk.BooleanVar()
        self.is_ghostscript_postprocessing_checked = tk.BooleanVar()
        self.isMarkedSrc = tk.BooleanVar()
        self.is_reflow_text_checked = tk.BooleanVar()
        self.is_erase_vertical_line_checked = tk.BooleanVar()
        self.is_erase_horizontal_line_checked = tk.BooleanVar()
        self.is_fast_preview_checked = tk.BooleanVar()
        self.isAvoidOverlap = tk.BooleanVar()
        self.is_ignore_small_defects_checked = tk.BooleanVar()
        self.is_autocrop_checked = tk.BooleanVar()

        self.preview_output_arg_name = '-bmp'
        self.preview_image_path = './k2pdfopt_out.png'

        self.default_var_map = {
            self.device_arg_name:                    ['Kindle 1-5'],
            self.screen_unit_prefix:                 ['Pixels'],
            self.width_arg_name:                     ['560'],
            self.height_arg_name:                    ['735'],
            self.conversion_mode_arg_name:           ['Default'],
            self.output_path_arg_name:               [''],

            self.column_num_arg_name:                [False, '2'],
            self.resolution_multiplier_arg_name:     [False, '1.0'],
            self.crop_margin_arg_name:               [
                                                        False,
                                                        # '',
                                                        '0.0',
                                                        '0.0',
                                                        '0.0',
                                                        '0.0',
                                                    ],
            self.dpi_arg_name:                       [False, '167'],
            self.page_num_arg_name:                  [''],
            self.fixed_font_size_arg_name:           [False, '12'],
            self.ocr_arg_name:                       [False, '50'],
            self.ocr_cpu_arg_name:                   [False, '50'],
            self.landscape_arg_name:                 [False, ''],
            self.linebreak_arg_name:                 [True, '0.200'],

            self.auto_straignten_arg_name:           [False],
            self.break_page_avoid_overlap_arg_name:  [False, False],
            self.color_output_arg_name:              [False],
            self.native_pdf_arg_name:                [False],
            self.right_to_left_arg_name:             [False],
            self.post_gs_arg_name:                   [False],
            self.marked_source_arg_name:             [False],
            self.reflow_text_arg_name:               [True],
            self.erase_vertical_line_arg_name:       [False],
            self.erase_horizontal_line_arg_name:     [False],
            self.fast_preview_arg_name:              [True],
            self.ign_small_defects_arg_name:         [False],
            self.auto_crop_arg_name:                 [False],

            self.preview_output_arg_name:            []
        }

        self.arg_var_map = {
            self.device_arg_name:                    [self.strvar_device],
            self.screen_unit_prefix:                 [self.strvar_screen_unit],
            self.width_arg_name:                     [self.strvar_screen_width],
            self.height_arg_name:                    [self.strvar_screen_height],
            self.conversion_mode_arg_name:           [self.strvar_conversion_mode],
            self.output_path_arg_name:               [self.strvar_output_file_path],

            self.column_num_arg_name:                [
                                                    self.is_column_num_checked,
                                                    self.strvar_column_num,
                                                ],
            self.resolution_multiplier_arg_name:     [
                                                    self.is_resolution_multipler_checked,
                                                    self.strvar_resolution_multiplier,
                                                ],
            self.crop_margin_arg_name:               [
                                                    self.is_crop_margin_checked,
                                                    # self.strvar_crop_page_range,
                                                    self.strvar_left_margin,
                                                    self.strvar_top_margin,
                                                    self.strvar_width_margin,
                                                    self.strvar_height_margin,
                                                ],
            self.dpi_arg_name:                       [
                                                    self.is_dpi_checked,
                                                    self.strvar_dpi,
                                                ],
            self.page_num_arg_name:                  [
                                                    self.strvar_page_numbers,
                                                ],

            self.fixed_font_size_arg_name:           [
                                                    self.is_fixed_font_size_checked,
                                                    self.strvar_fixed_font_size,
                                                ],
            self.ocr_arg_name:                       [
                                                    self.is_ocr_cpu_limitation_checked,
                                                    self.strvar_ocr_cpu_percentage,
                                                ],
            self.ocr_cpu_arg_name:                   [
                                                    self.is_ocr_cpu_limitation_checked,
                                                    self.strvar_ocr_cpu_percentage,
                                                ],
            self.landscape_arg_name:                 [
                                                    self.is_landscape_checked,
                                                    self.strvar_landscape_pages,
                                                ],
            self.linebreak_arg_name:            [
                                                    self.is_smart_linebreak_checked,
                                                    self.strvar_linebreak_space,
                                                ],

            self.auto_straignten_arg_name:           [self.is_autostraighten_checked],
            self.break_page_avoid_overlap_arg_name:  [self.isBreakPage, self.isAvoidOverlap],
            self.color_output_arg_name:              [self.is_coloroutput_checked],
            self.native_pdf_arg_name:                [self.is_native_pdf_checked],
            self.right_to_left_arg_name:             [self.is_right_to_left_checked],
            self.post_gs_arg_name:                   [self.is_ghostscript_postprocessing_checked],
            self.marked_source_arg_name:             [self.isMarkedSrc],
            self.reflow_text_arg_name:               [self.is_reflow_text_checked],
            self.erase_vertical_line_arg_name:       [self.is_erase_vertical_line_checked],
            self.erase_horizontal_line_arg_name:     [self.is_erase_horizontal_line_checked],
            self.fast_preview_arg_name:              [self.is_fast_preview_checked],
            # break_page_avoid_overlap_arg_name:  []
            self.ign_small_defects_arg_name:         [self.is_ignore_small_defects_checked],
            self.auto_crop_arg_name:                 [self.is_autocrop_checked],
            self.preview_output_arg_name:            []
        }

        self.current_preview_page_index = 0
        self.background_process = None
        self.background_future = None

        s = ttk.Style()
        s.configure('TLabelframe.Label', font=('arial', 14, 'bold'))

        self.create_menus()
        self.create_tabs()

        self.bool_var_list = [
            self.is_column_num_checked,
            self.is_resolution_multipler_checked,
            self.is_crop_margin_checked,
            self.is_dpi_checked,
            self.is_fixed_font_size_checked,
            self.is_ocr_cpu_limitation_checked,
            self.is_landscape_checked,
            self.is_smart_linebreak_checked,

            self.is_autostraighten_checked,
            self.isBreakPage,
            self.is_coloroutput_checked,
            self.is_native_pdf_checked,
            self.is_right_to_left_checked,
            self.is_ghostscript_postprocessing_checked,
            self.isMarkedSrc,
            self.is_reflow_text_checked,
            self.is_erase_vertical_line_checked,
            self.is_erase_horizontal_line_checked,
            self.is_fast_preview_checked,
            self.isAvoidOverlap,
            self.is_ignore_small_defects_checked,
            self.is_autocrop_checked,
        ]

        self.string_var_list = [
            self.strvar_input_file_path,
            self.strvar_device,
            self.strvar_conversion_mode,
            self.strvar_screen_unit,
            self.strvar_screen_width,
            self.strvar_screen_height,
            self.strvar_column_num,
            self.strvar_resolution_multiplier,
            # self.strvar_crop_page_range,
            self.strvar_left_margin,
            self.strvar_width_margin,
            self.strvar_top_margin,
            self.strvar_height_margin,
            self.strvar_dpi,
            self.strvar_page_numbers,

            self.strvar_fixed_font_size,
            self.strvar_ocr_cpu_percentage,
            self.strvar_landscape_pages,
            self.strvar_linebreak_space,

            self.strvar_current_preview_page_num,
            self.strvar_output_file_path,
            self.strvar_command_args,
        ]

        self.combo_box_list = [
            self.device_combobox,
            self.mode_combobox,
            self.unit_combobox,
        ]

        self.entry_list = [
            self.input_path_entry,
            self.output_path_entry,
            self.command_arguments_entry,
            self.page_number_entry,
            self.landscapepage_number_entry,
            self.current_preview_page_number_entry,
        ]

        # Prepare to run
        self.thread_loop = asyncio.get_event_loop()
        run_loop_thread = Thread(target=self.start_loop, args=(self.thread_loop,), daemon=True)
        run_loop_thread.start()
        
        if not self.load_custom_preset():
            self.restore_default_values()

        self.log_string('Current directory : ' + os.getcwd())

    def create_tabs(self):
        ''' Create 'Conversion' and 'Logs' ReBook's tabs '''
        self.notebook = ttk.Notebook(self.root)
        self.conversion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.conversion_tab, text='Conversion')
        self.logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text='Logs')
        self.notebook.pack(expand=1, fill='both')

        self.fill_conversion_tab()
        self.fill_logs_tab()

    def create_menus(self):
        ''' Create the menus for ReBook. '''
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        # File menu
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label="Open file…", command=self.gui_open_pdf_file)
        menu_file.add_command(label='About', command=self.gui_about_box)
        menu_file.add_command(label="Quit", command=self.root.quit)

        # Settings menu
        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_settings, label='Settings')
        menu_settings.add_command(label='Save current settings', command=self.on_click_save_preset)
        menu_settings.add_command(label='Load settings', command=self.gui_open_preset_file)
        menu_settings.add_command(label='Reset settings to default', command=self.restore_default_values)

        # Help menu
        menu_help = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_help, label='Help')
        menu_help.add_command(label="K2pdfopt website helppage", command=self.gui_open_helpwebpage)
        menu_help.add_command(label="K2pdfopt command line manual", command=self.gui_open_cli_manual)

    def gui_open_helpwebpage(self):
        webbrowser.open('https://willus.com/k2pdfopt/help/')

    def gui_open_cli_manual(self):
        webbrowser.open('https://www.willus.com/k2pdfopt/help/options.shtml')

    def fill_left_side_of_conversion_tab(self):
        self.conversion_tab_left_part_column_num = 0
        self.conversion_tab_left_part_line_num = -1
        self.setup_file_frame()
        self.setup_device_frame()
        self.setup_parameters_frame()

    def fill_right_side_of_conversion_tab(self):
        self.conversion_tab_right_part_column_num = 1
        self.conversion_tab_right_part_line_num = 0
        self.setup_information_frame()
        self.setup_action_frame()

    def fill_conversion_tab(self):
        self.fill_left_side_of_conversion_tab()
        self.fill_right_side_of_conversion_tab()
        
        self.conversion_tab.columnconfigure(
            self.conversion_tab_right_part_column_num,
            weight=1,
        )
        self.conversion_tab.rowconfigure(
            self.conversion_tab_right_part_line_num,
            weight=1,
        )
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.rowconfigure(self.action_frame_row_num, weight=1)

    def fill_logs_tab(self):
        self.stdout_frame = ttk.Labelframe(self.logs_tab, text='k2pdfopt STDOUT:')
        self.stdout_frame.pack(expand=1, fill='both')
        self.stdout_frame.columnconfigure(0, weight=1)
        self.stdout_frame.rowconfigure(1, weight=1)

        self.stdout_text = scrolledtext.ScrolledText(
            self.stdout_frame,
            state=tk.DISABLED,
            wrap='word'
        )
        self.stdout_text.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.clear_button = ttk.Button(
            self.stdout_frame,
            text='Clear',
            command=self.gui_clear_log
        )
        self.clear_button.grid(
            column=0,
            row=1,
            sticky=tk.N+tk.E,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def setup_information_frame(self):
        self.information_frame = ttk.Labelframe(self.conversion_tab, text='Command-line Options')
        self.information_frame.grid(
            column=self.conversion_tab_right_part_column_num,
            row=self.conversion_tab_right_part_line_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.command_arguments_entry = ttk.Entry(
            self.information_frame, 
            state='readonly', 
            textvariable=self.strvar_command_args,
            width=100
        )
        self.command_arguments_entry.bind('<Button-1>', self.gui_cmd_args)
        self.command_arguments_entry.grid(
            column=0,
            row=0,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx
        )

    def setup_file_frame(self):
        ''' Set up the file frame. '''
        self.conversion_tab_left_part_line_num += 1
        self.half_screen = int(self.root.width / 2) - 55
        self.file_frame = ttk.Labelframe(self.conversion_tab, text='Files', width=self.half_screen, height=78)
        self.file_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.file_frame.grid_propagate(False)

        file_frame_line_number = 0

        open_button = ttk.Button(
            self.file_frame, 
            text='Choose a File', 
            command=self.gui_open_pdf_file
        )
        open_button.grid(
            column=0,
            row=file_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.input_path_entry = ttk.Entry(
            self.file_frame, 
            state='readonly', 
            textvariable=self.strvar_input_file_path,
            width=35
        )
        self.input_path_entry.grid(
            column=1,
            row=file_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        file_frame_line_number += 1

        output_label = ttk.Label(self.file_frame, text='Output file path')
        output_label.grid(column=0, row=file_frame_line_number, sticky=tk.N+tk.W, pady=self.default_pady, padx=self.default_padx)
        self.output_path_entry = ttk.Entry(
            self.file_frame, 
            state='readonly', 
            textvariable=self.strvar_output_file_path,
            width=40
        )
        self.output_path_entry.grid(
            column=1,
            row=file_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx
        )

    def setup_device_frame(self):
        ''' Set up the device frame. '''
        self.conversion_tab_left_part_line_num += 1

        self.device_frame = ttk.Labelframe(self.conversion_tab, text='Device', width=self.half_screen, height=110)
        self.device_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.device_frame.grid_propagate(False)

        device_frame_line_number = 0

        device_label = ttk.Label(self.device_frame, text='Device')
        device_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.device_combobox = ttk.Combobox(
            self.device_frame,
            state='readonly',
            textvariable=self.strvar_device,
            width=25
        )
        self.device_combobox['values'] = list(self.device_choice_map.values())
        self.device_combobox.current(0)
        self.device_combobox.bind('<<ComboboxSelected>>', self.gui_device_unit_cbox)
        self.device_combobox.grid(
            column=1,
            columnspan=3,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        device_frame_line_number += 1

        self.unit_label = ttk.Label(self.device_frame, text='Unit')
        self.unit_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.unit_combobox = ttk.Combobox(
            self.device_frame, 
            state='readonly', 
            textvariable=self.strvar_screen_unit,
            width=20
        )
        self.unit_combobox['values'] = list(self.unit_choice_map.values())
        self.unit_combobox.current(0)
        self.unit_combobox.bind('<<ComboboxSelected>>', self.gui_device_unit_cbox)
        self.unit_combobox.grid(
            column=1,
            columnspan=3,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        device_frame_line_number += 1

        self.width_label = ttk.Label(self.device_frame, text='Width')
        self.width_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.width_spinbox = ttk.Spinbox(
            self.device_frame,
            from_=0,
            to=10000,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_screen_width,
            command=self.gui_width_height,
            width=6
        )
        self.width_spinbox.grid(
            column=1,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        # device_frame_line_number += 1

        self.height_label = ttk.Label(self.device_frame, text='Height')
        self.height_label.grid(
            column=2,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_spinbox = ttk.Spinbox(
            self.device_frame,
            from_=0,
            to=10000,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_screen_height,
            command=self.gui_width_height,
            width=6
        )
        self.height_spinbox.grid(
            column=3,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.dpi_check_button = ttk.Checkbutton(
            self.device_frame,
            text='DPI',
            variable=self.is_dpi_checked,
            command=self.gui_dpi,
        )
        self.dpi_check_button.grid(
            column=4,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.dpi_spinbox = ttk.Spinbox(
            self.device_frame,
            from_=0,
            to=1000,
            increment=1,
            state='readonly',
            textvariable=self.strvar_dpi,
            command=self.gui_dpi,
            width=6
        )
        self.dpi_spinbox.grid(
            column=5,
            row=device_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def setup_parameters_frame(self):
        ''' Set up the parameters frame. '''
        self.conversion_tab_left_part_line_num += 1

        self.parameters_frame = ttk.Labelframe(self.conversion_tab, text='Parameters & options', width=self.half_screen, height=593)
        self.parameters_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.parameters_frame.grid_propagate(False)

        parameters_frame_line_number = 0

        conversion_mode_label = ttk.Label(self.parameters_frame, text='Conversion Mode')
        conversion_mode_label.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.mode_combobox = ttk.Combobox(
            self.parameters_frame,
            state='readonly', 
            textvariable=self.strvar_conversion_mode,
            width=10
        )
        self.mode_combobox['values'] = list(self.mode_choice_map.values())
        self.mode_combobox.current(0)
        self.mode_combobox.bind('<<ComboboxSelected>>', self.gui_mode_cbox)
        self.mode_combobox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        page_number_label = ttk.Label(self.parameters_frame, text='Pages to Convert')
        page_number_label.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.page_number_entry = ttk.Entry(
            self.parameters_frame,
            textvariable=self.strvar_page_numbers,
            validate='focusout',
            validatecommand=self.validate_and_update_page_nums,
            width=13
        )
        self.page_number_entry.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.landscape_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Output in Landscape',
            variable=self.is_landscape_checked,
            command=self.gui_and_validate_landscape,
        )
        self.landscape_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.landscapepage_number_entry = ttk.Entry(
            self.parameters_frame,
            textvariable=self.strvar_landscape_pages,
            validate='focusout',
            validatecommand=self.gui_and_validate_landscape,
            width=13
        )
        self.landscapepage_number_entry.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.max_column_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Maximum Columns',
            variable=self.is_column_num_checked,
            command=self.gui_column_num,
        )
        self.max_column_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.max_column_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=1,
            to=10,
            increment=1,
            state='readonly',
            textvariable=self.strvar_column_num,
            command=self.gui_column_num,
            width=6
        )
        self.max_column_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.resolution_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Document Resolution Factor',
            variable=self.is_resolution_multipler_checked,
            command=self.gui_resolution_multipler,
        )
        self.resolution_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.resolution_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0.1,
            to=10.0,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_resolution_multiplier,
            command=self.gui_resolution_multipler,
            width=6
        )
        self.resolution_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.margin_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Crop Margins (in)',
            variable=self.is_crop_margin_checked,
            command=self.gui_crop_margin,
        )
        self.margin_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        # parameters_frame_line_number += 1

        # crop_page_range_label = ttk.Label(self.parameters_frame, text='      Page Range')
        # crop_page_range_label.grid(
        #     column=0,
        #     row=parameters_frame_line_number,
        #     sticky=tk.N+tk.W,
        #     pady=self.default_pady,
        #     padx=self.default_padx,
        # )

        # self.crop_page_range_entry = ttk.Entry(
        #     self.parameters_frame,
        #     textvariable=self.strvar_crop_page_range,
        #     validate='focusout',
        #     validatecommand=self.gui_crop_margin,
        #     width=13
        # )
        # self.crop_page_range_entry.grid(
        #     column=1,
        #     row=parameters_frame_line_number,
        #     sticky=tk.N+tk.W,
        #     pady=self.default_pady,
        #     padx=self.default_padx,
        # )

        parameters_frame_line_number += 1

        left_margin_label = ttk.Label(self.parameters_frame, text='      Left')
        left_margin_label.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.left_margin_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0,
            to=10,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_left_margin,
            command=self.gui_crop_margin,
            width=6
        )
        self.left_margin_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        top_margin_label = ttk.Label(self.parameters_frame, text='      Top')
        top_margin_label.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.top_margin_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0,
            to=10,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_top_margin,
            command=self.gui_crop_margin,
            width=6
        )
        self.top_margin_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        width_margin_textlabel = ttk.Label(self.parameters_frame, text='      Right')
        width_margin_textlabel.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.width_margin_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0,
            to=10,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_width_margin,
            command=self.gui_crop_margin,
            width=6
        )
        self.width_margin_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        height_margin_textlabel = ttk.Label(self.parameters_frame, text='      Bottom')
        height_margin_textlabel.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.height_margin_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0,
            to=10,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_height_margin,
            command=self.gui_crop_margin,
            width=6
        )
        self.height_margin_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        # checkbox with value options
        parameters_frame_line_number += 1

        self.fixed_font_size_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Fixed Output Font Size',
            variable=self.is_fixed_font_size_checked,
            command=self.gui_fixed_font_size,
        )
        self.fixed_font_size_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.fixed_font_size_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0,
            to=100,
            increment=1,
            state='readonly',
            textvariable=self.strvar_fixed_font_size,
            command=self.gui_fixed_font_size,
            width=6
        )
        self.fixed_font_size_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.ocr_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='OCR (Tesseract) CPU %',
            variable=self.is_ocr_cpu_limitation_checked,
            command=self.gui_ocr_and_cpu,
        )
        self.ocr_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.ocr_cpu_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0,
            to=100,
            increment=1,
            state='readonly',
            textvariable=self.strvar_ocr_cpu_percentage,
            command=self.gui_ocr_and_cpu,
            width=6
        )
        self.ocr_cpu_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.smart_line_break_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Smart Line Breaks',
            variable=self.is_smart_linebreak_checked,
            command=self.gui_line_break,
        )
        self.smart_line_break_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.smart_line_break_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=0.01,
            to=2.00,
            increment=0.01,
            state='readonly',
            textvariable=self.strvar_linebreak_space,
            command=self.gui_line_break,
            width=6
        )
        self.smart_line_break_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        option_frame_left_part_col_num = 0
        parameters_frame_line_number += 1
        save_parameters_frame_line_number = parameters_frame_line_number

        self.autostraighten_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Autostraighten',
            variable=self.is_autostraighten_checked,
            command=self.gui_auto_straighten,
        )
        self.autostraighten_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.break_after_source_page_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Break After Each Source Page',
            variable=self.isBreakPage,
            command=self.gui_break_page,
        )
        self.break_after_source_page_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.color_output_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Color Output',
            variable=self.is_coloroutput_checked,
            command=self.gui_color_output,
        )
        self.color_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.native_pdf_output_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Native PDF Output',
            variable=self.is_native_pdf_checked,
            command=self.gui_native_pdf,
        )
        self.native_pdf_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.right_to_left_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Right-to-Left Text',
            variable=self.is_right_to_left_checked,
            command=self.gui_right_to_left,
        )
        self.right_to_left_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.post_process_ghostscript_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Post Process w/GhostScript',
            variable=self.is_ghostscript_postprocessing_checked,
            command=self.gui_post_gs,
        )
        self.post_process_ghostscript_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.generate_markup_source_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Generate Marked-up Source',
            variable=self.isMarkedSrc,
            command=self.gui_marked_src,
        )
        self.generate_markup_source_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        option_frace_right_part_col_num = 1
        parameters_frame_line_number = save_parameters_frame_line_number

        self.reflow_text_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Re-flow Text',
            variable=self.is_reflow_text_checked,
            command=self.gui_reflow_text,
        )
        self.reflow_text_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.erase_vline_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Erase Vertical Lines',
            variable=self.is_erase_vertical_line_checked,
            command=self.gui_erase_vertical_line,
        )
        self.erase_vline_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.erase_hline_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Erase Horizontal Lines',
            variable=self.is_erase_horizontal_line_checked,
            command=self.gui_erase_horizontal_line,
        )
        self.erase_hline_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.fast_preview_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Fast Preview',
            variable=self.is_fast_preview_checked,
            command=self.gui_fast_preview,
        )
        self.fast_preview_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.avoid_text_overlap_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Avoid Text Selection Overlap',
            variable=self.isAvoidOverlap,
            command=self.gui_avoid_text_selection_overlap,
        )
        self.avoid_text_overlap_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.ignore_defect_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Ignore Small Defects',
            variable=self.is_ignore_small_defects_checked,
            command=self.gui_ignore_small_defect,
        )
        self.ignore_defect_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.autocrop_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text='Auto-Crop',
            variable=self.is_autocrop_checked,
            command=self.gui_auto_crop,
        )
        self.autocrop_check_button.grid(
            column=option_frace_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def setup_action_frame(self):
        ''' Set up the action frame. '''
        self.conversion_tab_right_part_line_num += 1

        self.action_frame = ttk.Labelframe(self.conversion_tab, text='Actions')
        self.action_frame.grid(
            column=self.conversion_tab_right_part_column_num,
            row=self.conversion_tab_right_part_line_num,
            rowspan=3,
            sticky=tk.N+tk.S+tk.E+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_row_num = 0

        self.preview_button = ttk.Button(
            self.action_frame, 
            text='Preview', 
            command=self.gui_ten_page_up
        )
        self.preview_button.grid(
            column=0,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.convert_button = ttk.Button(
            self.action_frame, 
            text='Convert', 
            command=self.gui_convert_pdf
        )
        self.convert_button.grid(
            column=1,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.cancel_button = ttk.Button(
            self.action_frame, 
            text='Abort', 
            command=self.gui_abort_conversion
        )
        self.cancel_button.grid(
            column=2,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_row_num += 1

        self.current_preview_page_number_entry = ttk.Entry(
            self.action_frame,
            state='readonly',
            textvariable=self.strvar_current_preview_page_num
        )
        self.current_preview_page_number_entry.grid(
            column=0,
            row=self.action_frame_row_num,
            columnspan=2,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_column_num = 0
        self.action_frame_row_num += 1

        self.first_button = ttk.Button(
            self.action_frame, 
            text='<<', 
            command=self.gui_ten_page_up
        )
        self.first_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.action_frame_column_num += 1

        self.previous_button = ttk.Button(
            self.action_frame, 
            text='<', 
            command=self.gui_page_up
        )
        self.previous_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.action_frame_column_num += 1

        self.next_button = ttk.Button(
            self.action_frame, 
            text='>', 
            command=self.gui_page_down
        )
        self.next_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.action_frame_column_num += 1

        self.last_button = ttk.Button(
            self.action_frame,
            text='>>',
            command=self.gui_ten_page_down
        )
        self.last_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_column_num += 1
        self.action_frame_row_num += 1

        self.preview_canvas = tk.Canvas(self.action_frame, bd=0)
        self.preview_canvas.grid(
            column=0,
            row=self.action_frame_row_num,
            columnspan=self.action_frame_column_num,
            sticky=tk.N+tk.S+tk.E+tk.W,
        )

        x_scrollbar = ttk.Scrollbar(self.action_frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview)
        x_scrollbar.grid(
            column=0,
            row=self.action_frame_row_num+1,
            columnspan=self.action_frame_column_num,
            sticky=tk.E+tk.W,
        )

        y_scrollbar = ttk.Scrollbar(self.action_frame, command=self.preview_canvas.yview)
        y_scrollbar.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N+tk.S,
        )

        self.preview_canvas.configure(xscrollcommand=x_scrollbar.set)
        self.preview_canvas.configure(yscrollcommand=y_scrollbar.set)
        self.preview_canvas.bind('<MouseWheel>', self.yscroll_canvas)
        self.preview_canvas.bind("<Shift-MouseWheel>", self.xscroll_canvas)

    def initialize(self):
        ''' Simulate a click on every field : execute all the binded method. '''
        self.gui_device_unit_cbox()
        self.gui_mode_cbox()
        self.gui_width_height()
        self.gui_column_num()
        self.gui_resolution_multipler()
        self.gui_crop_margin()
        self.gui_dpi()
        self.validate_and_update_page_nums()
        self.gui_fixed_font_size()
        self.gui_ocr_and_cpu()
        self.gui_and_validate_landscape()
        self.gui_line_break()
        self.gui_auto_straighten()
        self.gui_break_page()
        self.gui_color_output()
        self.gui_native_pdf()
        self.gui_right_to_left()
        self.gui_post_gs()
        self.gui_marked_src()
        self.gui_reflow_text()
        self.gui_erase_vertical_line()
        self.gui_erase_horizontal_line()
        self.gui_fast_preview()
        self.gui_ignore_small_defect()
        self.gui_auto_crop()

    def initialize_vars(self, dict_vars):
        ''' Initialize variables from a dictionnary and build the associated command line. '''
        for key, value in dict_vars.items():
            for i in range(len(value)):
                self.arg_var_map[key][i].set(value[i])
        self.initialize()
        self.update_command_argument_entry_strvar()

    def create_widgets(self):
        pass

    # Command management methods
    def remove_command_argument(self, arg_key):
        ''' Removing argument from k2pdfopt command line. '''
        self.k2pdfopt_cmd_args.pop(arg_key, None)

    def add_or_update_command_argument(self, arg_key, arg_value):
        ''' Add or update argument to k2pdfopt command line. '''
        self.k2pdfopt_cmd_args[arg_key] = arg_value
        self.update_command_argument_entry_strvar()

    def update_command_argument_entry_strvar(self):
        self.strvar_command_args.set(self.generate_command_argument_string())

    def generate_command_argument_string(self):
        ''' Transforms the dictionary `k2pdfopt_cmd_args` into a command line arguments list.

            Remarks: at the end, the chosen argument are completed by `mandatory` arguments
                    ('-a- -ui- -x').
        '''
        device_arg = self.k2pdfopt_cmd_args.pop(self.device_arg_name, None)
        if device_arg is None:
            width_arg = self.k2pdfopt_cmd_args.pop(self.width_arg_name, None)
            height_arg = self.k2pdfopt_cmd_args.pop(self.height_arg_name, None)

        mode_arg = self.k2pdfopt_cmd_args.pop(self.conversion_mode_arg_name, None)
        if mode_arg is not None:
            arg_list = [mode_arg]  + list(self.k2pdfopt_cmd_args.values())
            self.k2pdfopt_cmd_args[self.conversion_mode_arg_name] = mode_arg
        else:
            arg_list = list(self.k2pdfopt_cmd_args.values())

        if device_arg is not None:
            arg_list.append(device_arg)
            self.k2pdfopt_cmd_args[self.device_arg_name] = device_arg
        elif width_arg is not None and height_arg is not None:
            arg_list.append(width_arg)
            arg_list.append(height_arg)
            self.k2pdfopt_cmd_args[self.width_arg_name] = width_arg
            self.k2pdfopt_cmd_args[self.height_arg_name] = height_arg

        arg_list.append('-a- -ui- -x')
        self.log_string('Generate Argument List: ' + str(arg_list))
        cmd_arg_str = ' '.join(arg_list)
        return cmd_arg_str

    def gui_about_box(self):
        about_message = \
            '''ReBook 2 ßeta

                TclTk GUI for k2pdfopt
                Largely based on
                Pu Wang's rebook.

                The source code can be found at:
                 - rebook: http://github.com/pwang7/rebook/
                 - ReBook2: https://github.com/R-e-d-J/rebook/'''

        messagebox.showinfo(message=about_message)

    def gui_open_pdf_file(self):
        ''' Select a PDF/DJVU file and generate output path '''
        supported_formats = [('PDF files', '*.pdf'), ('DJVU files', '*.djvu')]
        filename = filedialog.askopenfilename(
            filetypes=supported_formats,
            title='Select your file',
        )
        if filename is not None and len(filename.strip()) > 0:
            self.strvar_input_file_path.set(filename)
            (base_path, file_ext) = os.path.splitext(filename)
            self.strvar_output_file_path.set(base_path + '_k2opt.pdf')

    def on_click_save_preset(self):
        ''' Save the current present into a json file for next use. '''
        filename = filedialog.asksaveasfilename()
        if filename is not None and len(filename.strip()) > 0:
            filename += '.json'
            with open(filename, 'w') as preset_file:
                dict_to_save = {}
                for key, value in self.arg_var_map.items():
                    if(key != self.output_path_arg_name):
                        dict_to_save[key] = [var.get() for var in value]
                json.dump(dict_to_save, preset_file)

    def gui_open_preset_file(self):
        supported_formats = [('JSON files', '*.json'),]
        filename = filedialog.askopenfilename(
            filetypes=supported_formats,
            title='Select your preset file',
        )
        if filename is not None and len(filename.strip()) > 0:
            self.load_custom_preset(filename)

    def gui_device_unit_cbox(self, e=None):
        self.update_device_unit_width_height()

    def gui_width_height(self):
        self.update_device_unit_width_height()

    def update_device_unit_width_height(self):
        if self.device_combobox.current() != 20:  # non-other type
            # self.unit_label.grid_remove()
            # self.width_label.grid_remove()
            # self.height_label.grid_remove()
            # self.unit_combobox.grid_remove()
            # self.width_spinbox.grid_remove()
            # self.height_spinbox.grid_remove()
            device_type = self.device_argument_map[self.device_combobox.current()]
            arg = self.device_arg_name + ' ' + device_type
            self.add_or_update_command_argument(self.device_arg_name, arg)
            self.remove_command_argument(self.width_arg_name)
            self.remove_command_argument(self.height_arg_name)
        else:   # "Other type" chosen
            # self.unit_label.grid()
            # self.width_label.grid()
            # self.height_label.grid()
            # self.unit_combobox.grid()
            # self.width_spinbox.grid()
            # self.height_spinbox.grid()
            screen_unit = self.unit_argument_map[self.unit_combobox.current()]
            width_arg = (self.width_arg_name + ' ' + self.strvar_screen_width.get().strip() + screen_unit)
            self.add_or_update_command_argument(self.width_arg_name, width_arg)
            height_arg = (self.height_arg_name + ' ' + self.strvar_screen_height.get().strip() + screen_unit)
            self.add_or_update_command_argument(self.height_arg_name, height_arg)
            self.remove_command_argument(self.device_arg_name)

    def gui_mode_cbox(self, e=None):
        conversion_mode = self.mode_argument_map[self.mode_combobox.current()]
        arg = (self.conversion_mode_arg_name + ' ' + conversion_mode)
        self.add_or_update_command_argument(self.conversion_mode_arg_name, arg)

    def gui_cmd_args(self, e=None):
        self.update_command_argument_entry_strvar()

    def gui_column_num(self):
        if self.is_column_num_checked.get():
            arg = (self.column_num_arg_name + ' ' + self.strvar_column_num.get().strip())
            self.add_or_update_command_argument(self.column_num_arg_name, arg)
        else:
            self.remove_command_argument(self.column_num_arg_name)

    def gui_resolution_multipler(self):
        if self.is_resolution_multipler_checked.get():
            arg = (
                self.resolution_multiplier_arg_name + ' ' +
                self.strvar_resolution_multiplier.get().strip()
            )
            self.add_or_update_command_argument(self.resolution_multiplier_arg_name, arg)
        else:
            self.remove_command_argument(self.resolution_multiplier_arg_name)

    def gui_crop_margin(self):
        '''
        
            Remarks:
                - conflict with Auto-Crop option
        '''
        # if (len(self.strvar_crop_page_range.get().strip()) > 0 and
        #         not tools.check_page_nums(self.strvar_crop_page_range.get().strip())):
        #     self.remove_command_argument(self.crop_margin_arg_name)
        #     self.remove_command_argument(self.crop_margin_left_arg_name)
        #     self.remove_command_argument(self.crop_margin_top_arg_name)
        #     self.remove_command_argument(self.crop_margin_right_arg_name)
        #     self.remove_command_argument(self.crop_margin_bottom_arg_name)
        #     self.strvar_crop_page_range.set('')

        #     messagebox.showerror(
        #         message='Invalide Crop Page Range. It should be like : 2-5e,3-7o,9-'
        #     )

        #     return False

        if self.is_crop_margin_checked.get():
            self.is_autocrop_checked.set(False)
            self.remove_command_argument(self.auto_crop_arg_name)
            # page_range_arg = self.strvar_crop_page_range.get().strip()

            if len(self.strvar_left_margin.get().strip()) > 0:
                arg = self.crop_margin_left_arg_name + ' ' + self.strvar_left_margin.get().strip()
                self.add_or_update_command_argument(self.crop_margin_left_arg_name, arg)

            if len(self.strvar_top_margin.get().strip()) > 0:
                arg = self.crop_margin_top_arg_name + ' ' + self.strvar_top_margin.get().strip()
                self.add_or_update_command_argument(self.crop_margin_top_arg_name, arg)

            if len(self.strvar_width_margin.get().strip()) > 0:
                arg = self.crop_margin_right_arg_name + ' ' + self.strvar_width_margin.get().strip()
                self.add_or_update_command_argument(self.crop_margin_right_arg_name, arg)

            if len(self.strvar_height_margin.get().strip()) > 0:
                arg = self.crop_margin_bottom_arg_name + ' ' + self.strvar_height_margin.get().strip()
                self.add_or_update_command_argument(self.crop_margin_bottom_arg_name, arg)
        else:
            self.remove_command_argument(self.crop_margin_arg_name)
            self.remove_command_argument(self.crop_margin_left_arg_name)
            self.remove_command_argument(self.crop_margin_top_arg_name)
            self.remove_command_argument(self.crop_margin_right_arg_name)
            self.remove_command_argument(self.crop_margin_bottom_arg_name)

    # def gui_and_validate_cropbox(self):
    #     if (len(self.strvar_crop_page_range.get().strip()) > 0 and
    #             not tools.check_page_nums(self.strvar_crop_page_range.get().strip())):
    #         self.remove_command_argument(self.crop_margin_arg_name)
    #         self.strvar_crop_page_range.set('')

    #         messagebox.showerror(
    #             message='Invalide Crop Page Range. It should be like : 2-5e,3-7o,9-'
    #         )

    #         return False

    #     if self.is_crop_margin_checked.get():
    #         page_range_arg = self.strvar_crop_page_range.get().strip()
    #         margin_args = [
    #             self.strvar_left_margin.get(),
    #             self.strvar_top_margin.get(),
    #             self.strvar_width_margin.get(),
    #             self.strvar_height_margin.get(),
    #         ]
    #         arg = (
    #             # no space between -cbox and page range
    #             self.crop_margin_arg_name + page_range_arg + ' '
    #             + 'in,' . join(map(str.strip, margin_args)) + 'in'
    #         )
    #         self.add_or_update_command_argument(self.crop_margin_arg_name, arg)
    #     else:
    #         self.remove_command_argument(self.crop_margin_arg_name)

    def gui_dpi(self):
        if self.is_dpi_checked.get():
            arg = self.dpi_arg_name + ' ' + self.strvar_dpi.get().strip()
            self.add_or_update_command_argument(self.dpi_arg_name, arg)
        else:
            self.remove_command_argument(self.dpi_arg_name)

    def validate_and_update_page_nums(self):
        if (len(self.strvar_page_numbers.get().strip()) > 0 and
                not tools.check_page_nums(self.strvar_page_numbers.get().strip())):

            self.remove_command_argument(self.page_num_arg_name)
            self.strvar_page_numbers.set('')
            messagebox.showerror(
                message='Invalide Page Argument. It should be like: 2-5e,3-7o,9-'
            )
            return False

        if len(self.strvar_page_numbers.get().strip()) > 0:
            arg = self.page_num_arg_name + ' ' + self.strvar_page_numbers.get().strip()
            self.add_or_update_command_argument(self.page_num_arg_name, arg)
        else:
            self.remove_command_argument(self.page_num_arg_name)

        return True

    def gui_fixed_font_size(self):
        if self.is_fixed_font_size_checked.get():
            arg = (self.fixed_font_size_arg_name + ' ' + self.strvar_fixed_font_size.get().strip())
            self.add_or_update_command_argument(self.fixed_font_size_arg_name, arg)
        else:
            self.remove_command_argument(self.fixed_font_size_arg_name)


    def gui_ocr_and_cpu(self):
        ''' OCR CPU pourcentage management

            Remarks: 
                - ocr conflicts with native pdf
                - negtive integer means percentage
        '''
        if self.is_ocr_cpu_limitation_checked.get():
            self.is_native_pdf_checked.set(False) 
            self.remove_command_argument(self.native_pdf_arg_name)
            self.add_or_update_command_argument(self.ocr_arg_name, self.ocr_arg_name)
            ocr_cpu_arg = (self.ocr_cpu_arg_name + '-' + self.strvar_ocr_cpu_percentage.get().strip())
            self.add_or_update_command_argument(self.ocr_cpu_arg_name, ocr_cpu_arg)
        else:
            self.remove_command_argument(self.ocr_arg_name)
            self.remove_command_argument(self.ocr_cpu_arg_name)

    def gui_and_validate_landscape(self):
        if (len(self.strvar_landscape_pages.get().strip()) > 0 and
            not tools.check_page_nums(self.strvar_landscape_pages.get().strip())):

            self.remove_command_argument(self.landscape_arg_name)
            self.strvar_landscape_pages.set('')
            messagebox.showerror(message='Invalide `Output in Landscape` Page Argument!')

            return False

        if self.is_landscape_checked.get():
            arg = '-ls'
            if len(self.strvar_landscape_pages.get().strip()) > 0:
                # no space between -ls and page numbers
                arg += self.strvar_landscape_pages.get().strip()
            self.add_or_update_command_argument(self.landscape_arg_name, arg)
        else:
            self.remove_command_argument(self.landscape_arg_name)

        return True

    def gui_line_break(self):
        if self.is_smart_linebreak_checked.get():
            arg = (self.linebreak_arg_name + ' ' + self.strvar_linebreak_space.get().strip())
            self.add_or_update_command_argument(self.linebreak_arg_name, arg)
        else:
            self.remove_command_argument(self.linebreak_arg_name)

    def gui_auto_straighten(self):
        if self.is_autostraighten_checked.get():
            self.add_or_update_command_argument(self.auto_straignten_arg_name, self.auto_straignten_arg_name)
        else:
            self.remove_command_argument(self.auto_straignten_arg_name)

    def gui_break_page(self):
        ''' Native PDF management
        
            Remarks : break page conflicts with avoid overlap since they are both -bp flag
        '''
        if self.isBreakPage.get():
            self.isAvoidOverlap.set(False)
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)
            self.add_or_update_command_argument(self.break_page_avoid_overlap_arg_name, self.break_page_avoid_overlap_arg_name)
        else:
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)

    def gui_color_output(self):
        if self.is_coloroutput_checked.get():
            self.add_or_update_command_argument(self.color_output_arg_name, self.color_output_arg_name)
        else:
            self.remove_command_argument(self.color_output_arg_name)

    def gui_native_pdf(self):
        ''' Manage `Native PDF`option.
        
            Remarks : native pdf conflicts with 'ocr' and 'reflow text'
        '''
        if self.is_native_pdf_checked.get():
            self.is_reflow_text_checked.set(False)
            self.is_ocr_cpu_limitation_checked.set(False)
            self.remove_command_argument(self.ocr_arg_name)
            self.remove_command_argument(self.ocr_cpu_arg_name)
            self.remove_command_argument(self.reflow_text_arg_name)
            self.add_or_update_command_argument(self.native_pdf_arg_name, self.native_pdf_arg_name)
        else:
            self.remove_command_argument(self.native_pdf_arg_name)

    def gui_right_to_left(self):
        if self.is_right_to_left_checked.get():
            self.add_or_update_command_argument(self.right_to_left_arg_name, self.right_to_left_arg_name)
        else:
            self.remove_command_argument(self.right_to_left_arg_name)

    def gui_post_gs(self):
        if self.is_ghostscript_postprocessing_checked.get():
            self.add_or_update_command_argument(self.post_gs_arg_name, self.post_gs_arg_name)
        else:
            self.remove_command_argument(self.post_gs_arg_name)

    def gui_marked_src(self):
        if self.isMarkedSrc.get():
            self.add_or_update_command_argument(self.marked_source_arg_name, self.marked_source_arg_name)
        else:
            self.remove_command_argument(self.marked_source_arg_name)

    def gui_reflow_text(self):
        if self.is_reflow_text_checked.get():
            self.is_native_pdf_checked.set(False)  # reflow text conflicts with native pdf
            self.remove_command_argument(self.native_pdf_arg_name)
            arg = self.reflow_text_arg_name + '+'
            self.add_or_update_command_argument(self.reflow_text_arg_name, arg)
        else:
            self.remove_command_argument(self.reflow_text_arg_name)

    def gui_erase_vertical_line(self):
        ''' Manage `Erase vertical line` option '''
        if self.is_erase_vertical_line_checked.get():
            arg = self.erase_vertical_line_arg_name + ' 1'
            self.add_or_update_command_argument(self.erase_vertical_line_arg_name, arg)
        else:
            self.remove_command_argument(self.erase_vertical_line_arg_name)

    def gui_fast_preview(self):
        ''' Manage fast preview option.'''
        if self.is_fast_preview_checked.get():
            arg = self.fast_preview_arg_name + ' 0'
            self.add_or_update_command_argument(self.fast_preview_arg_name, arg)
        else:
            self.remove_command_argument(self.fast_preview_arg_name)

    def gui_avoid_text_selection_overlap(self):
        ''' Manage avoid text selection overlap. '''
        if self.isAvoidOverlap.get():
            # avoid overlap conflicts with break page since they are both -bp flag
            self.isBreakPage.set(False)
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)

            arg = self.break_page_avoid_overlap_arg_name + ' m'
            self.add_or_update_command_argument(self.break_page_avoid_overlap_arg_name, arg)
        else:
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)

    def gui_ignore_small_defect(self):
        ''' Manage `ignore small defect` option. '''
        if self.is_ignore_small_defects_checked.get():
            arg = (self.ign_small_defects_arg_name + ' 1.5')
            self.add_or_update_command_argument(self.ign_small_defects_arg_name, arg)
        else:
            self.remove_command_argument(self.ign_small_defects_arg_name)

    def gui_erase_horizontal_line(self):
        ''' Manage `Erase horizontal line` option '''
        if self.is_erase_horizontal_line_checked.get():
            arg = self.erase_horizontal_line_arg_name + ' 1'
            self.add_or_update_command_argument(self.erase_horizontal_line_arg_name, arg)
        else:
            self.remove_command_argument(self.erase_horizontal_line_arg_name)

    def gui_auto_crop(self):
        ''' Manage autocrop option.
        
            Remarks:
                - conflict with crop margin
        '''
        if self.is_autocrop_checked.get():
            self.is_crop_margin_checked.set(False)
            self.remove_command_argument(self.crop_margin_arg_name)
            self.remove_command_argument(self.crop_margin_left_arg_name)
            self.remove_command_argument(self.crop_margin_top_arg_name)
            self.remove_command_argument(self.crop_margin_right_arg_name)
            self.remove_command_argument(self.crop_margin_bottom_arg_name)
            arg = self.auto_crop_arg_name
            self.add_or_update_command_argument(self.auto_crop_arg_name, arg)
        else:
            self.remove_command_argument(self.auto_crop_arg_name)

    def remove_preview_image_and_clear_canvas(self):
        if os.path.exists(self.preview_image_path):
            os.remove(self.preview_image_path)
        self.preview_canvas.delete(tk.ALL)
        self.canvas_image_tag = None

    def load_preview_image(self, img_path, preview_page_index):
        if os.path.exists(img_path):
            image = Image.open(img_path)
            image = image.resize((750, 1061), Image.ANTIALIAS)
            self.preview_image = ImageTk.PhotoImage(image)
            self.canvas_image_tag = self.preview_canvas.create_image(
                (0, 0),
                anchor=tk.NW,
                image=self.preview_image,
                tags='preview',
            )
            self.preview_canvas.config(
                scrollregion=(
                    0,
                    0,
                    self.preview_image.width(),
                    self.preview_image.height(),
                ),
            )
            self.strvar_current_preview_page_num.set('Page: ' + str(preview_page_index))
        else:
            self.strvar_current_preview_page_num.set('No Page: ' + str(preview_page_index))

    def generate_one_preview_image(self, preview_page_index):
        ''' Generate the images previews. '''
        if not self.pdf_conversion_is_done():
            return

        if not os.path.exists(self.strvar_input_file_path.get().strip()):
            messagebox.showerror(
                message=(
                    "Failed to Find Input PDF File to convert for Preview: %s"
                    %
                    self.strvar_input_file_path.get().strip()
                ),
            )
            return

        self.remove_preview_image_and_clear_canvas()
        (base_path, file_ext) = os.path.splitext(self.strvar_input_file_path.get().strip())
        output_arg = ' '.join([self.preview_output_arg_name, str(preview_page_index)])
        self.background_future = self.convert_pdf_file(output_arg)
        self.strvar_current_preview_page_num.set('Preview Generating...')

        def preview_image_future(bgf):
            self.load_preview_image(self.preview_image_path, preview_page_index)
            self.log_string(
                "Preview generation for page %d finished" %
                preview_page_index
            )

        self.background_future.add_done_callback(preview_image_future)

    def gui_restore_default(self):
        ''' Restore all the default value (even if preset was defined). '''
        self.restore_default_values()

    def gui_abort_conversion(self):
        ''' Abord the process of the preview/conversion. '''
        if self.background_future is not None:
            self.background_future.cancel()
        if (self.background_process is not None and self.background_process.returncode is None):
            self.background_process.terminate()

    def gui_convert_pdf(self):
        if not self.pdf_conversion_is_done():
            return
        pdf_output_arg = self.output_path_arg_name + ' %s' + self.output_pdf_suffix
        self.background_future = self.convert_pdf_file(pdf_output_arg)

    def gui_ten_page_up(self):
        self.current_preview_page_index -= 10
        if self.current_preview_page_index < 1:
            self.current_preview_page_index = 1
        self.generate_one_preview_image(self.current_preview_page_index)

    def gui_page_up(self):
        if self.current_preview_page_index > 1:
            self.current_preview_page_index -= 1
        self.generate_one_preview_image(self.current_preview_page_index)

    def gui_page_down(self):
        self.current_preview_page_index += 1
        self.generate_one_preview_image(self.current_preview_page_index)

    def gui_ten_page_down(self):
        self.current_preview_page_index += 10
        self.generate_one_preview_image(self.current_preview_page_index)

    def yscroll_canvas(self, event):
        self.preview_canvas.yview_scroll(-1 * event.delta, 'units')

    def xscroll_canvas(self, event):
        self.preview_canvas.xview_scroll(-1 * event.delta, 'units')

    def gui_clear_log(self):
        self.clear_logs()

    def pdf_conversion_is_done(self):
        ''' Check if the PDF conversion is already done or not. '''
        if (self.background_future is None) or (self.background_future.done()):
            if ((self.background_process is None) or (self.background_process.returncode is not None)):
                return True

        messagebox.showerror(message='Background Conversion Not Finished Yet! Please Wait...')
        return False

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def convert_pdf_file(self, output_arg):
        ''' Convertion of the selected PDF file with chosen options. '''
        async def async_run_cmd_and_log(exec_cmd):
            executed = exec_cmd.strip()

            def log_bytes(log_btyes):
                self.log_string(log_btyes.decode('utf-8'))

            self.log_string(executed)

            p = await asyncio.create_subprocess_shell(
                executed,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self.background_process = p

            while True:
                line = await p.stdout.readline()
                log_bytes(line)

                if not line:
                    break

                if line == '' and p.returncode is not None:
                    break

        input_pdf_path = self.strvar_input_file_path.get().strip()

        # in case the file name contains space
        if ' ' in input_pdf_path:
            input_pdf_path = '\"' + input_pdf_path + '\"'

        executed = ' '.join([self.k2pdfopt_path, input_pdf_path, output_arg, self.generate_command_argument_string()])
        future = asyncio.run_coroutine_threadsafe(async_run_cmd_and_log(executed), self.thread_loop)

        return future

    def log_string(self, str_line):
        log_content = str_line.strip()

        if len(log_content) > 0:
            self.stdout_text.config(state=tk.NORMAL)
            self.stdout_text.insert(tk.END, log_content + '\n')
            self.stdout_text.config(state=tk.DISABLED)

    def clear_logs(self):
        self.stdout_text.config(state=tk.NORMAL)
        self.stdout_text.delete(1.0, tk.END)
        self.stdout_text.config(state=tk.DISABLED)

    def load_custom_preset(self, json_path_file=None):
        if json_path_file is None:
            json_path_file = self.custom_preset_file_path
        if os.path.exists(json_path_file):
            with open(json_path_file) as preset_file:
                dict_to_load = json.load(preset_file)

                if dict_to_load:
                    self.initialize_vars(dict_to_load)
                    return True

        return False

    def restore_default_values(self):
        '''
            Clear logs, preview and reset all the default values

            THINKING :
            1. Not sure the next 3 for loop are necessary
            2. Why erase input and output file path ?
            3. Why not restore with the custom preset ?
                or have another button to reload custom preset ?
        '''
        # for attribute, value in self.__dict__.items():
        #     print(attribute, "=", type(attribute))

        for sv in self.string_var_list:
            sv.set('')

        for bv in self.bool_var_list:
            bv.set(False)

        for b in self.combo_box_list:
            b.current(0)

        self.clear_logs()
        self.remove_preview_image_and_clear_canvas()
        self.initialize_vars(self.default_var_map)
    

class ReBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure_gui()

    def configure_gui(self):
        self.title('Rebook v2.0ß')
        self.width= self.winfo_screenwidth()
        self.height= self.winfo_screenheight()
        self.geometry('%dx%d' % (self.width, self.height))
        self.resizable(True, True)


def check_k2pdfopt_path_exists(k2pdfopt_path):
    if not os.path.exists(k2pdfopt_path):
        messagebox.showerror(
            message='Failed to find k2pdfopt, ' +
            'please put it under the same directory ' +
            'as rebook and then restart.'
        )
        quit()


if __name__ == "__main__":
    k2pdfopt_path = './k2pdfopt'
    check_k2pdfopt_path_exists(k2pdfopt_path)
    rebook = ReBook()
    frame = MainFrame(rebook, k2pdfopt_path)
    rebook.mainloop()