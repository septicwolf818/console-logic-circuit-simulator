class Lever:
    'Lever/logic input'

    def __init__(self):
        self.state = 0
        self.device_type = "Lever"
        self.id = 0

    def output(self):
        print("Lever: " + str(self.state))
        return self.state

    def set_state(self, data):
        self.state = data
        print("New lever state: " + str(self.state))

    def get_device_type(self):
        return self.device_type

    def set_id(self, id):
        self.id = id


class Not:
    'Logic not/inversion'

    def __init__(self):
        self.attached_id = -1
        self.device_type = "Not"
        self.state = 0
        self.id = 0

    def get_device_type(self):
        return self.device_type

    def set_state(self, data):
        self.state = data

    def output(self):
        if(self.state == 1):
            print("Not: " + str(0))
            return 0
        elif(self.state == 0):
            print("Not: " + str(1))
            return 1

    def set_id(self, id):
        self.id = id


class And:
    'And logic gate'

    def __init__(self):
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.a = 0
        self.b = 0
        self.device_type = "And"
        self.id = 0

    def output(self):
        if(self.a == 1 and self.b == 1):
            print("And: " + str(1))
            return 1
        else:
            print("And: " + str(0))
            return 0

    def set_a(self, data):
        self.a = data
        print("And A new state: " + str(self.a))

    def set_b(self, data):
        self.b = data
        print("And B new state: " + str(self.b))

    def get_device_type(self):
        return self.device_type

    def set_id(self, id):
        self.id = id


class Or:
    'Or logic gate'

    def __init__(self):
        self.a = 0
        self.b = 0
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.device_type = "Or"
        self.id = 0

    def output(self):
        if(self.a == 1 or self.b == 1):
            print("Or: " + str(1))
            return 1
        else:
            print("Or: " + str(0))
            return 0

    def set_a(self, data):
        self.a = data
        print("Or A new state: " + str(self.a))

    def set_b(self, data):
        self.b = data
        print("Or B new state: " + str(self.b))

    def get_device_type(self):
        return self.device_type

    def set_id(self, id):
        self.id = id


class Output:
    'Logic output'

    def __init__(self, name):
        self.attached_id = -1
        self.name = name
        self.device_type = "Output"
        self.id = 0
        self.state = 0

    def set_state(self, state):
        self.state = state

    def rename(self, new_name):
        self.name = new_name

    def output(self):
        print("Output [" + self.name + "]: " + str(self.state))
        return self.state

    def get_device_type(self):
        return self.device_type

    def set_id(self, id):
        self.id = id


class DeviceManager:
    'Device/circuit manager'

    def __init__(self):
        print("Device manager created")
        self.devices = []
        self.id = 0

    def get_output(self, id):
        device_type = ""
        for device in self.devices:
            if(device.id == id):
                device_type = device.get_device_type()
                if(device_type == "Lever"):
                    return device.output()
                elif(device_type == "Not"):
                    device.set_state(self.get_output(device.attached_id))
                    return device.output()
                elif(device_type == "And"):
                    device.set_a(self.get_output(device.a_attached_id))
                    device.set_b(self.get_output(device.b_attached_id))
                    return device.output()
                elif(device_type == "Or"):
                    device.set_a(self.get_output(device.a_attached_id))
                    device.set_b(self.get_output(device.b_attached_id))
                    return device.output()
        return 0

    def add_device(self, device):
        device.set_id(self.id)
        self.devices.append(device)
        self.id += 1

    def start(self):
        print("Device manager started")
        while(True):
            print("", "1. Add device", "2. Manage device", "3. Show devices",
                  "4. Run circuit", "5. Quit", "OPTION: ", sep="\n", end="")
            user_input = input()
            if(user_input == '1'):
                print("", "ADD DEVICE:", "1. Input", "2. Not gate", "3. And gate",
                      "4. Or gate", "5. Output", "6. Cancel", "OPTION: ", sep="\n", end="")
                user_input = input()
                if(user_input == "1"):
                    self.add_device(Lever())
                elif(user_input == "2"):
                    self.add_device(Not())
                elif(user_input == "3"):
                    self.add_device(And())
                elif(user_input == "4"):
                    self.add_device(Or())
                elif(user_input == "5"):
                    device_name = input("Device name: ")
                    self.add_device(Output(device_name))
                elif(user_input == "6"):
                    print("Canceled")
                else:
                    print("Invalid option")
                print()
            elif(user_input == '2'):
                print()
                if(len(self.devices) == 0):
                    print("No devices found")
                else:
                    print("MANAGE DEVICE: ",
                          "DEVICE ID: ", sep="\n", end="")
                    user_input = input()
                    try:
                        device_id = int(user_input)
                        for index, device in enumerate(self.devices):
                            if(device.id == device_id):
                                device_type = device.get_device_type()
                                if(device_type == "Lever"):
                                    print("1. Set state to 1", "2. Set state to 0",
                                          "3. Cancel", "OPTION: ", sep="\n", end="")
                                    user_input = input()
                                    if(user_input == "1"):
                                        device.set_state(1)
                                    elif(user_input == "2"):
                                        device.set_state(0)
                                    elif(user_input == "3"):
                                        print("Canceled")
                                    else:
                                        print("Invalid input")
                                elif(device_type == "Not"):
                                    print("1. Attach device", "2. Cancel",
                                          "OPTION: ", sep="\n", end="")
                                    user_input = input()
                                    if(user_input == "1"):
                                        print("ID: ", end="")
                                        user_input = input()
                                        device.attached_id = int(
                                            user_input)
                                    elif(user_input == "2"):
                                        print("Canceled")
                                elif(device_type == "And"):
                                    print("1. Attach device to A", "2. Attach device to B",
                                          "3. Cancel", "OPTION: ", sep="\n", end="")
                                    user_input = input()
                                    if(user_input == "1"):
                                        print("ID: ", end="")
                                        user_input = input()
                                        device.a_attached_id = int(
                                            user_input)
                                    if(user_input == "2"):
                                        print("ID: ", end="")
                                        user_input = input()
                                        device.b_attached_id = int(
                                            user_input)
                                    elif(user_input == "3"):
                                        print("Canceled")
                                elif(device_type == "Or"):
                                    print("1. Attach device to A", "2. Attach device to B",
                                          "3. Cancel", "OPTION: ", sep="\n", end="")
                                    user_input = input()
                                    if(user_input == "1"):
                                        print("ID: ", end="")
                                        user_input = input()
                                        device.a_attached_id = int(
                                            user_input)
                                    elif(user_input == "2"):
                                        print("ID: ", end="")
                                        user_input = input()
                                        device.b_attached_id = int(
                                            user_input)
                                    elif(user_input == "3"):
                                        print("Canceled")
                                elif(device_type == "Output"):
                                    print("1. Attach device", "2. Rename",
                                          "3. Cancel", "OPTION: ", sep="\n", end="")
                                    user_input = input()
                                    if(user_input == "1"):
                                        print("ID: ", end="")
                                        user_input = input()
                                        device.attached_id = int(
                                            user_input)
                                    elif(user_input == "2"):
                                        print("New name: ", end="")
                                        user_input = input()
                                        device.rename(user_input)
                                    elif(user_input == "3"):
                                        print("Canceled")
                                break
                            if(index == len(self.devices)-1):
                                print("Device not found")
                    except:
                        print("Invalid input")
            elif(user_input == '3'):
                print()
                print("DEVICES:")
                if(len(self.devices) == 0):
                    print("No devices found")
                else:
                    for device in self.devices:
                        if(device.get_device_type() == "Output"):
                            print(str(device.id) + ": " +
                                  device.get_device_type() + " ["+device.name+"]")
                        else:
                            print(str(device.id) + ": " +
                                  device.get_device_type())
                print()
            elif(user_input == '4'):
                for device in self.devices:
                    if(device.get_device_type() == "Output"):
                        device.set_state(
                            self.get_output(device.attached_id))
                        device.output()
            elif(user_input == '5'):
                print("Shutting down")
                exit()
            else:
                print("Invalid option")


DM = DeviceManager()
DM.start()
