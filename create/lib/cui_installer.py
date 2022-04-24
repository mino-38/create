from create.lib.base import Create_Installer
import subprocess
import shutil
import sys

class create_cui_installer(Create_Installer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.compress()
        if self.run_exe:
            shutil.rmtree("dist")
        self.make_py_file()
        self.make_installer(gui=False)
        
    def make_py_file(self):
        if self.name.endswith("-installer"):
            name = self.name.rstrip("installer").rstrip("-")
        else:
            name = self.name
        with open(self.zip_file, "rb") as f:
            zip_byte = f.read()
        body = """import argparse
import subprocess
import tempfile
import zipfile
import shutil
import tqdm
import sys
import os

_file = os.path.abspath(sys.argv[0])
_FILES = {files}
_yes = False

def _path(path):
    while not os.path.isfile(path):
        if path.count(os.sep) <= 1:
            print("failed", file=sys.stderr)
            sys.exit(1)
        path = os.path.join(os.path.dirname(os.path.dirname(path)), os.path.basename(path))
    return path

def ask(path):
    global _yes
    s = _ask(path)
    while s not in ["y", "n", "A"]:
        s = _ask(path)
    if s == "y":
        return True
    elif s == "n":
        print("failed to install")
        sys.exit(1)
    else:
        _yes = True
        return _yes

def _ask(path):
    tqdm.tqdm.write("\\"%s\\" has already exists\\ncan I overwrite?[y/n/A]\\n" % path, end="")
    return sys.stdin.readline().strip()

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
    with tempfile.NamedTemporaryFile("wb") as tmp:
        tmp.write({zip_byte})
        with zipfile.ZipFile(tmp.name) as zip:
            for f in tqdm.tqdm(_FILES):
                if not os.path.isdir(os.path.dirname(f) or "."):
                    os.makedirs(os.path.dirname(f), exist_ok=True)
                if os.path.exists(f):
                    if not _yes:
                        ask(os.path.abspath(f))
                    if os.path.isfile(f):
                        os.remove(f)
                    else:
                        shutil.rmtree(f)
                zip.extract(f)
                tqdm.tqdm.write("create '%s'" % os.path.abspath(f))

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--install-directory", nargs="?", default=".")
    return parser.parse_args()

def main(title=True):
    args = argument()
    if title:
        print("This is a '{name}' setupper\\nDo you want to install this in '%s'?" % os.path.abspath(args.install_directory))
    else:
        print("Do you want to install this in '%s'?" % os.path.abspath(args.install_directory))
    print("[y/n/C] ", end="")
    sys.stdout.flush()
    s = sys.stdin.readline().rstrip().lower()
    while s not in ["y", "n", "c", "yes", "no", "change"]:
        print("[y/n/C] ", end="")
        sys.stdout.flush()
        s = sys.stdin.readline().rstrip().lower()
    if s in ["y", "yes"]:
        uncompress(args.install_directory)
        print("\\ndone.")
    elif s in ["c", "change"]:
        print("Please enter the installing to directory\\n> ", end="")
        dir = sys.stdin.readline().rstrip()
        sys.argv = [sys.argv[0], "-d", dir]
        main(title=False)

if __name__== "__main__":
    main()""".format(files=self.files, zip_byte=zip_byte, name=name)
        with open(self.name+".py", "w") as f:
            f.write(body)
        self._remove.append(self.name+".py")
        self._remove.append(self.zip_file)
