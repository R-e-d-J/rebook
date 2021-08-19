from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
import asyncio
import json
import os


class MainFrame(ttk.Frame):
    root = None             # root of tkinter

    log_tab = None
    base_tab = None
    conversion_tab = None

    k2pdfopt_cmd_args = None
    strvar_device = None    # tk.StringVar()
    strvar_screen_unit = None   # tk.StringVar()
    strvar_screen_width = None  # tk.StringVar()
    strvar_screen_height = None # tk.StringVar()
    strvar_input_file_path = None   # tk.StringVar()
    strvar_output_file_path = None   # tk.StringVar()
    strvar_conversion_mode = None   # tk.StringVar()
    conversion_mode_arg_name = '-mode'  # -mode <mode>

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

    def __init__(self, container):
        super().__init__(container)
        self.root = container
        self.create_tab()
        self.create_menu()
        self.create_widget()

    def create_tab(self):
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

    def create_widget(self):
        conversion_tab_left_part_column_num = 0
        conversion_tab_left_part_row_num = 0

        required_input_frame = ttk.Labelframe(self.conversion_tab, text='Required Inputs')
        required_input_frame.grid(
            column=conversion_tab_left_part_column_num,
            row=conversion_tab_left_part_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        required_frame_row_num = 0

        input_path_entry = ttk.Entry(required_input_frame, state='readonly', textvariable=self.strvar_input_file_path)
        input_path_entry.grid(
            column=0,
            row=required_frame_row_num,
            sticky=tk.N+tk.W,
            pady=0,
            padx=5,
        )

        open_button = ttk.Button(required_input_frame, text='Choose a File', command=self.on_command_open_pdf_file_cb)
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

        device_combobox = ttk.Combobox(required_input_frame, state='readonly', textvariable=self.strvar_device)
        device_combobox['values'] = list(self.device_choice_map.values())
        device_combobox.current(0)
        device_combobox.bind('<<ComboboxSelected>>', self.on_bind_event_device_unit_cb)
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

        unit_combobox = ttk.Combobox(required_input_frame, state='readonly', textvariable=self.strvar_screen_unit)
        unit_combobox['values'] = list(self.unit_choice_map.values())
        unit_combobox.current(0)
        unit_combobox.bind('<<ComboboxSelected>>', self.on_bind_event_device_unit_cb)
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
            textvariable=self.strvar_screen_width,
            command=self.on_command_width_height_cb,
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
            textvariable=self.strvar_screen_height,
            command=self.on_command_width_height_cb,
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

        mode_combobox = ttk.Combobox(required_input_frame, state='readonly', textvariable=self.strvar_conversion_mode)
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
            # print(filename)
            self.strvar_input_file_path = tk.StringVar()
            self.strvar_input_file_path.set(filename)

            # self.input_path_entry.delete(0, tk.END)     # deletes the current value
            # self.input_path_entry.set(0, filename)      # inserts new value assigned by 2nd parameter
            (base_path, file_ext) = os.path.splitext(filename)
            self.strvar_output_file_path = base_path + '-output.pdf'

    def on_bind_event_device_unit_cb(self, e=None):
        self.update_device_unit_width_height()

    def on_command_width_height_cb(self):
        self.update_device_unit_width_height()

    def update_device_unit_width_height(self):
        if self.device_combobox.current() != 20:  # non-other type
            device_type = self.device_argument_map[self.device_combobox.current()]
            arg = self.device_arg_name + ' ' + device_type
            self.add_or_update_command_argument(self.device_arg_name, arg)
            self.remove_command_argument(self.width_arg_name)
            self.remove_command_argument(self.height_arg_name)
        else:
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