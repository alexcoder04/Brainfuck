# BF interpreter in Python

## Usage in a Python script
```python
from interpreter import Interpreter

interpreter = Interpreter()
interpreter.run_file("your_code.bf")
interpreter.print_debug_info()
# ...
```
## Methods

### Reset interpreter: `interpreter.reset()`

Resets the memory, the cell pointer and the loops.

### Run BF file: `interpreter.run_file(filename: str)`

Opens the file and runs it.

### Open console: `interpreter.console()`

Starts a BF console where you can live run BF code and run additional commands.

### Run BF code: `interpreter.run_code(code: str, extra_commands: bool)`

Runs bf code.
With `extra_commands`, you can decide whether those can be run or not (see below).

### Modify current cell: `interpreter.modify_current_cell(mode: bool)`

Equivalent to +/- BF command. Set `mode` to `True` if you want `+` or `False` if you want `-`.

### Execute command: `interpreter.execute(command: chr)`

Executes a single BF command.

### Debug info: `interpreter.print_debug_info()`

Prints information like current memory state, current cell pointer and loops.

### Help: `interpreter.print_help()`

Prints some help.

# Console

You can start a bf console by calling `interpreter.console()`.
In there, you can run raw bf code and extra commands.

## Extra commands

Extra commands are commands that not belong to the standard Brainfuck.
These are some Vim-inspired bindings which can be useful for the interactive bf console.
They must be on a separate line, start with `:` and `interpreter.run_code` must receive the argument `extra_commands=True`.

### Exit: `:q`, `:quit`, `:exit`

### Run file: `:e path/to/file.bf`

### Reset interpreter: `:r`

### Clear the console: `:l`

### Print help text: `:help`

### Write code that was run in the session to a file: `:w path/to/file.bf`

# Scripting

You can also write files with bf code and execute them.
You can use all normal commandsa and extra commands there.
You can also create one-line-comments with `;`. Example:

```brainfuck
; a program that prints "hello"
; prints h
++++++[>++++++++++++<-]
>.[-]<
; prints e
++++++++++[>++++++++++<-]>+<
>.[-]<
; prints l two times
+++++++++[>++++++++++++<-]
>..[-]<
; prints o
+++++++++++[>++++++++++<-]>+<
>.[-]<
```



