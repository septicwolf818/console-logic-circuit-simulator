from abc import ABC, abstractmethod
from typing import Optional

_device_registry: dict[str, type["Device"]] = {}

def register(cls):
    _device_registry[cls.__name__] = cls
    return cls

def get_device_types() -> list[str]:
    return list(_device_registry.keys())

class Device(ABC):
    def __init__(self, device_type: str):
        self.device_type = device_type
        self.id = 0
        self.name = ""

    def set_id(self, id: int):
        self.id = id

    @abstractmethod
    def output(self) -> int:
        pass

    def get_input_ports(self) -> list[str]:
        return []

    def get_connection(self, port: str) -> int:
        return -1

    def set_connection(self, port: str, device_id: int):
        pass

    def set_input_value(self, port: str, value: int):
        pass

    def get_connections(self) -> list[tuple[str, int]]:
        return [(p, self.get_connection(p)) for p in self.get_input_ports()]

    def validate(self) -> list[str]:
        errors = []
        for port, conn_id in self.get_connections():
            if conn_id < 0:
                errors.append(f"  {self}: port '{port}' not connected")
        return errors

    def to_dict(self) -> dict:
        return {"device_type": self.device_type, "id": self.id}

    def manage_cli(self, manager: "DeviceManager") -> str:
        return "Nothing to configure"

    def __str__(self):
        label = self.device_type
        if self.name:
            label += f" [{self.name}]"
        label += f"(id={self.id})"
        return label

    @classmethod
    def from_dict(cls, data: dict) -> "Device":
        dtype = data["device_type"]
        if dtype not in _device_registry:
            raise ValueError(f"Unknown device type: {dtype}")
        return _device_registry[dtype].from_dict(data)


class SingleInputMixin:
    connections: dict
    input_values: dict

    def get_input_ports(self) -> list[str]:
        return ["in"]

    def get_connection(self, port: str) -> int:
        return self.connections["in"]

    def set_connection(self, port: str, device_id: int):
        self.connections["in"] = device_id

    def set_input_value(self, port: str, value: int):
        self.input_values["in"] = value

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["attached_id"] = self.connections["in"]
        data["state"] = self.input_values["in"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Device":
        device = cls()
        device.id = data["id"]
        device.connections["in"] = data.get("attached_id", -1)
        device.input_values["in"] = data.get("state", 0)
        return device

    def manage_cli(self, manager: "DeviceManager") -> str:
        print("1. Attach device\n2. Cancel\nOPTION: ", end="")
        choice = input().strip()
        if choice == "1":
            print("Device ID: ", end="")
            self.connections["in"] = int(input().strip())
            return f"Connected to device {self.connections['in']}"
        return "Canceled"


class TwoInputMixin:
    connections: dict
    input_values: dict

    def get_input_ports(self) -> list[str]:
        return ["A", "B"]

    def get_connection(self, port: str) -> int:
        return self.connections[port]

    def set_connection(self, port: str, device_id: int):
        self.connections[port] = device_id

    def set_input_value(self, port: str, value: int):
        self.input_values[port] = value

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["a_attached_id"] = self.connections["A"]
        data["b_attached_id"] = self.connections["B"]
        data["a"] = self.input_values["A"]
        data["b"] = self.input_values["B"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Device":
        device = cls()
        device.id = data["id"]
        device.connections["A"] = data.get("a_attached_id", -1)
        device.connections["B"] = data.get("b_attached_id", -1)
        device.input_values["A"] = data.get("a", 0)
        device.input_values["B"] = data.get("b", 0)
        return device

    def manage_cli(self, manager: "DeviceManager") -> str:
        print("1. Attach device to A\n2. Attach device to B\n3. Cancel\nOPTION: ", end="")
        choice = input().strip()
        if choice == "1":
            print("Device ID: ", end="")
            self.connections["A"] = int(input().strip())
            return f"Connected A to device {self.connections['A']}"
        elif choice == "2":
            print("Device ID: ", end="")
            self.connections["B"] = int(input().strip())
            return f"Connected B to device {self.connections['B']}"
        return "Canceled"


@register
class Lever(Device):
    def __init__(self, name: str = ""):
        super().__init__("Lever")
        self.name = name
        self.state = 0
        self.manager: Optional["DeviceManager"] = None

    def get_input_ports(self) -> list[str]:
        return []

    def output(self) -> int:
        return self.state

    def set_state(self, data: int):
        self.state = data
        if self.manager is not None:
            self.manager.update_all_outputs()

    def rename(self, new_name: str):
        self.name = new_name

    def to_dict(self) -> dict:
        data = Device.to_dict(self)
        data["state"] = self.state
        data["name"] = self.name
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Device":
        device = cls(data.get("name", ""))
        device.id = data["id"]
        device.state = data["state"]
        return device

    def manage_cli(self, manager: "DeviceManager") -> str:
        print("1. Set state to 1\n2. Set state to 0\n3. Rename\n4. Cancel\nOPTION: ", end="")
        choice = input().strip()
        if choice == "1":
            self.set_state(1)
            return "State set to 1"
        elif choice == "2":
            self.set_state(0)
            return "State set to 0"
        elif choice == "3":
            print("New name: ", end="")
            self.rename(input().strip())
            return f"Renamed to {self.name}"
        return "Canceled"


@register
class Not(SingleInputMixin, Device):
    def __init__(self):
        super().__init__("Not")
        self.connections = {"in": -1}
        self.input_values = {"in": 0}

    def output(self) -> int:
        return 0 if self.input_values["in"] == 1 else 1


@register
class Buffer(SingleInputMixin, Device):
    def __init__(self):
        super().__init__("Buffer")
        self.connections = {"in": -1}
        self.input_values = {"in": 0}

    def output(self) -> int:
        return self.input_values["in"]


@register
class And(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("And")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 1 if self.input_values["A"] == 1 and self.input_values["B"] == 1 else 0


@register
class Nand(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("Nand")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 0 if self.input_values["A"] == 1 and self.input_values["B"] == 1 else 1


@register
class Or(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("Or")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 1 if self.input_values["A"] == 1 or self.input_values["B"] == 1 else 0


@register
class Nor(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("Nor")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 0 if self.input_values["A"] == 1 or self.input_values["B"] == 1 else 1


@register
class Xor(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("Xor")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 1 if self.input_values["A"] != self.input_values["B"] else 0


@register
class Xnor(TwoInputMixin, Device):
    def __init__(self):
        super().__init__("Xnor")
        self.connections = {"A": -1, "B": -1}
        self.input_values = {"A": 0, "B": 0}

    def output(self) -> int:
        return 1 if self.input_values["A"] == self.input_values["B"] else 0


@register
class Output(SingleInputMixin, Device):
    def __init__(self, name: str = ""):
        super().__init__("Output")
        self.name = name
        self.connections = {"in": -1}
        self.input_values = {"in": 0}

    def set_state(self, state: int):
        self.input_values["in"] = state

    def rename(self, new_name: str):
        self.name = new_name

    def output(self) -> int:
        return self.input_values["in"]

    def to_dict(self) -> dict:
        data = Device.to_dict(self)
        data["attached_id"] = self.connections["in"]
        data["name"] = self.name
        data["state"] = self.input_values["in"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Device":
        device = cls(data.get("name", ""))
        device.id = data["id"]
        device.connections["in"] = data.get("attached_id", -1)
        device.input_values["in"] = data.get("state", 0)
        return device

    def manage_cli(self, manager: "DeviceManager") -> str:
        print("1. Attach device\n2. Rename\n3. Cancel\nOPTION: ", end="")
        choice = input().strip()
        if choice == "1":
            print("Device ID: ", end="")
            self.connections["in"] = int(input().strip())
            return f"Connected to device {self.connections['in']}"
        elif choice == "2":
            print("New name: ", end="")
            self.rename(input().strip())
            return f"Renamed to {self.name}"
        return "Canceled"
