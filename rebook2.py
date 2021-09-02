""" This script define a GUI to choose options to build a k2pdfopt command-line """

from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import asyncio
import json
import sys
import os
import webbrowser
from PIL import Image, ImageTk

import tools


class MainFrame(ttk.Frame):
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=too-many-ancestors
    # pylint: disable=too-many-statements

    """MainFrame for ReBook Application"""

    device_argument_map = {
        0: "k2",
        1: "dx",
        2: "kpw",
        3: "kp2",
        4: "kp3",
        5: "kv",
        6: "ko2",
        7: "pb2",
        8: "nookst",
        9: "kbt",
        10: "kbg",
        11: "kghd",
        12: "kghdfs",
        13: "kbm",
        14: "kba",
        15: "kbhd",
        16: "kbh2o",
        17: "kbh2ofs",
        18: "kao",
        19: "koc",
        20: "kof",
        21: "kol",
        22: "nex7",
        23: None,
    }

    device_width_height_dpi_info = {
        0: [560, 735, 167],
        1: [800, 1180, 167],
        2: [658, 889, 212],
        3: [718, 965, 212],
        4: [1016, 1354, 300],
        5: [1016, 1354, 300],
        6: [1200, 1583, 300],
        7: [600, 800, 167],
        8: [352, 725, 167],
        9: [600, 735, 167],
        10: [758, 942, 218],
        11: [1072, 1328, 250],
        12: [1072, 1448, 250],
        13: [600, 730, 200],
        14: [758, 932, 211],
        15: [1080, 1320, 250],
        16: [1080, 1309, 265],
        17: [1080, 1429, 265],
        18: [1404, 1713, 300],
        19: [1072, 1317, 300],
        20: [1440, 1745, 300],
        21: [1264, 1527, 300],
        22: [1187, 1811, 323],
    }

    device_choice_map = {
        0: "Kindle 1-5",
        1: "Kindle DX",
        2: "Kindle Paperwhite",
        3: "Kindle Paperwhite 2",
        4: "Kindle Paperwhite 3",
        5: "Kindle Voyage/PW3+/Oasis",
        6: "Kindle Oasis 2",
        7: "Pocketbook Basic 2",
        8: "Nook Simple Touch",
        9: "Kobo Touch",
        10: "Kobo Glo",
        11: "Kobo Glo HD",
        12: "Kobo Glo HD Full Screen",
        13: "Kobo Mini",
        14: "Kobo Aura",
        15: "Kobo Aura HD",
        16: "Kobo H2O",
        17: "Kobo H2O Full Screen",
        18: "Kobo Aura One",
        19: "Kobo Clara HD",
        20: "Kobo Forma",
        21: "Kobo Libra H20",
        22: "Nexus 7",
        23: "Other (specify width & height)",
    }

    mode_argument_map = {
        0: "def",
        1: "copy",
        2: "fp",
        3: "fw",
        4: "2col",
        5: "tm",
        6: "crop",
        7: "concat",
    }

    mode_choice_map = {
        0: "Default",
        1: "Copy",
        2: "Fit Page",
        3: "Fit Width",
        4: "2 Columns",
        5: "Trim Margins",
        6: "Crop",
        7: "Concat",
    }

    unit_argument_map = {
        0: "in",
        1: "cm",
        2: "s",
        3: "t",
        4: "p",
        5: "x",
    }

    unit_choice_map = {
        0: "Inches",
        1: "Centimeters",
        2: "Source Page Size",
        3: "Trimmed Source Region Size",
        4: "Pixels",
        5: "Relative to the OCR Text Layer",
    }

    language_argument_map = {
        0: "afr",
        1: "amh",
        2: "ara",
        3: "asm",
        4: "aze",
        5: "aze_cyrl",
        6: "bel",
        7: "ben",
        8: "bod",
        9: "bos",
        10: "bre",
        11: "bul",
        12: "cat",
        13: "ceb",
        14: "ces",
        15: "chi_sim",
        16: "chi_tra",
        17: "chr",
        18: "cos",
        19: "cym",
        20: "dan",
        21: "deu",
        22: "dzo",
        23: "ell",
        24: "eng",
        25: "enm",
        26: "epo",
        27: "est",
        28: "eus",
        29: "fao",
        30: "fas",
        31: "fil",
        32: "fin",
        33: "fra",
        34: "frk",
        35: "frm",
        36: "fry",
        37: "gla",
        38: "gle",
        39: "glg",
        40: "grc",
        41: "guj",
        42: "hat",
        43: "heb",
        44: "hin",
        45: "hrv",
        46: "hun",
        47: "hye",
        48: "iku",
        49: "ind",
        50: "isl",
        51: "ita",
        52: "ita_old",
        53: "jav",
        54: "jpn",
        55: "kan",
        56: "kat",
        57: "kat_old",
        58: "kaz",
        59: "khm",
        60: "kir",
        61: "kmr",
        62: "kor",
        63: "kor_vert",
        64: "lao",
        65: "lat",
        66: "lav",
        67: "lit",
        68: "ltz",
        69: "mal",
        70: "mar",
        71: "mkd",
        72: "mlt",
        73: "mon",
        74: "mri",
        75: "msa",
        76: "mya",
        77: "nep",
        78: "nld",
        79: "nor",
        80: "oci",
        81: "ori",
        82: "pan",
        83: "pol",
        84: "por",
        85: "pus",
        86: "que",
        87: "ron",
        88: "rus",
        89: "san",
        90: "sin",
        91: "slk",
        92: "slv",
        93: "snd",
        94: "spa",
        95: "spa_old",
        96: "sqi",
        97: "srp",
        98: "srp_latn",
        99: "sun",
        100: "swa",
        101: "swe",
        102: "syr",
        103: "tam",
        104: "tat",
        105: "tel",
        106: "tgk",
        107: "tha",
        108: "tir",
        109: "ton",
        110: "tur",
        111: "uig",
        112: "ukr",
        113: "urd",
        114: "uzb",
        115: "uzb_cyrl",
        116: "vie",
        117: "yid",
        118: "yor",
    }

    language_map = {
        0: "Afrikaans",
        1: "Amharic",
        2: "Arabic",
        3: "Assamese",
        4: "Azerbaijani",
        5: "Azerbaijani - Cyrilic",
        6: "Belarusian",
        7: "Bengali",
        8: "Tibetan",
        9: "Bosnian",
        10: "Breton",
        11: "Bulgarian",
        12: "Catalan; Valencian",
        13: "Cebuano",
        14: "Czech",
        15: "Chinese - Simplified",
        16: "Chinese - Traditional",
        17: "Cherokee",
        18: "Corsican",
        19: "Welsh",
        20: "Danish",
        21: "German",
        22: "Dzongkha",
        23: "Greek, Modern (1453-)",
        24: "English",
        25: "English, Middle (1100-1500)",
        26: "Esperanto",
        27: "Estonian",
        28: "Basque",
        29: "Faroese",
        30: "Persian",
        31: "Filipino (old - Tagalog)",
        32: "Finnish",
        33: "French",
        34: "German - Fraktur",
        35: "French, Middle (ca.1400-1600)",
        36: "Western Frisian",
        37: "Scottish Gaelic",
        38: "Irish",
        39: "Galician",
        40: "Greek, Ancient (to 1453)",
        41: "Gujarati",
        42: "Haitian; Haitian Creole",
        43: "Hebrew",
        44: "Hindi",
        45: "Croatian",
        46: "Hungarian",
        47: "Armenian",
        48: "Inuktitut",
        49: "Indonesian",
        50: "Icelandic",
        51: "Italian",
        52: "Italian - Old",
        53: "Javanese",
        54: "Japanese",
        55: "Kannada",
        56: "Georgian",
        57: "Georgian - Old",
        58: "Kazakh",
        59: "Central Khmer",
        60: "Kirghiz; Kyrgyz",
        61: "Kurmanji (Kurdish - Latin Script)",
        62: "Korean",
        63: "Korean (vertical)",
        64: "Lao",
        65: "Latin",
        66: "Latvian",
        67: "Lithuanian",
        68: "Luxembourgish",
        69: "Malayalam",
        70: "Marathi",
        71: "Macedonian",
        72: "Maltese",
        73: "Mongolian",
        74: "Maori",
        75: "Malay",
        76: "Burmese",
        77: "Nepali",
        78: "Dutch; Flemish",
        79: "Norwegian",
        80: "Occitan (post 1500)",
        81: "Oriya",
        82: "Panjabi; Punjabi",
        83: "Polish",
        84: "Portuguese",
        85: "Pushto; Pashto",
        86: "Quechua",
        87: "Romanian; Moldavian; Moldovan",
        88: "Russian",
        89: "Sanskrit",
        90: "Sinhala; Sinhalese",
        91: "Slovak",
        92: "Slovenian",
        93: "Sindhi",
        94: "Spanish; Castilian",
        95: "Spanish; Castilian - Old",
        96: "Albanian",
        97: "Serbian",
        98: "Serbian - Latin",
        99: "Sundanese",
        100: "Swahili",
        101: "Swedish",
        102: "Syriac",
        103: "Tamil",
        104: "Tatar",
        105: "Telugu",
        106: "Tajik",
        107: "Thai",
        108: "Tigrinya",
        109: "Tonga",
        110: "Turkish",
        111: "Uighur; Uyghur",
        112: "Ukrainian",
        113: "Urdu",
        114: "Uzbek",
        115: "Uzbek - Cyrilic",
        116: "Vietnamese",
        117: "Yiddish",
        118: "Yoruba",
    }

    ocrd_argument_map = {
        0: "w",
        1: "l",
        2: "c",
        3: "p",
    }

    ocrd_map = {
        0: "word",
        1: "line",
        2: "column",
        3: "page",
    }

    def __init__(self, app, k2pdfopt_path):
        super().__init__(app)
        self.root = app  # root of tkinter

        self.half_width_screen = int(self.root.width / 2) - 60

        # limits and default value
        self.device_width_min_value = 300
        self.device_width_max_value = 2500
        self.device_height_min_value = 700
        self.device_height_max_value = 3000
        self.device_dpi_min_value = 100
        self.device_dpi_max_value = 500
        self.max_column_min_value = 1
        self.max_column_max_value = 10
        self.fixed_font_size_min_value = 9
        self.fixed_font_size_max_value = 48
        self.ocr_cpu_min_value = 1
        self.ocr_cpu_max_value = 100
        self.document_resolution_factor_min_value = 0.1
        self.document_resolution_factor_max_value = 10.0
        self.smart_line_break_min_value = 0.01
        self.smart_line_break_max_value = 2.00
        self.margin_and_crop_areas_min_value = 0
        self.margin_and_crop_areas_max_value = 10
        self.default_padx = 5
        self.default_pady = 0
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
        self.strvar_tesseract_detection = tk.StringVar()

        self.device_arg_name = "-dev"  # -dev <name>
        self.device_width_arg_name = "-w"  # -w <width>[in|cm|s|t|p]
        self.device_height_arg_name = "-h"  # -h <height>[in|cm|s|t|p|x]
        self.conversion_mode_arg_name = "-mode"  # -mode <mode>
        self.output_path_arg_name = "-o"  # -o <namefmt>
        self.output_file_suffix = "_k2opt.pdf"
        self.screen_unit_prefix = "-screen_unit"

        # Parameters frame
        self.column_num_arg_name = "-col"  # -col <maxcol>
        self.resolution_multiplier_arg_name = "-dr"  # -dr <value>
        self.cropmargin_arg_name = "m"
        self.cropbox_arg_name = "-cbox"  # -cbox[<pagelist>|u|-]
        self.cropbox_1_arg_name = "cbox_1"
        self.cropbox_2_arg_name = "cbox_2"
        self.cropbox_3_arg_name = "cbox_3"
        self.cropbox_4_arg_name = "cbox_4"
        self.cropbox_5_arg_name = "cbox_5"
        self.crop_margin_left_arg_name = "-ml"
        self.crop_margin_top_arg_name = "-mt"
        self.crop_margin_right_arg_name = "-mr"
        self.crop_margin_bottom_arg_name = "-mb"
        self.dpi_arg_name = "-dpi"  # -dpi <dpival>
        self.page_num_arg_name = "-p"  # -p <pagelist>
        self.fixed_font_size_arg_name = "-fs"  # -fs 0/-fs <font size>[+]
        self.ocr_arg_name = "-ocr"  # -ocr-/-ocr t
        self.tesseract_language_arg_name = "-ocrlang"  # -ocrlang <lang>
        self.tesseract_fast_arg_name = "-fast"
        self.tesseract_detection_arg_name = "-ocrd" # -ocrd w|l|c|p
        self.ocr_cpu_arg_name = "-nt"  # -nt -50/-nt <percentage>
        self.landscape_arg_name = "-ls"  # -ls[-][pagelist]
        self.linebreak_arg_name = "-ws"  # -ws <spacing>

        self.strvar_tesseract_language = tk.StringVar()

        # Crop Maring
        self.is_cropmargin_checked = tk.BooleanVar()
        self.strvar_top_cropmargin = tk.StringVar()
        self.strvar_left_cropmargin = tk.StringVar()
        self.strvar_width_cropmargin = tk.StringVar()
        self.strvar_height_cropmargin = tk.StringVar()
        self.strvar_crop_page_range = tk.StringVar()

        # cropbox 1
        self.is_cropbox_1_checked = tk.BooleanVar()
        self.strvar_left_cropbox_1 = tk.StringVar()
        self.strvar_top_cropbox_1 = tk.StringVar()
        self.strvar_width_cropbox_1 = tk.StringVar()
        self.strvar_height_cropbox_1 = tk.StringVar()
        self.strvar_page_range_cropbox_1 = tk.StringVar()

        # cropbox 2
        self.is_cropbox_2_checked = tk.BooleanVar()
        self.strvar_left_cropbox_2 = tk.StringVar()
        self.strvar_top_cropbox_2 = tk.StringVar()
        self.strvar_width_cropbox_2 = tk.StringVar()
        self.strvar_height_cropbox_2 = tk.StringVar()
        self.strvar_page_range_cropbox_2 = tk.StringVar()

        # cropbox 3
        self.is_cropbox_3_checked = tk.BooleanVar()
        self.strvar_left_cropbox_3 = tk.StringVar()
        self.strvar_top_cropbox_3 = tk.StringVar()
        self.strvar_width_cropbox_3 = tk.StringVar()
        self.strvar_height_cropbox_3 = tk.StringVar()
        self.strvar_page_range_cropbox_3 = tk.StringVar()

        # cropbox 4
        self.is_cropbox_4_checked = tk.BooleanVar()
        self.strvar_left_cropbox_4 = tk.StringVar()
        self.strvar_top_cropbox_4 = tk.StringVar()
        self.strvar_width_cropbox_4 = tk.StringVar()
        self.strvar_height_cropbox_4 = tk.StringVar()
        self.strvar_page_range_cropbox_4 = tk.StringVar()

        # cropbox 5
        self.is_cropbox_5_checked = tk.BooleanVar()
        self.strvar_left_cropbox_5 = tk.StringVar()
        self.strvar_top_cropbox_5 = tk.StringVar()
        self.strvar_width_cropbox_5 = tk.StringVar()
        self.strvar_height_cropbox_5 = tk.StringVar()
        self.strvar_page_range_cropbox_5 = tk.StringVar()

        self.is_dpi_checked = tk.BooleanVar()
        self.is_landscape_checked = tk.BooleanVar()
        self.is_column_num_checked = tk.BooleanVar()
        self.is_smart_linebreak_checked = tk.BooleanVar()  # -ws 0.01~10
        self.is_fixed_font_size_checked = tk.BooleanVar()
        self.is_tesseract_checked = tk.BooleanVar()
        self.is_tesseract_fast_checked = tk.BooleanVar()
        self.is_resolution_multipler_checked = tk.BooleanVar()

        self.strvar_column_num = tk.StringVar()
        self.strvar_page_numbers = tk.StringVar()
        self.strvar_fixed_font_size = tk.StringVar()
        self.strvar_landscape_pages = tk.StringVar()  # 1,3,5-10
        self.strvar_linebreak_space = tk.StringVar()
        self.strvar_device_screen_dpi = tk.StringVar()
        self.strvar_ocr_cpu_percentage = tk.StringVar()
        self.strvar_resolution_multiplier = tk.StringVar()

        self.auto_straignten_arg_name = "-as"  # -as-/-as
        self.break_page_avoid_overlap_arg_name = "-bp"  # -bp-/-bp
        self.color_output_arg_name = "-c"  # -c-/-c
        self.native_pdf_arg_name = "-n"  # -n-/-n
        self.right_to_left_arg_name = "-r"  # -r-/-r
        self.post_gs_arg_name = "-ppgs"  # -ppgs-/-ppgs
        self.marked_source_arg_name = "-sm"  # -sm-/-sm
        self.reflow_text_arg_name = "-wrap"  # -wrap+/-wrap-
        self.erase_vertical_line_arg_name = "-evl"  # -evl 0/-evl 1
        self.erase_horizontal_line_arg_name = "-ehl"  # -ehl 0/-ehl 1
        self.fast_preview_arg_name = "-rt"  # -rt /-rt 0
        self.ign_small_defects_arg_name = "-de"  # -de 1.0/-de 1.5
        self.auto_crop_arg_name = "-ac"  # -ac-/-ac

        self.is_autocrop_checked = tk.BooleanVar()
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

        self.preview_output_arg_name = "-bmp"
        self.preview_image_path = "./k2pdfopt_out.png"

        self.default_var_map = {
            self.device_arg_name: ["Kindle Paperwhite 3"],
            self.screen_unit_prefix: ["Pixels"],
            self.device_width_arg_name: ["560"],
            self.device_height_arg_name: ["735"],
            self.conversion_mode_arg_name: ["Default"],
            self.output_path_arg_name: [""],
            self.column_num_arg_name: [False, "2"],
            self.resolution_multiplier_arg_name: [False, "1.0"],
            self.cropmargin_arg_name: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
            ],
            self.cropbox_1_arg_name: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            self.cropbox_2_arg_name: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            self.cropbox_3_arg_name: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            self.cropbox_4_arg_name: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            self.cropbox_5_arg_name: [
                False,
                "0.0",
                "0.0",
                "0.0",
                "0.0",
                "",
            ],
            self.dpi_arg_name: [False, "167"],
            self.page_num_arg_name: [""],
            self.fixed_font_size_arg_name: [False, "12"],
            self.landscape_arg_name: [False, ""],
            self.linebreak_arg_name: [True, "0.200"],
            self.auto_straignten_arg_name: [False],
            self.break_page_avoid_overlap_arg_name: [False, False],
            self.color_output_arg_name: [False],
            self.native_pdf_arg_name: [False],
            self.right_to_left_arg_name: [False],
            self.post_gs_arg_name: [False],
            self.marked_source_arg_name: [True],
            self.reflow_text_arg_name: [True],
            self.erase_vertical_line_arg_name: [True],
            self.erase_horizontal_line_arg_name: [True],
            self.fast_preview_arg_name: [True],
            self.ign_small_defects_arg_name: [False],
            self.auto_crop_arg_name: [False],
            self.ocr_arg_name: [False, "50"],
            self.ocr_cpu_arg_name: [False, "50"],
            self.tesseract_language_arg_name: ["English"],
            self.tesseract_fast_arg_name: [False],
            self.tesseract_detection_arg_name: ["line"],
            self.preview_output_arg_name: [],
        }

        self.arg_var_map = {
            self.device_arg_name: [self.strvar_device],
            self.screen_unit_prefix: [self.strvar_screen_unit],
            self.device_width_arg_name: [self.strvar_device_screen_width],
            self.device_height_arg_name: [self.strvar_device_screen_height],
            self.conversion_mode_arg_name: [self.strvar_conversion_mode],
            self.output_path_arg_name: [self.strvar_output_file_path],
            self.column_num_arg_name: [
                self.is_column_num_checked,
                self.strvar_column_num,
            ],
            self.resolution_multiplier_arg_name: [
                self.is_resolution_multipler_checked,
                self.strvar_resolution_multiplier,
            ],
            self.cropmargin_arg_name: [
                self.is_cropmargin_checked,
                self.strvar_left_cropmargin,
                self.strvar_top_cropmargin,
                self.strvar_width_cropmargin,
                self.strvar_height_cropmargin,
            ],
            self.cropbox_1_arg_name: [
                self.is_cropbox_1_checked,
                self.strvar_left_cropbox_1,
                self.strvar_top_cropbox_1,
                self.strvar_width_cropbox_1,
                self.strvar_height_cropbox_1,
                self.strvar_page_range_cropbox_1,
            ],
            self.cropbox_2_arg_name: [
                self.is_cropbox_2_checked,
                self.strvar_left_cropbox_2,
                self.strvar_top_cropbox_2,
                self.strvar_width_cropbox_2,
                self.strvar_height_cropbox_2,
                self.strvar_page_range_cropbox_2,
            ],
            self.cropbox_3_arg_name: [
                self.is_cropbox_3_checked,
                self.strvar_left_cropbox_3,
                self.strvar_top_cropbox_3,
                self.strvar_width_cropbox_3,
                self.strvar_height_cropbox_3,
                self.strvar_page_range_cropbox_3,
            ],
            self.cropbox_4_arg_name: [
                self.is_cropbox_4_checked,
                self.strvar_left_cropbox_4,
                self.strvar_top_cropbox_4,
                self.strvar_width_cropbox_4,
                self.strvar_height_cropbox_4,
                self.strvar_page_range_cropbox_4,
            ],
            self.cropbox_5_arg_name: [
                self.is_cropbox_5_checked,
                self.strvar_left_cropbox_5,
                self.strvar_top_cropbox_5,
                self.strvar_width_cropbox_5,
                self.strvar_height_cropbox_5,
                self.strvar_page_range_cropbox_5,
            ],
            self.dpi_arg_name: [
                self.is_dpi_checked,
                self.strvar_device_screen_dpi,
            ],
            self.page_num_arg_name: [self.strvar_page_numbers],
            self.fixed_font_size_arg_name: [
                self.is_fixed_font_size_checked,
                self.strvar_fixed_font_size,
            ],
            self.ocr_arg_name: [
                self.is_tesseract_checked,
                self.strvar_ocr_cpu_percentage,
            ],
            self.ocr_cpu_arg_name: [
                self.is_tesseract_checked,
                self.strvar_ocr_cpu_percentage,
            ],
            self.tesseract_language_arg_name: [self.strvar_tesseract_language],
            self.tesseract_fast_arg_name: [self.is_tesseract_fast_checked],
            self.tesseract_detection_arg_name: [self.strvar_tesseract_detection],
            self.landscape_arg_name: [
                self.is_landscape_checked,
                self.strvar_landscape_pages,
            ],
            self.linebreak_arg_name: [
                self.is_smart_linebreak_checked,
                self.strvar_linebreak_space,
            ],
            self.auto_straignten_arg_name: [self.is_autostraighten_checked],
            self.break_page_avoid_overlap_arg_name: [
                self.is_break_page_checked,
                self.is_avoid_overlap_checked,
            ],
            self.color_output_arg_name: [self.is_coloroutput_checked],
            self.native_pdf_arg_name: [self.is_native_pdf_checked],
            self.right_to_left_arg_name: [self.is_right_to_left_checked],
            self.post_gs_arg_name: [self.is_ghostscript_postprocessing_checked],
            self.marked_source_arg_name: [self.is_markedup_source_checked],
            self.reflow_text_arg_name: [self.is_reflow_text_checked],
            self.erase_vertical_line_arg_name: [self.is_erase_vertical_line_checked],
            self.erase_horizontal_line_arg_name: [
                self.is_erase_horizontal_line_checked
            ],
            self.fast_preview_arg_name: [self.is_fast_preview_checked],
            self.ign_small_defects_arg_name: [self.is_ignore_small_defects_checked],
            self.auto_crop_arg_name: [self.is_autocrop_checked],
            self.preview_output_arg_name: [],
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

        # self.advanced_tab = ttk.Frame(self.notebook)
        # self.notebook.add(self.advanced_tab, text="Advanced")

        self.logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text="Logs")

        self.notebook.pack(expand=1, fill="both")

        self.__fill_conversion_tab()
        # self.__fill_advanced_tab()
        self.__fill_logs_tab()

    def create_menus(self):
        """Create the menus for ReBook"""
        menu_bar = tk.Menu(self.root)
        self.root["menu"] = menu_bar

        # File menu
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label="File")
        menu_file.add_command(label="Open file…", command=self.menu_open_pdf_file)
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
        self.conversion_tab_left_part_column_num = 0
        self.conversion_tab_left_part_line_num = -1
        self.__setup_file_frame()
        self.__setup_device_frame()
        self.__setup_margin_and_cropboxes_frame()
        self.__setup_parameters_frame()
        self.__setup_tesseract_frame()

    def __fill_right_side_of_conversion_tab(self):
        """Fill the right side of Conversion tab"""
        self.conversion_tab_right_part_column_num = 1
        self.conversion_tab_right_part_line_num = -1
        self.__setup_command_line_frame()
        self.__setup_action_frame()

    def __fill_conversion_tab(self):
        """Fill the Conversion tab"""
        self.__fill_left_side_of_conversion_tab()
        self.__fill_right_side_of_conversion_tab()

        self.conversion_tab.columnconfigure(
            self.conversion_tab_right_part_column_num,
            weight=1,
        )
        self.conversion_tab.rowconfigure(
            self.conversion_tab_left_part_line_num,
            weight=1,
        )
        self.action_frame.columnconfigure(0, weight=1)
        self.action_frame.rowconfigure(self.action_frame_row_num, weight=1)

    def __fill_advanced_tab(self):
        """Fill the advanced option tab"""
        self.advanced_tab_left_part_line_num = 0

        # device_frame_line_number += 1

        self.advanced_option_frame = ttk.Labelframe(
            self.advanced_tab,
            text="Advanced options",
        )
        self.advanced_option_frame.grid(
            column=0,
            row=self.advanced_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line = 0

        self.min_column_gap_width_label = ttk.Label(
            self.advanced_option_frame, text="Minimum column gap width (-cg)"
        )
        self.min_column_gap_width_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.min_column_gap_width = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.min_column_gap_width.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line += 1

        self.max_gap_between_column_label = ttk.Label(
            self.advanced_option_frame, text="Max allowed gap between columns (-cgmax)"
        )
        self.max_gap_between_column_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.max_gap_between_column = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.max_gap_between_column.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line += 1

        self.column_gap_range_label = ttk.Label(
            self.advanced_option_frame, text="Column-gap range (-cgr)"
        )
        self.column_gap_range_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.column_gap_range = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.column_gap_range.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line += 1

        self.minimum_column_height_label = ttk.Label(
            self.advanced_option_frame, text="Minimum column height (-ch)"
        )
        self.minimum_column_height_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.minimum_column_height = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.minimum_column_height.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line += 1

        self.minimum_column_height_label = ttk.Label(
            self.advanced_option_frame, text="Column Offset Maximum (-comax)"
        )
        self.minimum_column_height_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.minimum_column_height = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.minimum_column_height.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line += 1

        self.minimum_column_height_label = ttk.Label(
            self.advanced_option_frame, text="min height of the blank area (-crgh)"
        )
        self.minimum_column_height_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.minimum_column_height = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.minimum_column_height.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        line += 1

        self.minimum_column_height_label = ttk.Label(
            self.advanced_option_frame, text="Insert Breack page (-bpl)"
        )
        self.minimum_column_height_label.grid(
            column=0,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.minimum_column_height = ttk.Spinbox(
            self.advanced_option_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=0.1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.minimum_column_height.grid(
            column=1,
            row=line,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __setup_file_frame(self):
        """Set up the file frame"""
        self.conversion_tab_left_part_line_num += 1

        self.file_frame = ttk.Labelframe(
            self.conversion_tab, text="Files", width=self.half_width_screen, height=78
        )
        self.file_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.file_frame.grid_propagate(False)

        file_frame_line_number = 0

        open_button = ttk.Button(
            self.file_frame, text="Input file", command=self.menu_open_pdf_file
        )
        open_button.grid(
            column=0,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.input_path_entry = ttk.Entry(
            self.file_frame, textvariable=self.strvar_input_file_path, width=35
        )
        self.input_path_entry.grid(
            column=1,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        file_frame_line_number += 1

        output_folder_label = ttk.Button(
            self.file_frame, text="Output folder", command=self.choose_output_folder
        )
        output_folder_label.grid(
            column=0,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.output_path_entry = ttk.Entry(
            self.file_frame, textvariable=self.strvar_output_file_path, width=40
        )
        self.output_path_entry.grid(
            column=1,
            row=file_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __setup_device_frame(self):
        """Set up the device frame"""
        self.conversion_tab_left_part_line_num += 1

        self.device_frame = ttk.Labelframe(
            self.conversion_tab, text="Device", width=self.half_width_screen, height=80
        )
        self.device_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.device_frame.grid_propagate(False)

        device_frame_line_number = 0

        device_label = ttk.Label(self.device_frame, text="Device")
        device_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.device_combobox = ttk.Combobox(
            self.device_frame, textvariable=self.strvar_device, width=25
        )
        self.device_combobox["values"] = list(self.device_choice_map.values())
        self.device_combobox.current(0)
        self.device_combobox.bind("<<ComboboxSelected>>", self.gui_device_unit_cbox)
        self.device_combobox.grid(
            column=1,
            columnspan=3,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.unit_label = ttk.Label(self.device_frame, text="Unit")
        self.unit_label.grid(
            column=4,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.unit_combobox = ttk.Combobox(
            self.device_frame, textvariable=self.strvar_screen_unit, width=20
        )
        self.unit_combobox["values"] = list(self.unit_choice_map.values())
        self.unit_combobox.current(0)
        self.unit_combobox.bind("<<ComboboxSelected>>", self.gui_device_unit_cbox)
        self.unit_combobox.grid(
            column=5,
            columnspan=3,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        device_frame_line_number += 1

        self.device_width_label = ttk.Label(self.device_frame, text="Width")
        self.device_width_label.grid(
            column=0,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.device_width_spinbox = ttk.Spinbox(
            self.device_frame,
            from_=self.device_width_min_value,
            to=self.device_width_max_value,
            increment=1,
            textvariable=self.strvar_device_screen_width,
            command=self.gui_width_height,
            width=6,
        )
        self.device_width_spinbox.grid(
            column=1,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.device_height_label = ttk.Label(self.device_frame, text="Height")
        self.device_height_label.grid(
            column=2,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.device_height_spinbox = ttk.Spinbox(
            self.device_frame,
            from_=self.device_height_min_value,
            to=self.device_height_max_value,
            increment=1,
            textvariable=self.strvar_device_screen_height,
            command=self.gui_width_height,
            width=6,
        )
        self.device_height_spinbox.grid(
            column=3,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.dpi_check_button = ttk.Checkbutton(
            self.device_frame,
            text="DPI",
            variable=self.is_dpi_checked,
            command=self.gui_dpi,
        )
        self.dpi_check_button.grid(
            column=4,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.device_dpi_spinbox = ttk.Spinbox(
            self.device_frame,
            from_=self.device_dpi_min_value,
            to=self.device_dpi_max_value,
            increment=1,
            textvariable=self.strvar_device_screen_dpi,
            command=self.gui_dpi,
            width=6,
        )
        self.device_dpi_spinbox.grid(
            column=5,
            row=device_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __setup_margin_and_cropboxes_frame(self):
        """Set up the cropbax and margin frame"""
        self.conversion_tab_left_part_line_num += 1

        self.margin_and_cropboxes_frame = ttk.Labelframe(
            self.conversion_tab,
            text="Margin & cropboxes",
            width=self.half_width_screen,
            height=223,
        )
        self.margin_and_cropboxes_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.margin_and_cropboxes_frame.grid_propagate(False)

        margin_and_cropboxes_frame_line_number = 0

        self.cropmargin_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Crop Margins (in)",
        )
        self.cropmargin_label.grid(
            column=0,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropmargin_check_button = ttk.Checkbutton(
            self.margin_and_cropboxes_frame,
            variable=self.is_cropmargin_checked,
            command=self.gui_crop_margin,
        )
        self.cropmargin_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.left_cropmargin_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_left_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        self.left_cropmargin_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.top_cropmargin_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_top_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        self.top_cropmargin_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.width_cropmargin_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_width_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        self.width_cropmargin_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_cropmargin_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_height_cropmargin,
            command=self.gui_crop_margin,
            width=4,
        )
        self.height_cropmargin_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropmargin_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="(left, top, right, bottom)",
        )
        self.cropmargin_label.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        margin_and_cropboxes_frame_line_number += 1
        whitespace_label = ttk.Label(self.margin_and_cropboxes_frame, text="")
        whitespace_label.grid(column=1, row=margin_and_cropboxes_frame_line_number)
        margin_and_cropboxes_frame_line_number += 1

        self.cropbox_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Crop Areas (in)",
        )
        self.cropbox_label.grid(
            column=0,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        cropaera_left_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Left",
        )
        cropaera_left_label.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        cropaera_top_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Top",
        )
        cropaera_top_label.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        cropaera_width_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Width",
        )
        cropaera_width_label.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        cropaera_height_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Height",
        )
        cropaera_height_label.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        cropaera_page_range_label = ttk.Label(
            self.margin_and_cropboxes_frame,
            text="Page range",
            anchor=tk.CENTER,
        )
        cropaera_page_range_label.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        margin_and_cropboxes_frame_line_number += 1

        self.cropbox1_check_button = ttk.Checkbutton(
            self.margin_and_cropboxes_frame,
            variable=self.is_cropbox_1_checked,
            command=self.gui_cropbox1_margin,
        )
        self.cropbox1_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.left_cropbox1_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_1,
            command=self.gui_cropbox1_margin,
            width=4,
        )
        self.left_cropbox1_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.top_cropbox1_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_1,
            command=self.gui_cropbox1_margin,
            width=4,
        )
        self.top_cropbox1_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.width_cropbox1_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_1,
            command=self.gui_cropbox1_margin,
            width=4,
        )
        self.width_cropbox1_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_cropbox1_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_1,
            command=self.gui_cropbox1_margin,
            width=4,
        )
        self.height_cropbox1_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropbox1_page_range_entry = ttk.Entry(
            self.margin_and_cropboxes_frame,
            textvariable=self.strvar_page_range_cropbox_1,
            validate="focusout",
            validatecommand=self.gui_cropbox1_margin,
            width=13,
        )
        self.cropbox1_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        margin_and_cropboxes_frame_line_number += 1

        self.cropbox2_check_button = ttk.Checkbutton(
            self.margin_and_cropboxes_frame,
            variable=self.is_cropbox_2_checked,
            command=self.gui_cropbox2_margin,
        )
        self.cropbox2_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.left_cropbox2_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_2,
            command=self.gui_cropbox2_margin,
            width=4,
        )
        self.left_cropbox2_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.top_cropbox2_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_2,
            command=self.gui_cropbox2_margin,
            width=4,
        )
        self.top_cropbox2_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.width_cropbox2_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_2,
            command=self.gui_cropbox2_margin,
            width=4,
        )
        self.width_cropbox2_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_cropbox2_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_2,
            command=self.gui_cropbox2_margin,
            width=4,
        )
        self.height_cropbox2_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropbox2_page_range_entry = ttk.Entry(
            self.margin_and_cropboxes_frame,
            textvariable=self.strvar_page_range_cropbox_2,
            validate="focusout",
            validatecommand=self.gui_cropbox2_margin,
            width=13,
        )
        self.cropbox2_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        margin_and_cropboxes_frame_line_number += 1

        self.cropbox3_check_button = ttk.Checkbutton(
            self.margin_and_cropboxes_frame,
            variable=self.is_cropbox_3_checked,
            command=self.gui_cropbox3_margin,
        )
        self.cropbox3_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.left_cropbox3_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_3,
            command=self.gui_cropbox3_margin,
            width=4,
        )
        self.left_cropbox3_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.top_cropbox3_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_3,
            command=self.gui_cropbox3_margin,
            width=4,
        )
        self.top_cropbox3_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.width_cropbox3_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_3,
            command=self.gui_cropbox3_margin,
            width=4,
        )
        self.width_cropbox3_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_cropbox3_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_3,
            command=self.gui_cropbox3_margin,
            width=4,
        )
        self.height_cropbox3_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropbox3_page_range_entry = ttk.Entry(
            self.margin_and_cropboxes_frame,
            textvariable=self.strvar_page_range_cropbox_3,
            validate="focusout",
            validatecommand=self.gui_cropbox3_margin,
            width=13,
        )
        self.cropbox3_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        margin_and_cropboxes_frame_line_number += 1

        self.cropbox4_check_button = ttk.Checkbutton(
            self.margin_and_cropboxes_frame,
            variable=self.is_cropbox_4_checked,
            command=self.gui_cropbox4_margin,
        )
        self.cropbox4_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.left_cropbox4_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_4,
            command=self.gui_cropbox4_margin,
            width=4,
        )
        self.left_cropbox4_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.top_cropbox4_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_4,
            command=self.gui_cropbox4_margin,
            width=4,
        )
        self.top_cropbox4_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.width_cropbox4_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_4,
            command=self.gui_cropbox4_margin,
            width=4,
        )
        self.width_cropbox4_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_cropbox4_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_4,
            command=self.gui_cropbox4_margin,
            width=4,
        )
        self.height_cropbox4_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropbox4_page_range_entry = ttk.Entry(
            self.margin_and_cropboxes_frame,
            textvariable=self.strvar_page_range_cropbox_4,
            validate="focusout",
            validatecommand=self.gui_cropbox4_margin,
            width=13,
        )
        self.cropbox4_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        margin_and_cropboxes_frame_line_number += 1

        self.cropbox5_check_button = ttk.Checkbutton(
            self.margin_and_cropboxes_frame,
            variable=self.is_cropbox_5_checked,
            command=self.gui_cropbox5_margin,
        )
        self.cropbox5_check_button.grid(
            column=1,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.left_cropbox5_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_left_cropbox_5,
            command=self.gui_cropbox5_margin,
            width=4,
        )
        self.left_cropbox5_spinbox.grid(
            column=2,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.top_cropbox5_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_top_cropbox_5,
            command=self.gui_cropbox5_margin,
            width=4,
        )
        self.top_cropbox5_spinbox.grid(
            column=3,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.width_cropbox5_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_width_cropbox_5,
            command=self.gui_cropbox5_margin,
            width=4,
        )
        self.width_cropbox5_spinbox.grid(
            column=4,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.height_cropbox5_spinbox = ttk.Spinbox(
            self.margin_and_cropboxes_frame,
            from_=self.margin_and_crop_areas_min_value,
            to=self.margin_and_crop_areas_max_value,
            increment=0.1,
            textvariable=self.strvar_height_cropbox_5,
            command=self.gui_cropbox5_margin,
            width=4,
        )
        self.height_cropbox5_spinbox.grid(
            column=5,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.cropbox5_page_range_entry = ttk.Entry(
            self.margin_and_cropboxes_frame,
            textvariable=self.strvar_page_range_cropbox_5,
            validate="focusout",
            validatecommand=self.gui_cropbox5_margin,
            width=13,
        )
        self.cropbox5_page_range_entry.grid(
            column=6,
            row=margin_and_cropboxes_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __setup_parameters_frame(self):
        """Draw the parameters frame and its widgets"""
        self.conversion_tab_left_part_line_num += 1

        self.parameters_frame = ttk.Labelframe(
            self.conversion_tab,
            text="Parameters & options",
            width=self.half_width_screen,
            height=290,
        )
        self.parameters_frame.grid(
            column=self.conversion_tab_left_part_column_num,
            row=self.conversion_tab_left_part_line_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.parameters_frame.grid_propagate(False)

        parameters_frame_line_number = 0

        conversion_mode_label = ttk.Label(self.parameters_frame, text="Conversion Mode")
        conversion_mode_label.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.mode_combobox = ttk.Combobox(
            self.parameters_frame, textvariable=self.strvar_conversion_mode, width=10
        )
        self.mode_combobox["values"] = list(self.mode_choice_map.values())
        self.mode_combobox.current(0)
        self.mode_combobox.bind("<<ComboboxSelected>>", self.gui_mode_cbox)
        self.mode_combobox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        # parameters_frame_line_number += 1

        page_number_label = ttk.Label(self.parameters_frame, text="Pages to Convert")
        page_number_label.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.page_number_entry = ttk.Entry(
            self.parameters_frame,
            textvariable=self.strvar_page_numbers,
            validate="focusout",
            validatecommand=self.validate_and_update_page_nums,
            width=13,
        )
        self.page_number_entry.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.max_column_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Maximum Columns",
            variable=self.is_column_num_checked,
            command=self.gui_column_num,
        )
        self.max_column_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.max_column_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=self.max_column_min_value,
            to=self.max_column_max_value,
            increment=1,
            textvariable=self.strvar_column_num,
            command=self.gui_column_num,
            width=4,
        )
        self.max_column_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.landscape_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Output in Landscape",
            variable=self.is_landscape_checked,
            command=self.gui_validate_landscape,
        )
        self.landscape_check_button.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.landscapepage_number_entry = ttk.Entry(
            self.parameters_frame,
            textvariable=self.strvar_landscape_pages,
            validate="focusout",
            validatecommand=self.gui_validate_landscape,
            width=13,
        )
        self.landscapepage_number_entry.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.resolution_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Document Resolution Factor",
            variable=self.is_resolution_multipler_checked,
            command=self.gui_document_resolution_multipler,
        )
        self.resolution_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.resolution_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=self.document_resolution_factor_min_value,
            to=self.document_resolution_factor_max_value,
            increment=0.1,
            textvariable=self.strvar_resolution_multiplier,
            command=self.gui_document_resolution_multipler,
            width=4,
        )
        self.resolution_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        # checkbox with value options
        # parameters_frame_line_number += 1

        self.fixed_font_size_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Fixed Output Font Size",
            variable=self.is_fixed_font_size_checked,
            command=self.gui_fixed_font_size,
        )
        self.fixed_font_size_check_button.grid(
            column=2,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.fixed_font_size_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=self.fixed_font_size_min_value,
            to=self.fixed_font_size_max_value,
            increment=1,
            textvariable=self.strvar_fixed_font_size,
            command=self.gui_fixed_font_size,
            width=4,
        )
        self.fixed_font_size_spinbox.grid(
            column=3,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.smart_line_break_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Smart Line Breaks",
            variable=self.is_smart_linebreak_checked,
            command=self.gui_line_break,
        )
        self.smart_line_break_check_button.grid(
            column=0,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.smart_line_break_spinbox = ttk.Spinbox(
            self.parameters_frame,
            from_=self.smart_line_break_min_value,
            to=self.smart_line_break_max_value,
            increment=0.01,
            textvariable=self.strvar_linebreak_space,
            command=self.gui_line_break,
            width=5,
        )
        self.smart_line_break_spinbox.grid(
            column=1,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        option_frame_left_part_col_num = 0
        parameters_frame_line_number += 1
        save_parameters_frame_line_number = parameters_frame_line_number

        self.autostraighten_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Autostraighten",
            variable=self.is_autostraighten_checked,
            command=self.gui_auto_straighten,
        )
        self.autostraighten_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.break_after_source_page_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Break after each source page",
            variable=self.is_break_page_checked,
            command=self.gui_break_page,
        )
        self.break_after_source_page_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.color_output_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Color Output",
            variable=self.is_coloroutput_checked,
            command=self.gui_color_output,
        )
        self.color_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.native_pdf_output_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Native PDF output",
            variable=self.is_native_pdf_checked,
            command=self.gui_native_pdf,
        )
        self.native_pdf_output_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.avoid_text_overlap_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Avoid text selection overlap",
            variable=self.is_avoid_overlap_checked,
            command=self.gui_avoid_text_selection_overlap,
        )
        self.avoid_text_overlap_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.post_process_ghostscript_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Post process w/GhostScript",
            variable=self.is_ghostscript_postprocessing_checked,
            command=self.gui_post_gs,
        )
        self.post_process_ghostscript_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.generate_markup_source_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Generate marked-up source",
            variable=self.is_markedup_source_checked,
            command=self.gui_marked_source,
        )
        self.generate_markup_source_check_button.grid(
            column=option_frame_left_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        option_frame_right_part_col_num = 2
        parameters_frame_line_number = save_parameters_frame_line_number

        self.reflow_text_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Re-flow text",
            variable=self.is_reflow_text_checked,
            command=self.gui_reflow_text,
        )
        self.reflow_text_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.erase_vline_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Erase vertical lines",
            variable=self.is_erase_vertical_line_checked,
            command=self.gui_erase_vertical_line,
        )
        self.erase_vline_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.erase_hline_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Erase horizontal lines",
            variable=self.is_erase_horizontal_line_checked,
            command=self.gui_erase_horizontal_line,
        )
        self.erase_hline_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.fast_preview_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Fast preview",
            variable=self.is_fast_preview_checked,
            command=self.gui_fast_preview,
        )
        self.fast_preview_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.right_to_left_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Right-to-left text",
            variable=self.is_right_to_left_checked,
            command=self.gui_right_to_left,
        )
        self.right_to_left_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        parameters_frame_line_number += 1

        self.ignore_defect_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Ignore small defects",
            variable=self.is_ignore_small_defects_checked,
            command=self.gui_ignore_small_defect,
        )
        self.ignore_defect_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        parameters_frame_line_number += 1

        self.autocrop_check_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Auto-Crop",
            variable=self.is_autocrop_checked,
            command=self.gui_auto_crop,
        )
        self.autocrop_check_button.grid(
            column=option_frame_right_part_col_num,
            row=parameters_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __setup_tesseract_frame(self):
        """Set up the tesseract options frame and draw its widgets"""
        self.conversion_tab_left_part_line_num += 1

        self.tesseract_frame = ttk.Labelframe(
            self.conversion_tab,
            text="Tesseract",
            width=self.half_width_screen,
            height=20,
        )
        self.tesseract_frame.grid(
            column=0,
            row=self.conversion_tab_left_part_line_num,
            # rowspan=3,
            sticky=tk.N + tk.S + tk.E + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.tesseract_frame.grid_propagate(False)

        tesseract_frame_line_number = 1

        self.ocr_check_button = ttk.Checkbutton(
            self.tesseract_frame,
            text="Tesseract (OCR)",
            variable=self.is_tesseract_checked,
            command=self.gui_ocr_and_cpu,
        )
        self.ocr_check_button.grid(
            column=0,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.ocr_cpu_spinbox = ttk.Spinbox(
            self.tesseract_frame,
            from_=self.ocr_cpu_min_value,
            to=self.ocr_cpu_max_value,
            increment=1,
            # text='CPU %',
            textvariable=self.strvar_ocr_cpu_percentage,
            command=self.gui_ocr_and_cpu,
            width=4,
        )
        self.ocr_cpu_spinbox.grid(
            column=1,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.tesseract_fast_check_button = ttk.Checkbutton(
            self.tesseract_frame,
            text="Fast",
            variable=self.is_tesseract_fast_checked,
            command=self.gui_tesseract_fast,
        )
        self.tesseract_fast_check_button.grid(
            column=2,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        tesseract_frame_line_number += 1

        self.tesseract_language_label = ttk.Label(
            self.tesseract_frame, text="Language"
        )
        self.tesseract_language_label.grid(
            column=0,
            row=tesseract_frame_line_number,
            rowspan=2,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.tesseract_language = ttk.Combobox(
            self.tesseract_frame, textvariable=self.strvar_tesseract_language, width=22
        )
        self.tesseract_language["values"] = list(self.language_map.values())
        self.tesseract_language.current(24)
        self.tesseract_language.bind(
            "<<ComboboxSelected>>", self.gui_tesseract_language_cbox
        )
        self.tesseract_language.grid(
            column=1,
            row=tesseract_frame_line_number,
            columnspan=2,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        tesseract_frame_line_number += 1

        ocr_detection_label = ttk.Label(self.tesseract_frame, text="OCR Detection")
        ocr_detection_label.grid(
            column=0,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.ocr_detection_combobox = ttk.Combobox(
            self.tesseract_frame, textvariable=self.strvar_tesseract_detection, width=25
        )
        self.ocr_detection_combobox["values"] = list(self.ocrd_map.values())
        self.ocr_detection_combobox.current(0)
        self.ocr_detection_combobox.bind("<<ComboboxSelected>>", self.gui_tesseract_detection_cbox)
        self.ocr_detection_combobox.grid(
            column=1,
            columnspan=3,
            row=tesseract_frame_line_number,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )


    def __setup_action_frame(self):
        """Set up the action frame and draw its widgets"""
        self.conversion_tab_right_part_line_num += 1

        self.action_frame = ttk.Labelframe(self.conversion_tab, text="Actions")
        self.action_frame.grid(
            column=self.conversion_tab_right_part_column_num,
            row=self.conversion_tab_right_part_line_num,
            rowspan=3,
            sticky=tk.N + tk.S + tk.E + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_row_num = 0

        self.preview_button = ttk.Button(
            self.action_frame, text="Preview", command=self.action_preview_current_page
        )
        self.preview_button.grid(
            column=0,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.convert_button = ttk.Button(
            self.action_frame, text="Convert", command=self.action_convert_pdf
        )
        self.convert_button.grid(
            column=1,
            row=self.action_frame_row_num,
            # sticky=tk.N + tk.W,
            # pady=self.default_pady,
            # padx=self.default_padx,
        )

        self.abort_button = ttk.Button(
            self.action_frame, text="Abort", command=self.action_abort_conversion
        )
        self.abort_button.grid(
            column=2,
            row=self.action_frame_row_num,
            # sticky=tk.N + tk.W,
            # pady=self.default_pady,
            # padx=self.default_padx,
        )

        self.action_frame_row_num += 1

        self.current_preview_page_number_entry = ttk.Entry(
            self.action_frame,
            textvariable=self.strvar_current_preview_page_num,
            width=100,
        )
        self.current_preview_page_number_entry.grid(
            column=0,
            row=self.action_frame_row_num,
            columnspan=3,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_column_num = 0
        self.action_frame_row_num += 1

        self.first_button = ttk.Button(
            self.action_frame, text="<<", command=self.action_ten_page_up
        )
        self.first_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.action_frame_column_num += 1

        self.previous_button = ttk.Button(
            self.action_frame, text="<", command=self.action_page_up
        )
        self.previous_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.action_frame_column_num += 1

        self.next_button = ttk.Button(
            self.action_frame, text=">", command=self.action_page_down
        )
        self.next_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )
        self.action_frame_column_num += 1

        self.last_button = ttk.Button(
            self.action_frame, text=">>", command=self.action_ten_page_down
        )
        self.last_button.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.action_frame_column_num += 1
        self.action_frame_row_num += 1

        self.preview_canvas = tk.Canvas(self.action_frame, bd=0)
        self.preview_canvas.grid(
            column=0,
            columnspan=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.S + tk.E + tk.W,
        )

        x_scrollbar = ttk.Scrollbar(
            self.action_frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview
        )
        x_scrollbar.grid(
            column=0,
            row=self.action_frame_row_num + 1,
            columnspan=self.action_frame_column_num,
            sticky=tk.E + tk.W,
        )

        y_scrollbar = ttk.Scrollbar(
            self.action_frame, command=self.preview_canvas.yview
        )
        y_scrollbar.grid(
            column=self.action_frame_column_num,
            row=self.action_frame_row_num,
            sticky=tk.N + tk.S,
        )

        self.preview_canvas.configure(xscrollcommand=x_scrollbar.set)
        self.preview_canvas.configure(yscrollcommand=y_scrollbar.set)
        self.preview_canvas.bind("<MouseWheel>", self.yscroll_canvas)
        self.preview_canvas.bind("<Shift-MouseWheel>", self.xscroll_canvas)

    def __fill_logs_tab(self):
        """Fill the Log tab with widget"""
        self.stdout_frame = ttk.Labelframe(self.logs_tab, text="k2pdfopt STDOUT:")
        self.stdout_frame.pack(expand=1, fill="both")
        self.stdout_frame.columnconfigure(0, weight=1)
        self.stdout_frame.rowconfigure(1, weight=1)

        self.stdout_text = scrolledtext.ScrolledText(
            self.stdout_frame, state=tk.DISABLED, wrap="word"
        )
        self.stdout_text.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.clear_button = ttk.Button(
            self.stdout_frame, text="Clear", command=self.__clear_logs
        )
        self.clear_button.grid(
            column=0,
            row=1,
            sticky=tk.N + tk.E,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __setup_command_line_frame(self):
        """Set up the `command line` frame and draw its widgets"""
        self.conversion_tab_right_part_line_num += 1

        self.information_frame = ttk.Labelframe(
            self.conversion_tab, text="Command-line Options"
        )
        self.information_frame.grid(
            column=self.conversion_tab_right_part_column_num,
            row=self.conversion_tab_right_part_line_num,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

        self.command_arguments_entry = ttk.Entry(
            self.information_frame, textvariable=self.strvar_command_args, width=80
        )
        self.command_arguments_entry.bind("<Button-1>", self.gui_cmd_args)
        self.command_arguments_entry.grid(
            column=0,
            row=0,
            sticky=tk.N + tk.W,
            pady=self.default_pady,
            padx=self.default_padx,
        )

    def __initialize(self):
        """Simulate a click on every field : execute all the binded method

            TODO: rename `validate_and_update_page_nums` to `gui_validate_and_update_page_nums`
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

        device_arg = self.k2pdfopt_command_args.pop(self.device_arg_name, None)
        if device_arg is None:
            width_arg = self.k2pdfopt_command_args.pop(self.device_width_arg_name, None)
            height_arg = self.k2pdfopt_command_args.pop(
                self.device_height_arg_name, None
            )

        mode_arg = self.k2pdfopt_command_args.pop(self.conversion_mode_arg_name, None)
        if mode_arg is not None:
            arg_list = [mode_arg] + list(self.k2pdfopt_command_args.values())
            self.k2pdfopt_command_args[self.conversion_mode_arg_name] = mode_arg
        else:
            arg_list = list(self.k2pdfopt_command_args.values())

        if device_arg is not None:
            arg_list.append(device_arg)
            self.k2pdfopt_command_args[self.device_arg_name] = device_arg
        elif width_arg is not None and height_arg is not None:
            arg_list.append(width_arg)
            arg_list.append(height_arg)
            self.k2pdfopt_command_args[self.device_width_arg_name] = width_arg
            self.k2pdfopt_command_args[self.device_height_arg_name] = height_arg

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

    def menu_open_pdf_file(self):
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

    def choose_output_folder(self):
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
                    if key != self.output_path_arg_name:
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
            device_type = self.device_argument_map[self.device_combobox.current()]
            arg = self.device_arg_name + " " + device_type
            self.__add_or_update_command_argument(self.device_arg_name, arg)
            self.__remove_command_argument(self.device_width_arg_name)
            self.__remove_command_argument(self.device_height_arg_name)
            self.strvar_device_screen_width.set(
                self.device_width_height_dpi_info[self.device_combobox.current()][0]
            )
            self.strvar_device_screen_height.set(
                self.device_width_height_dpi_info[self.device_combobox.current()][1]
            )
            self.strvar_device_screen_dpi.set(
                self.device_width_height_dpi_info[self.device_combobox.current()][2]
            )
        else:  # "Other type" chosen
            screen_unit = self.unit_argument_map[self.unit_combobox.current()]

            width = self.strvar_device_screen_width.get().strip()
            if tools.is_acceptable_number(
                width, "int", self.device_width_min_value, self.device_width_max_value
            ):
                width_arg = self.device_width_arg_name + " " + width + screen_unit
                self.__add_or_update_command_argument(
                    self.device_width_arg_name, width_arg
                )
            else:
                self.__remove_command_argument(self.device_width_arg_name)

            height = self.strvar_device_screen_height.get().strip()
            if tools.is_acceptable_number(
                width, "int", self.device_height_min_value, self.device_height_max_value
            ):
                height_arg = self.device_height_arg_name + " " + height + screen_unit
                self.__add_or_update_command_argument(
                    self.device_height_arg_name, height_arg
                )
            else:
                self.__remove_command_argument(self.device_height_arg_name)

            self.__remove_command_argument(self.device_arg_name)

    def gui_mode_cbox(self, binded_event=None):  # pylint: disable=unused-argument
        """Manage `Mode` options"""
        conversion_mode = self.mode_argument_map[self.mode_combobox.current()]
        arg = self.conversion_mode_arg_name + " " + conversion_mode
        self.__add_or_update_command_argument(self.conversion_mode_arg_name, arg)

    def gui_cmd_args(self, binded_event=None):  # pylint: disable=unused-argument
        """update the k2pdfopt command-line"""
        self.__update_command_argument_entry_strvar()

    def gui_column_num(self):
        """Manage `Max Column` options"""
        nb_column = self.strvar_column_num.get().strip()
        if self.is_column_num_checked.get() and tools.is_acceptable_number(
            nb_column, "int", self.max_column_min_value, self.max_column_min_value
        ):
            arg = self.column_num_arg_name + " " + nb_column
            self.__add_or_update_command_argument(self.column_num_arg_name, arg)
        else:
            self.__remove_command_argument(self.column_num_arg_name)

    def gui_document_resolution_multipler(self):
        """Manage `Document Resolution Factor` options"""
        multiplier = self.strvar_resolution_multiplier.get().strip()
        if self.is_resolution_multipler_checked.get() and tools.is_acceptable_number(
            multiplier,
            "float",
            self.document_resolution_factor_min_value,
            self.document_resolution_factor_max_value,
        ):
            arg = self.resolution_multiplier_arg_name + " " + multiplier
            self.__add_or_update_command_argument(
                self.resolution_multiplier_arg_name, arg
            )
        else:
            self.__remove_command_argument(self.resolution_multiplier_arg_name)

    def gui_crop_margin(self):
        """Manage `Crop Margin` option

        Remarks:
            - conflict with `Auto-Crop` option
            - conflict with `Cropboxes` options
        """

        if self.is_cropmargin_checked.get():
            self.is_autocrop_checked.set(False)
            self.__remove_command_argument(self.auto_crop_arg_name)
            self.is_cropbox_1_checked.set(False)
            self.__remove_command_argument(self.cropbox_1_arg_name)
            self.is_cropbox_2_checked.set(False)
            self.__remove_command_argument(self.cropbox_2_arg_name)
            self.is_cropbox_3_checked.set(False)
            self.__remove_command_argument(self.cropbox_3_arg_name)
            self.is_cropbox_4_checked.set(False)
            self.__remove_command_argument(self.cropbox_4_arg_name)
            self.is_cropbox_5_checked.set(False)
            self.__remove_command_argument(self.cropbox_5_arg_name)

            if len(self.strvar_left_cropmargin.get().strip()) > 0:
                arg = (
                    self.crop_margin_left_arg_name
                    + " "
                    + self.strvar_left_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    self.crop_margin_left_arg_name, arg
                )

            if len(self.strvar_top_cropmargin.get().strip()) > 0:
                arg = (
                    self.crop_margin_top_arg_name
                    + " "
                    + self.strvar_top_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    self.crop_margin_top_arg_name, arg
                )

            if len(self.strvar_width_cropmargin.get().strip()) > 0:
                arg = (
                    self.crop_margin_right_arg_name
                    + " "
                    + self.strvar_width_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    self.crop_margin_right_arg_name, arg
                )

            if len(self.strvar_height_cropmargin.get().strip()) > 0:
                arg = (
                    self.crop_margin_bottom_arg_name
                    + " "
                    + self.strvar_height_cropmargin.get().strip()
                )
                self.__add_or_update_command_argument(
                    self.crop_margin_bottom_arg_name, arg
                )
        else:
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)

    def gui_cropbox1_margin(self):
        """Manage `Cropbox 1` options"""
        page_range = self.strvar_page_range_cropbox_1.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            # self.__remove_command_argument(self.cropbox_arg_name)
            self.strvar_page_range_cropbox_1.set("")
            messagebox.showerror(
                message="Invalide cropbox 1's page range. It should be like : 2-5e,3-7o,9-"
            )
            return

        if self.is_cropbox_1_checked.get():
            self.is_cropmargin_checked.set(False)
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)

            # page_range_arg = self.strvar_crop_page_range.get().strip()
            cropbox_value = [
                self.strvar_left_cropbox_1.get(),
                self.strvar_top_cropbox_1.get(),
                self.strvar_width_cropbox_1.get(),
                self.strvar_height_cropbox_1.get(),
            ]
            arg = (
                # no space between -cbox and page range
                self.cropbox_arg_name
                + page_range
                + " "
                + ",".join(map(str.strip, cropbox_value))
            )
            self.__add_or_update_command_argument(self.cropbox_1_arg_name, arg)
        else:
            self.__remove_command_argument(self.cropbox_1_arg_name)

    def gui_cropbox2_margin(self):
        """Manage `Cropbox 2` options"""
        page_range = self.strvar_page_range_cropbox_2.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            # self.__remove_command_argument(self.cropbox_arg_name)
            self.strvar_page_range_cropbox_2.set("")
            messagebox.showerror(
                message="Invalide cropbox 2's page range. It should be like : 2-5e,3-7o,9-"
            )
            return

        if self.is_cropbox_2_checked.get():
            self.is_cropmargin_checked.set(False)
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)

            # page_range_arg = self.strvar_crop_page_range.get().strip()
            cropbox_value = [
                self.strvar_left_cropbox_2.get(),
                self.strvar_top_cropbox_2.get(),
                self.strvar_width_cropbox_2.get(),
                self.strvar_height_cropbox_2.get(),
            ]
            arg = (
                # no space between -cbox and page range
                self.cropbox_arg_name
                + page_range
                + " "
                + ",".join(map(str.strip, cropbox_value))
            )
            self.__add_or_update_command_argument(self.cropbox_2_arg_name, arg)
        else:
            self.__remove_command_argument(self.cropbox_2_arg_name)

    def gui_cropbox3_margin(self):
        """Manage `Cropbox 3` options"""
        page_range = self.strvar_page_range_cropbox_3.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            # self.__remove_command_argument(self.cropbox_arg_name)
            self.strvar_page_range_cropbox_3.set("")
            messagebox.showerror(
                message="Invalide cropbox 3's page range. It should be like : 2-5e,3-7o,9-"
            )
            return

        if self.is_cropbox_3_checked.get():
            self.is_cropmargin_checked.set(False)
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)

            # page_range_arg = self.strvar_crop_page_range.get().strip()
            cropbox_value = [
                self.strvar_left_cropbox_3.get(),
                self.strvar_top_cropbox_3.get(),
                self.strvar_width_cropbox_3.get(),
                self.strvar_height_cropbox_3.get(),
            ]
            arg = (
                # no space between -cbox and page range
                self.cropbox_arg_name
                + page_range
                + " "
                + ",".join(map(str.strip, cropbox_value))
            )
            self.__add_or_update_command_argument(self.cropbox_3_arg_name, arg)
        else:
            self.__remove_command_argument(self.cropbox_3_arg_name)

    def gui_cropbox4_margin(self):
        """Manage `Cropbox 4` options"""
        page_range = self.strvar_page_range_cropbox_4.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            # self.__remove_command_argument(self.cropbox_arg_name)
            self.strvar_page_range_cropbox_4.set("")
            messagebox.showerror(
                message="Invalide cropbox 4's page range. It should be like : 2-5e,3-7o,9-"
            )
            return

        if self.is_cropbox_4_checked.get():
            self.is_cropmargin_checked.set(False)
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)

            # page_range_arg = self.strvar_crop_page_range.get().strip()
            cropbox_value = [
                self.strvar_left_cropbox_4.get(),
                self.strvar_top_cropbox_4.get(),
                self.strvar_width_cropbox_4.get(),
                self.strvar_height_cropbox_4.get(),
            ]
            arg = (
                # no space between -cbox and page range
                self.cropbox_arg_name
                + page_range
                + " "
                + ",".join(map(str.strip, cropbox_value))
            )
            self.__add_or_update_command_argument(self.cropbox_4_arg_name, arg)
        else:
            self.__remove_command_argument(self.cropbox_4_arg_name)

    def gui_cropbox5_margin(self):
        """Manage `Cropbox 5` options"""
        page_range = self.strvar_page_range_cropbox_5.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):
            # self.__remove_command_argument(self.cropbox_arg_name)
            self.strvar_page_range_cropbox_5.set("")
            messagebox.showerror(
                message="Invalide cropbox 5's page range. It should be like : 2-5e,3-7o,9-"
            )
            return

        if self.is_cropbox_5_checked.get():
            self.is_cropmargin_checked.set(False)
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)

            # page_range_arg = self.strvar_crop_page_range.get().strip()
            cropbox_value = [
                self.strvar_left_cropbox_5.get(),
                self.strvar_top_cropbox_5.get(),
                self.strvar_width_cropbox_5.get(),
                self.strvar_height_cropbox_5.get(),
            ]
            arg = (
                # no space between -cbox and page range
                self.cropbox_arg_name
                + page_range
                + " "
                + ",".join(map(str.strip, cropbox_value))
            )
            self.__add_or_update_command_argument(self.cropbox_5_arg_name, arg)
        else:
            self.__remove_command_argument(self.cropbox_5_arg_name)

    def gui_dpi(self):
        """Manage device's `DPI` option"""
        dpi_value = self.strvar_device_screen_dpi.get().strip()
        if self.is_dpi_checked.get() and tools.is_acceptable_number(
            dpi_value, "int", self.device_dpi_min_value, self.device_dpi_max_value
        ):
            arg = self.dpi_arg_name + " " + dpi_value
            self.__add_or_update_command_argument(self.dpi_arg_name, arg)
        else:
            self.__remove_command_argument(self.dpi_arg_name)

    def validate_and_update_page_nums(self):
        """Update the command-line with page range if it's a valid range"""
        if len(
            self.strvar_page_numbers.get().strip()
        ) > 0 and not tools.check_page_nums(self.strvar_page_numbers.get().strip()):

            self.__remove_command_argument(self.page_num_arg_name)
            self.strvar_page_numbers.set("")
            messagebox.showerror(
                message="Invalide Page Argument. It should be like: 2-5e,3-7o,9-"
            )
            return False

        if len(self.strvar_page_numbers.get().strip()) > 0:
            arg = self.page_num_arg_name + " " + self.strvar_page_numbers.get().strip()
            self.__add_or_update_command_argument(self.page_num_arg_name, arg)
        else:
            self.__remove_command_argument(self.page_num_arg_name)

        return True

    def gui_fixed_font_size(self):
        """Manage `Fixed output font size` option"""
        font_size = self.strvar_fixed_font_size.get().strip()
        if self.is_fixed_font_size_checked.get() and tools.is_acceptable_number(
            font_size,
            "int",
            self.fixed_font_size_min_value,
            self.fixed_font_size_max_value,
        ):
            arg = self.fixed_font_size_arg_name + " " + font_size
            self.__add_or_update_command_argument(self.fixed_font_size_arg_name, arg)
        else:
            self.__remove_command_argument(self.fixed_font_size_arg_name)

    def gui_ocr_and_cpu(self):
        """OCR CPU pourcentage management

        Remarks:
            - ocr conflicts with native pdf
            - negtive integer means percentage
        """
        if self.is_tesseract_checked.get():
            self.is_native_pdf_checked.set(False)
            self.__remove_command_argument(self.native_pdf_arg_name)
            self.__add_or_update_command_argument(self.ocr_arg_name, self.ocr_arg_name)
            ocr_cpu_arg = (
                self.ocr_cpu_arg_name
                + " -"
                + self.strvar_ocr_cpu_percentage.get().strip()
            )
            self.__add_or_update_command_argument(self.ocr_cpu_arg_name, ocr_cpu_arg)
            self.gui_tesseract_fast()
            self.gui_tesseract_language_cbox()
        else:
            self.__remove_command_argument(self.ocr_arg_name)
            self.__remove_command_argument(self.ocr_cpu_arg_name)
            self.__remove_command_argument(self.tesseract_language_arg_name)
            self.__remove_command_argument(self.tesseract_fast_arg_name)
            self.__remove_command_argument(self.tesseract_detection_arg_name)

    def gui_tesseract_fast(self):
        """Manage `Fast` option for Tesseract"""
        if self.is_tesseract_checked.get() and self.is_tesseract_fast_checked.get():
            self.__add_or_update_command_argument(self.tesseract_fast_arg_name, self.tesseract_fast_arg_name)
        else:
            self.__remove_command_argument(self.tesseract_fast_arg_name)

    def gui_tesseract_language_cbox(
        self, binded_event=None
    ):  # pylint: disable=unused-argument
        """Manage the `language` option for Tesseract"""
        if self.is_tesseract_checked.get():
            language_arg = self.language_argument_map[self.tesseract_language.current()]
            arg = self.tesseract_language_arg_name + " " + language_arg
            self.__add_or_update_command_argument(self.tesseract_language_arg_name, arg)
        else:
            self.__remove_command_argument(self.tesseract_language_arg_name)

    def gui_tesseract_detection_cbox(self, binded_event=None):
        """Manage `OCR Detection` option for Tesseract"""
        if self.is_tesseract_checked.get():
            detection_type = self.tesseract_detection_arg_name + ' ' + self.ocrd_argument_map[self.ocr_detection_combobox.current()]
            self.__add_or_update_command_argument(
                self.tesseract_detection_arg_name, detection_type
            )
        else:
            self.__remove_command_argument(self.tesseract_detection_arg_name)

    def gui_validate_landscape(self):
        """Update the command-line with landscape (page range if valid range)"""
        page_range = self.strvar_landscape_pages.get().strip()
        if len(page_range) > 0 and not tools.check_page_nums(page_range):

            self.__remove_command_argument(self.landscape_arg_name)
            self.strvar_landscape_pages.set("")
            messagebox.showerror(
                message="Invalide `Output in Landscape` Page Argument!"
            )

            return False

        if self.is_landscape_checked.get():
            arg = self.landscape_arg_name
            if len(page_range) > 0:
                arg += page_range  # no space between -ls and page numbers
            self.__add_or_update_command_argument(self.landscape_arg_name, arg)
        else:
            self.__remove_command_argument(self.landscape_arg_name)

        return True

    def gui_line_break(self):
        """Manage `Line Breack on eacht source page breack` option"""
        line_break = self.strvar_linebreak_space.get().strip()
        if self.is_smart_linebreak_checked.get() and tools.is_acceptable_number(
            line_break,
            "float",
            self.smart_line_break_min_value,
            self.smart_line_break_max_value,
        ):
            arg = self.linebreak_arg_name + " " + str(line_break)
            self.__add_or_update_command_argument(self.linebreak_arg_name, arg)
        else:
            self.__remove_command_argument(self.linebreak_arg_name)

    def gui_auto_straighten(self):
        """Manage `Auto Straighten` option"""
        if self.is_autostraighten_checked.get():
            self.__add_or_update_command_argument(
                self.auto_straignten_arg_name, self.auto_straignten_arg_name
            )
        else:
            self.__remove_command_argument(self.auto_straignten_arg_name)

    def gui_break_page(self):
        """Native PDF management

        Remarks : `break page` conflicts with `avoid overlap` since they are both -bp flag
        """
        if self.is_break_page_checked.get():
            self.is_avoid_overlap_checked.set(False)
            self.__remove_command_argument(self.break_page_avoid_overlap_arg_name)
            self.__add_or_update_command_argument(
                self.break_page_avoid_overlap_arg_name,
                self.break_page_avoid_overlap_arg_name,
            )
        else:
            self.__remove_command_argument(self.break_page_avoid_overlap_arg_name)

    def gui_color_output(self):
        """Manage `Color Output` option"""
        if self.is_coloroutput_checked.get():
            self.__add_or_update_command_argument(
                self.color_output_arg_name, self.color_output_arg_name
            )
        else:
            self.__remove_command_argument(self.color_output_arg_name)

    def gui_native_pdf(self):
        """Manage `Native PDF`option.

        Remarks: `native pdf` conflicts with 'ocr' and 'reflow text'
        """
        if self.is_native_pdf_checked.get():
            self.is_reflow_text_checked.set(False)
            self.is_tesseract_checked.set(False)
            self.__remove_command_argument(self.ocr_arg_name)
            self.__remove_command_argument(self.ocr_cpu_arg_name)
            self.__remove_command_argument(self.reflow_text_arg_name)
            self.__add_or_update_command_argument(
                self.native_pdf_arg_name, self.native_pdf_arg_name
            )
        else:
            self.__remove_command_argument(self.native_pdf_arg_name)

    def gui_right_to_left(self):
        """Manage `Right to left` option"""
        if self.is_right_to_left_checked.get():
            self.__add_or_update_command_argument(
                self.right_to_left_arg_name, self.right_to_left_arg_name
            )
        else:
            self.__remove_command_argument(self.right_to_left_arg_name)

    def gui_post_gs(self):
        """Manage `post precessing with GhostScript` option"""
        if self.is_ghostscript_postprocessing_checked.get():
            self.__add_or_update_command_argument(
                self.post_gs_arg_name, self.post_gs_arg_name
            )
        else:
            self.__remove_command_argument(self.post_gs_arg_name)

    def gui_marked_source(self):
        """Manage `Show Markup Source` option"""
        if self.is_markedup_source_checked.get():
            self.__add_or_update_command_argument(
                self.marked_source_arg_name, self.marked_source_arg_name
            )
        else:
            self.__remove_command_argument(self.marked_source_arg_name)

    def gui_reflow_text(self):
        """

        Remarks: `reflow text` conflicts with `native pdf`
        """
        if self.is_reflow_text_checked.get():
            self.is_native_pdf_checked.set(False)
            self.__remove_command_argument(self.native_pdf_arg_name)
            arg = self.reflow_text_arg_name + "+"
            self.__add_or_update_command_argument(self.reflow_text_arg_name, arg)
        else:
            self.__remove_command_argument(self.reflow_text_arg_name)

    def gui_erase_vertical_line(self):
        """Manage `Erase vertical line` option"""
        if self.is_erase_vertical_line_checked.get():
            arg = self.erase_vertical_line_arg_name + " 1"
            self.__add_or_update_command_argument(
                self.erase_vertical_line_arg_name, arg
            )
        else:
            self.__remove_command_argument(self.erase_vertical_line_arg_name)

    def gui_fast_preview(self):
        """Manage fast preview option"""
        if self.is_fast_preview_checked.get():
            arg = self.fast_preview_arg_name + " 0"
            self.__add_or_update_command_argument(self.fast_preview_arg_name, arg)
        else:
            self.__remove_command_argument(self.fast_preview_arg_name)

    def gui_avoid_text_selection_overlap(self):
        """Manage `Avoid text selection overlap` option

        Remarks: avoid overlap conflicts with break page since they are both -bp flag
        """
        if self.is_avoid_overlap_checked.get():
            self.is_break_page_checked.set(False)
            self.__remove_command_argument(self.break_page_avoid_overlap_arg_name)

            arg = self.break_page_avoid_overlap_arg_name + " m"
            self.__add_or_update_command_argument(
                self.break_page_avoid_overlap_arg_name, arg
            )
        else:
            self.__remove_command_argument(self.break_page_avoid_overlap_arg_name)

    def gui_ignore_small_defect(self):
        """Manage `ignore small defect` option"""
        if self.is_ignore_small_defects_checked.get():
            arg = self.ign_small_defects_arg_name + " 1.5"
            self.__add_or_update_command_argument(self.ign_small_defects_arg_name, arg)
        else:
            self.__remove_command_argument(self.ign_small_defects_arg_name)

    def gui_erase_horizontal_line(self):
        """Manage `Erase horizontal line` option"""
        if self.is_erase_horizontal_line_checked.get():
            arg = self.erase_horizontal_line_arg_name + " 1"
            self.__add_or_update_command_argument(
                self.erase_horizontal_line_arg_name, arg
            )
        else:
            self.__remove_command_argument(self.erase_horizontal_line_arg_name)

    def gui_auto_crop(self):
        """Manage `Auto-Crop` option.

        Remarks: conflict with `crop margin`
        """
        if self.is_autocrop_checked.get():
            self.is_cropmargin_checked.set(False)
            self.__remove_command_argument(self.cropbox_arg_name)
            self.__remove_command_argument(self.crop_margin_left_arg_name)
            self.__remove_command_argument(self.crop_margin_top_arg_name)
            self.__remove_command_argument(self.crop_margin_right_arg_name)
            self.__remove_command_argument(self.crop_margin_bottom_arg_name)
            arg = self.auto_crop_arg_name
            self.__add_or_update_command_argument(self.auto_crop_arg_name, arg)
        else:
            self.__remove_command_argument(self.auto_crop_arg_name)

    def __remove_preview_image_and_clear_canvas(self):
        """Remove the preview image and clear the preview canevas"""
        if os.path.exists(self.preview_image_path):
            os.remove(self.preview_image_path)
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
        output_arg = " ".join([self.preview_output_arg_name, str(preview_page_index)])
        self.background_future = self.convert_pdf_file(output_arg)
        self.strvar_current_preview_page_num.set("Preview Generating...")

        def preview_image_future(bgf):
            self.load_preview_image(self.preview_image_path, preview_page_index)
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
        # pdf_output_arg = self.output_path_arg_name + self.output_file_suffix + ".pdf"
        # pdf_output_arg = self.output_path_arg_name + "_k2opt_.pdf"
        pdf_output_arg = (
            self.output_path_arg_name + " %s" + self.output_file_suffix
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


class ReBook(tk.Tk):
    """Application class"""

    def __init__(self):
        super().__init__()
        self.__configure_gui()

    def __configure_gui(self):
        """Configure the application's windows"""
        self.title("Rebook v2.0ß")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry("%dx%d" % (self.width, self.height))
        self.resizable(True, True)


def check_k2pdfopt_path_exists(k2pdfopt_path):
    """Check if k2pdfopt is reachable"""
    if not os.path.exists(k2pdfopt_path):
        messagebox.showerror(
            message="Failed to find k2pdfopt, "
            + "please put it under the same directory "
            + "as rebook and then restart."
        )
        sys.exit()


if __name__ == "__main__":
    K2PDFOPT_PATH = "./k2pdfopt"
    check_k2pdfopt_path_exists(K2PDFOPT_PATH)
    rebook = ReBook()
    frame = MainFrame(rebook, K2PDFOPT_PATH)
    rebook.mainloop()
