#!/usr/bin/python

from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext as scrltxt
import asyncio
import glob     # a supprimer... ?
import json
import os
import subprocess as sub     # a supprimer... ?

import globals


# https://willus.com/k2pdfopt/help/
def check_page_nums(input_pages):
	page_num_list = re.split(',|-|o|e', input_pages)

	for page_num in page_num_list:
		if len(page_num) > 0 and not page_num.isdigit():
			return False
	return True


# ############################################################################################### #
# Generating k2pdfopt command line
# ############################################################################################### #
def update_cmd_arg_entry_strvar():
	global STRVAR_COMMAND_ARGS
	STRVAR_COMMAND_ARGS.set(generate_cmd_arg_str())


def add_or_update_one_cmd_arg(arg_key, arg_value):
	globals.K2PDFOPT_CMD_ARGS[arg_key] = arg_value


def remove_one_cmd_arg(arg_key):
	previous = globals.K2PDFOPT_CMD_ARGS.pop(arg_key, None)
	return previous


# ############################################################################################### #
# GUI construction
# ############################################################################################### #
root = tk.Tk()
root.title('rebook')
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.resizable(False, False)

STDOUT_TEXT = None
STRVAR_COMMAND_ARGS = tk.StringVar()
STRVAR_OUTPUT_FILE_PATH = tk.StringVar()
STRVAR_CURRENT_PREVIEW_PAGE_NUM = tk.StringVar()

k2pdfopt_path = './k2pdfopt'
custom_preset_file_path = 'rebook_preset.json'


# ############################################################################################### #
# MAIN TAB
# ############################################################################################### #
base_tab = ttk.Notebook(root)

conversion_tab = ttk.Frame(base_tab)
base_tab.add(conversion_tab, text='Conversion')

log_tab = ttk.Frame(base_tab)
base_tab.add(log_tab, text='Logs')

base_tab.pack(expand=1, fill='both')


# ############################################################################################### #
# MENU
# ############################################################################################### #
menu_bar = tk.Menu(root)
root['menu'] = menu_bar

def on_command_about_box_cb():
	about_message = \
		'''rebook

TclTk GUI for k2pdfopt by Pu Wang

The source code can be found at:
http://github.com/pwang7/rebook/rebook.py'''

	tkinter.messagebox.showinfo(message=about_message)

menu_file = tk.Menu(menu_bar)
menu_bar.add_cascade(menu=menu_file, label='File')
menu_file.add_command(label='About', command=on_command_about_box_cb)

# root.createcommand('tkAboutDialog', on_command_about_box_cb)
# root.createcommand('::tk::mac::ShowHelp', on_command_about_box_cb)

def check_k2pdfopt_path_exists():
	if not os.path.exists(k2pdfopt_path):
		tkinter.messagebox.showerror(
			message='Failed to find k2pdfopt, ' +
			'please put it under the same directory ' +
			'as rebook and then restart.'
		)
		quit()


def load_custom_preset():
	# global STRVAR_OUTPUT_FILE_PATH    # unused

	if os.path.exists(custom_preset_file_path):
		with open(custom_preset_file_path) as preset_file:
			dict_to_load = json.load(preset_file)

			if dict_to_load:
				log_string('Load Preset: ' + str(dict_to_load))
				initialize_vars(dict_to_load)
				return True

	return False


def log_string(str_line):
	global STDOUT_TEXT

	log_content = str_line.strip()

	if len(log_content) > 0:
		STDOUT_TEXT.config(state=tk.NORMAL)
		print('=== ' + log_content)  # TODO: remove print
		STDOUT_TEXT.insert(tk.END, log_content + '\n')
		STDOUT_TEXT.config(state=tk.DISABLED)


def clear_logs():
	STDOUT_TEXT.config(state=tk.NORMAL)
	STDOUT_TEXT.delete(1.0, tk.END)
	STDOUT_TEXT.config(state=tk.DISABLED)


def initialize_vars(dict_vars):

	for k, v in dict_vars.items():
		for i in range(len(v)):
			arg_var_map[k][i].set(v[i])

	for cb_func in arg_cb_map.values():
		if cb_func is not None:
			cb_func()

	update_cmd_arg_entry_strvar()	# must be after loading preset values


def restore_default_values():
	"""
		Clear logs, preview and reset all the default values

		THINKING :
		1. Not sure the next 3 for loop are necessary
		2. Why erase input and output file path ?
		3. Why not restore with the custom preset ?
			or have another button to reload custom preset ?
	"""
	clear_logs()
	remove_preview_image_and_clear_canvas()

	for sv in string_var_list:
		sv.set('')

	for bv in bool_var_list:
		bv.set(False)

	for b in combo_box_list:
		b.current(0)

	initialize_vars(default_var_map)


def start_loop(loop):
	asyncio.set_event_loop(loop)
	loop.run_forever()


thread_loop = asyncio.get_event_loop()
run_loop_thread = Thread(target=start_loop, args=(thread_loop,), daemon=True)
run_loop_thread.start()

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


def generate_cmd_arg_str():
	must_have_args = '-a- -ui- -x'
	device_arg = globals.K2PDFOPT_CMD_ARGS.pop(device_arg_name, None)

	if device_arg is None:
		width_arg = globals.K2PDFOPT_CMD_ARGS.pop(width_arg_name)
		height_arg = globals.K2PDFOPT_CMD_ARGS.pop(height_arg_name)

	mode_arg = globals.K2PDFOPT_CMD_ARGS.pop(conversion_mode_arg_name)
	arg_list = [mode_arg] + list(globals.K2PDFOPT_CMD_ARGS.values())
	globals.K2PDFOPT_CMD_ARGS[conversion_mode_arg_name] = mode_arg

	if device_arg is not None:
		arg_list.append(device_arg)
		globals.K2PDFOPT_CMD_ARGS[device_arg_name] = device_arg
	else:
		arg_list.append(width_arg)
		arg_list.append(height_arg)
		globals.K2PDFOPT_CMD_ARGS[width_arg_name] = width_arg
		globals.K2PDFOPT_CMD_ARGS[height_arg_name] = height_arg

	arg_list.append(must_have_args)
	log_string('Generate Argument List: ' + str(arg_list))
	cmd_arg_str = ' ' . join(arg_list)

	return cmd_arg_str


def convert_pdf_file(output_arg):
	check_k2pdfopt_path_exists()

	async def async_run_cmd_and_log(exec_cmd):

		executed = exec_cmd.strip()

		def log_bytes(log_btyes):
			log_string(log_btyes.decode('utf-8'))

		log_string(executed)

		p = await asyncio.create_subprocess_shell(
			executed,
			stdout=asyncio.subprocess.PIPE,
			stderr=asyncio.subprocess.PIPE,
		)
		globals.BACKGROUND_PROCESS = p

		while True:
			line = await p.stdout.readline()
			log_bytes(line)

			if not line:
				break
			if line == '' and p.returncode is not None:
				break

	input_pdf_path = strvar_input_file_path.get().strip()

	# in case the file name contains space
	if ' ' in input_pdf_path:
		input_pdf_path = '\"' + input_pdf_path + '\"'

	executed = ' '.join([k2pdfopt_path, input_pdf_path, output_arg, generate_cmd_arg_str()])
	future = asyncio.run_coroutine_threadsafe(async_run_cmd_and_log(executed), thread_loop)

	return future


def pdf_conversion_is_done():
	if (globals.BACKGROUND_FUTURE is None) or (globals.BACKGROUND_FUTURE.done()):
		if ((globals.BACKGROUND_PROCESS is None) or (globals.BACKGROUND_PROCESS.returncode is not None)):
			return True

	tkinter.messagebox.showerror(message='Background Conversion Not Finished Yet! Please Wait...')
	return False

# ############################################################################################### #
# CONVERSION TAB
# ############################################################################################### #
conversion_tab_left_part_column_num = 0
conversion_tab_left_part_row_num = -1


# ############################################################################################### #
# REQUIRED INPUTS FRAME
# ############################################################################################### #
conversion_tab_left_part_row_num += 1

device_arg_name = '-dev'            # -dev <name>
width_arg_name = '-w'               # -w <width>[in|cm|s|t|p]
height_arg_name = '-h'              # -h <height>[in|cm|s|t|p|x]
conversion_mode_arg_name = '-mode'  # -mode <mode>
output_path_arg_name = '-o'         # -o <namefmt>
output_pdf_suffix = '-output.pdf'
screen_unit_prefix = '-screen_unit'

strvar_device = tk.StringVar()
strvar_screen_unit = tk.StringVar()
strvar_screen_width = tk.StringVar()
strvar_screen_height = tk.StringVar()
strvar_input_file_path = tk.StringVar()
strvar_conversion_mode = tk.StringVar()

def on_command_open_pdf_file_cb():
	supported_formats = [('PDF files', '*.pdf'), ('DJVU files', '*.djvu')]

	filename = tkinter.filedialog.askopenfilename(
		parent=root,
		filetypes=supported_formats,
		title='Select your file',
	)

	if filename is not None and len(filename.strip()) > 0:
		strvar_input_file_path.set(filename)
		(base_path, file_ext) = os.path.splitext(filename)
		STRVAR_OUTPUT_FILE_PATH.set(base_path + output_pdf_suffix)


def update_device_unit_width_height():
	if device_combobox.current() != 20:  # non-other type
		device_type = device_argument_map[device_combobox.current()]
		arg = device_arg_name + ' ' + device_type
		add_or_update_one_cmd_arg(device_arg_name, arg)
		remove_one_cmd_arg(width_arg_name)
		remove_one_cmd_arg(height_arg_name)
	else:
		screen_unit = unit_argument_map[unit_combobox.current()]

		width_arg = (width_arg_name + ' ' + strvar_screen_width.get().strip() + screen_unit)
		add_or_update_one_cmd_arg(width_arg_name, width_arg)

		height_arg = (height_arg_name + ' ' + strvar_screen_height.get().strip() + screen_unit)
		add_or_update_one_cmd_arg(height_arg_name, height_arg)

		remove_one_cmd_arg(device_arg_name)


def on_bind_event_device_unit_cb(e=None):
	update_device_unit_width_height()


def on_command_width_height_cb():
	update_device_unit_width_height()


def on_bind_event_mode_cb(e=None):
	conversion_mode = mode_argument_map[mode_combobox.current()]
	arg = (conversion_mode_arg_name + ' ' + conversion_mode)
	add_or_update_one_cmd_arg(conversion_mode_arg_name, arg)


required_input_frame = ttk.Labelframe(conversion_tab, text='Required Inputs')
required_input_frame.grid(
	column=conversion_tab_left_part_column_num,
	row=conversion_tab_left_part_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

required_frame_row_num = 0

input_path_entry = ttk.Entry(required_input_frame, state='readonly', textvariable=strvar_input_file_path)
input_path_entry.grid(
	column=0,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

open_button = ttk.Button(required_input_frame, text='Choose a File', command=on_command_open_pdf_file_cb)
open_button.grid(
	column=1,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

required_frame_row_num += 1

device_label = ttk.Label(required_input_frame, text='Device')
device_label.grid(
	column=0,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

device_combobox = ttk.Combobox(required_input_frame, state='readonly', textvariable=strvar_device)
device_combobox['values'] = list(device_choice_map.values())
device_combobox.current(0)
device_combobox.bind('<<ComboboxSelected>>', on_bind_event_device_unit_cb)
device_combobox.grid(
	column=1,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

required_frame_row_num += 1

unit_label = ttk.Label(required_input_frame, text='Unit')
unit_label.grid(
	column=0,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

unit_combobox = ttk.Combobox(required_input_frame, state='readonly', textvariable=strvar_screen_unit)
unit_combobox['values'] = list(unit_choice_map.values())
unit_combobox.current(0)
unit_combobox.bind('<<ComboboxSelected>>', on_bind_event_device_unit_cb)
unit_combobox.grid(
	column=1,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

required_frame_row_num += 1

width_label = ttk.Label(required_input_frame, text='Width')
width_label.grid(
	column=0,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

width_spinbox = ttk.Spinbox(
	required_input_frame,
	from_=0,
	to=10000,
	increment=0.1,
	state='readonly',
	textvariable=strvar_screen_width,
	command=on_command_width_height_cb,
)
width_spinbox.grid(
	column=1,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

required_frame_row_num += 1

height_label = ttk.Label(required_input_frame, text='Height')
height_label.grid(
	column=0,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)
height_spinbox = ttk.Spinbox(
	required_input_frame,
	from_=0,
	to=10000,
	increment=0.1,
	state='readonly',
	textvariable=strvar_screen_height,
	command=on_command_width_height_cb,
)
height_spinbox.grid(
	column=1,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

required_frame_row_num += 1

conversion_mode_label = ttk.Label(required_input_frame, text='Conversion Mode')
conversion_mode_label.grid(
	column=0,
	row=required_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

mode_combobox = ttk.Combobox(required_input_frame, state='readonly', textvariable=strvar_conversion_mode)
mode_combobox['values'] = list(mode_choice_map.values())
mode_combobox.current(0)
mode_combobox.bind('<<ComboboxSelected>>', on_bind_event_mode_cb)
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


def on_command_save_cb():
	with open(custom_preset_file_path, 'w') as preset_file:
		dict_to_save = {}
		for k, v in arg_var_map.items():
			dict_to_save[k] = [var.get() for var in v]

		json.dump(dict_to_save, preset_file)


def on_bind_event_cmd_args_cb(e=None):
	update_cmd_arg_entry_strvar()


information_frame = ttk.Labelframe(conversion_tab, text='Related Informations')
information_frame.grid(
	column=conversion_tab_left_part_column_num,
	row=conversion_tab_left_part_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

save_label = ttk.Label(information_frame, text='Save Current Setting as Preset')
save_label.grid(column=0, row=0, sticky=tk.N+tk.W, pady=0, padx=5)

save_button = ttk.Button(information_frame, text='Save', command=on_command_save_cb)
save_button.grid(column=1, row=0, sticky=tk.N+tk.W, pady=0, padx=5)

output_label = ttk.Label(information_frame, text='Output Pdf File Path')
output_label.grid(column=0, row=1, sticky=tk.N+tk.W, pady=0, padx=5)

output_path_entry = ttk.Entry(information_frame, state='readonly', textvariable=STRVAR_OUTPUT_FILE_PATH)
output_path_entry.grid(column=1, row=1, sticky=tk.N+tk.W, pady=0, padx=5)

command_arguments_label = ttk.Label(information_frame, text='Command-line Options')
command_arguments_label.grid(column=0, row=2, sticky=tk.N+tk.W, pady=0, padx=5)

command_arguments_entry = ttk.Entry(information_frame, state='readonly', textvariable=STRVAR_COMMAND_ARGS)
command_arguments_entry.bind('<Button-1>', on_bind_event_cmd_args_cb)
command_arguments_entry.grid(column=1, row=2, sticky=tk.N+tk.W, pady=0, padx=5)


# ############################################################################################### #
# PARAMETERS FRAME
# ############################################################################################### #
conversion_tab_left_part_row_num += 1

column_num_arg_name = '-col'            # -col <maxcol>
resolution_multiplier_arg_name = '-dr'  # -dr <value>
crop_margin_arg_name = '-cbox'          # -cbox[<pagelist>|u|-]
dpi_arg_name = '-dpi'                   # -dpi <dpival>
page_num_arg_name = '-p'                # -p <pagelist>
fixed_font_size_arg_name = '-fs'        # -fs 0/-fs <font size>[+]
ocr_arg_name = '-ocr'                   # -ocr-/-ocr t
ocr_cpu_arg_name = '-nt'                # -nt -50/-nt <percentage>
landscape_arg_name = '-ls'              # -ls[-][pagelist]
linebreak_arg_name = '-ws'              # -ws <spacing>

is_column_num_checked = tk.BooleanVar()
is_resolution_multipler_checked = tk.BooleanVar()
is_crop_margin_checked = tk.BooleanVar()
is_dpi_checked = tk.BooleanVar()
is_fixed_font_size_checked = tk.BooleanVar()
is_ocr_cpu_limitation_checked = tk.BooleanVar()
is_landscape_checked = tk.BooleanVar()
is_smart_linebreak_checked = tk.BooleanVar()  # -ws 0.01~10

strvar_column_num = tk.StringVar()
strvar_resolution_multiplier = tk.StringVar()
strvar_crop_page_range = tk.StringVar()
strvar_left_margin = tk.StringVar()
strvar_top_margin = tk.StringVar()
strvarRightMargin = tk.StringVar()         # Must it be "width" ?
strvarBottomMargin = tk.StringVar()        # Must if be "height" ?
strvar_dpi = tk.StringVar()
strvar_page_numbers = tk.StringVar()
strvar_fixed_font_size = tk.StringVar()
strvar_ocr_cpu_percentage = tk.StringVar()
strvar_landscape_pages = tk.StringVar()      # 1,3,5-10
strvar_linebreak_space = tk.StringVar()


def on_command_column_num_cb():
	if is_column_num_checked.get():
		arg = (column_num_arg_name + ' ' + strvar_column_num.get().strip())
		add_or_update_one_cmd_arg(column_num_arg_name, arg)
	else:
		remove_one_cmd_arg(column_num_arg_name)


def on_command_resolution_multipler_cb():
	if is_resolution_multipler_checked.get():
		arg = (
			resolution_multiplier_arg_name + ' ' +
			strvar_resolution_multiplier.get().strip()
		)
		add_or_update_one_cmd_arg(resolution_multiplier_arg_name, arg)
	else:
		remove_one_cmd_arg(resolution_multiplier_arg_name)


def on_command_and_validate_crop_margin_cb():
	if (len(strvar_crop_page_range.get().strip()) > 0 and
			not check_page_nums(strvar_crop_page_range.get().strip())):
		remove_one_cmd_arg(crop_margin_arg_name)
		strvar_crop_page_range.set('')

		tkinter.messagebox.showerror(
			message='Invalide Crop Page Range. It should be like : 2-5e,3-7o,9-'
		)

		return False

	if is_crop_margin_checked.get():
		page_range_arg = strvar_crop_page_range.get().strip()
		margin_args = [
			strvar_left_margin.get(),
			strvar_top_margin.get(),
			strvarRightMargin.get(),
			strvarBottomMargin.get(),
		]
		arg = (
			# no space between -cbox and page range
			crop_margin_arg_name + page_range_arg + ' '
			+ 'in,' . join(map(str.strip, margin_args)) + 'in'
		)
		add_or_update_one_cmd_arg(crop_margin_arg_name, arg)
	else:
		remove_one_cmd_arg(crop_margin_arg_name)


def on_command_dpi_cb():
	if is_dpi_checked.get():
		arg = dpi_arg_name + ' ' + strvar_dpi.get().strip()
		add_or_update_one_cmd_arg(dpi_arg_name, arg)
	else:
		remove_one_cmd_arg(dpi_arg_name)


def validate_and_update_page_nums():
	if (len(strvar_page_numbers.get().strip()) > 0 and
			not check_page_nums(strvar_page_numbers.get().strip())):

		remove_one_cmd_arg(page_num_arg_name)
		strvar_page_numbers.set('')
		tkinter.messagebox.showerror(
			message='Invalide Page Argument. It should be like: 2-5e,3-7o,9-'
		)
		return False

	if len(strvar_page_numbers.get().strip()) > 0:
		arg = page_num_arg_name + ' ' + strvar_page_numbers.get().strip()
		add_or_update_one_cmd_arg(page_num_arg_name, arg)
	else:
		remove_one_cmd_arg(page_num_arg_name)

	return True


def on_validate_page_nums_cb():
	validate_and_update_page_nums()


def on_command_fixed_font_size_cb():
	if is_fixed_font_size_checked.get():
		arg = (fixed_font_size_arg_name + ' ' + strvar_fixed_font_size.get().strip())
		add_or_update_one_cmd_arg(fixed_font_size_arg_name, arg)
	else:
		remove_one_cmd_arg(fixed_font_size_arg_name)


def on_command_ocr_and_cpu_cb():
	if is_ocr_cpu_limitation_checked.get():
		is_native_pdf_checked.set(False)  # ocr conflicts with native pdf
		remove_one_cmd_arg(native_pdf_arg_name)
		ocr_arg = ocr_arg_name
		add_or_update_one_cmd_arg(ocr_arg_name, ocr_arg)

		# negtive integer means percentage
		ocr_cpu_arg = (ocr_cpu_arg_name + '-' + strvar_ocr_cpu_percentage.get().strip())
		add_or_update_one_cmd_arg(ocr_cpu_arg_name, ocr_cpu_arg)
	else:
		remove_one_cmd_arg(ocr_arg_name)
		remove_one_cmd_arg(ocr_cpu_arg_name)


def on_command_and_validate_landscape_cb():
	if (len(strvar_landscape_pages.get().strip()) > 0 and
			not check_page_nums(strvar_landscape_pages.get().strip())):

		remove_one_cmd_arg(landscape_arg_name)
		strvar_landscape_pages.set('')
		tkinter.messagebox.showerror(message='Invalide `Output in Landscape` Page Argument!')

		return False

	if is_landscape_checked.get():
		arg = '-ls'
		if len(strvar_landscape_pages.get().strip()) > 0:
			# no space between -ls and page numbers
			arg += strvar_landscape_pages.get()

		add_or_update_one_cmd_arg(landscape_arg_name, arg.strip())
	else:
		remove_one_cmd_arg(landscape_arg_name)

	return True


def on_command_line_break_cb():
	if is_smart_linebreak_checked.get():
		arg = (linebreak_arg_name + ' ' + strvar_linebreak_space.get().strip())
		add_or_update_one_cmd_arg(linebreak_arg_name, arg)
	else:
		remove_one_cmd_arg(linebreak_arg_name)


parameters_frame = ttk.Labelframe(conversion_tab, text='Parameters')
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
	variable=is_column_num_checked,
	command=on_command_column_num_cb,
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
	textvariable=strvar_column_num,
	command=on_command_column_num_cb,
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
	variable=is_resolution_multipler_checked,
	command=on_command_resolution_multipler_cb,
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
	textvariable=strvar_resolution_multiplier,
	command=on_command_resolution_multipler_cb,
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
	variable=is_crop_margin_checked,
	command=on_command_and_validate_crop_margin_cb,
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
	textvariable=strvar_crop_page_range,
	validate='focusout',
	validatecommand=on_command_and_validate_crop_margin_cb,
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
	textvariable=strvar_left_margin,
	command=on_command_and_validate_crop_margin_cb,
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
	textvariable=strvar_top_margin,
	command=on_command_and_validate_crop_margin_cb,
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
	textvariable=strvarRightMargin,
	command=on_command_and_validate_crop_margin_cb,
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
	textvariable=strvarBottomMargin,
	command=on_command_and_validate_crop_margin_cb,
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
	variable=is_dpi_checked,
	command=on_command_dpi_cb,
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
	textvariable=strvar_dpi,
	command=on_command_dpi_cb,
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
	textvariable=strvar_page_numbers,
	validate='focusout',
	validatecommand=on_validate_page_nums_cb,
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
	variable=is_fixed_font_size_checked,
	command=on_command_fixed_font_size_cb,
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
	textvariable=strvar_fixed_font_size,
	command=on_command_fixed_font_size_cb,
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
	variable=is_ocr_cpu_limitation_checked,
	command=on_command_ocr_and_cpu_cb,
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
	textvariable=strvar_ocr_cpu_percentage,
	command=on_command_ocr_and_cpu_cb,
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
	variable=is_landscape_checked,
	command=on_command_and_validate_landscape_cb,
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
	textvariable=strvar_landscape_pages,
	validate='focusout',
	validatecommand=on_command_and_validate_landscape_cb,
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
	variable=is_smart_linebreak_checked,
	command=on_command_line_break_cb,
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
	textvariable=strvar_linebreak_space,
	command=on_command_line_break_cb,
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

auto_straignten_arg_name = '-as'            # -as-/-as
break_page_avoid_overlap_arg_name = '-bp'   # -bp-/-bp
color_output_arg_name = '-c'                # -c-/-c
native_pdf_arg_name = '-n'                  # -n-/-n
right_to_left_arg_name = '-r'               # -r-/-r
post_gs_arg_name = '-ppgs'                  # -ppgs-/-ppgs
marked_source_arg_name = '-sm'              # -sm-/-sm
reflow_text_arg_name = '-wrap'              # -wrap+/-wrap-
erase_vertical_line_arg_name = '-evl'       # -evl 0/-evl 1
erase_horizontal_line_arg_name = '-ehl'     # -ehl 0/-ehl 1
fast_preview_arg_name = '-rt'               # -rt /-rt 0
ign_small_defects_arg_name = '-de'          # -de 1.0/-de 1.5
auto_crop_arg_name = '-ac'                  # -ac-/-ac

is_autostraighten_checked = tk.BooleanVar()
isBreakPage = tk.BooleanVar()
isColorOutput = tk.BooleanVar()
is_native_pdf_checked = tk.BooleanVar()
is_right_to_left_checked = tk.BooleanVar()
isPostGs = tk.BooleanVar()
isMarkedSrc = tk.BooleanVar()
is_reflow_text_checked = tk.BooleanVar()
is_erase_vertical_line_checked = tk.BooleanVar()
is_erase_horizontal_line_checked = tk.BooleanVar()
is_fast_preview_checked = tk.BooleanVar()
isAvoidOverlap = tk.BooleanVar()
isIgnSmallDefects = tk.BooleanVar()
is_autocrop_checked = tk.BooleanVar()


def on_command_auto_straighten_cb():
	if is_autostraighten_checked.get():
		arg = auto_straignten_arg_name
		add_or_update_one_cmd_arg(auto_straignten_arg_name, arg)
	else:
		remove_one_cmd_arg(auto_straignten_arg_name)


def on_command_break_page_cb():
	if isBreakPage.get():
		# break page conflicts with avoid overlap since they are both -bp flag
		isAvoidOverlap.set(False)
		remove_one_cmd_arg(break_page_avoid_overlap_arg_name)

		arg = break_page_avoid_overlap_arg_name
		add_or_update_one_cmd_arg(break_page_avoid_overlap_arg_name, arg)
	else:
		remove_one_cmd_arg(break_page_avoid_overlap_arg_name)


def on_command_color_output_cb():
	if isColorOutput.get():
		arg = color_output_arg_name
		add_or_update_one_cmd_arg(color_output_arg_name, arg)
	else:
		remove_one_cmd_arg(color_output_arg_name)


def on_command_native_pdf_cb():
	if is_native_pdf_checked.get():
		# native pdf conflicts with ocr and reflow text
		is_ocr_cpu_limitation_checked.set(False)
		remove_one_cmd_arg(ocr_arg_name)
		remove_one_cmd_arg(ocr_cpu_arg_name)

		is_reflow_text_checked.set(False)
		remove_one_cmd_arg(reflow_text_arg_name)

		arg = native_pdf_arg_name
		add_or_update_one_cmd_arg(native_pdf_arg_name, arg)
	else:
		remove_one_cmd_arg(native_pdf_arg_name)


def on_command_right_to_left_cb():
	if is_right_to_left_checked.get():
		arg = right_to_left_arg_name
		add_or_update_one_cmd_arg(right_to_left_arg_name, arg)
	else:
		remove_one_cmd_arg(right_to_left_arg_name)


def on_command_post_gs_cb():
	if isPostGs.get():
		arg = post_gs_arg_name
		add_or_update_one_cmd_arg(post_gs_arg_name, arg)
	else:
		remove_one_cmd_arg(post_gs_arg_name)


def on_command_marked_src_cb():
	if isMarkedSrc.get():
		arg = marked_source_arg_name
		add_or_update_one_cmd_arg(marked_source_arg_name, arg)
	else:
		remove_one_cmd_arg(marked_source_arg_name)


def on_command_reflow_text_cb():
	if is_reflow_text_checked.get():
		is_native_pdf_checked.set(False)  # reflow text conflicts with native pdf
		remove_one_cmd_arg(native_pdf_arg_name)
		arg = reflow_text_arg_name + '+'
		add_or_update_one_cmd_arg(reflow_text_arg_name, arg)
	else:
		remove_one_cmd_arg(reflow_text_arg_name)


def on_command_erase_vertical_line_cb():
	if is_erase_vertical_line_checked.get():
		arg = erase_vertical_line_arg_name + ' 1'
		add_or_update_one_cmd_arg(erase_vertical_line_arg_name, arg)
	else:
		remove_one_cmd_arg(erase_vertical_line_arg_name)


def on_command_fast_preview_cb():
	if is_fast_preview_checked.get():
		arg = fast_preview_arg_name + ' 0'
		add_or_update_one_cmd_arg(fast_preview_arg_name, arg)
	else:
		remove_one_cmd_arg(fast_preview_arg_name)


def on_command_avoid_text_selection_overlap_cb():
	if isAvoidOverlap.get():
		# avoid overlap conflicts with break page since they are both -bp flag
		isBreakPage.set(False)
		remove_one_cmd_arg(break_page_avoid_overlap_arg_name)

		arg = break_page_avoid_overlap_arg_name + ' m'
		add_or_update_one_cmd_arg(break_page_avoid_overlap_arg_name, arg)
	else:
		remove_one_cmd_arg(break_page_avoid_overlap_arg_name)


def on_command_ign_small_defect_cb():
	if isIgnSmallDefects.get():
		arg = (ign_small_defects_arg_name + ' 1.5')
		add_or_update_one_cmd_arg(ign_small_defects_arg_name, arg)
	else:
		remove_one_cmd_arg(ign_small_defects_arg_name)


def on_command_erase_horizontal_line_cb():
	if is_erase_horizontal_line_checked.get():
		arg = erase_horizontal_line_arg_name + ' 1'
		add_or_update_one_cmd_arg(erase_horizontal_line_arg_name, arg)
	else:
		remove_one_cmd_arg(erase_horizontal_line_arg_name)


def on_command_auto_crop_cb():
	if is_autocrop_checked.get():
		arg = auto_crop_arg_name
		add_or_update_one_cmd_arg(auto_crop_arg_name, arg)
	else:
		remove_one_cmd_arg(auto_crop_arg_name)


optionFrame = ttk.Labelframe(
	conversion_tab,
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
	variable=is_autostraighten_checked,
	command=on_command_auto_straighten_cb,
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
	variable=isBreakPage,
	command=on_command_break_page_cb,
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
	variable=isColorOutput,
	command=on_command_color_output_cb,
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
	variable=is_native_pdf_checked,
	command=on_command_native_pdf_cb,
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
	variable=is_right_to_left_checked,
	command=on_command_right_to_left_cb,
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
	variable=isPostGs,
	command=on_command_post_gs_cb,
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
	variable=isMarkedSrc,
	command=on_command_marked_src_cb,
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
	variable=is_reflow_text_checked,
	command=on_command_reflow_text_cb,
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
	variable=is_erase_vertical_line_checked,
	command=on_command_erase_vertical_line_cb,
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
	variable=is_erase_horizontal_line_checked,
	command=on_command_erase_horizontal_line_cb,
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
	variable=is_fast_preview_checked,
	command=on_command_fast_preview_cb,
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
	variable=isAvoidOverlap,
	command=on_command_avoid_text_selection_overlap_cb,
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
	variable=isIgnSmallDefects,
	command=on_command_ign_small_defect_cb,
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
	variable=is_autocrop_checked,
	command=on_command_auto_crop_cb,
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

preview_output_arg_name = '-bmp'
preview_image_path = './k2pdfopt_out.png'

def remove_preview_image_and_clear_canvas():
	globals.CANVAS_IMAGE_TAG
	# global STRVAR_CURRENT_PREVIEW_PAGE_NUM    # unused !

	if os.path.exists(preview_image_path):
		os.remove(preview_image_path)

	globals.PREVIEW_IMAGE_CANVAS.delete(tk.ALL)
	globals.CANVAS_IMAGE_TAG = None


def load_preview_image(img_path, preview_page_index):

	if os.path.exists(img_path):
		globals.PREVIEW_IMAGE = tk.PhotoImage(file=img_path)

		globals.CANVAS_IMAGE_TAG = globals.PREVIEW_IMAGE_CANVAS.create_image(
			(0, 0),
			anchor=tk.NW,
			image=globals.PREVIEW_IMAGE,
			tags='preview',
		)

		(left_pos, top_pos, right_pos, bottom_pos) = (
			0,
			0,
			globals.PREVIEW_IMAGE.width(),
			globals.PREVIEW_IMAGE.height(),
		)
		globals.PREVIEW_IMAGE_CANVAS.config(
			scrollregion=(left_pos, top_pos, right_pos, bottom_pos),
		)
		# canvas.scale('preview', 0, 0, 0.1, 0.1)
		STRVAR_CURRENT_PREVIEW_PAGE_NUM.set('Page: ' + str(preview_page_index))
	else:
		STRVAR_CURRENT_PREVIEW_PAGE_NUM.set('No Page: ' + str(preview_page_index))


def generate_one_preview_image(preview_page_index):

	if not pdf_conversion_is_done():
		return

	if not os.path.exists(strvar_input_file_path.get().strip()):
		tkinter.messagebox.showerror(
			message=(
				"Failed to Find Input PDF File to convert for Preview: %s"
				%
				strvar_input_file_path.get().strip()
			),
		)
		return

	remove_preview_image_and_clear_canvas()
	(base_path, file_ext) = os.path.splitext(strvar_input_file_path.get().strip())
	output_arg = ' '.join([preview_output_arg_name, str(preview_page_index)])
	globals.BACKGROUND_FUTURE = convert_pdf_file(output_arg)
	STRVAR_CURRENT_PREVIEW_PAGE_NUM.set('Preview Generating...')

	def preview_image_future_cb(bgf):
		load_preview_image(preview_image_path, preview_page_index)
		log_string(
			"Preview generation for page %d finished" %
			preview_page_index
		)

	globals.BACKGROUND_FUTURE.add_done_callback(preview_image_future_cb)


def on_command_restore_default_cb():
	restore_default_values()


def on_command_abort_conversion_cb():
	if globals.BACKGROUND_FUTURE is not None:
		globals.BACKGROUND_FUTURE.cancel()

	if (globals.BACKGROUND_PROCESS is not None and globals.BACKGROUND_PROCESS.returncode is None):
		globals.BACKGROUND_PROCESS.terminate()


def on_command_convert_pdf_cb():
	if not pdf_conversion_is_done():
		return

	pdf_output_arg = output_path_arg_name + ' %s' + output_pdf_suffix
	globals.BACKGROUND_FUTURE = convert_pdf_file(pdf_output_arg)


def on_command_ten_page_up_cb():
	globals.CURRENT_PREVIEW_PAGE_INDEX -= 10
	if globals.CURRENT_PREVIEW_PAGE_INDEX < 1:
		globals.CURRENT_PREVIEW_PAGE_INDEX = 1
	generate_one_preview_image(globals.CURRENT_PREVIEW_PAGE_INDEX)


def on_command_page_up_cb():
	if globals.CURRENT_PREVIEW_PAGE_INDEX > 1:
		globals.CURRENT_PREVIEW_PAGE_INDEX -= 1
	generate_one_preview_image(globals.CURRENT_PREVIEW_PAGE_INDEX)


def on_command_page_down_cb():
	globals.CURRENT_PREVIEW_PAGE_INDEX += 1
	generate_one_preview_image(globals.CURRENT_PREVIEW_PAGE_INDEX)


def on_command_ten_page_down_cb():
	globals.CURRENT_PREVIEW_PAGE_INDEX += 10
	generate_one_preview_image(globals.CURRENT_PREVIEW_PAGE_INDEX)


preview_frame = ttk.Labelframe(conversion_tab, text='Preview & Convert')
preview_frame.grid(
	column=conversion_tab_right_part_column_num,
	row=conversion_tab_right_part_row_num,
	rowspan=3,
	sticky=tk.N+tk.S+tk.E+tk.W,
	pady=0,
	padx=5,
)

preview_frame_row_num = 0

reset_button = ttk.Button(preview_frame, text='Reset Default', command=on_command_restore_default_cb)
reset_button.grid(
	column=0,
	row=preview_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

cancel_button = ttk.Button(preview_frame, text='Abort', command=on_command_abort_conversion_cb)
cancel_button.grid(
	column=1,
	row=preview_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

convert_button = ttk.Button(preview_frame, text='Convert', command=on_command_convert_pdf_cb)
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
	textvariable=STRVAR_CURRENT_PREVIEW_PAGE_NUM
)
current_preview_page_number_entry.grid(
	column=0,
	row=preview_frame_row_num,
	columnspan=2,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

preview_button = ttk.Button(preview_frame, text='Preview', command=on_command_ten_page_up_cb)
preview_button.grid(
	column=2,
	row=preview_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

preview_frame_column_num = 0
preview_frame_row_num += 1

first_button = ttk.Button(preview_frame, text='<<', command=on_command_ten_page_up_cb)
first_button.grid(
	column=preview_frame_column_num,
	row=preview_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)
preview_frame_column_num += 1

previous_button = ttk.Button(preview_frame, text='<', command=on_command_page_up_cb)
previous_button.grid(
	column=preview_frame_column_num,
	row=preview_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)
preview_frame_column_num += 1

next_button = ttk.Button(preview_frame, text='>', command=on_command_page_down_cb)
next_button.grid(
	column=preview_frame_column_num,
	row=preview_frame_row_num,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)
preview_frame_column_num += 1

last_button = ttk.Button(preview_frame, text='>>', command=on_command_ten_page_down_cb)
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

globals.PREVIEW_IMAGE_CANVAS = tk.Canvas(
	preview_frame,
	bd=0,
	xscrollcommand=xScrollBar.set,
	yscrollcommand=yScrollBar.set,
)
globals.PREVIEW_IMAGE_CANVAS.grid(
	column=0,
	row=preview_frame_row_num,
	columnspan=preview_frame_column_num,
	sticky=tk.N+tk.S+tk.E+tk.W,
)

xScrollBar.config(command=globals.PREVIEW_IMAGE_CANVAS.xview)
yScrollBar.config(command=globals.PREVIEW_IMAGE_CANVAS.yview)

conversion_tab.columnconfigure(
	conversion_tab_right_part_column_num,
	weight=1,
)
conversion_tab.rowconfigure(
	conversion_tab_right_part_row_num,
	weight=1,
)
preview_frame.columnconfigure(0, weight=1)
preview_frame.rowconfigure(preview_frame_row_num, weight=1)

def yscroll_canvas(event):
	globals.PREVIEW_IMAGE_CANVAS.yview_scroll(-1 * event.delta, 'units')

def xscroll_canvas(event):
	globals.PREVIEW_IMAGE_CANVAS.xview_scroll(-1 * event.delta, 'units')

globals.PREVIEW_IMAGE_CANVAS.bind('<MouseWheel>', yscroll_canvas)
globals.PREVIEW_IMAGE_CANVAS.bind("<Shift-MouseWheel>", xscroll_canvas)

preview_frame_row_num += 1

# collect all vars
bool_var_list = [
	is_column_num_checked,
	is_resolution_multipler_checked,
	is_crop_margin_checked,
	is_dpi_checked,
	is_fixed_font_size_checked,
	is_ocr_cpu_limitation_checked,
	is_landscape_checked,
	is_smart_linebreak_checked,

	is_autostraighten_checked,
	isBreakPage,
	isColorOutput,
	is_native_pdf_checked,
	is_right_to_left_checked,
	isPostGs,
	isMarkedSrc,
	is_reflow_text_checked,
	is_erase_vertical_line_checked,
	is_erase_horizontal_line_checked,
	is_fast_preview_checked,
	isAvoidOverlap,
	isIgnSmallDefects,
	is_autocrop_checked,
]

string_var_list = [
	strvar_input_file_path,
	strvar_device,
	strvar_conversion_mode,
	strvar_screen_unit,
	strvar_screen_width,
	strvar_screen_height,
	strvar_column_num,
	strvar_resolution_multiplier,
	strvar_crop_page_range,
	strvar_left_margin,
	strvarRightMargin,
	strvar_top_margin,
	strvarBottomMargin,
	strvar_dpi,
	strvar_page_numbers,

	strvar_fixed_font_size,
	strvar_ocr_cpu_percentage,
	strvar_landscape_pages,
	strvar_linebreak_space,

	STRVAR_CURRENT_PREVIEW_PAGE_NUM,
    STRVAR_OUTPUT_FILE_PATH,
	STRVAR_COMMAND_ARGS,
]

combo_box_list = [
	device_combobox,
	mode_combobox,
	unit_combobox,
]

entry_list = [
	input_path_entry,
	output_path_entry,
	command_arguments_entry,
	page_number_entry,
	landscapepage_number_entry,
	current_preview_page_number_entry,
]

default_var_map = {
	device_arg_name:                    ['Kindle 1-5'],
	screen_unit_prefix:                 ['Pixels'],
	width_arg_name:                     ['560'],
	height_arg_name:                    ['735'],
	conversion_mode_arg_name:           ['Default'],
	output_path_arg_name:               [''],

	column_num_arg_name:                [False, '2'],
	resolution_multiplier_arg_name:     [False, '1.0'],
	crop_margin_arg_name:               [
											False,
											'',
											'0.00',
											'0.00',
											'0.00',
											'0.00',
										],
	dpi_arg_name:                       [False, '167'],
	page_num_arg_name:                  [''],
	fixed_font_size_arg_name:           [False, '12'],
	ocr_arg_name:                       [False, '50'],
	ocr_cpu_arg_name:                   [False, '50'],
	landscape_arg_name:                 [False, ''],
	linebreak_arg_name:                 [True, '0.200'],

	auto_straignten_arg_name:           [False],
	break_page_avoid_overlap_arg_name:  [False, False],
	color_output_arg_name:              [False],
	native_pdf_arg_name:                [False],
	right_to_left_arg_name:             [False],
	post_gs_arg_name:                   [False],
	marked_source_arg_name:             [False],
	reflow_text_arg_name:               [True],
	erase_vertical_line_arg_name:       [False],
	erase_horizontal_line_arg_name:     [False],
	fast_preview_arg_name:              [True],
	ign_small_defects_arg_name:         [False],
	auto_crop_arg_name:                 [False],

	preview_output_arg_name:            []
}

arg_var_map = {
	device_arg_name:                    [strvar_device],
	screen_unit_prefix:                 [strvar_screen_unit],
	width_arg_name:                     [strvar_screen_width],
	height_arg_name:                    [strvar_screen_height],
	conversion_mode_arg_name:           [strvar_conversion_mode],
	output_path_arg_name:               [STRVAR_OUTPUT_FILE_PATH],

	column_num_arg_name:                [
											is_column_num_checked,
											strvar_column_num,
										],
	resolution_multiplier_arg_name:     [
											is_resolution_multipler_checked,
											strvar_resolution_multiplier,
										],
	crop_margin_arg_name:               [
											is_crop_margin_checked,
											strvar_crop_page_range,
											strvar_left_margin,
											strvar_top_margin,
											strvarRightMargin,
											strvarBottomMargin,
										],
	dpi_arg_name:                       [
											is_dpi_checked,
											strvar_dpi,
										],
	page_num_arg_name:                  [
											strvar_page_numbers,
										],

	fixed_font_size_arg_name:           [
											is_fixed_font_size_checked,
											strvar_fixed_font_size,
										],
	ocr_arg_name:                       [
											is_ocr_cpu_limitation_checked,
											strvar_ocr_cpu_percentage,
										],
	ocr_cpu_arg_name:                   [
											is_ocr_cpu_limitation_checked,
											strvar_ocr_cpu_percentage,
										],
	landscape_arg_name:                 [
											is_landscape_checked,
											strvar_landscape_pages,
										],
	linebreak_arg_name:                 [
											is_smart_linebreak_checked,
											strvar_linebreak_space,
										],

	auto_straignten_arg_name:           [is_autostraighten_checked],
	break_page_avoid_overlap_arg_name:  [isBreakPage, isAvoidOverlap],
	color_output_arg_name:              [isColorOutput],
	native_pdf_arg_name:                [is_native_pdf_checked],
	right_to_left_arg_name:             [is_right_to_left_checked],
	post_gs_arg_name:                   [isPostGs],
	marked_source_arg_name:             [isMarkedSrc],
	reflow_text_arg_name:               [is_reflow_text_checked],
	erase_vertical_line_arg_name:       [is_erase_vertical_line_checked],
	erase_horizontal_line_arg_name:     [is_erase_horizontal_line_checked],
	fast_preview_arg_name:              [is_fast_preview_checked],
	# break_page_avoid_overlap_arg_name:  []
	ign_small_defects_arg_name:         [isIgnSmallDefects],
	auto_crop_arg_name:                 [is_autocrop_checked],
	preview_output_arg_name:            []
}

arg_cb_map = {
	device_arg_name:                   on_bind_event_device_unit_cb,
	width_arg_name:                    on_command_width_height_cb,
	height_arg_name:                   on_command_width_height_cb,
	conversion_mode_arg_name:          on_bind_event_mode_cb,
	output_path_arg_name:              None,

	column_num_arg_name:               on_command_column_num_cb,
	resolution_multiplier_arg_name:    on_command_resolution_multipler_cb,
	crop_margin_arg_name:              on_command_and_validate_crop_margin_cb,
	dpi_arg_name:                      on_command_dpi_cb,
	page_num_arg_name:                 on_validate_page_nums_cb,

	fixed_font_size_arg_name:          on_command_fixed_font_size_cb,
	ocr_arg_name:                      on_command_ocr_and_cpu_cb,
	ocr_cpu_arg_name:                  on_command_ocr_and_cpu_cb,
	landscape_arg_name:                on_command_and_validate_landscape_cb,
	linebreak_arg_name:                on_command_line_break_cb,

	auto_straignten_arg_name:          on_command_auto_straighten_cb,
	break_page_avoid_overlap_arg_name: on_command_break_page_cb,
	color_output_arg_name:             on_command_color_output_cb,
	native_pdf_arg_name:               on_command_native_pdf_cb,
	right_to_left_arg_name:            on_command_right_to_left_cb,
	post_gs_arg_name:                  on_command_post_gs_cb,
	marked_source_arg_name:            on_command_marked_src_cb,
	reflow_text_arg_name:              on_command_reflow_text_cb,
	erase_vertical_line_arg_name:      on_command_erase_vertical_line_cb,
	erase_horizontal_line_arg_name:    on_command_erase_horizontal_line_cb,
	fast_preview_arg_name:             on_command_fast_preview_cb,
	ign_small_defects_arg_name:        on_command_ign_small_defect_cb,
	auto_crop_arg_name:                on_command_auto_crop_cb,

	preview_output_arg_name:           None
}

# ############################################################################################### #
# K2PDFOPT STDOUT TAB
# ############################################################################################### #
stdout_frame = ttk.Labelframe(log_tab, text='k2pdfopt STDOUT:')
stdout_frame.pack(expand=1, fill='both')


def on_command_clear_log_cb():
	clear_logs()


def initialize():
	check_k2pdfopt_path_exists()

	if not load_custom_preset():
		restore_default_values()

	pwd = os.getcwd()
	log_string('Current directory: ' + pwd)


clear_button = ttk.Button(stdout_frame, text='Clear', command=on_command_clear_log_cb)
clear_button.grid(
	column=0,
	row=0,
	sticky=tk.N+tk.W,
	pady=0,
	padx=5,
)

STDOUT_TEXT = scrltxt.ScrolledText(stdout_frame, state=tk.DISABLED, wrap='word')
STDOUT_TEXT.grid(column=0, row=1, sticky=tk.N+tk.S+tk.E+tk.W)
stdout_frame.columnconfigure(0, weight=1)
stdout_frame.rowconfigure(1, weight=1)
# STDOUT_TEXT.pack(expand=1, fill='both')


# initialization
initialize()


# start TclTk loop
root.mainloop()