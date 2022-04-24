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
    def __init__(self, script_path, name, console, run_exe, use_cmd, debug):
        self.path = script_path
        self.name = name or os.path.splitext(os.path.basename(os.path.abspath(self.path)))[0]+"-installer"
        self.console = console
        self.cmd = use_cmd
        self.run_exe = run_exe
        self.debug = debug
        self.dist = None
        self._remove = []
        self._is_win = platform.system() == "Windows"
        if run_exe:
            self.make_exe()

    def _build_cmd(self, file, *args):
        if self.cmd == "pyinstaller":
            cmd = ["pyinstaller", file]
            cmd.extend(list(args))
        else:
            cmd = ["cxfreeze", "-c", file, "--target-dir", "dist"]
        return cmd

    def make_exe(self):
        print("\ncreating executable file...")
        cmd = self._build_cmd(self.path, "--clean")
        self._is_success(subprocess.run(cmd))
        self.dist = "dist"
        
    def _is_success(self, p):
        if p.returncode != 0:
            sys.exit(p.returncode)

    def compress(self):
        print()
        target = self.dist if self.dist else self.path
        os.chdir(target)
        self.files = [f for f in glob.glob("**", recursive=True) if os.path.isfile(f)]
        os.chdir(_cwd)
        self.zip_file = self.name+".zip"
        with zipfile.ZipFile(self.zip_file, "w", zipfile.ZIP_DEFLATED) as zip:
            for f in tqdm.tqdm(self.files, desc="compressing... ", leave=True, ascii=".#"):
                zip.write(os.path.join(target, f), arcname=f)
        self._remove.append(self.zip_file)

    def make_installer(self, gui=True):
        print("\ncreating installer...")
        cmd = self._build_cmd(self.name+".py", "--onefile", "--clean")
        if self.cmd == "pyinstaller":
            if gui:
                cmd.append("--noconsole")
                if self._is_win:
                    cmd.append("--windowed")
        p = subprocess.run(cmd)
        self._is_success(p)
        self._remove.append("build")
        if self.cmd == "cx_Freeze":
            shutil.move(self.zip_file, os.path.join("dist", self.zip_file))

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
        if not self.debug:
            for f in self._remove:
                self._rm(f)
