
import os
from datetime import datetime

# main class with the interpreter code
class Interpreter:
    def __init__(self):
        self.VERSION = "1.1"
        self.reset()

    def reset(self):
        self.memory = [0, 0, 0]
        self.currentcell = 0

    # opens and runs a bf file
    def run_file(self, fname):
        if not os.path.isfile(fname):
            print(f"Error: File '{fname}' not found")
            return
        code = self._get_file_content(fname)
        self.run_code(code)

    # gets text in a file
    def _get_file_content(self, fname):
        f = open(fname, "r")
        cont = f.read()
        f.close()
        return cont

    def _get_datetime(self):
        return datetime.now().strftime("%a, %e.%m - %R:%S")

    # a loop where you can input and run bf code
    def console(self):
        # greeting
        print("Welcome to the Brainfuck console!")
        print(f"Brainfuck {self.VERSION}, {self._get_datetime()} on {os.name}")
        inp = input("bf> ")
        # enter ":q" to exit
        while inp != ":q":
            # ":r" resets the interpreter
            if inp == ":r":
                self.reset()
            # ":e" to run a file
            elif inp == ":e":
                fname = input("filename> ")
                self.run_file(fname)
            elif inp == ":l":
                if os.name == "nt": os.system("cls")
                else: os.system("clear")
            # just run raw bf code
            else:
                try:
                    self.run_code(inp)
                except KeyboardInterrupt:
                    print("Execution terminated by user.")
                    self.print_debug_info()
            print()
            try:
                inp = input("bf> ")
            except KeyboardInterrupt:
                print("Program terminated by user")
                exit(1)

    def run_code(self, code: str):
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
            #print(f"after: {status}")
            #print(return_to)

    # runs one bf command
    # status:
    # 0 - just ran the command
    # 1 - entered a loop
    # 2 - return back to the beginning of the loop
    # 3 - skipping a loop
    def execute(self, command):
        status = 0
        if command == '+':
            self.modify_current_cell(True)
        if command == '-':
            self.modify_current_cell(False)
        if command == '<':
            self.currentcell -= 1
            if self.currentcell < 0:
                self.currentcell = 0
        if command == '>':
            self.currentcell += 1
        if command == ',':
            self._input()
        if command == '.':
            self._output(self.memory[self.currentcell])
        if command == "#":
            self.print_debug_info()
        if command == '[':
            if self.memory[self.currentcell] == 0: status = 3
            else: status = 1
        if command == ']':
            status = 2
        #print(f"in exe: {status}")
        return status

    # +/- bf commands
    def modify_current_cell(self, mode=True):
        try:
            if mode:
                self.memory[self.currentcell] += 1
                return
            self.memory[self.currentcell] -= 1
            if self.memory[self.currentcell] < 0: self.memory[self.currentcell] = 0
        except IndexError:
            if mode:
                for cell in range(self.currentcell - len(self.memory)):
                    self.memory.append(0)
                self.memory.append(1)
                return
            for cell in range(self.currentcell + 1 - len(self.memory)):
                self.memory.append(0)

    # prints debug information
    def print_debug_info(self):
        print("==========DEBUG==========")
        print(f"memory: {self.memory}")
        print(f"pointer: {self.currentcell}")
        print("=========================")

    # prints a char to the terminal (bf .)
    def _output(self, number):
        if number < 32: number = 32
        print(chr(number), end="")

    # input a char (bf ,)
    def _input(self):
        inp = input("\nbf input> ")
        if len(inp) > 1:
            inp = inp[0]
            print("?> " + inp)
        try:
            self.memory[self.currentcell] = ord(inp)
        except IndexError:
            self._fill_cells()
            self.memory[self.currentcell] = ord(inp)

    def _fill_cells(self):
        for cell in range(self.currentcell + 1 - len(self.memory)):
            self.memory.append(0)
