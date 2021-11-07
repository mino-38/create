import argparse
import sys
import os

_file = os.path.abspath(sys.argv[0])

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("Script_File", default=os.path.join(os.path.dirname(_file),"__main__.py"))
    parser.add_argument("-o", "--output", default="")
    parser.add_argument("-c", "--cui", action="store_true")
    parser.add_argument("-e", "--exe", action="store_true")
    parser.add_argument("--noconsole", action="store_false")
    return parser.parse_args()

def main():
    args = argument()
    if not os.path.exists(args.Script_File):
        print("{} does not exists".format(args.Script_File))
        return 1
    if args.cui:
        from create.lib.cui_installer import create
    else:
        from create.lib.gui_installer import create
    setup = create(
        args.Script_File,
        name=args.output,
        console=args.noconsole,
        run_exe=args.exe
    )
    setup.run()

if __name__ == "__main__":
    sys.exit(main())