# Rebook 2

rebook is a Tcl/Tk based GUI for the PDF conversion tool, k2pdfopt.

Rebook depends on python3 and Tcl/Tk 8.6. Tck/Tk with version lower than 8.6 doesn't work.

## Installation
Download or clone the git projet.
With your terminal go in the projet's folder and create a virtual environnement:

```
python3 -m venv /path/to/new/virtual/environment
```

Then check activate it

```
source /path/to/new/virtual/environment/bin/activate 
```

And install the dependancies 

```
pip install -r requirements.txt
```

To check if the dependencies are correctly installed, just run 

```
python3 -m tkinter
```

To run rebook, put k2pdfopt binary and rebook.py into the same directory and run `python3 rebook.py`

rebook is still under developing, please feel free to report any issue.
