from enderpearl import *

class MyCommand(Command):
    def __init__(self) -> None: super().__init__("mycommand",
        simple = "My command description",
        description = "mycommand <args>"
    )
    def run(self, cliargs: list[str]) -> bool:
        if h(self.name, cliargs): return HANDLED
        LOG.log("My command has been run!")
        return HANDLED

MYCOMMAND = MyCommand()
COMMANDS.add(MYCOMMAND)

def command_parser(cmd: str, args: list[str]) -> bool:
    if cmd.startswith("help"):
        if HELP.run(args): return HANDLED

    elif cmd.startswith("mycommand"):
        if MYCOMMAND.run(args): return HANDLED

    return NOT_HANDLED

def helper() -> str: return COMMANDS.as_list_help()