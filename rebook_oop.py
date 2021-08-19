from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
import asyncio
import json
import os

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
                        7: 'Concat',
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

    # bool_var_list = [
    #     is_column_num_checked,
    #     is_resolution_multipler_checked,
    #     is_crop_margin_checked,
    #     is_dpi_checked,
    #     is_fixed_font_size_checked,
    #     is_ocr_cpu_limitation_checked,
    #     is_landscape_checked,
    #     is_smart_linebreak_checked,

    #     is_autostraighten_checked,
    #     isBreakPage,
    #     is_coloroutput_checked,
    #     is_native_pdf_checked,
    #     is_right_to_left_checked,
    #     isPostGs,
    #     isMarkedSrc,
    #     is_reflow_text_checked,
    #     is_erase_vertical_line_checked,
    #     is_erase_horizontal_line_checked,
    #     is_fast_preview_checked,
    #     isAvoidOverlap,
    #     isIgnSmallDefects,
    #     is_autocrop_checked,
    # ]

    # string_var_list = [
    #     strvar_input_file_path,
    #     strvar_device,
    #     strvar_conversion_mode,
    #     strvar_screen_unit,
    #     strvar_screen_width,
    #     strvar_screen_height,
    #     strvar_column_num,
    #     strvar_resolution_multiplier,
    #     strvar_crop_page_range,
    #     strvar_left_margin,
    #     strvarRightMargin,
    #     strvar_top_margin,
    #     strvarBottomMargin,
    #     strvar_dpi,
    #     strvar_page_numbers,

    #     strvar_fixed_font_size,
    #     strvar_ocr_cpu_percentage,
    #     strvar_landscape_pages,
    #     strvar_linebreak_space,

    #     STRVAR_CURRENT_PREVIEW_PAGE_NUM,
    #     STRVAR_OUTPUT_FILE_PATH,
    #     STRVAR_COMMAND_ARGS,
    # ]

    # combo_box_list = [
    #     device_combobox,
    #     mode_combobox,
    #     unit_combobox,
    # ]

    # entry_list = [
    #     input_path_entry,
    #     output_path_entry,
    #     command_arguments_entry,
    #     page_number_entry,
    #     landscapepage_number_entry,
    #     current_preview_page_number_entry,
    # ]

    # default_var_map = {
    #     device_arg_name:                    ['Kindle 1-5'],
    #     screen_unit_prefix:                 ['Pixels'],
    #     width_arg_name:                     ['560'],
    #     height_arg_name:                    ['735'],
    #     conversion_mode_arg_name:           ['Default'],
    #     output_path_arg_name:               [''],

    #     column_num_arg_name:                [False, '2'],
    #     resolution_multiplier_arg_name:     [False, '1.0'],
    #     crop_margin_arg_name:               [
    #                                             False,
    #                                             '',
    #                                             '0.00',
    #                                             '0.00',
    #                                             '0.00',
    #                                             '0.00',
    #                                         ],
    #     dpi_arg_name:                       [False, '167'],
    #     page_num_arg_name:                  [''],
    #     fixed_font_size_arg_name:           [False, '12'],
    #     ocr_arg_name:                       [False, '50'],
    #     ocr_cpu_arg_name:                   [False, '50'],
    #     landscape_arg_name:                 [False, ''],
    #     linebreak_arg_name:                 [True, '0.200'],

    #     auto_straignten_arg_name:           [False],
    #     break_page_avoid_overlap_arg_name:  [False, False],
    #     color_output_arg_name:              [False],
    #     native_pdf_arg_name:                [False],
    #     right_to_left_arg_name:             [False],
    #     post_gs_arg_name:                   [False],
    #     marked_source_arg_name:             [False],
    #     reflow_text_arg_name:               [True],
    #     erase_vertical_line_arg_name:       [False],
    #     erase_horizontal_line_arg_name:     [False],
    #     fast_preview_arg_name:              [True],
    #     ign_small_defects_arg_name:         [False],
    #     auto_crop_arg_name:                 [False],

    #     preview_output_arg_name:            []
    # }

    # arg_var_map = {
    #     device_arg_name:                    [strvar_device],
    #     screen_unit_prefix:                 [strvar_screen_unit],
    #     width_arg_name:                     [strvar_screen_width],
    #     height_arg_name:                    [strvar_screen_height],
    #     conversion_mode_arg_name:           [strvar_conversion_mode],
    #     output_path_arg_name:               [STRVAR_OUTPUT_FILE_PATH],

    #     column_num_arg_name:                [
    #                                             is_column_num_checked,
    #                                             strvar_column_num,
    #                                         ],
    #     resolution_multiplier_arg_name:     [
    #                                             is_resolution_multipler_checked,
    #                                             strvar_resolution_multiplier,
    #                                         ],
    #     crop_margin_arg_name:               [
    #                                             is_crop_margin_checked,
    #                                             strvar_crop_page_range,
    #                                             strvar_left_margin,
    #                                             strvar_top_margin,
    #                                             strvarRightMargin,
    #                                             strvarBottomMargin,
    #                                         ],
    #     dpi_arg_name:                       [
    #                                             is_dpi_checked,
    #                                             strvar_dpi,
    #                                         ],
    #     page_num_arg_name:                  [
    #                                             strvar_page_numbers,
    #                                         ],

    #     fixed_font_size_arg_name:           [
    #                                             is_fixed_font_size_checked,
    #                                             strvar_fixed_font_size,
    #                                         ],
    #     ocr_arg_name:                       [
    #                                             is_ocr_cpu_limitation_checked,
    #                                             strvar_ocr_cpu_percentage,
    #                                         ],
    #     ocr_cpu_arg_name:                   [
    #                                             is_ocr_cpu_limitation_checked,
    #                                             strvar_ocr_cpu_percentage,
    #                                         ],
    #     landscape_arg_name:                 [
    #                                             is_landscape_checked,
    #                                             strvar_landscape_pages,
    #                                         ],
    #     linebreak_arg_name:                 [
    #                                             is_smart_linebreak_checked,
    #                                             strvar_linebreak_space,
    #                                         ],

    #     auto_straignten_arg_name:           [is_autostraighten_checked],
    #     break_page_avoid_overlap_arg_name:  [isBreakPage, isAvoidOverlap],
    #     color_output_arg_name:              [is_coloroutput_checked],
    #     native_pdf_arg_name:                [is_native_pdf_checked],
    #     right_to_left_arg_name:             [is_right_to_left_checked],
    #     post_gs_arg_name:                   [isPostGs],
    #     marked_source_arg_name:             [isMarkedSrc],
    #     reflow_text_arg_name:               [is_reflow_text_checked],
    #     erase_vertical_line_arg_name:       [is_erase_vertical_line_checked],
    #     erase_horizontal_line_arg_name:     [is_erase_horizontal_line_checked],
    #     fast_preview_arg_name:              [is_fast_preview_checked],
    #     # break_page_avoid_overlap_arg_name:  []
    #     ign_small_defects_arg_name:         [isIgnSmallDefects],
    #     auto_crop_arg_name:                 [is_autocrop_checked],
    #     preview_output_arg_name:            []
    # }

    # arg_cb_map = {
    #     device_arg_name:                   on_bind_event_device_unit_cb,
    #     width_arg_name:                    on_command_width_height_cb,
    #     height_arg_name:                   on_command_width_height_cb,
    #     conversion_mode_arg_name:          on_bind_event_mode_cb,
    #     output_path_arg_name:              None,

    #     column_num_arg_name:               on_command_column_num_cb,
    #     resolution_multiplier_arg_name:    on_command_resolution_multipler_cb,
    #     crop_margin_arg_name:              on_command_and_validate_crop_margin_cb,
    #     dpi_arg_name:                      on_command_dpi_cb,
    #     page_num_arg_name:                 on_validate_page_nums_cb,

    #     fixed_font_size_arg_name:          on_command_fixed_font_size_cb,
    #     ocr_arg_name:                      on_command_ocr_and_cpu_cb,
    #     ocr_cpu_arg_name:                  on_command_ocr_and_cpu_cb,
    #     landscape_arg_name:                on_command_and_validate_landscape_cb,
    #     linebreak_arg_name:                on_command_line_break_cb,

    #     auto_straignten_arg_name:          on_command_auto_straighten_cb,
    #     break_page_avoid_overlap_arg_name: on_command_break_page_cb,
    #     color_output_arg_name:             on_command_color_output_cb,
    #     native_pdf_arg_name:               on_command_native_pdf_cb,
    #     right_to_left_arg_name:            on_command_right_to_left_cb,
    #     post_gs_arg_name:                  on_command_post_gs_cb,
    #     marked_source_arg_name:            on_command_marked_src_cb,
    #     reflow_text_arg_name:              on_command_reflow_text_cb,
    #     erase_vertical_line_arg_name:      on_command_erase_vertical_line_cb,
    #     erase_horizontal_line_arg_name:    on_command_erase_horizontal_line_cb,
    #     fast_preview_arg_name:             on_command_fast_preview_cb,
    #     ign_small_defects_arg_name:        on_command_ign_small_defect_cb,
    #     auto_crop_arg_name:                on_command_auto_crop_cb,

    #     preview_output_arg_name:           None
    # }

    def __init__(self, container):
        super().__init__(container)
        self.root = container           # root of tkinter

        self.log_tab = None
        self.base_tab = None
        self.conversion_tab = None

        self.k2pdfopt_path = './k2pdfopt'
        self.k2pdfopt_cmd_args = {}

        thread_loop = asyncio.get_event_loop()
        run_loop_thread = Thread(target=self.start_loop, args=(thread_loop,), daemon=True)
        run_loop_thread.start()

        self.strvar_device = tk.StringVar()
        self.strvar_screen_unit = tk.StringVar()
        self.strvar_screen_width = tk.StringVar()
        self.strvar_screen_height = tk.StringVar()
        self.strvar_input_file_path = tk.StringVar()
        self.strvar_output_file_path = tk.StringVar()
        self.strvar_conversion_mode = tk.StringVar()

        self.stdout_text = None
        self.strvar_command_args = tk.StringVar()
        self.strvar_current_preview_page_num = tk.StringVar()
        
        self.device_arg_name = '-dev'            # -dev <name>
        self.width_arg_name = '-w'               # -w <width>[in|cm|s|t|p]
        self.height_arg_name = '-h'              # -h <height>[in|cm|s|t|p|x]
        self.conversion_mode_arg_name = '-mode'  # -mode <mode>
        self.output_path_arg_name = '-o'         # -o <namefmt>
        self.output_pdf_suffix = '-output.pdf'
        self.screen_unit_prefix = '-screen_unit'

        # Parameters frame
        self.column_num_arg_name = '-col'            # -col <maxcol>
        self.resolution_multiplier_arg_name = '-dr'  # -dr <value>
        self.crop_margin_arg_name = '-cbox'          # -cbox[<pagelist>|u|-]
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
        self.strvar_crop_page_range = tk.StringVar()
        self.strvar_left_margin = tk.StringVar()
        self.strvar_top_margin = tk.StringVar()
        self.strvarRightMargin = tk.StringVar()         # Must it be "width" ?
        self.strvarBottomMargin = tk.StringVar()        # Must if be "height" ?
        self.strvar_dpi = tk.StringVar()
        self.strvar_page_numbers = tk.StringVar()
        self.strvar_fixed_font_size = tk.StringVar()
        self.strvar_ocr_cpu_percentage = tk.StringVar()
        self.strvar_landscape_pages = tk.StringVar()      # 1,3,5-10
        self.strvar_linebreak_space = tk.StringVar()

        # Rigth par of GUI
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
        self.isPostGs = tk.BooleanVar()
        self.isMarkedSrc = tk.BooleanVar()
        self.is_reflow_text_checked = tk.BooleanVar()
        self.is_erase_vertical_line_checked = tk.BooleanVar()
        self.is_erase_horizontal_line_checked = tk.BooleanVar()
        self.is_fast_preview_checked = tk.BooleanVar()
        self.isAvoidOverlap = tk.BooleanVar()
        self.isIgnSmallDefects = tk.BooleanVar()
        self.is_autocrop_checked = tk.BooleanVar()

        # ############################################################################################### #
        # PREVIEW FRAME
        # ############################################################################################### #
        self.preview_output_arg_name = '-bmp'
        self.preview_image_path = './k2pdfopt_out.png'

        self.strvar_current_preview_page_num = None
        self.canvas_image_tag = None
        self.current_preview_page_index = 0
        self.background_future = None
        self.background_process = None

        self.create_tabs()
        self.create_menu()
        # self.create_widgets()
        conversion_tab_left_part_column_num = 0
        conversion_tab_left_part_row_num = 0

        self.required_input_frame = ttk.Labelframe(self.conversion_tab, text='Required Inputs')
        self.required_input_frame.grid(
            column=conversion_tab_left_part_column_num,
            row=conversion_tab_left_part_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        required_frame_row_num = 0

        self.input_path_entry = ttk.Entry(self.required_input_frame, state='readonly', textvariable=self.strvar_input_file_path)
        self.input_path_entry.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        open_button = ttk.Button(self.required_input_frame, text='Choose a File', command=self.on_command_open_pdf_file_cb)
        open_button.grid(
            column=1,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        required_frame_row_num += 1

        device_label = ttk.Label(self.required_input_frame, text='Device')
        device_label.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        self.device_combobox = ttk.Combobox(self.required_input_frame, state='readonly', textvariable=self.strvar_device)
        self.device_combobox['values'] = list(self.device_choice_map.values())
        self.device_combobox.current(0)
        self.device_combobox.bind('<<ComboboxSelected>>', self.on_bind_event_device_unit_cb)
        self.device_combobox.grid(
            column=1,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        required_frame_row_num += 1

        unit_label = ttk.Label(self.required_input_frame, text='Unit')
        unit_label.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        self.unit_combobox = ttk.Combobox(self.required_input_frame, state='readonly', textvariable=self.strvar_screen_unit)
        self.unit_combobox['values'] = list(self.unit_choice_map.values())
        self.unit_combobox.current(0)
        self.unit_combobox.bind('<<ComboboxSelected>>', self.on_bind_event_device_unit_cb)
        self.unit_combobox.grid(
            column=1,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        self.unit_combobox.configure(state='disabled')

        required_frame_row_num += 1

        width_label = ttk.Label(self.required_input_frame, text='Width')
        width_label.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        self.width_spinbox = ttk.Spinbox(
            self.required_input_frame,
            from_=0,
            to=10000,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_screen_width,
            command=self.on_command_width_height_cb,
        )
        self.width_spinbox.grid(
            column=1,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        self.width_spinbox.configure(state='disabled')

        required_frame_row_num += 1

        height_label = ttk.Label(self.required_input_frame, text='Height')
        height_label.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        self.height_spinbox = ttk.Spinbox(
            self.required_input_frame,
            from_=0,
            to=10000,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_screen_height,
            command=self.on_command_width_height_cb,
        )
        self.height_spinbox.grid(
            column=1,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        self.height_spinbox.configure(state='disabled')

        required_frame_row_num += 1

        conversion_mode_label = ttk.Label(self.required_input_frame, text='Conversion Mode')
        conversion_mode_label.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        mode_combobox = ttk.Combobox(self.required_input_frame, state='readonly', textvariable=self.strvar_conversion_mode)
        mode_combobox['values'] = list(self.mode_choice_map.values())
        mode_combobox.current(0)
        mode_combobox.bind('<<ComboboxSelected>>', self.on_bind_event_mode_cb)
        mode_combobox.grid(
            column=1,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        # ############################################################################################### #
        # INFORMATIONS FRAME
        # ############################################################################################### #
        conversion_tab_left_part_row_num += 1

        information_frame = ttk.Labelframe(self.conversion_tab, text='Related Informations')
        information_frame.grid(
            column=conversion_tab_left_part_column_num,
            row=conversion_tab_left_part_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        save_label = ttk.Label(information_frame, text='Save Current Setting as Preset')
        save_label.grid(column=0, row=0, sticky=tk.N+tk.W, pady=0, padx=5)

        self.save_button = ttk.Button(information_frame, text='Save', command=self.on_command_save_cb)
        self.save_button.grid(column=1, row=0, sticky=tk.N+tk.W, pady=0, padx=5)

        output_label = ttk.Label(information_frame, text='Output Pdf File Path')
        output_label.grid(column=0, row=1, sticky=tk.N+tk.W, pady=0, padx=5)

        self.output_path_entry = ttk.Entry(information_frame, state='readonly', textvariable=self.strvar_output_file_path)
        self.output_path_entry.grid(column=1, row=1, sticky=tk.N+tk.W, pady=0, padx=5)

        command_arguments_label = ttk.Label(information_frame, text='Command-line Options')
        command_arguments_label.grid(column=0, row=2, sticky=tk.N+tk.W, pady=0, padx=5)

        self.command_arguments_entry = ttk.Entry(information_frame, state='readonly', textvariable=self.strvar_command_args)
        self.command_arguments_entry.bind('<Button-1>', self.on_bind_event_cmd_args_cb)
        self.command_arguments_entry.grid(column=1, row=2, sticky=tk.N+tk.W, pady=0, padx=5)

        # ############################################################################################### #
        # PARAMETERS FRAME
        # ############################################################################################### #
        conversion_tab_left_part_row_num += 1

        parameters_frame = ttk.Labelframe(self.conversion_tab, text='Parameters')
        parameters_frame.grid(
            column=conversion_tab_left_part_column_num,
            row=conversion_tab_left_part_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number = 0

        max_column_check_button = ttk.Checkbutton(
            parameters_frame,
            text='Maximum Columns',
            variable=self.is_column_num_checked,
            command=self.on_command_column_num_cb,
        )
        max_column_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        max_column_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=1,
            to=10,
            increment=1,
            state='readonly',
            textvariable=self.strvar_column_num,
            command=self.on_command_column_num_cb,
        )
        max_column_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        resolution_check_button = ttk.Checkbutton(
            parameters_frame,
            text='Document Resolution Factor',
            variable=self.is_resolution_multipler_checked,
            command=self.on_command_resolution_multipler_cb,
        )
        resolution_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        resolution_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0.1,
            to=10.0,
            increment=0.1,
            state='readonly',
            textvariable=self.strvar_resolution_multiplier,
            command=self.on_command_resolution_multipler_cb,
        )
        resolution_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        margin_check_button = ttk.Checkbutton(
            parameters_frame,
            text='Crop Margins (in)',
            variable=self.is_crop_margin_checked,
            command=self.on_command_and_validate_crop_margin_cb,
        )
        margin_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        crop_page_range_label = ttk.Label(parameters_frame, text='      Page Range')
        crop_page_range_label.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        crop_page_range_entry = ttk.Entry(
            parameters_frame,
            textvariable=self.strvar_crop_page_range,
            validate='focusout',
            validatecommand=self.on_command_and_validate_crop_margin_cb,
        )
        crop_page_range_entry.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        left_margin_label = ttk.Label(parameters_frame, text='      Left Margin')
        left_margin_label.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        left_margin_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=100,
            increment=0.01,
            state='readonly',
            textvariable=self.strvar_left_margin,
            command=self.on_command_and_validate_crop_margin_cb,
        )
        left_margin_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        top_margin_label = ttk.Label(parameters_frame, text='      Top Margin')
        top_margin_label.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        top_margin_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=100,
            increment=0.01,
            state='readonly',
            textvariable=self.strvar_top_margin,
            command=self.on_command_and_validate_crop_margin_cb,
        )
        top_margin_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        rightMarginTextLabel = ttk.Label(parameters_frame, text='      Width')
        rightMarginTextLabel.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        rightMarginSpinBox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=100,
            increment=0.01,
            state='readonly',
            textvariable=self.strvarRightMargin,
            command=self.on_command_and_validate_crop_margin_cb,
        )
        rightMarginSpinBox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        bottomMarginTextLabel = ttk.Label(parameters_frame, text='      Height')
        bottomMarginTextLabel.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        bottomMarginSpinBox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=100,
            increment=0.01,
            state='readonly',
            textvariable=self.strvarBottomMargin,
            command=self.on_command_and_validate_crop_margin_cb,
        )
        bottomMarginSpinBox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        dpi_check_button = ttk.Checkbutton(
            parameters_frame,
            text='DPI',
            variable=self.is_dpi_checked,
            command=self.on_command_dpi_cb,
        )
        dpi_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        dpi_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=1000,
            increment=1,
            state='readonly',
            textvariable=self.strvar_dpi,
            command=self.on_command_dpi_cb,
        )
        dpi_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        page_number_label = ttk.Label(  parameters_frame, text='Pages to Convert')
        page_number_label.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        page_number_entry = ttk.Entry(
            parameters_frame,
            textvariable=self.strvar_page_numbers,
            validate='focusout',
            validatecommand=self.on_validate_page_nums_cb,
        )
        page_number_entry.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        # checkbox with value options
        parameters_frame_row_number += 1

        fixed_font_size_check_button = ttk.Checkbutton(
            parameters_frame,
            text='Fixed Output Font Size',
            variable=self.is_fixed_font_size_checked,
            command=self.on_command_fixed_font_size_cb,
        )
        fixed_font_size_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        fixed_font_size_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=100,
            increment=1,
            state='readonly',
            textvariable=self.strvar_fixed_font_size,
            command=self.on_command_fixed_font_size_cb,
        )
        fixed_font_size_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        ocr_check_button = ttk.Checkbutton(
            parameters_frame,
            text='OCR (Tesseract) and CPU %',
            variable=self.is_ocr_cpu_limitation_checked,
            command=self.on_command_ocr_and_cpu_cb,
        )
        ocr_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        ocr_cpu_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0,
            to=100,
            increment=1,
            state='readonly',
            textvariable=self.strvar_ocr_cpu_percentage,
            command=self.on_command_ocr_and_cpu_cb,
        )
        ocr_cpu_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        landscape_check_button = ttk.Checkbutton(
            parameters_frame,
            text='Output in Landscape',
            variable=self.is_landscape_checked,
            command=self.on_command_and_validate_landscape_cb,
        )
        landscape_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        landscapepage_number_entry = ttk.Entry(
            parameters_frame,
            textvariable=self.strvar_landscape_pages,
            validate='focusout',
            validatecommand=self.on_command_and_validate_landscape_cb,
        )
        landscapepage_number_entry.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        parameters_frame_row_number += 1

        smart_line_break_check_button = ttk.Checkbutton(
            parameters_frame,
            text='Smart Line Breaks',
            variable=self.is_smart_linebreak_checked,
            command=self.on_command_line_break_cb,
        )
        smart_line_break_check_button.grid(
            column=0,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        smart_line_break_spinbox = ttk.Spinbox(
            parameters_frame,
            from_=0.01,
            to=2.00,
            increment=0.01,
            state='readonly',
            textvariable=self.strvar_linebreak_space,
            command=self.on_command_line_break_cb,
        )
        smart_line_break_spinbox.grid(
            column=1,
            row=parameters_frame_row_number,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        # ############################################################################################### #
        # RIGHT SIDE OF CONVERSION TAB
        # ############################################################################################### #
        conversion_tab_right_part_column_num = 1
        conversion_tab_right_part_row_num = -1

        # ############################################################################################### #
        # OPTIONS FRAME
        # ############################################################################################### #
        conversion_tab_right_part_row_num += 1

        optionFrame = ttk.Labelframe(
            self.conversion_tab,
            text='Options',
        )
        optionFrame.grid(
            column=conversion_tab_right_part_column_num,
            row=conversion_tab_right_part_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        option_frame_left_part_col_num = 0
        option_frame_row_num = 0

        autostraighten_check_button = ttk.Checkbutton(
            optionFrame,
            text='Autostraighten',
            variable=self.is_autostraighten_checked,
            command=self.on_command_auto_straighten_cb,
        )
        autostraighten_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        break_after_source_page_check_button = ttk.Checkbutton(
            optionFrame,
            text='Break After Each Source Page',
            variable=self.isBreakPage,
            command=self.on_command_break_page_cb,
        )
        break_after_source_page_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        color_output_check_button = ttk.Checkbutton(
            optionFrame,
            text='Color Output',
            variable=self.is_coloroutput_checked,
            command=self.on_command_color_output_cb,
        )
        color_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        native_pdf_output_check_button = ttk.Checkbutton(
            optionFrame,
            text='Native PDF Output',
            variable=self.is_native_pdf_checked,
            command=self.on_command_native_pdf_cb,
        )
        native_pdf_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        right_to_left_check_button = ttk.Checkbutton(
            optionFrame,
            text='Right-to-Left Text',
            variable=self.is_right_to_left_checked,
            command=self.on_command_right_to_left_cb,
        )
        right_to_left_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        post_process_ghostscript_check_button = ttk.Checkbutton(
            optionFrame,
            text='Post Process w/GhostScript',
            variable=self.isPostGs,
            command=self.on_command_post_gs_cb,
        )
        post_process_ghostscript_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        generate_markup_source_check_button = ttk.Checkbutton(
            optionFrame,
            text='Generate Marked-up Source',
            variable=self.isMarkedSrc,
            command=self.on_command_marked_src_cb,
        )
        generate_markup_source_check_button.grid(
            column=option_frame_left_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        option_frace_right_part_col_num = 1
        option_frame_row_num = 0

        reflow_text_check_button = ttk.Checkbutton(
            optionFrame,
            text='Re-flow Text',
            variable=self.is_reflow_text_checked,
            command=self.on_command_reflow_text_cb,
        )
        reflow_text_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        erase_vline_check_button = ttk.Checkbutton(
            optionFrame,
            text='Erase Vertical Lines',
            variable=self.is_erase_vertical_line_checked,
            command=self.on_command_erase_vertical_line_cb,
        )
        erase_vline_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        erase_hline_check_button = ttk.Checkbutton(
            optionFrame,
            text='Erase Horizontal Lines',
            variable=self.is_erase_horizontal_line_checked,
            command=self.on_command_erase_horizontal_line_cb,
        )
        erase_hline_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        fast_preview_check_button = ttk.Checkbutton(
            optionFrame,
            text='Fast Preview',
            variable=self.is_fast_preview_checked,
            command=self.on_command_fast_preview_cb,
        )
        fast_preview_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        avoid_text_overlap_check_button = ttk.Checkbutton(
            optionFrame,
            text='Avoid Text Selection Overlap',
            variable=self.isAvoidOverlap,
            command=self.on_command_avoid_text_selection_overlap_cb,
        )
        avoid_text_overlap_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        ignore_defect_check_button = ttk.Checkbutton(
            optionFrame,
            text='Ignore Small Defects',
            variable=self.isIgnSmallDefects,
            command=self.on_command_ign_small_defect_cb,
        )
        ignore_defect_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        autocrop_check_button = ttk.Checkbutton(
            optionFrame,
            text='Auto-Crop',
            variable=self.is_autocrop_checked,
            command=self.on_command_auto_crop_cb,
        )
        autocrop_check_button.grid(
            column=option_frace_right_part_col_num,
            row=option_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        option_frame_row_num += 1

        # ############################################################################################### #
        # PREVIEW FRAME
        # ############################################################################################### #
        conversion_tab_right_part_row_num += 1

        preview_frame = ttk.Labelframe(self.conversion_tab, text='Preview & Convert')
        preview_frame.grid(
            column=conversion_tab_right_part_column_num,
            row=conversion_tab_right_part_row_num,
            rowspan=3,
            sticky=tk.N+tk.S+tk.E+tk.W,
            pady=0,
            padx=5,
        )

        preview_frame_row_num = 0

        reset_button = ttk.Button(preview_frame, text='Reset Default', command=self.on_command_restore_default_cb)
        reset_button.grid(
            column=0,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        cancel_button = ttk.Button(preview_frame, text='Abort', command=self.on_command_abort_conversion_cb)
        cancel_button.grid(
            column=1,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        convert_button = ttk.Button(preview_frame, text='Convert', command=self.on_command_convert_pdf_cb)
        convert_button.grid(
            column=2,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        preview_frame_row_num += 1

        current_preview_page_number_entry = ttk.Entry(
            preview_frame,
            state='readonly',
            textvariable=self.strvar_current_preview_page_num
        )
        current_preview_page_number_entry.grid(
            column=0,
            row=preview_frame_row_num,
            columnspan=2,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        preview_button = ttk.Button(preview_frame, text='Preview', command=self.on_command_ten_page_up_cb)
        preview_button.grid(
            column=2,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        preview_frame_column_num = 0
        preview_frame_row_num += 1

        first_button = ttk.Button(preview_frame, text='<<', command=self.on_command_ten_page_up_cb)
        first_button.grid(
            column=preview_frame_column_num,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        preview_frame_column_num += 1

        previous_button = ttk.Button(preview_frame, text='<', command=self.on_command_page_up_cb)
        previous_button.grid(
            column=preview_frame_column_num,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        preview_frame_column_num += 1

        next_button = ttk.Button(preview_frame, text='>', command=self.on_command_page_down_cb)
        next_button.grid(
            column=preview_frame_column_num,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )
        preview_frame_column_num += 1

        last_button = ttk.Button(preview_frame, text='>>', command=self.on_command_ten_page_down_cb)
        last_button.grid(
            column=preview_frame_column_num,
            row=preview_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        preview_frame_column_num += 1
        preview_frame_row_num += 1

        xScrollBar = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL)
        xScrollBar.grid(
            column=0,
            row=preview_frame_row_num+1,
            columnspan=preview_frame_column_num,
            sticky=tk.E+tk.W,
        )

        yScrollBar = ttk.Scrollbar(preview_frame)
        yScrollBar.grid(
            column=preview_frame_column_num,
            row=preview_frame_row_num,
            sticky=tk.N+tk.S,
        )

        self.preview_image_canvas = tk.Canvas(
            preview_frame,
            bd=0,
            xscrollcommand=xScrollBar.set,
            yscrollcommand=yScrollBar.set,
        )
        self.preview_image_canvas.grid(
            column=0,
            row=preview_frame_row_num,
            columnspan=preview_frame_column_num,
            sticky=tk.N+tk.S+tk.E+tk.W,
        )

        xScrollBar.config(command=self.preview_image_canvas.xview)
        yScrollBar.config(command=self.preview_image_canvas.yview)
        self.preview_image_canvas.bind('<MouseWheel>', self.yscroll_canvas)
        self.preview_image_canvas.bind("<Shift-MouseWheel>", self.xscroll_canvas)

        self.conversion_tab.columnconfigure(
            conversion_tab_right_part_column_num,
            weight=1,
        )
        self.conversion_tab.rowconfigure(
            conversion_tab_right_part_row_num,
            weight=1,
        )
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(preview_frame_row_num, weight=1)

        # ############################################################################################### #
        # K2PDFOPT STDOUT TAB
        # ############################################################################################### #
        stdout_frame = ttk.Labelframe(self.log_tab, text='k2pdfopt STDOUT:')
        stdout_frame.pack(expand=1, fill='both')

    def create_tabs(self):
        self.base_tab = ttk.Notebook(self.root)

        self.conversion_tab = ttk.Frame(self.base_tab)
        self.base_tab.add(self.conversion_tab, text='Conversion')

        self.log_tab = ttk.Frame(self.base_tab)
        self.base_tab.add(self.log_tab, text='Logs')

        self.base_tab.pack(expand=1, fill='both')

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='About', command=self.on_command_about_box_cb)

    def create_widgets(self):
        pass

    def remove_command_argument(self, arg_key):
        self.k2pdfopt_cmd_args.pop(arg_key, None)

    def on_command_about_box_cb(self):
        about_message = \
            '''rebook

                TclTk GUI for k2pdfopt by Pu Wang

                The source code can be found at:
                http://github.com/pwang7/rebook/rebook.py'''

        messagebox.showinfo(message=about_message)

    def on_command_open_pdf_file_cb(self):
        supported_formats = [('PDF files', '*.pdf'), ('DJVU files', '*.djvu')]

        filename = filedialog.askopenfilename(
            parent=self.root,
            filetypes=supported_formats,
            title='Select your file',
        )

        if filename is not None and len(filename.strip()) > 0:
            self.strvar_input_file_path.set(filename)
            (base_path, file_ext) = os.path.splitext(filename)
            self.strvar_output_file_path.set(base_path + '-output.pdf')

    def on_bind_event_device_unit_cb(self, e=None):
        self.update_device_unit_width_height()

    def on_command_width_height_cb(self):
        self.update_device_unit_width_height()

    def update_device_unit_width_height(self):
        if self.device_combobox.current() != 20:  # non-other type
            self.unit_combobox.configure(state='disabled')
            self.width_spinbox.configure(state='disabled')
            self.height_spinbox.configure(state='disabled')

            device_type = self.device_argument_map[self.device_combobox.current()]
            arg = self.device_arg_name + ' ' + device_type
            self.add_or_update_command_argument(self.device_arg_name, arg)
            self.remove_command_argument(self.width_arg_name)
            self.remove_command_argument(self.height_arg_name)

        else:   # "Other type" chosen
            self.unit_combobox.configure(state='normal')
            self.width_spinbox.configure(state='normal')
            self.height_spinbox.configure(state='normal')
            
            screen_unit = self.unit_argument_map[self.unit_combobox.current()]

            width_arg = (self.width_arg_name + ' ' + self.strvar_screen_width.get().strip() + screen_unit)
            self.add_or_update_command_argument(self.width_arg_name, width_arg)

            height_arg = (self.height_arg_name + ' ' + self.strvar_screen_height.get().strip() + screen_unit)
            self.add_or_update_command_argument(self.height_arg_name, height_arg)

            self.remove_command_argument(self.device_arg_name)

    def on_bind_event_mode_cb(self, e=None):
        conversion_mode = self.mode_argument_map[self.mode_combobox.current()]
        arg = (self.conversion_mode_arg_name + ' ' + conversion_mode)
        self.add_or_update_command_argument(self.conversion_mode_arg_name, arg)

    def add_or_update_command_argument(self, arg_key, arg_value):
        self.k2pdfopt_cmd_args[arg_key] = arg_value

    def on_command_save_cb(self):
        pass
        # with open(custom_preset_file_path, 'w') as preset_file:
        #     dict_to_save = {}
        #     for k, v in arg_var_map.items():
        #         dict_to_save[k] = [var.get() for var in v]

        #     json.dump(dict_to_save, preset_file)

    def on_bind_event_cmd_args_cb(self, e=None):
        self.update_cmd_arg_entry_strvar()

    def on_command_column_num_cb(self):
        if self.is_column_num_checked.get():
            arg = (self.column_num_arg_name + ' ' + self.strvar_column_num.get().strip())
            self.add_or_update_command_argument(self.column_num_arg_name, arg)
        else:
            self.remove_command_argument(self.column_num_arg_name)


    def on_command_resolution_multipler_cb(self):
        if self.is_resolution_multipler_checked.get():
            arg = (
                self.resolution_multiplier_arg_name + ' ' +
                self.strvar_resolution_multiplier.get().strip()
            )
            self.add_or_update_command_argument(self.resolution_multiplier_arg_name, arg)
        else:
            self.remove_command_argument(self.resolution_multiplier_arg_name)


    def on_command_and_validate_crop_margin_cb(self):
        if (len(self.strvar_crop_page_range.get().strip()) > 0 and
                not tools.check_page_nums(self.strvar_crop_page_range.get().strip())):
            self.remove_command_argument(self.crop_margin_arg_name)
            self.strvar_crop_page_range.set('')

            messagebox.showerror(
                message='Invalide Crop Page Range. It should be like : 2-5e,3-7o,9-'
            )

            return False

        if self.is_crop_margin_checked.get():
            page_range_arg = self.strvar_crop_page_range.get().strip()
            margin_args = [
                self.strvar_left_margin.get(),
                self.strvar_top_margin.get(),
                self.strvarRightMargin.get(),
                self.strvarBottomMargin.get(),
            ]
            arg = (
                # no space between -cbox and page range
                self.crop_margin_arg_name + page_range_arg + ' '
                + 'in,' . join(map(str.strip, margin_args)) + 'in'
            )
            self.add_or_update_command_argument(self.crop_margin_arg_name, arg)
        else:
            self.remove_command_argument(self.crop_margin_arg_name)


    def on_command_dpi_cb(self):
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


    def on_validate_page_nums_cb(self):
        self.validate_and_update_page_nums()


    def on_command_fixed_font_size_cb(self):
        if self.is_fixed_font_size_checked.get():
            arg = (self.fixed_font_size_arg_name + ' ' + self.strvar_fixed_font_size.get().strip())
            self.add_or_update_command_argument(self.fixed_font_size_arg_name, arg)
        else:
            self.remove_command_argument(self.fixed_font_size_arg_name)


    def on_command_ocr_and_cpu_cb(self):
        if self.is_ocr_cpu_limitation_checked.get():
            self.is_native_pdf_checked.set(False)  # ocr conflicts with native pdf
            self.remove_command_argument(self.native_pdf_arg_name)
            ocr_arg = self.ocr_arg_name
            self.add_or_update_command_argument(self.ocr_arg_name, ocr_arg)

            # negtive integer means percentage
            ocr_cpu_arg = (self.ocr_cpu_arg_name + '-' + self.strvar_ocr_cpu_percentage.get().strip())
            self.add_or_update_command_argument(self.ocr_cpu_arg_name, ocr_cpu_arg)
        else:
            self.remove_command_argument(self.ocr_arg_name)
            self.remove_command_argument(self.ocr_cpu_arg_name)


    def on_command_and_validate_landscape_cb(self):
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
                arg += self.strvar_landscape_pages.get()

            self.add_or_update_command_argument(self.landscape_arg_name, arg.strip())
        else:
            self.remove_command_argument(self.landscape_arg_name)

        return True

    def on_command_line_break_cb(self):
        if self.is_smart_linebreak_checked.get():
            arg = (self.linebreak_arg_name + ' ' + self.strvar_linebreak_space.get().strip())
            self.add_or_update_command_argument(self.linebreak_arg_name, arg)
        else:
            self.remove_command_argument(self.linebreak_arg_name)

    def on_command_auto_straighten_cb(self):
        if self.is_autostraighten_checked.get():
            arg = self.auto_straignten_arg_name
            self.add_or_update_command_argument(self.auto_straignten_arg_name, arg)
        else:
            self.remove_command_argument(self.auto_straignten_arg_name)


    def on_command_break_page_cb(self):
        if self.isBreakPage.get():
            # break page conflicts with avoid overlap since they are both -bp flag
            self.isAvoidOverlap.set(False)
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)

            arg = self.break_page_avoid_overlap_arg_name
            self.add_or_update_command_argument(self.break_page_avoid_overlap_arg_name, arg)
        else:
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)


    def on_command_color_output_cb(self):
        if self.is_coloroutput_checked.get():
            arg = self.color_output_arg_name
            self.add_or_update_command_argument(self.color_output_arg_name, arg)
        else:
            self.remove_command_argument(self.color_output_arg_name)


    def on_command_native_pdf_cb(self):
        if self.is_native_pdf_checked.get():
            # native pdf conflicts with ocr and reflow text
            self.is_ocr_cpu_limitation_checked.set(False)
            self.remove_command_argument(self.ocr_arg_name)
            self.remove_command_argument(self.ocr_cpu_arg_name)

            self.is_reflow_text_checked.set(False)
            self.remove_command_argument(self.reflow_text_arg_name)

            arg = self.native_pdf_arg_name
            self.add_or_update_command_argument(self.native_pdf_arg_name, arg)
        else:
            self.remove_command_argument(self.native_pdf_arg_name)


    def on_command_right_to_left_cb(self):
        if self.is_right_to_left_checked.get():
            arg = self.right_to_left_arg_name
            self.add_or_update_command_argument(self.right_to_left_arg_name, arg)
        else:
            self.remove_command_argument(self.right_to_left_arg_name)


    def on_command_post_gs_cb(self):
        if self.isPostGs.get():
            arg = self.post_gs_arg_name
            self.add_or_update_command_argument(self.post_gs_arg_name, arg)
        else:
            self.remove_command_argument(self.post_gs_arg_name)


    def on_command_marked_src_cb(self):
        if self.isMarkedSrc.get():
            arg = self.marked_source_arg_name
            self.add_or_update_command_argument(self.marked_source_arg_name, arg)
        else:
            self.remove_command_argument(self.marked_source_arg_name)


    def on_command_reflow_text_cb(self):
        if self.is_reflow_text_checked.get():
            self.is_native_pdf_checked.set(False)  # reflow text conflicts with native pdf
            self.remove_command_argument(self.native_pdf_arg_name)
            arg = self.reflow_text_arg_name + '+'
            self.add_or_update_command_argument(self.reflow_text_arg_name, arg)
        else:
            self.remove_command_argument(self.reflow_text_arg_name)


    def on_command_erase_vertical_line_cb(self):
        if self.is_erase_vertical_line_checked.get():
            arg = self.erase_vertical_line_arg_name + ' 1'
            self.add_or_update_command_argument(self.erase_vertical_line_arg_name, arg)
        else:
            self.remove_command_argument(self.erase_vertical_line_arg_name)


    def on_command_fast_preview_cb(self):
        if self.is_fast_preview_checked.get():
            arg = self.fast_preview_arg_name + ' 0'
            self.add_or_update_command_argument(self.fast_preview_arg_name, arg)
        else:
            self.remove_command_argument(self.fast_preview_arg_name)


    def on_command_avoid_text_selection_overlap_cb(self):
        if self.isAvoidOverlap.get():
            # avoid overlap conflicts with break page since they are both -bp flag
            self.isBreakPage.set(False)
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)

            arg = self.break_page_avoid_overlap_arg_name + ' m'
            self.add_or_update_command_argument(self.break_page_avoid_overlap_arg_name, arg)
        else:
            self.remove_command_argument(self.break_page_avoid_overlap_arg_name)


    def on_command_ign_small_defect_cb(self):
        if self.isIgnSmallDefects.get():
            arg = (self.ign_small_defects_arg_name + ' 1.5')
            self.add_or_update_command_argument(self.ign_small_defects_arg_name, arg)
        else:
            self.remove_command_argument(self.ign_small_defects_arg_name)


    def on_command_erase_horizontal_line_cb(self):
        if self.is_erase_horizontal_line_checked.get():
            arg = self.erase_horizontal_line_arg_name + ' 1'
            self.add_or_update_command_argument(self.erase_horizontal_line_arg_name, arg)
        else:
            self.remove_command_argument(self.erase_horizontal_line_arg_name)


    def on_command_auto_crop_cb(self):
        if self.is_autocrop_checked.get():
            arg = self.auto_crop_arg_name
            self.add_or_update_command_argument(self.auto_crop_arg_name, arg)
        else:
            self.remove_command_argument(self.auto_crop_arg_name)

    def remove_preview_image_and_clear_canvas(self):
        if os.path.exists(self.preview_image_path):
            os.remove(self.preview_image_path)

        self.preview_image_canvas.delete(tk.ALL)
        self.canvas_image_tag = None

    def load_preview_image(self, img_path, preview_page_index):

        if os.path.exists(img_path):
            self.preview_image = tk.PhotoImage(file=img_path)

            self.canvas_image_tag = self.preview_image_canvas.create_image(
                (0, 0),
                anchor=tk.NW,
                image=self.preview_image,
                tags='preview',
            )

            (left_pos, top_pos, right_pos, bottom_pos) = (
                0,
                0,
                self.preview_image.width(),
                self.preview_image.height(),
            )
            self.preview_image_canvas.config(
                scrollregion=(left_pos, top_pos, right_pos, bottom_pos),
            )
            # canvas.scale('preview', 0, 0, 0.1, 0.1)
            self.strvar_current_preview_page_num.set('Page: ' + str(preview_page_index))
        else:
            self.strvar_current_preview_page_num.set('No Page: ' + str(preview_page_index))


    def generate_one_preview_image(self, preview_page_index):

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

        def preview_image_future_cb(self, bgf):
            self.load_preview_image(self.preview_image_path, preview_page_index)
            self.log_string(
                "Preview generation for page %d finished" %
                preview_page_index
            )

        self.background_future.add_done_callback(preview_image_future_cb)

    def on_command_restore_default_cb(self):
        self.restore_default_values()

    def on_command_abort_conversion_cb(self):
        if self.background_future is not None:
            self.background_future.cancel()

        if (self.background_process is not None and self.background_process.returncode is None):
            self.background_process.terminate()

    def on_command_convert_pdf_cb(self):
        if not self.pdf_conversion_is_done():
            return

        pdf_output_arg = self.output_path_arg_name + ' %s' + self.output_pdf_suffix
        self.background_future = self.convert_pdf_file(pdf_output_arg)

    def on_command_ten_page_up_cb(self):
        self.current_preview_page_index -= 10
        if self.current_preview_page_index < 1:
            self.current_preview_page_index = 1
        self.generate_one_preview_image(self.current_preview_page_index)

    def on_command_page_up_cb(self):
        if self.current_preview_page_index > 1:
            self.current_preview_page_index -= 1
        self.generate_one_preview_image(self.current_preview_page_index)

    def on_command_page_down_cb(self):
        self.current_preview_page_index += 1
        self.generate_one_preview_image(self.current_preview_page_index)

    def on_command_ten_page_down_cb(self):
        self.current_preview_page_index += 10
        self.generate_one_preview_image(self.current_preview_page_index)

    def yscroll_canvas(self, event):
        self.preview_image_canvas.yview_scroll(-1 * event.delta, 'units')

    def xscroll_canvas(self, event):
        self.preview_image_canvas.xview_scroll(-1 * event.delta, 'units')

    def on_command_clear_log_cb(self):
        self.clear_logs()

    def pdf_conversion_is_done(self):
        if (self.background_future is None) or (self.background_future.done()):
            if ((self.background_process is None) or (self.background_process.returncode is not None)):
                return True

        messagebox.showerror(message='Background Conversion Not Finished Yet! Please Wait...')
        return False

    def check_k2pdfopt_path_exists(self):
        if not os.path.exists(self.k2pdfopt_path):
            messagebox.showerror(
                message='Failed to find k2pdfopt, ' +
                'please put it under the same directory ' +
                'as rebook and then restart.'
            )
            quit()

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def generate_command_argument_string(self):
        """ Transforms the global dictionary `K2PDFOPT_CMD_ARGS` into a command line arguments list.

            Remarks: at the end, the chosen argument are completed by `mandatory` arguments
                    ('-a- -ui- -x').
        """

        device_arg = self.k2pdfopt_cmd_args.pop(self.device_arg_name, None)
        if device_arg is None:
            width_arg = self.k2pdfopt_cmd_args.pop(self.width_arg_name)
            height_arg = self.k2pdfopt_cmd_args.pop(self.height_arg_name)

        mode_arg = self.k2pdfopt_cmd_args.pop(self.conversion_mode_arg_name)
        arg_list = [mode_arg] + list(self.k2pdfopt_cmd_argsvalues())
        self.k2pdfopt_cmd_args[self.conversion_mode_arg_name] = mode_arg

        if device_arg is not None:
            arg_list.append(device_arg)
            self.k2pdfopt_cmd_args[self.device_arg_name] = device_arg
        else:
            arg_list.append(width_arg)
            arg_list.append(height_arg)
            self.k2pdfopt_cmd_args[self.width_arg_name] = width_arg
            self.k2pdfopt_cmd_args[self.height_arg_name] = height_arg

        arg_list.append('-a- -ui- -x')
        self.log_string('Generate Argument List: ' + str(arg_list))
        cmd_arg_str = ' '.join(arg_list)
        return cmd_arg_str

    def convert_pdf_file(self, output_arg):
        self.check_k2pdfopt_path_exists()

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


class ReBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure_gui()

    def configure_gui(self):
        self.title('Rebook')
        # self.geometry("500x500")
        # self.resizable(False, False)


if __name__ == "__main__":
    rebook = ReBook()
    frame = MainFrame(rebook)
    rebook.mainloop()