# Rebook 2

ReBook2 is a OOP rewriting of rebook whitch is a Tcl/Tk based GUI for the PDF conversion tool, k2pdfopt.
ReBook2 is ***largely*** inspired by ***Pu Wang's rebook***.

#### Advantages of ReBook2

- rebook totally rewritten in the *Object Oriented Programming* paradigm (and other code improvement)
- GUI rethought
- run in a virtual environnement
- cropboxes bug fixed
- support crop-margin and cropboxes
- support multiple saved settings files
- support more devices
- support DJVU file
- better Tesseract support (i.e. more options)
- advanced options availables
- …

Rebook2 depends on python3 and Tcl/Tk 8.6 (Tck/Tk with version lower than 8.6 doesn't work).

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

To run rebook, put k2pdfopt binary and rebook.py into the same directory and run `python3 rebook2.py`

ReBook2 is still under development so, please report any issue.
