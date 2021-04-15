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

Starts a BF console where you can live run BF code and open files.

### Run BF code: `interpreter.run_code(code: str)`

Runs raw bf code.

### Modify current cell: `interpreter.modify_current_cell(mode: bool)`

Equivalent to +/- BF command. Set `mode` to `True` if you want `+` or `False` if you want `-`.

### Execute command: `interpreter.execute(command: chr)`

Executes a single BF command.

### Debug info: `interpreter.print_debug_info()`

Prints information like current memory state, current cell pointer and loops.

## Console commands

### Exit: `:q`

### Run file: `:e`

### Reset interpreter: `:r`

### Clear the console: `:l`






