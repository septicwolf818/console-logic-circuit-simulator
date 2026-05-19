# Console Logic Circuit Simulator

Terminal-based logic circuit simulator for learning logic design. Zero external dependencies.

Build circuits with levers (inputs), logic gates (Buffer, Not, And, Nand, Or, Nor, Xor, Xnor), and outputs. Run them interactively, generate truth tables, validate connections, and save/load designs.

## Quick start

```sh
python -m pylogic
# or
python pylogic.py
```

Requires Python 3.7+. No pip install needed.

## Examples

```sh
python -c "from pylogic import DeviceManager; DeviceManager().load_state_from_file('examples/half_adder.clcs').truth_table()"
```

Circuit files (`examples/*.clcs`) include: not_gate, and_gate, or_gate, xor_gate, half_adder, full_adder.
