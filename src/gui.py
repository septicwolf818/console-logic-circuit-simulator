import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import time
from typing import Union
from device import Device, Lever, Not, And, Nand, Or, Xor, Output
from device_manager import DeviceManager

class DeviceManagerGUI:
    def __init__(self, manager: DeviceManager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Device Manager GUI")
        self.root.geometry("1200x800")
        self.selected_device_id = None
        self.resize_id = None
        self.create_widgets()
        self.update_graph()

    def create_widgets(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.device_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Device", menu=self.device_menu)
        self.device_menu.add_command(label="Add", command=self.add_device)
        self.device_menu.add_command(label="Delete", command=self.delete_device)

        self.circuit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Circuit", menu=self.circuit_menu)
        self.circuit_menu.add_command(label="Save State", command=self.manager.save_state)
        self.circuit_menu.add_command(label="Load State", command=self.manager.load_state)
        self.circuit_menu.add_command(label="Render Graph", command=self.render_graph)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.exit_gui)

        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.tree_frame = ttk.Frame(self.main_frame, padding="5")
        self.tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1, minsize=200)

        self.graph_frame = ttk.Frame(self.main_frame, padding="5")
        self.graph_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.settings_frame = ttk.Frame(self.main_frame, padding="5")
        self.settings_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1, minsize=200)

        self.device_tree = ttk.Treeview(self.tree_frame, columns=("Type", "State", "Name"), show="headings")
        self.device_tree.heading("Type", text="Type")
        self.device_tree.heading("State", text="State")
        self.device_tree.heading("Name", text="Name")
        self.device_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.device_tree.bind("<Button-1>", self.on_tree_click)
        self.device_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.graph_label = ttk.Label(self.graph_frame)
        self.graph_label.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.root.bind("<Configure>", self.on_resize)

    def set_status(self, message: str):
        self.status_bar.config(text=message)

    def on_resize(self, event):
        if self.resize_id:
            self.root.after_cancel(self.resize_id)
        self.resize_id = self.root.after(500, self.update_graph)

    def add_device(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Device")

        ttk.Label(self.add_window, text="Select Device Type:").grid(row=0, column=0, padx=5, pady=5)
        self.device_type = tk.StringVar()
        self.device_type.set("Lever")
        device_types = ["Lever", "Not", "And", "Nand", "Or", "Xor", "Output"]
        self.device_menu = ttk.OptionMenu(self.add_window, self.device_type, *device_types)
        self.device_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.add_window, text="Add", command=self.confirm_add_device).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def confirm_add_device(self):
        device_type = self.device_type.get()
        if (device_type == "Lever"):
            if device_name:
                device_name = tk.simpledialog.askstring("Lever Device", "Enter device name:")
                self.manager.add_device(Lever(device_name))
        elif (device_type == "Not"):
            self.manager.add_device(Not())
        elif (device_type == "And"):
            self.manager.add_device(And())
        elif (device_type == "Nand"):
            self.manager.add_device(Nand())
        elif (device_type == "Or"):
            self.manager.add_device(Or())
        elif (device_type == "Xor"):
            self.manager.add_device(Xor())
        elif (device_type == "Output"):
            device_name = tk.simpledialog.askstring("Output Device", "Enter device name:")
            if device_name:
                self.manager.add_device(Output(device_name))
        self.add_window.destroy()
        self.update_tree()
        self.update_graph()
        self.set_status(f"Added {device_type}")

    def delete_device(self):
        selected_item = self.device_tree.selection()[0]
        device_id = int(self.device_tree.item(selected_item, "text").split('|')[0])
        self.manager.delete_device(device_id)
        self.set_status(f"Deleted device {device_id}")

    def on_tree_select(self, event):
        selected_item = self.device_tree.selection()
        if selected_item:
            device_id = int(self.device_tree.item(selected_item[0], "text").split('|')[0])
            self.selected_device_id = device_id
            for device in self.manager.devices:
                if (device.id == device_id):
                    self.show_device_settings(device)
                    break
        else:
            self.selected_device_id = None
            self.clear_settings_frame()
        self.update_graph()

    def on_tree_click(self, event):
        if not self.device_tree.identify_row(event.y):
            self.device_tree.selection_remove(self.device_tree.selection())

    def show_device_settings(self, device: Device):
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        device_type = device.get_device_type()
        if (device_type == "Lever"):
            self.manage_lever(device)
        elif (device_type == "Not"):
            self.manage_not(device)
        elif (device_type in {"And", "Nand", "Or", "Xor"}):
            self.manage_logic_gate(device)
        elif (device_type == "Output"):
            self.manage_output(device)

    def manage_lever(self, device: Lever):
        ttk.Label(self.settings_frame, text="Set State:").grid(row=0, column=0, padx=5, pady=5)
        self.state = tk.IntVar()
        self.state.set(device.state)
        ttk.Radiobutton(self.settings_frame, text="1", variable=self.state, value=1).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.settings_frame, text="0", variable=self.state, value=0).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.settings_frame, text="Set", command=lambda: self.set_lever_state(device)).grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        ttk.Label(self.settings_frame, text="Rename:").grid(row=2, column=0, padx=5, pady=5)
        self.new_name = tk.StringVar()
        self.new_name.set(device.name)
        ttk.Entry(self.settings_frame, textvariable=self.new_name).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.settings_frame, text="Update", command=lambda: self.update_lever_name(device)).grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    def set_lever_state(self, device: Lever):
        device.set_state(self.state.get())
        self.update_tree()
        self.update_graph()
        self.set_status(f"Lever state set to {self.state.get()}")

    def update_lever_name(self, device: Lever):
        device.rename(self.new_name.get())
        self.update_tree()
        self.update_graph()
        self.set_status(f"Lever renamed to {self.new_name.get()}")

    def manage_not(self, device: Not):
        ttk.Label(self.settings_frame, text="Attach Device:").grid(row=0, column=0, padx=5, pady=5)
        self.attached_device_selection = tk.StringVar()
        device_options = [
            f"{d.id}|{d.get_device_type()}{'|' + d.name if isinstance(d, Output) else ''}"
            for d in self.manager.devices if (d.id != device.id)
        ]
        self.attached_device_menu = ttk.OptionMenu(self.settings_frame, self.attached_device_selection, *device_options)
        self.attached_device_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.settings_frame, text="Attach", command=lambda: self.attach_device(device)).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def attach_device(self, device: Not):
        selected_option = self.attached_device_selection.get()
        if selected_option:
            device.attached_id = int(selected_option.split('|')[0])
        self.update_tree()
        self.update_graph()
        self.set_status(f"Attached device {device.attached_id} to Not gate")

    def manage_logic_gate(self, device: Union[And, Nand, Or, Xor]):
        ttk.Label(self.settings_frame, text="Attach Device to A:").grid(row=0, column=0, padx=5, pady=5)
        self.a_attached_device_selection = tk.StringVar()
        device_options = [
            f"{d.id}|{d.get_device_type()}{'|' + d.name if isinstance(d, Output) else ''}"
            for d in self.manager.devices if (d.id != device.id)
        ]
        self.a_attached_device_menu = ttk.OptionMenu(self.settings_frame, self.a_attached_device_selection, *device_options)
        self.a_attached_device_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.settings_frame, text="Attach Device to B:").grid(row=1, column=0, padx=5, pady=5)
        self.b_attached_device_selection = tk.StringVar()
        self.b_attached_device_menu = ttk.OptionMenu(self.settings_frame, self.b_attached_device_selection, *device_options)
        self.b_attached_device_menu.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.settings_frame, text="Attach", command=lambda: self.attach_logic_gate(device)).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def attach_logic_gate(self, device: Union[And, Nand, Or, Xor]):
        selected_option_a = self.a_attached_device_selection.get()
        selected_option_b = self.b_attached_device_selection.get()
        if selected_option_a:
            device.a_attached_id = int(selected_option_a.split('|')[0])
        if selected_option_b:
            device.b_attached_id = int(selected_option_b.split('|')[0])
        self.update_tree()
        self.update_graph()
        self.set_status(f"Attached devices {device.a_attached_id} and {device.b_attached_id} to {device.device_type} gate")

    def manage_output(self, device: Output):
        ttk.Label(self.settings_frame, text="Attach Device:").grid(row=0, column=0, padx=5, pady=5)
        self.attached_device_selection = tk.StringVar()
        device_options = [
            f"{d.id}|{d.get_device_type()}{'|' + d.name if isinstance(d, Output) else ''}"
            for d in self.manager.devices if (d.id != device.id)
        ]
        self.attached_device_menu = ttk.OptionMenu(self.settings_frame, self.attached_device_selection, *device_options)
        self.attached_device_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.settings_frame, text="Rename:").grid(row=1, column=0, padx=5, pady=5)
        self.new_name = tk.StringVar()
        self.new_name.set(device.name)
        ttk.Entry(self.settings_frame, textvariable=self.new_name).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.settings_frame, text="Update", command=lambda: self.update_output(device)).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def update_output(self, device: Output):
        selected_option = self.attached_device_selection.get()
        if selected_option:
            device.attached_id = int(selected_option.split('|')[0])
        device.rename(self.new_name.get())
        self.update_tree()
        self.update_graph()
        self.set_status(f"Updated Output device {device.id}")

    def update_tree(self):
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
        for device in self.manager.devices:
            state = device.output()
            name = device.name if hasattr(device, 'name') else ''
            self.device_tree.insert("", "end", text=f"{device.id}|{device.get_device_type()}|{state}|{name}", values=(device.get_device_type(), state, name))

    def render_graph(self):
        filename = tk.simpledialog.askstring("Render Graph", "Enter filename to render graph:")
        if filename:
            self.manager.render_graph(filename)
            self.update_graph()
            self.set_status(f"Graph rendered to {filename}.png")

    def update_graph(self):
        image = self.manager.render_graph()
        height = self.graph_frame.winfo_height() - 20
        if height > 0:
            image = image.resize((height, height), Image.LANCZOS)
            self.img = ImageTk.PhotoImage(image)
            self.graph_label.config(image=self.img)
            self.graph_label.image = self.img

    def clear_settings_frame(self):
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

    def exit_gui(self):
        self.root.quit()

    def run(self):
        self.update_tree()
        self.root.mainloop()
