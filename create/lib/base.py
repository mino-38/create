import subprocess
import platform
import zipfile
import tqdm
import glob
import sys
import os

_cwd = os.getcwd()

class Create_Installer:
    def __init__(self, script_path, name, console, run_exe):
        self.path = script_path
        self.name = name or os.path.splitext(os.path.basename(os.path.abspath(self.path)))[0]+"-installer"
        self.console = console
        self.dist = None
        self._is_win = platform.system() == "Windows"
        if run_exe:
            self.make_exe()

    def make_exe(self):
        cmd = ["pyinstaller", "--clean", self.path]
        self._is_success(subprocess.run(cmd))
        self.dist = "dist"

    def _is_success(self, p):
        if p.returncode !=0:
            sys.exit(p.returncode)

    def compress(self):
        target = self.dist if self.dist else self.path
        os.chdir(target)
        self.files = glob.glob("*")
        os.chdir(_cwd)
        self.zip_file = self.name+".zip"
        with zipfile.ZipFile(self.zip_file, "w", compression=zipfile.ZIP_DEFLATED) as zip:
            for f in tqdm.tqdm(self.files, desc="compressing... ", leave=True, ascii=".#"):
                zip.write(os.path.join(target, f), arcname=f)

    def make_installer(self, gui=True):
        cmd = ["pyinstaller", "--onefile", "--clean", "--add-data", "{zip}{join}{zip}".format(zip=self.zip_file, join=(";" if sys.platform == "win32" else ":"))]
        if gui:
            cmd.append("--noconsole")
            if self._is_win:
                cmd.append("--windowed")
        cmd.append(self.name+".py")
        p = subprocess.run(cmd)
        self._is_success(p)