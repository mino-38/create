import subprocess
import zipfile
import tqdm
import glob
import sys
import os

_cwd = os.getcwd()

class Create_Installer:
    def __init__(self, script_path, console, run_exe):
        self.path = script_path
        self.name = os.path.splitext(os.path.basename(os.path.abspath(self.path)))[0]
        self.console = console
        self.dist = None
        if run_exe:
            self.run_exe()

    def run_exe(self):
        cmd = ["pyinstaller", self.path]
        self._is_success(subprocess.run(cmd))
        self.dist = "dist"

    def _is_success(self, p):
        if p.return_code !=0:
            sys.exit(p.return_code)

    def compress(self):
        target = self.dist if self.dist else self.path
        os.chdir(target)
        self.files = glob.glob("*")
        os.chdir(_cwd)
        self.zip_file = self.name+".zip"
        with zipfile.ZipFile(self.zip_file, "w", compression=zipfile.ZIP_DEFLATED) as zip:
            for f in tqdm.tqdm(self.files, desc="compressing... ", leave=True, ascii=".#"):
                zip.write(f, arcname=f)