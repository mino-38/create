import subprocess
import platform
import zipfile
import tqdm
import glob
import shutil
import sys
import os

_cwd = os.getcwd()

class Create_Installer:
    def __init__(self, script_path, name, console, run_exe):
        self.path = script_path
        self.name = name or os.path.splitext(os.path.basename(os.path.abspath(self.path)))[0]+"-installer"
        self.console = console
        self.dist = None
        self._remove = []
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
        self._remove.append(self.zip_file)

    def make_installer(self, gui=True):
        cmd = ["pyinstaller", "--onefile", "--clean", "--add-data", "{zip}{join}{zip}".format(zip=self.zip_file, join=(";" if sys.platform == "win32" else ":"))]
        if gui:
            cmd.append("--noconsole")
            if self._is_win:
                cmd.append("--windowed")
        cmd.append(self.name+".py")
        p = subprocess.run(cmd)
        self._is_success(p)
        self._remove.append("build")

    def _rm(self, path):
        if os.path.isfile(path):
            try:
                os.remove(path)
            except:
                pass
        elif os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        for f in self._remove:
            self._rm(f)