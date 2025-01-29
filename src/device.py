from typing import Union

class Device:
    def __init__(self, device_type: str):
        self.device_type = device_type
        self.id = 0

    def get_device_type(self) -> str:
        return self.device_type

    def set_id(self, id: int):
        self.id = id

    def output(self) -> int:
        raise NotImplementedError("Must be implemented by subclasses")

    def to_dict(self) -> dict:
        return {
            "device_type": self.device_type,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data: dict):
        device_type = data["device_type"]
        if (device_type == "Lever"):
            device = Lever()
        elif (device_type == "Not"):
            device = Not()
        elif (device_type == "And"):
            device = And()
        elif (device_type == "Nand"):
            device = Nand()
        elif (device_type == "Or"):
            device = Or()
        elif (device_type == "Xor"):
            device = Xor()
        elif (device_type == "Output"):
            device = Output(data["name"])
        else:
            raise ValueError(f"Unknown device type: {device_type}")
        device.id = data["id"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "ellipse"
        return f'{self.id} [label="{self.device_type} ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Device(type={self.device_type}, id={self.id})"


class Lever(Device):
    'Lever/logic input'

    def __init__(self, name: str = ""):
        super().__init__("Lever")
        self.state = 0
        self.name = name

    def output(self) -> int:
        print(f"Lever: {self.state}")
        return self.state

    def set_state(self, data: int):
        self.state = data
        print(f"New lever state: {self.state}")
        # Trigger update of all outputs when lever state changes
        if hasattr(self, 'manager'):
            self.manager.update_all_outputs()

    def rename(self, new_name: str):
        self.name = new_name

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"state": self.state, "name": self.name})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.state = data["state"]
        device.name = data["name"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "ellipse"
        return f'{self.id} [label="{self.device_type} [{self.name}] ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Lever(id={self.id}, state={self.state}, name={self.name})"


class Not(Device):
    'Logic not/inversion'

    def __init__(self):
        super().__init__("Not")
        self.attached_id = -1
        self.state = 0

    def set_state(self, data: int):
        self.state = data

    def output(self) -> int:
        result = 0 if (self.state == 1) else 1
        print(f"Not: {result}")
        return result

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"attached_id": self.attached_id, "state": self.state})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.attached_id = data["attached_id"]
        device.state = data["state"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "invtriangle"
        return f'{self.id} [label="{self.device_type} ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Not(id={self.id}, attached_id={self.attached_id}, state={self.state})"


class And(Device):
    'And logic gate'

    def __init__(self):
        super().__init__("And")
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.a = 0
        self.b = 0

    def output(self) -> int:
        result = 1 if (self.a == 1 and self.b == 1) else 0
        print(f"And: {result}")
        return result

    def set_a(self, data: int):
        self.a = data
        print(f"And A new state: {self.a}")

    def set_b(self, data: int):
        self.b = data
        print(f"And B new state: {self.b}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"a_attached_id": self.a_attached_id, "b_attached_id": self.b_attached_id, "a": self.a, "b": self.b})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.a_attached_id = data["a_attached_id"]
        device.b_attached_id = data["b_attached_id"]
        device.a = data["a"]
        device.b = data["b"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "box"
        return f'{self.id} [label="{self.device_type} ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"And(id={self.id}, a_attached_id={self.a_attached_id}, b_attached_id={self.b_attached_id}, a={self.a}, b={self.b})"


class Nand(Device):
    'Nand logic gate'

    def __init__(self):
        super().__init__("Nand")
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.a = 0
        self.b = 0

    def output(self) -> int:
        result = 0 if (self.a == 1 and self.b == 1) else 1
        print(f"Nand: {result}")
        return result

    def set_a(self, data: int):
        self.a = data
        print(f"Nand A new state: {self.a}")

    def set_b(self, data: int):
        self.b = data
        print(f"Nand B new state: {self.b}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"a_attached_id": self.a_attached_id, "b_attached_id": self.b_attached_id, "a": self.a, "b": self.b})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.a_attached_id = data["a_attached_id"]
        device.b_attached_id = data["b_attached_id"]
        device.a = data["a"]
        device.b = data["b"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "box"
        return f'{self.id} [label="{self.device_type} ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Nand(id={self.id}, a_attached_id={self.a_attached_id}, b_attached_id={self.b_attached_id}, a={self.a}, b={self.b})"


class Or(Device):
    'Or logic gate'

    def __init__(self):
        super().__init__("Or")
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.a = 0
        self.b = 0

    def output(self) -> int:
        result = 1 if (self.a == 1 or self.b == 1) else 0
        print(f"Or: {result}")
        return result

    def set_a(self, data: int):
        self.a = data
        print(f"Or A new state: {self.a}")

    def set_b(self, data: int):
        self.b = data
        print(f"Or B new state: {self.b}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"a_attached_id": self.a_attached_id, "b_attached_id": self.b_attached_id, "a": self.a, "b": self.b})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.a_attached_id = data["a_attached_id"]
        device.b_attached_id = data["b_attached_id"]
        device.a = data["a"]
        device.b = data["b"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "ellipse"
        return f'{self.id} [label="{self.device_type} ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Or(id={self.id}, a_attached_id={self.a_attached_id}, b_attached_id={self.b_attached_id}, a={self.a}, b={self.b})"


class Xor(Device):
    'Xor logic gate'

    def __init__(self):
        super().__init__("Xor")
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.a = 0
        self.b = 0

    def output(self) -> int:
        result = 1 if (self.a != self.b) else 0
        print(f"Xor: {result}")
        return result

    def set_a(self, data: int):
        self.a = data
        print(f"Xor A new state: {self.a}")

    def set_b(self, data: int):
        self.b = data
        print(f"Xor B new state: {self.b}")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"a_attached_id": self.a_attached_id, "b_attached_id": self.b_attached_id, "a": self.a, "b": self.b})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.a_attached_id = data["a_attached_id"]
        device.b_attached_id = data["b_attached_id"]
        device.a = data["a"]
        device.b = data["b"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "ellipse"
        return f'{self.id} [label="{self.device_type} ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Xor(id={self.id}, a_attached_id={self.a_attached_id}, b_attached_id={self.b_attached_id}, a={self.a}, b={self.b})"


class Output(Device):
    'Logic output'

    def __init__(self, name: str):
        super().__init__("Output")
        self.attached_id = -1
        self.name = name
        self.state = 0

    def set_state(self, state: int):
        self.state = state

    def rename(self, new_name: str):
        self.name = new_name

    def output(self) -> int:
        print(f"Output [{self.name}]: {self.state}")
        return self.state

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"attached_id": self.attached_id, "name": self.name, "state": self.state})
        return data

    @classmethod
    def from_dict(cls, data: dict):
        device = super().from_dict(data)
        device.attached_id = data["attached_id"]
        device.name = data["name"]
        device.state = data["state"]
        return device

    def to_graphviz(self) -> str:
        color = "green" if (self.output() == 1) else "red"
        shape = "ellipse"
        return f'{self.id} [label="{self.device_type} [{self.name}] ({self.output()})", color="{color}", shape="{shape}"]'

    def __str__(self):
        return f"Output(id={self.id}, attached_id={self.attached_id}, name={self.name}, state={self.state})"
