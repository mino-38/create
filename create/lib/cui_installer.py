from create.lib.base import Create_Installer
import subprocess

class create_cui_installer(Create_Installer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.compress()
        self.make_py_file()
        self.make_installer()

    def make_installer(self):
        cmd = ["pyinstaller", "--clean", "--onefile", self.name+".py"]
        p = subprocess.run(cmd)
        self._is_success(p)

    def make_py_file(self):
        body = """import argparse
import zipfile
import tqdm
import sys
import os

_file = os.path.abspath(sys.argv[0])

def resource(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS)
    else:
        return os.path.join(_file, path)

def uncompress(directory):
    with zipfile.ZipFile(resource("{zip_file}"), "r") as zip:
        for f in tqdm.tqdm({files}, desc="uncompressing... ", leave=True, ascii=".#"):
            zip.extract(f, os.path.join(directory, f))

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--install-directory", nargs="?", default=".")
    return parser.parse_args()

def main():
    args = argument()
    uncompress(args.install_directory)

if __name__== "__main__":
    main()""".format(zip_file=self.zip_file, files=self.files)
        with open(self.name+".py", "w") as f:
            f.write(body)