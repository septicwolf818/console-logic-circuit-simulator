import json
from typing import Optional
from pylogic.device import Device, Lever, Output, get_device_types, _device_registry
from pylogic import tui


class DeviceManager:
    def __init__(self):
        self.devices: list[Device] = []
        self.id = 0
        self._last_status = "Ready"

    def set_status(self, msg: str):
        self._last_status = msg

    def find_device(self, device_id: int) -> Optional[Device]:
        for d in self.devices:
            if d.id == device_id:
                return d
        return None

    def get_output(self, device_id: int) -> int:
        device = self.find_device(device_id)
        if device is None:
            return 0
        for port in device.get_input_ports():
            conn_id = device.get_connection(port)
            if conn_id >= 0:
                value = self.get_output(conn_id)
                device.set_input_value(port, value)
        return device.output()

    def update_all_outputs(self):
        for device in self.devices:
            if isinstance(device, Output):
                device.set_state(self.get_output(device.id))

    def add_device(self, device: Device):
        device.set_id(self.id)
        self.devices.append(device)
        self.id += 1
        if isinstance(device, Lever):
            device.manager = self
        self.update_all_outputs()
        self.set_status(f"Added {device.device_type} (ID {device.id})")

    def delete_device(self, device_id: int):
        self.devices = [d for d in self.devices if d.id != device_id]
        self.set_status(f"Deleted device {device_id}")

    # --- Persistence ---

    def save_state_to_file(self, filename: str):
        with open(filename, 'w') as file:
            json.dump([d.to_dict() for d in self.devices], file, indent=2)
        self.set_status(f"Saved to {filename}")

    def load_state_from_file(self, filename: str):
        try:
            with open(filename, 'r') as file:
                devices_data = json.load(file)
        except FileNotFoundError:
            self.set_status(f"File {filename} not found")
            return

        self.devices = [Device.from_dict(data) for data in devices_data]
        self.id = max(d.id for d in self.devices) + 1 if self.devices else 0

        for device in self.devices:
            if isinstance(device, Lever):
                device.manager = self

        self.update_all_outputs()
        self.set_status(f"Loaded from {filename}")

    # --- Device listing ---

    def show_devices(self):
        if not self.devices:
            print(tui.dim("  (no devices)"))
            return

        print()
        header = f"  {'ID':>3}  Type          Name          Connections        Out"
        sep = f"  {'-'*3}  {'-'*12}  {'-'*14}  {'-'*18}  {'-'*3}"
        print(tui.dim(header))
        print(tui.dim(sep))
        for d in self.devices:
            name = d.name if d.name else tui.dim("-")
            conn_parts = []
            for p, cid in d.get_connections():
                if cid >= 0:
                    conn_parts.append(f"{p}<={cid}")
                else:
                    conn_parts.append(f"{p}<=?")
            conns = ",".join(conn_parts) if conn_parts else tui.dim("-")
            out = tui.bit(d.output())
            print(f"  {d.id:>3}  {d.device_type:<12} {name:<14} {conns:<18} {out}")
        print()

    # --- Run circuit ---

    def show_all_values(self):
        if not self.devices:
            print(tui.dim("  (no devices)"))
            return
        print()
        print(tui.bold(tui.cyan("  Circuit state")))
        for d in self.devices:
            val = self.get_output(d.id)
            sym = tui.on(val)

            label = d.device_type
            if d.name:
                label += f" [{d.name}]"

            conns = "; ".join(
                f"{p}<-{tui.bit(self.get_output(cid)) if cid>=0 else '?'}"
                for p, cid in d.get_connections()
            ) if d.get_connections() else tui.dim("-")

            print(f"  {sym} {d.id:>2} {label:<20} out={tui.bit(val):>1}  ({tui.dim(conns)})")
        print()

    # --- Truth table ---

    def truth_table(self):
        levers = [d for d in self.devices if isinstance(d, Lever)]
        outputs = [d for d in self.devices if isinstance(d, Output)]

        if not levers:
            print(tui.red("  No levers in circuit"))
            return
        if not outputs:
            print(tui.red("  No outputs in circuit"))
            return

        saved = {d.id: d.state for d in levers}
        n = len(levers)

        lhs = " | ".join(f"{d.name or f'In{d.id}':>6}" for d in levers)
        rhs = " | ".join(f"{d.name or f'Out{d.id}':>6}" for d in outputs)
        header = f"  {lhs} | {rhs}"
        sep = "  " + "-" * (len(header) - 2)

        print(f"\n  {tui.bold('Truth table')} ({n} inputs, {len(outputs)} outputs)")
        print(header)
        print(tui.dim(sep))

        for combo in range(1 << n):
            for i, lev in enumerate(levers):
                bit_val = (combo >> (n - 1 - i)) & 1
                lev.state = bit_val
            self.update_all_outputs()

            lhs_vals = " | ".join(
                f"{(combo >> (n - 1 - i)) & 1:>6}" for i in range(n)
            )
            rhs_vals = " | ".join(
                f"{self.get_output(d.id):>6}" for d in outputs
            )
            print(f"  {lhs_vals} | {rhs_vals}")

        for d in levers:
            d.state = saved[d.id]
        self.update_all_outputs()
        print()

    # --- Validation ---

    def validate_circuit(self):
        errors = []
        for d in self.devices:
            errors.extend(d.validate())

        if self._has_cycle():
            errors.append("  Circuit contains a cycle (combinational loop)")

        if not errors:
            print(f"  {tui.green('Circuit looks valid')}.")
        else:
            print(f"  {tui.red('Validation errors:')}")
            for e in errors:
                print(f"    {e}")
        print()

    def _has_cycle(self) -> bool:
        visited = set()
        in_stack = set()

        def dfs(device_id: int) -> bool:
            if device_id in in_stack:
                return True
            if device_id in visited:
                return False
            device = self.find_device(device_id)
            if device is None:
                return False
            visited.add(device_id)
            in_stack.add(device_id)
            for _, conn_id in device.get_connections():
                if conn_id >= 0 and dfs(conn_id):
                    return True
            in_stack.remove(device_id)
            return False

        for d in self.devices:
            if dfs(d.id):
                return True
        return False

    # --- Quick lever states ---

    def set_levers_menu(self):
        levers = [d for d in self.devices if isinstance(d, Lever)]
        if not levers:
            print(tui.red("  No levers in circuit"))
            return

        print(f"\n  {tui.bold('Lever states')}")
        for d in levers:
            print(f"  {tui.on(d.state)} ID={d.id}  {d.name or '(unnamed)'}  [{d.state}]")

        while True:
            print(f"\n  {tui.dim('Enter lever ID to toggle, blank to done: ')}", end="")
            raw = input().strip()
            if not raw:
                break
            try:
                lid = int(raw)
                lev = self.find_device(lid)
                if lev is None or not isinstance(lev, Lever):
                    print(f"  {tui.red('Not a lever')}")
                    continue
                lev.set_state(0 if lev.state else 1)
                sym = tui.on(lev.state)
                print(f"  {sym} ID={lev.id}  {lev.name or '(unnamed)'}  [{lev.state}]")
            except ValueError:
                print(f"  {tui.red('Invalid')}")

    # --- Add device menu ---

    def add_device_menu(self):
        types = get_device_types()
        print(f"\n  {tui.bold('Device types')}")
        for i, t in enumerate(types, 1):
            print(f"  {tui.green(str(i)):>4} {t}")
        print(f"  {tui.green(str(len(types)+1)):>4} {tui.dim('Cancel')}")
        print(f"  {tui.dim('Select type: ')}", end="")

        try:
            idx = int(input().strip())
            if 1 <= idx <= len(types):
                dtype = types[idx - 1]
                self._create_device(dtype)
            else:
                print(f"  {tui.dim('Canceled')}")
        except ValueError:
            print(f"  {tui.red('Invalid')}")

    def _create_device(self, dtype: str):
        cls = _device_registry[dtype]
        if dtype in ("Lever", "Output"):
            name = input(f"  Name for {dtype}: ").strip()
            device = cls(name)
        else:
            device = cls()
        self.add_device(device)

    # --- Manage device menu ---

    def manage_device_menu(self):
        if not self.devices:
            print(tui.red("  No devices"))
            return

        while True:
            self.show_devices()
            print(f"  {tui.dim('Enter device ID to manage, blank to go back: ')}", end="")
            raw = input().strip()
            if not raw:
                break
            try:
                did = int(raw)
                device = self.find_device(did)
                if device is None:
                    print(tui.red("  Not found"))
                    continue
                print(f"\n  {tui.bold(f'Manage {device}')}")
                msg = device.manage_cli(self)
                if msg:
                    print(f"  {tui.green(msg)}")
                    self.set_status(msg)
                    self.update_all_outputs()
            except ValueError:
                print(tui.red("  Invalid"))

    # --- Main REPL ---

    def start(self):
        while True:
            count = len(self.devices)
            lever_count = sum(1 for d in self.devices if isinstance(d, Lever))
            output_count = sum(1 for d in self.devices if isinstance(d, Output))
            gate_count = count - lever_count - output_count

            status_line = f"Devices: {count}  Levers: {lever_count}  Gates: {gate_count}  Outputs: {output_count}"
            tui.menu("Logic Circuit Simulator", [
                ("1", "Add device"),
                ("2", "List devices"),
                ("3", "Set lever states"),
                ("4", "Run circuit"),
                ("5", "Truth table"),
                ("6", "Validate circuit"),
                ("7", "Manage device"),
                ("8", "Save state"),
                ("9", "Load state"),
                ("0", "Quit"),
            ], status=status_line, subtitle=self._last_status)

            choice = input().strip()

            if choice == "1":
                self.add_device_menu()
            elif choice == "2":
                self.show_devices()
            elif choice == "3":
                self.set_levers_menu()
            elif choice == "4":
                self.show_all_values()
            elif choice == "5":
                self.truth_table()
            elif choice == "6":
                self.validate_circuit()
            elif choice == "7":
                self.manage_device_menu()
            elif choice == "8":
                self.save_state()
            elif choice == "9":
                self.load_state()
            elif choice == "0":
                print(f"\n  {tui.dim('Goodbye')}")
                break
            else:
                print(tui.red("  Invalid option"))

    # --- Save/Load with prompt ---

    def save_state(self):
        fn = input("  Filename (.clcs): ").strip()
        if fn:
            self.save_state_to_file(fn)
            print(f"  {tui.green(f'Saved to {fn}')}")
        else:
            print(tui.dim("  Canceled"))

    def load_state(self):
        fn = input("  Filename (.clcs): ").strip()
        if fn:
            self.load_state_from_file(fn)
            print(f"  {tui.green(f'Loaded from {fn}')}")
        else:
            print(tui.dim("  Canceled"))
