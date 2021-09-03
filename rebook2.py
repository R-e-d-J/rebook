""" This script define a GUI to choose options to build a k2pdfopt command-line """

import app.frames as frames
import app.app as app
from tkinter import messagebox
import sys
import os


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
    rebook = app.ReBook()
    frame = frames.MainFrame(rebook, K2PDFOPT_PATH)
    rebook.mainloop()
