from create.lib.create_parser import Parser
import argparse
import sys
import os

SPEC = "SPEC.cfg"

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("Script_File", nargs="?", default=os.path.join(os.getcwd(), "SPEC.cfg"))
    parser.add_argument("-o", "--output-name", default="")
    parser.add_argument("-c", "--cui", action="store_true")
    parser.add_argument("--onefile", action="store_true")
    parser.add_argument("-e", "--exe", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--noconsole", action="store_false")
    parser.add_argument("--use-exe-library", choices=["pyinstaller", "cx_Freeze"], default="pyinstaller")
    return parser.parse_args()

def main():
    args = argument()
    if not os.path.exists(args.Script_File):
        print("{} does not exists".format(args.Script_File))
        return 1
    if args.Script_File.endswith(SPEC):
        args = Parser(SPEC).parse(args.debug)
    if args.cui:
        from create.lib.cui_installer import create_cui_installer as create
    else:
        from create.lib.gui_installer import create_gui_installer as create
    with create(
        args.Script_File,
        name=args.output_name,
        onefile=args.onefile,
        console=args.noconsole,
        run_exe=args.exe,
        use_cmd=args.use_exe_library,
        debug=args.debug
    ) as installer:
        installer.run()
    print("\n\033[32mdone\033[0m")

if __name__ == "__main__":
    sys.exit(main())
