# Console Logic Circuit Simulator — Agent Guide

## Run

```sh
python -m pylogic        # preferred
python pylogic.py        # convenience wrapper
```

Pure terminal TUI. Zero external dependencies, no graphics.

## Package layout

| Path | Purpose |
|---|---|
| `pylogic/__main__.py` | Entrypoint — calls `DeviceManager().start()` |
| `pylogic/device.py` | Device base, `@register` decorator, mixins, 10 gate classes |
| `pylogic/manager.py` | `DeviceManager` — circuit logic, REPL, persistence |
| `pylogic/tui.py` | ANSI colour helpers, menu renderer |
| `pylogic/__init__.py` | Re-exports key symbols |
| `pylogic.py` | Root wrapper script |
| `examples/*.clcs` | Example circuit files (not_gate, and_gate, half_adder …) |

## Key patterns

- **Polymorphic manager.** No `isinstance` type switches. Manager uses `device.get_input_ports()`, `device.get_connection()`, `device.set_input_value()`, `device.manage_cli()`.
- **`@register` registry.** Adding a gate = write a class, mix in `SingleInputMixin` or `TwoInputMixin`, implement `output()`, decorate with `@register`. No wiring needed.
- **Graph evaluation.** `get_output(id)` recursively resolves inputs, sets cached values via `set_input_value()`, calls `output()`. `Lever.set_state()` triggers `update_all_outputs()`.
- **Persistence.** `.clcs` files are JSON arrays of device dicts. Backward-compatible with the old flat `src/` structure.

## Adding a new gate

```python
@register
class MyGate(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("MyGate")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 1 if self.input_values["A"] != self.input_values["B"] else 0
```

## REPL options

| Key | Action |
|---|---|
| 1 | Add device (pick from registered types) |
| 2 | List devices |
| 3 | Set lever states interactively |
| 4 | Run circuit (show all values) |
| 5 | Truth table (all 2^n combos) |
| 6 | Validate circuit (unconnected ports, cycles) |
| 7 | Manage device (by ID — attach/rename/set state) |
| 8 | Save state to `.clcs` |
| 9 | Load state from `.clcs` |
| 0 | Quit |
