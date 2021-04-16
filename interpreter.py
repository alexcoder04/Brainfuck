
import os
import sys
import re
from datetime import datetime

# main class with the interpreter code
class Interpreter:
    def __init__(self):
        self.VERSION = "1.1"
        self.reset()

    def reset(self):
        self.memory = [0, 0, 0]
        self.pointer = 0

    # opens and runs a bf file
    def run_file(self, fname):
        if not os.path.isfile(fname):
            print(f"Error: File '{fname}' not found")
            return
        code = self._read_file(fname)
        self.run_code(code, extra_commands=True)

    # gets text in a file
    def _read_file(self, fname):
        f = open(fname, "r")
        cont = f.read()
        f.close()
        return re.sub(";.*", "", cont)

    def _get_datetime(self):
        return datetime.now().strftime("%a, %e.%m - %R:%S")

    # a loop where you can input and run bf code
    def console(self):
        # greeting
        print("Welcome to the Brainfuck console!")
        print(f"Brainfuck {self.VERSION}, {self._get_datetime()} on {os.name}")
        while True:
            try:
                self.run_code(input("\nbf> "), extra_commands=True)
            except KeyboardInterrupt:
                print("Terminated by user")
                exit(1)

    def run_extra(self, command: str):
        if command.startswith("q") or command.startswith("quit") or command.startswith("exit"):
            exit(0)
        if command.startswith("r"):
            self.reset()
            return
        if command.startswith("e"):
            try: fname = command.split()[1]
            except IndexError: print("You need to provide an argument to ':e'")
            else: self.run_file(fname)
        if command.startswith("l"):
            if os.name == "nt": os.system("cls")
            else: os.system("clear")
            return
        if command.startswith("help"):
            self.print_help()
            return
        print(f"Command '{command.split()[0]}' was not found")

    def _run(self, code):
        pointer = 0
        return_to = []
        returned = False
        while pointer < len(code):
            status = self.execute(code[pointer])
            if status == 0:
                pointer += 1
            if status == 1:
                if not returned:
                    return_to.append(pointer)
                pointer += 1
            if status == 2:
                pointer = return_to[-1]
                returned = True
            if status == 3:
                while code[pointer] != "]":
                    pointer += 1
                del return_to[-1]
                returned = False
                pointer += 1
            # print(f"after: {status}")
            # print(return_to)

    def run_code(self, code: str, extra_commands=False):
        if extra_commands:
            for line in code.split("\n"):
                if line.startswith(":"):
                    self.run_extra(line[1:])
                    continue
                self._run(line)
            return
        self._run(code)

    # runs one bf command
    # status:
    # 0 - just ran the command
    # 1 - entered a loop
    # 2 - return back to the beginning of the loop
    # 3 - skipping a loop
    def execute(self, command):
        status = 0
        if command == '+': self.modify_current_cell(True)
        if command == '-': self.modify_current_cell(False)
        if command == ',': self._input()
        if command == '.': self._output()
        if command == "#": self.print_debug_info()
        if command == '<':
            self.pointer -= 1
            if self.pointer < 0: self.pointer = 0
        if command == '>':
            self.pointer += 1
            self._fill_cells()
        if command == '[':
            if self.memory[self.pointer] == 0: status = 3
            else: status = 1
        if command == ']':
            status = 2
        return status

    # +/- bf commands
    def modify_current_cell(self, mode=True):
        self._fill_cells()
        if mode:
            self.memory[self.pointer] += 1
            return
        self.memory[self.pointer] -= 1
        if self.memory[self.pointer] < 0: self.memory[self.pointer] = 0

    # prints debug information
    def print_debug_info(self):
        print()
        print("==========DEBUG==========")
        print(f"memory: {self.memory}")
        print(f"pointer: {self.pointer}")
        print("=========================")
        print()

    def print_help(self):
        print("Help was not implemented yet")

    # prints a char to the terminal (bf .)
    def _output(self):
        number = self.memory[self.pointer]
        if number < 32: number = 32
        #print(chr(number), end="")
        sys.stdout.write(chr(number))

    # input a char (bf ,)
    def _input(self):
        inp = input("\nbf input> ")
        if len(inp) > 1:
            inp = inp[0]
            print("?> " + inp)
        if len(inp) < 1:
            self.memory[self.pointer] = 0
            return
        self._fill_cells()
        self.memory[self.pointer] = ord(inp)

    def _fill_cells(self):
        for cell in range(self.pointer + 1 - len(self.memory)):
            self.memory.append(0)
