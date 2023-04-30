import platform, shutil, sys, os
from enderpearl.utils import *
from enum import Enum
class TokenType(Enum):
    CommandName = 1,
    Command = 2,
    NONE = 3
class Command(object):
    def __init__(self, command: str):
        self.command: str = command
    def run(self, root: str = "") -> None:
        osRun(
            "cd " + os.getcwd() +
            ("\\" if platform.system() == "Windows" else "/") +
            root + " && " + self.command
        )
class Operation(object):
    def __init__(self):
        self.name: str = ""
        self.commands: list[Command] = []
    def run(self, root: str = "") -> None:
        for command in self.commands:
            command.run(root)
class EnderPearl(object):
    def __init__(self, prnt: bool = True):
        self.prnt: bool = prnt
        self.operations: list[Operation] = []
    def newop(self, op: Operation) -> None:
        self.operations.append(op)
    def run(self, name: str, root: str = "") -> None:
        runcmd(name, self, root)
def tokenize(string: str, prefix: str = "#") -> EnderPearl:
    efile = EnderPearl(True)
    op = Operation()
    opstr, cmds = "", ""
    txttype = TokenType.NONE
    for part in string:
        if part == prefix:
            op = Operation()
            txttype = TokenType.CommandName
        elif part == "(":
            txttype = TokenType.Command
        elif part == ")":
            txttype = TokenType.NONE
            for part in opstr:
                if part == "\n":
                    if cmds != "":
                        op.commands.append(Command(cmds))
                    cmds = ""
                else:
                    cmds += part
            efile.newop(op)
            op = Operation()
            opstr = ""
        elif txttype == TokenType.CommandName and part != " ":
            op.name += part
        elif txttype == TokenType.Command and part != "\r":
            opstr += part
    return efile
def runcmd(cmd: str, tkn: EnderPearl, root: str = "") -> None:
    for op in tkn.operations:
        if op.name.lower() == "pre": op.run(root)
    for op in tkn.operations:
        if op.name.lower() == cmd: op.run(root)
    for op in tkn.operations:
        if op.name.lower() == "post": op.run(root)
def main():
    import enderpearl.extension
    def argfilter(x: str): return not (x == "-Fdebug" or x == "--clean")
    should_clean: bool = True
    if "--clean" in sys.argv: should_clean = True
    SYSARGS = list(filter(argfilter,sys.argv))
    if len(SYSARGS) < 2: cmd = "help"
    else: cmd = str(SYSARGS[1])
    if cmd.startswith("-h") or cmd.startswith("--help"): cmd = "help"
    enderpearl.extension.command_parser(cmd, SYSARGS[2:])

    if should_clean:
        unsafeRun(shutil.rmtree, "./enderpearl/__pycache__", panic=False)
        unsafeRun(shutil.rmtree, "./__pycache__", panic=False)
    sys.exit(0)
unsafeRun(main)

# 
# MIT License
# 
# Copyright (c) 2022 AtomicGamer9523
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without lfailableRunmitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
