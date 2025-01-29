import json
import graphviz
from typing import List, Union
from device import Device, Lever, Not, And, Nand, Or, Xor, Output
from tkinter import filedialog
import io
from PIL import Image

class DeviceManager:
    'Device/circuit manager'

    def __init__(self):
        print("Device manager created")
        self.devices: List[Device] = []
        self.id = 0
        self.device_name = ""

    def get_output(self, id: int) -> int:
        for device in self.devices:
            if (device.id == id):
                if isinstance(device, Lever):
                    return device.output()
                elif isinstance(device, Not):
                    device.set_state(self.get_output(device.attached_id))
                    return device.output()
                elif isinstance(device, (And, Nand, Or, Xor)):
                    device.set_a(self.get_output(device.a_attached_id))
                    device.set_b(self.get_output(device.b_attached_id))
                    return device.output()
                elif isinstance(device, Output):
                    device.set_state(self.get_output(device.attached_id))
                    return device.output()
        return 0

    def update_all_outputs(self):
        for device in self.devices:
            if isinstance(device, Output):
                device.set_state(self.get_output(device.attached_id))

    def add_device(self, device: Device):
        device.set_id(self.id)
        self.devices.append(device)
        self.id += 1
        # Set manager reference for devices that need it
        if isinstance(device, Lever):
            device.manager = self
        self.gui.update_tree()

    def save_state(self):
        filename = filedialog.asksaveasfilename(defaultextension=".clcs", filetypes=[("CLCS files", "*.clcs"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as file:
                json.dump([device.to_dict() for device in self.devices], file)
            print(f"State saved to {filename}")
            self.gui.update_tree()

    def load_state(self):
        filename = filedialog.askopenfilename(defaultextension=".clcs", filetypes=[("CLCS files", "*.clcs"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    devices_data = json.load(file)
                    print(f"Loaded data from {filename}: {devices_data}")
                    
                    # Create devices from the loaded data
                    self.devices = [Device.from_dict(data) for data in devices_data]
                    self.id = max(device.id for device in self.devices) + 1
                    print(f"Devices created: {self.devices}")
                    
                    # Create a dictionary for quick lookup
                    device_dict = {device.id: device for device in self.devices}
                    print(f"Device dictionary: {device_dict}")
                    
                    # Update connections and states
                    for device in self.devices:
                        print(f"Updating device {device.id}: {device}")
                        if isinstance(device, Lever):
                            device.manager = self
                            device.state = devices_data[device.id]["state"]
                            device.name = devices_data[device.id]["name"]
                            print(f"Set manager for Lever {device.id}")
                        elif isinstance(device, Not):
                            device.attached_id = devices_data[device.id]["attached_id"]
                            print(f"Updated attached_id for Not {device.id} to {device.attached_id}")
                        elif isinstance(device, (And, Nand, Or, Xor)):
                            device.a_attached_id = devices_data[device.id]["a_attached_id"]
                            device.b_attached_id = devices_data[device.id]["b_attached_id"]
                            print(f"Updated a_attached_id for {device.device_type} {device.id} to {device.a_attached_id}")
                            print(f"Updated b_attached_id for {device.device_type} {device.id} to {device.b_attached_id}")
                        elif isinstance(device, Output):
                            device.attached_id = devices_data[device.id]["attached_id"]
                            print(f"Updated attached_id for Output {device.id} to {device.attached_id}")
                        print(f"Device {device.id} updated: {device}")
                    
                    self.update_all_outputs()
                    print("All outputs updated")
                    
                    for device in self.devices:
                        print(f"Final state of device {device.id}: {device}")
                    
                    print(f"State loaded from {filename}")
                    self.gui.update_tree()
                    self.gui.update_graph()

            except FileNotFoundError:
                print(f"File {filename} not found")

    def render_graph(self):
        self.update_all_outputs()
        dot = graphviz.Digraph()
        for device in self.devices:
            label = f'{device.id}: {device.device_type} ({device.name}) ({device.output()})' if isinstance(device, Output) else f'{device.id}: {device.device_type} ({device.output()})'
            color = "blue" if device.id == self.gui.selected_device_id else ("green" if (device.output() == 1) else "red")
            dot.node(str(device.id), label=label, color=color, shape="ellipse")
            if isinstance(device, Not):
                dot.edge(str(device.attached_id), str(device.id))
            elif isinstance(device, (And, Nand, Or, Xor)):
                dot.edge(str(device.a_attached_id), str(device.id))
                dot.edge(str(device.b_attached_id), str(device.id))
            elif isinstance(device, Output):
                dot.edge(str(device.attached_id), str(device.id))
        
        # Render the graph to a PNG image in memory
        png_data = dot.pipe(format='png')
        image = Image.open(io.BytesIO(png_data))
        return image

    def start(self):
        print("Device manager started")
        while True:
            print("\n1. Add device\n2. Manage device\n3. Show devices\n4. Run circuit\n5. Save state\n6. Load state\n7. Render graph\n8. Start GUI\n9. Quit\nOPTION: ", end="")
            user_input = input().strip()
            if (user_input == '1'):
                self.add_device_menu()
            elif (user_input == '2'):
                self.manage_device_menu()
            elif (user_input == '3'):
                self.show_devices()
            elif (user_input == '4'):
                self.run_circuit()
            elif (user_input == '5'):
                self.save_state()
            elif (user_input == '6'):
                self.load_state()
            elif (user_input == '7'):
                filename = input("Enter filename to render graph: ").strip()
                self.render_graph(filename)
            elif (user_input == '8'):
                self.start_gui()
            elif (user_input == '9'):
                print("Shutting down")
                break
            else:
                print("Invalid option")

    def start_gui(self):
        from gui import DeviceManagerGUI
        self.gui = DeviceManagerGUI(self)
        self.gui.run()

    def add_device_menu(self):
        print("\nADD DEVICE:\n1. Input\n2. Not gate\n3. And gate\n4. Nand gate\n5. Or gate\n6. Xor gate\n7. Output\n8. Cancel\nOPTION: ", end="")
        user_input = input().strip()
        if (user_input == "1"):
            device_name = input("Device name: ").strip()
            self.add_device(Lever(device_name))
        elif (user_input == "2"):
            self.add_device(Not())
        elif (user_input == "3"):
            self.add_device(And())
        elif (user_input == "4"):
            self.add_device(Nand())
        elif (user_input == "5"):
            self.add_device(Or())
        elif (user_input == "6"):
            self.add_device(Xor())
        elif (user_input == "7"):
            device_name = input("Device name: ").strip()
            self.add_device(Output(device_name))
        elif (user_input == "8"):
            print("Canceled")
        else:
            print("Invalid option")

    def manage_device_menu(self):
        print()
        if not self.devices:
            print("No devices found")
            return
        print("MANAGE DEVICE:\nDEVICE ID: ", end="")
        try:
            device_id = int(input().strip())
            for device in self.devices:
                if (device.id == device_id):
                    self.manage_device(device)
                    break
            else:
                print("Device not found")
        except ValueError:
            print("Invalid input")

    def manage_device(self, device: Device):
        device_type = device.get_device_type()
        if (device_type == "Lever"):
            self.manage_lever(device)
        elif (device_type == "Not"):
            self.manage_not(device)
        elif (device_type in {"And", "Nand", "Or", "Xor"}):
            self.manage_logic_gate(device)
        elif (device_type == "Output"):
            self.manage_output(device)
        self.gui.update_tree()

    def manage_lever(self, device: Lever):
        print("1. Set state to 1\n2. Set state to 0\n3. Rename\n4. Cancel\nOPTION: ", end="")
        user_input = input().strip()
        if (user_input == "1"):
            device.set_state(1)
        elif (user_input == "2"):
            device.set_state(0)
        elif (user_input == "3"):
            print("New name: ", end="")
            device.rename(input().strip())
        elif (user_input == "4"):
            print("Canceled")
        else:
            print("Invalid input")
        self.gui.update_tree()

    def manage_not(self, device: Not):
        print("1. Attach device\n2. Cancel\nOPTION: ", end="")
        user_input = input().strip()
        if (user_input == "1"):
            print("ID: ", end="")
            device.attached_id = int(input().strip())
        elif (user_input == "2"):
            print("Canceled")
        self.gui.update_tree()

    def manage_logic_gate(self, device: Union[And, Nand, Or, Xor]):
        print("1. Attach device to A\n2. Attach device to B\n3. Cancel\nOPTION: ", end="")
        user_input = input().strip()
        if (user_input == "1"):
            print("ID: ", end="")
            device.set_a(int(input().strip()))
        elif (user_input == "2"):
            print("ID: ", end="")
            device.set_b(int(input().strip()))
        elif (user_input == "3"):
            print("Canceled")
        self.gui.update_tree()

    def manage_output(self, device: Output):
        print("1. Attach device\n2. Rename\n3. Cancel\nOPTION: ", end="")
        user_input = input().strip()
        if (user_input == "1"):
            print("ID: ", end="")
            device.attached_id = int(input().strip())
        elif (user_input == "2"):
            print("New name: ", end="")
            device.rename(input().strip())
        elif (user_input == "3"):
            print("Canceled")
        self.gui.update_tree()

    def show_devices(self):
        print("\nDEVICES:")
        if not self.devices:
            print("No devices found")
        else:
            for device in self.devices:
                if (device.get_device_type() == "Output"):
                    print(f"{device.id}: {device.get_device_type()} [{device.name}]")
                else:
                    print(f"{device.id}: {device.get_device_type()}")
        print()

    def run_circuit(self):
        self.update_all_outputs()
        for device in self.devices:
            if (device.get_device_type() == "Output"):
                device.output()

    def delete_device(self, device_id: int):
        self.devices = [device for device in self.devices if device.id != device_id]
        self.gui.update_tree()
        self.gui.clear_settings_frame()
        self.gui.update_graph()
