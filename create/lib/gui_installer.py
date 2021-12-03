from create.lib.base import Create_Installer
import subprocess
import shutil

class create_gui_installer(Create_Installer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.compress()
        if self.run_exe:
            shutil.rmtree("dist")
        self.make_py_file()
        self.make_installer()

    def make_py_file(self):
        body = """from tkinter import filedialog
from tkinter import ttk
import tkinter
import zipfile
import shutil
import tqdm
import sys
import os

_file = os.path.abspath(sys.argv[0])
FILES = {file_list}
_all_yes = False


def resource(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.join(os.path.dirname(_file), path)

def ask(path):
    global yes
    yes = False
    sub = tkinter.Toplevel()
    sub.geometry("500x300")
    label = ttk.Label(sub, text="'%s' has already exists\\ncan I overwrite?")
    label.grid(column=0, row=0)
    yes_bt = ttk.Button(sub, text="Yes", command=lambda: on_yes(sub))
    yes_bt.grid(column=0, row=1)
    no_bt = ttk.Button(sub, text="No", command=lambda: on_no(sub))
    no_bt.grid(column=1, row=1)
    all_yes_bt = ttk.Button(sub, text="All Yes", command=lambda: on_all_yes(sub))
    all_yes_bt.grid(column=2, row=1)
    while not yes:
        pass

def on_yes(sub):
    global yes
    yes = True
    sub.destroy()

def on_no(sub):
    on_yes(sub)
    sys.exit(1)

def on_all_yes(sub):
    global _all_yes
    on_yes(sub)
    _all_yes = True

def _remove(path):
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)

def uncompress(frame, d, directory):
    with zipfile.ZipFile(resource("{zip_file}"), "r") as zip:
        for f in FILES:
            if os.path.exists(f):
                if not _all_yes:
                    ask(os.path.abspath(f))
                _remove(f)
            zip.extract(f, os.path.join(directory, f))
            p.set(p.get()+1)
    frame.destroy()
    label = ttk.Label(root, text="Installing has already done\\nYou can close this")
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

if __name__ == "__main__":
    main()
        """.format(zip_file=self.zip_file, file_list=self.files, name=self.name)
        with open(self.name+".py", "w") as f:
            f.write(body)
        self._remove.append(self.name+".py")