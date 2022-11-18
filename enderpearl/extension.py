import enderpearl


"""
If the the '--release' flag is passed, this will be set to True
otherwise it will be set to False
Modifications highly unrecommended
"""
RELEASE: bool


"""
Called to retrieve the help command value
called when the user runs the help command
Modification highly recommended
"""
def helper() -> str:
    return "HELP MESSAGE HERE"


"""
Command parser, called when a command has been recieved
This is where you can add your own commands
Modification highly recommended
"""
def command_parser(cmd: str) -> None:
    # Automatically handles help command
    # Should be the first to be handled
    if cmd.startswith("help"): return print(helper())



    # This is where you can add your own commands
    elif cmd.startswith("mycommand"):
        return run(cmd)



    # Runs command from .enderpearl file
    else: return enderpearl.parser.default_run(cmd)


"""
Recomended way to handle your own commands
Modification encouraged
"""
def run(cmd: str) -> None:
    print("Recieved command: " + cmd + ", release: " + str(enderpearl.extension.RELEASE))
    return
