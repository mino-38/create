from create.lib.base import Create_Installer
import subprocess

class create_gui_installer(Create_Installer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.compress()
        self.make_py_file()

    def make_py_file(self):
        body = """from tkinter import filedialog
from tkinter import ttk
import tkinter
import zipfile
import tpdm
import sys
import os

_file = os.path.abspath(sys.argv[0])
FILES = {file_list}

def resource(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(_file), path)

def uncompress(frame, d, directory):
    with zipfile.ZipFile(resource("{zip_file}"), "r") as zip:
        for f in FILES:
            zip.extract(f, os.path.join(directory, f))
            p.set(p.get()+1)
    frame.destroy()
    label = ttk.Label(root, text="Installing has already done\nYou can close this")
    label.pack()

def select_path(e):
    directory = filedialog.askdirectory()
    if directory:
        e.delete(0, tkinter.END)
        e.insert(tkinter.END, directory)

def install(root, frame, directory):
    if not os.path.isdir(directory):
        return
    frame.destroy()
    installing_frame = tkinter.Frame(root)
    label = ttk.Label(installing_frame, text="installing... ")
    label.pack()
    done_files = tkinter.IntVar(value=0)
    progressbar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", variable=done_files)
    progressbar.pack()
    progressbar.configure(maximum=len(FILES), value=0)
    uncompress(installing_frame, done_files, directory)

def main():
    global root
    root = tkinter.Tk()
    root.geometry("400x600")
    root.title("{name} setup")
    frame = tkinter.Frame(root)
    label = ttk.Label(frame, text="Please specify the installation destination")
    label.grid(column=0, row=0)
    directory = tkinter.StringVar()
    entry = ttk.Entry(frame, textvariable=directory)
    entry.grid(column=0, row=1)
    entry.insert(tkinter.END, os.getcwd())
    button1 = ttk.Button(frame, text="reference", command=lambda: select_path(entry))
    button1.grid(column=1, row=1)
    button2 = ttk.Button(frame, text="Next", command=lambda: install(root, frame, directory.get()))
    button2.grid(column=0, row=2)
    frame.pack()
    root.mainloop()
        """