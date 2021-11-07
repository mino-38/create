import argparse
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
    with zipfile.ZipFile(resource("create-installer.zip"), "r") as zip:
        for f in tqdm.tqdm(['__init__.py', '__pycache__', '__main__.py', 'lib'], desc="uncompressing... ", leave=True, ascii=".#"):
            zip.extract(f, os.path.join(directory, f))

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--install-directory", nargs="?", default=".")
    return parser.parse_args()

def main():
    args = argument()
    uncompress(args.install_directory)

if __name__== "__main__":
    main()