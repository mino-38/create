from configparser import ConfigParser
from dataclasses import dataclass

parser = ConfigParser()

class CreateSyntaxError(Exception):
    pass

@dataclass
class Data:
    Script_File: str
    output_name: str
    installer_type: str
    use_exe_library: str
    console: bool
    debug: bool

    @property
    def cui(self):
        return True if (not self.installer_type or self.installer_type.lower() == "cui") else False

    @property
    def noconsole(self):
        return not self.console

    @property
    def exe(self):
        return self.Script_File.endswith(".py")

class Parser:
    def __init__(self, path):
        self.file = path

    def parse(self, debug):
        parser.read(self.file)
        try:
            data = parser["data"]
        except KeyError:
            raise CreateSyntaxError("Please specify the data field")
        option = dict(parser).get("option", dict())
        try:
            return Data(
                Script_File=data["ScriptFile"],
                output_name=data.get("Name"),
                installer_type=option.get("Type"),
                use_exe_library=option.get("UseExeLiblary", "pyinstaller"),
                console=self._syntax_console(option.get("Console")),
                debug=debug
            )
        except KeyError:
            raise CreateSyntaxError("Please specify the value of ScriptFile")

    def _syntax_console(self, v):
        if not v or v.lower() == "true":
            return True
        elif v.lower() == "false":
            return False
        else:
            raise CreateSyntaxError("Value of console is wrong")