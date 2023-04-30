if __name__ == "__main__": raise Exception("This file is not meant to be run directly")
from abc import ABC, abstractmethod
from typing import Callable
HANDLED = True
NOT_HANDLED = False
def conc(*args: object) -> list[object]:
    out: list[object] = []
    for arg in args:
        if isinstance(arg, list): out += arg
        else: out.append(arg)
    return out
class COLORS:
    GRAY = "\033[90m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
class Command():
    def __init__(self, name: str, **args: str) -> None:
        self.name: str = name
        self.simple: str = args.get("simple", "No simple discription provided")
        self.description: str = args.get("description", "No description provided")
        self.color: str = args.get("color", COLORS.OKGREEN)
    def as_simple_help(self) -> str: return f"{self.color}{self.name}{COLORS.ENDC}: {self.simple}"
    def as_list_help(self) -> str: return f"  - {self.color}{self.name}{COLORS.ENDC}: {self.simple}"
    def as_full_help(self) -> str: return f"{self.color}{self.name}{COLORS.ENDC}: {self.description}"
    @abstractmethod
    def run(self, cliargs: list[str], **args: object) -> bool: pass
class CommandGroup(ABC):
    def __init__(self) -> None: self.commands: dict[str, Command] = {}
    def add(self, command: Command) -> None: self.commands[command.name] = command
    def get(self, name: str) -> Command: return self.commands[name]
    def as_list_help(self) -> str:
        res = ""
        i = 0
        LEN = self.commands.__len__()
        for command in self.commands:
            i += 1
            res += self.commands[command].as_list_help() + ("\n" if i < LEN else "")
        return res
    def display_command_help(self, name: str) -> None: LOG.log(self.commands[name].as_full_help())
    def __iter__(self): return iter(self.commands)
    def __str__(self) -> str: return self.as_list_help()
class Logger():
    def __init__(self, logger: Callable[..., None]) -> None: self.logger: Callable[..., None] = logger
    def log(self, *args: object): self.logger(" ".join([arg.__str__() for arg in args]))
def h(cmd: str, args: list[str], checkForLength: bool = True) -> bool:
    if (
        args.__contains__("-h") or
        args.__contains__("--help") or
        args.__contains__("help") or
        ((args.__len__() <= 0) if checkForLength else False)
    ):
        COMMANDS.display_command_help(cmd)
        return HANDLED
    return NOT_HANDLED
def unsafeRun(func: Callable[..., object], *args: object, **kvargs: bool) -> object:
    try:
        return func(*args)
    except Exception as e:
        import sys
        if "-Fdebug" in sys.argv:
            print(COLORS.FAIL+"Failed to run function: "+COLORS.ENDC+func.__name__)
            print(COLORS.FAIL+"Error:"+COLORS.ENDC,end=" ")
            print(e)
        if kvargs.get("panic", True):
            exit(1)
def osRun(cmd: str) -> None:
    def osRunner(cmd: str):
        import os
        RES = os.system(cmd)
        if RES != 0:
            raise Exception("Failed to run command: " + cmd)
    unsafeRun(osRunner, cmd)
class HelpCommand(Command):
    def __init__(self) -> None: super().__init__("help",
        simple = "shows this help message",
        description = f"""Shows this help message.
      If you need help with a specific command, add a {COLORS.HEADER}-h{COLORS.ENDC} to the end.""",
        color = COLORS.OKGREEN
    )
    def run(self, cliargs: list[str]) -> bool:
        if h(self.name, cliargs, False): return HANDLED
        LOG.log(COMMANDS.as_list_help())
        return HANDLED
COMMANDS = CommandGroup()
LOG = Logger(print)
HELP = HelpCommand()
COMMANDS.add(HELP)

# 
# MIT License
# 
# Copyright (c) 2022 AtomicGamer9523
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
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
