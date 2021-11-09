from create.lib.base import Create_Installer
import subprocess
import sys

class create_cui_installer(Create_Installer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.compress()
        self.make_py_file()
        self.make_installer(gui=False)
        
    def make_py_file(self):
        body = """import argparse
import subprocess
import zipfile
import sys
import os

_file = os.path.abspath(sys.argv[0])

cmd = {cmd}

def _path(path):
    while not os.path.isfile(path):
        if path.count(os.sep) <= 1:
            print("failed", file=sys.stderr)
            sys.exit(1)
        path = os.path.join(os.path.dirname(os.path.dirname(path)), os.path.basename(path))
    return path

def resource(path):
    if hasattr(sys, "_MEIPASS"):
        path = os.path.join(sys._MEIPASS)
        while not os.path.isfile(path):
            path = _path(os.path.join(os.path.dirname(os.path.dirname(path)), os.path.basename(path)))
    else:
        path = _path(os.path.join(os.path.dirname(_file), path))
    return path

def uncompress(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    os.chdir(directory)
    print("installing \\"{name}\\"... ")
    cmd.append(resource("{zip_file}"))
    p = subprocess.run(cmd)
    if p.returncode != 0:
        sys.exit(p.returncode)

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--install-directory", nargs="?", default=".")
    return parser.parse_args()

def main():
    args = argument()
    uncompress(args.install_directory)
    print("\\ndone.")

if __name__== "__main__":
    main()""".format(cmd=(["compact", "/u"] if self._is_win else ["unzip"]), zip_file=self.zip_file, files=self.files, name=self.name)
        with open(self.name+".py", "w") as f:
            f.write(body)
        self._remove.append(self.name+".py")