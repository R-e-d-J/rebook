"""This modile declare all the constants for ReBook2"""

DEVICE_ARGUMENT_MAP = {
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

DEVICE_WIDTH_HEIGHT_DPI_INFO = {
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

DEVICE_CHOICE_MAP = {
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

MODE_ARGUMENT_MAP = {
    0: "def",
    1: "copy",
    2: "fp",
    3: "fw",
    4: "2col",
    5: "tm",
    6: "crop",
    7: "concat",
}

MODE_CHOICE_MAP = {
    0: "Default",
    1: "Copy",
    2: "Fit Page",
    3: "Fit Width",
    4: "2 Columns",
    5: "Trim Margins",
    6: "Crop",
    7: "Concat",
}

UNIT_ARGUMENT_MAP = {
    0: "in",
    1: "cm",
    2: "s",
    3: "t",
    4: "p",
    5: "x",
}

UNIT_CHOICE_MAP = {
    0: "Inches",
    1: "Centimeters",
    2: "Source Page Size",
    3: "Trimmed Source Region Size",
    4: "Pixels",
    5: "Relative to the OCR Text Layer",
}

LANGUAGE_ARGUMENT_MAP = {
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

LANGUAGE_MAP = {
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

OCRD_ARGUMENT_MAP = {
    0: "w",
    1: "l",
    2: "c",
    3: "p",
}

OCRD_MAP = {
    0: "word",
    1: "line",
    2: "column",
    3: "page",
}

# LIMITS
DEVICE_WIDTH_MIN_VALUE = 300
DEVICE_WIDTH_MAX_VALUE = 2500
DEVICE_HEIGHT_MIN_VALUE = 700
DEVICE_HEIGHT_MAX_VALUE = 3000
DEVICE_DPI_MIN_VALUE = 100
DEVICE_DPI_MAX_VALUE = 500
MAX_COLUMN_MIN_VALUE = 1
MAX_COLUMN_MAX_VALUE = 10
FIXED_FONT_SIZE_MIN_VALUE = 9
FIXED_FONT_SIZE_MAX_VALUE = 48
OCR_CPU_MIN_VALUE = 1
OCR_CPU_MAX_VALUE = 100
DOCUMENT_RESOLUTION_FACTOR_MIN_VALUE = 0.1
DOCUMENT_RESOLUTION_FACTOR_MAX_VALUE = 10.0
SMART_LINE_BREAK_MIN_VALUE = 0.01
SMART_LINE_BREAK_MAX_VALUE = 2.00
MARGIN_AND_CROP_AREAS_MIN_VALUE = 0
MARGIN_AND_CROP_AREAS_MAX_VALUE = 10
STRVAR_MIN_COLUMN_GAP_WIDTH_MIN_VALUE = 0.00
STRVAR_MIN_COLUMN_GAP_WIDTH_MAX_VALUE = 5.00
COLUMN_GAP_RANGE_MIN_VALUE = 0
COLUMN_GAP_RANGE_MAX_VALUE = 1
MINIMUM_COLUMN_HEIGHT_MIN_VALUE = 0.00
MINIMUM_COLUMN_HEIGHT_MAX_VALUE = 5.00
COLUMN_OFFSET_MAXIMUM_MIN_VALUE = 0.0
COLUMN_OFFSET_MAXIMUM_MAX_VALUE = 1.0
DEFAULT_PADX = 5
DEFAULT_PADY = 0

# Arguments Key
DEVICE_ARG_NAME = "-dev"  # -dev <name>
DEVICE_WIDTH_ARG_NAME = "-w"  # -w <width>[in|cm|s|t|p]
DEVICE_HEIGHT_ARG_NAME = "-h"  # -h <height>[in|cm|s|t|p|x]
CONVERSION_MODE_ARG_NAME = "-mode"  # -mode <mode>
OUTPUT_PATH_ARG_NAME = "-o"  # -o <namefmt>
OUTPUT_FILE_SUFFIX = "_k2opt.pdf"
SCREEN_UNIT_PREFIX = "-screen_unit"
COLUMN_NUM_ARG_NAME = "-col"  # -col <maxcol>
RESOLUTION_MULTIPLIER_ARG_NAME = "-dr"  # -dr <value>
CROPMARGIN_ARG_NAME = "m"
CROPBOX_ARG_NAME = "-cbox"  # -cbox[<pagelist>|u|-]
CROPBOX_1_ARG_NAME = "cbox_1"
CROPBOX_2_ARG_NAME = "cbox_2"
CROPBOX_3_ARG_NAME = "cbox_3"
CROPBOX_4_ARG_NAME = "cbox_4"
CROPBOX_5_ARG_NAME = "cbox_5"
CROP_MARGIN_LEFT_ARG_NAME = "-ml"
CROP_MARGIN_TOP_ARG_NAME = "-mt"
CROP_MARGIN_RIGHT_ARG_NAME = "-mr"
CROP_MARGIN_BOTTOM_ARG_NAME = "-mb"
DPI_ARG_NAME = "-dpi"  # -dpi <dpival>
PAGE_NUM_ARG_NAME = "-p"  # -p <pagelist>
FIXED_FONT_SIZE_ARG_NAME = "-fs"  # -fs 0/-fs <font size>[+]
OCR_ARG_NAME = "-ocr"  # -ocr-/-ocr t
TESSERACT_LANGUAGE_ARG_NAME = "-ocrlang"  # -ocrlang <lang>
TESSERACT_FAST_ARG_NAME = "-fast"
TESSERACT_DETECTION_ARG_NAME = "-ocrd"  # -ocrd w|l|c|p
OCR_CPU_ARG_NAME = "-nt"  # -nt -50/-nt <percentage>
LANDSCAPE_ARG_NAME = "-ls"  # -ls[-][pagelist]
LINEBREAK_ARG_NAME = "-ws"  # -ws <spacing>
AUTO_CROP_ARG_NAME = "-ac"  # -ac-/-ac
BREAK_PAGE_AVOID_OVERLAP_ARG_NAME = "-bp"  # -bp-/-bp
NATIVE_PDF_ARG_NAME = "-n"  # -n-/-n
COLOR_OUTPUT_ARG_NAME = "-c"  # -c-/-c
REFLOW_TEXT_ARG_NAME = "-wrap"  # -wrap+/-wrap-
FAST_PREVIEW_ARG_NAME = "-rt"  # -rt /-rt 0
RIGHT_TO_LEFT_ARG_NAME = "-r"  # -r-/-r
AUTO_STRAIGNTEN_ARG_NAME = "-as"  # -as-/-as
MARKED_SOURCE_ARG_NAME = "-sm"  # -sm-/-sm
ERASE_VERTICAL_LINE_ARG_NAME = "-evl"  # -evl 0/-evl 1
IGN_SMALL_DEFECTS_ARG_NAME = "-de"  # -de 1.0/-de 1.5
ERASE_HORIZONTAL_LINE_ARG_NAME = "-ehl"  # -ehl 0/-ehl 1
POST_GS_ARG_NAME = "-ppgs"  # -ppgs-/-ppgs
MIN_COLUMN_GAP_WIDTH_ARG_NAME = "-cg"  # -cg <inches>
MAX_GAP_BETWEEN_COLUMN_ARG_NAME = "-cgmax"
COLUMN_GAP_RANGE_ARG_NAME = "-cgr"
MINIMUM_COLUMN_HEIGHT_ARG_NAME = "-ch"
COLUMN_OFFSET_MAXIMUM_ARG_NAME = "-comax"
PREVIEW_OUTPUT_ARG_NAME = "-bmp"
PREVIEW_IMAGE_PATH = "./k2pdfopt_out.png"