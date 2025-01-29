# Console Logic Circuit Simulator

A simple console-based logic circuit simulator.

With this simulator, you can see how logic circuits work. Use logic gates such as And, Nand, Not, Or, and Xor to connect levers and logic outputs to see how the system behaves in a given situation.

## Features

- Simulate basic logic gates: And, Nand, Not, Or, Xor
- Create and manage devices like Levers and Outputs
- Save and load circuit states
- Render circuit graphs
- GUI for managing and visualizing circuits

## Requirements

This project requires Python >= 3.7 and the following Python packages:

- `tkinter`
- `Pillow`
- `graphviz`

To install these packages, run:

```sh
pip install tkinter Pillow graphviz
```

Additionally, you need to install Graphviz on your system. On Ubuntu, you can install it with:

```sh
sudo apt-get install graphviz
```

## How to Run

### Console Mode

To start the simulator in console mode, run the `pylogic.py` file:

```sh
python pylogic.py
```

This will start the main simulator loop.

### GUI Mode

To start the simulator in GUI mode, run the `pylogic.py` file with the `--gui` option:

```sh
python pylogic.py --gui
```

This will launch the GUI for managing and visualizing circuits.

## Example Circuits

### Half Adder

A half adder circuit with inputs A and B, and outputs Sum and Carry.

```json
[
    {"device_type": "Lever", "id": 0, "state": 1, "name": "A"},
    {"device_type": "Lever", "id": 1, "state": 0, "name": "B"},
    {"device_type": "Xor", "id": 2, "a_attached_id": 0, "b_attached_id": 1, "a": 1, "b": 0},
    {"device_type": "And", "id": 3, "a_attached_id": 0, "b_attached_id": 1, "a": 1, "b": 0},
    {"device_type": "Output", "id": 4, "attached_id": 2, "name": "Sum", "state": 1},
    {"device_type": "Output", "id": 5, "attached_id": 3, "name": "Carry", "state": 1}
]
```

### Full Adder

A full adder circuit with inputs A, B, and Cin, and outputs Sum and Carry Out.

```json
[
    {"device_type": "Lever", "id": 0, "state": 1, "name": "A"},
    {"device_type": "Lever", "id": 1, "state": 0, "name": "B"},
    {"device_type": "Lever", "id": 2, "state": 1, "name": "Cin"},
    {"device_type": "Xor", "id": 3, "a_attached_id": 0, "b_attached_id": 1, "a": 1, "b": 0},
    {"device_type": "And", "id": 4, "a_attached_id": 0, "b_attached_id": 1, "a": 1, "b": 0},
    {"device_type": "Xor", "id": 5, "a_attached_id": 3, "b_attached_id": 2, "a": 1, "b": 1},
    {"device_type": "And", "id": 6, "a_attached_id": 3, "b_attached_id": 2, "a": 1, "b": 1},
    {"device_type": "Or", "id": 7, "a_attached_id": 4, "b_attached_id": 6, "a": 1, "b": 1},
    {"device_type": "Output", "id": 8, "attached_id": 5, "name": "Sum", "state": 1},
    {"device_type": "Output", "id": 9, "attached_id": 7, "name": "Carry Out", "state": 1}
]
```

### Complex Circuit

A complex circuit with multiple logic gates and outputs.

```json
[
    {"device_type": "Lever", "id": 0, "state": 1, "name": "Input A"},
    {"device_type": "Lever", "id": 1, "state": 0, "name": "Input B"},
    {"device_type": "And", "id": 2, "a_attached_id": 0, "b_attached_id": 1, "a": 1, "b": 0},
    {"device_type": "Not", "id": 3, "attached_id": 2, "state": 0},
    {"device_type": "Or", "id": 4, "a_attached_id": 0, "b_attached_id": 3, "a": 1, "b": 1},
    {"device_type": "Output", "id": 5, "attached_id": 4, "name": "Complex Output", "state": 1}
]
```

## Screenshot

![Ubuntu Screenshot of Gui mode](pylogic_ubuntu.png)