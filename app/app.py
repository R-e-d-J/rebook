"""Main Application class for ReBook2"""
import tkinter as tk

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