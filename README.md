# Console Logic Circuit Simulator

A terminal-based logic circuit simulator. Design combinational circuits, run them interactively, and generate truth tables.

```sh
python -m pylogic           # start the simulator
python -m pylogic --help    # available options
```

Python 3.7+. No external dependencies.

## How it works

The simulator is a REPL menu. Add devices (levers for inputs, gates for logic, outputs for results), wire them together by ID, then run the circuit or generate a truth table. The app lists all available device types when you choose "Add device" — no need to memorise them.

## Example circuits

Pre-built circuits are in `examples/`. Load one from the REPL (option 9) or via the command line:

```sh
python -c "
from pylogic import DeviceManager
dm = DeviceManager()
dm.load_state_from_file('examples/half_adder.clcs')
dm.truth_table()
"
```

Explore them: `ls examples/`
