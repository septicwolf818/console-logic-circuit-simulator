class DeviceManager:
    'Device/circuit manager'

    def __init__(self):
        print("Device manager created")
        self.devices = []
        self.id = 0

    def getOutput(self, id):
        device_type = ""
        for device in self.devices:
            if(device.id == id):
                device_type = device.getDeviceType()
                if(device_type == "Lever"):
                    return device.output()
                elif(device_type == "Not"):
                    device.setState(self.getOutput(device.attached_id))
                    return device.output()
                elif(device_type == "And"):
                    device.setA(self.getOutput(device.a_attached_id))
                    device.setB(self.getOutput(device.b_attached_id))
                    return device.output()
                elif(device_type == "Or"):
                    device.setA(self.getOutput(device.a_attached_id))
                    device.setB(self.getOutput(device.b_attached_id))
                    return devive.output()
        return 0

    def start(self):
        print("Device manager started")
        while(True):
            print()
            print("1. Add device")
            print("2. Manage device")
            print("3. Show devices")
            print("4. Run circuit")
            print("5. Quit")
            print("OPTION: ", end="")
            userinput = input()
            if(userinput == '1'):
                print()
                print("ADD DEVICE:")
                print("1. Input")
                print("2. Not gate")
                print("3. And gate")
                print("4. Or gate")
                print("5. Output")
                print("6. Cancel")
                print("OPTION: ", end="")
                userinput = input()
                if(userinput == "1"):
                    self.addDevice(Lever())
                elif(userinput == "2"):
                    self.addDevice(Not())
                elif(userinput == "3"):
                    self.addDevice(And())
                elif(userinput == "4"):
                    self.addDevice(Or())
                elif(userinput == "5"):
                    devicename = input("Device name: ")
                    self.addDevice(Output(devicename))
                elif(userinput == "6"):
                    print("Canceled")
                else:
                    print("Invalid option")
                print()
            elif(userinput == '2'):
                print(
                    "Device management option is still under development - may not work properly")
                print()
                if(len(self.devices) == 0):
                    print("No devices found")
                else:
                    print("MANAGE DEVICE: ")
                    print("DEVICE ID: ", end="")
                    userinput = input()
                    try:
                        device_id = int(userinput)
                        for index, device in enumerate(self.devices):
                            if(device.id == device_id):
                                device_type = device.getDeviceType()
                                if(device_type == "Lever"):
                                    print("1. Set state to 1")
                                    print("2. Set state to 0")
                                    print("3. Cancel")
                                    print("OPTION: ", end="")
                                    userinput = input()
                                    if(userinput == "1"):
                                        device.setState(1)
                                    elif(userinput == "2"):
                                        device.setState(0)
                                    elif(userinput == "3"):
                                        print("Canceled")
                                    else:
                                        print("Invalid input")
                                elif(device_type == "Not"):
                                    print("1. Attach device")
                                    print("2. Cancel")
                                    print("OPTION: ", end="")
                                    userinput = input()
                                    if(userinput == "1"):
                                        print("ID: ", end="")
                                        userinput = input()
                                        device.attached_id = int(userinput)
                                    elif(userinput == "2"):
                                        print("Canceled")
                                elif(device_type == "And"):
                                    print("1. Attach device to A")
                                    print("2. Attach device to B")
                                    print("3. Cancel")
                                    print("OPTION: ", end="")
                                    userinput = input()
                                    if(userinput == "1"):
                                        print("ID: ", end="")
                                        userinput = input()
                                        device.a_attached_id = int(userinput)
                                    if(userinput == "2"):
                                        print("ID: ", end="")
                                        userinput = input()
                                        device.b_attached_id = int(userinput)
                                    elif(userinput == "3"):
                                        print("Canceled")
                                elif(device_type == "Or"):
                                    print("1. Attach device to A")
                                    print("2. Attach device to B")
                                    print("3. Cancel")
                                    print("OPTION: ", end="")
                                    userinput = input()
                                    if(userinput == "1"):
                                        print("ID: ", end="")
                                        userinput = input()
                                        device.a_attached_id = int(userinput)
                                    elif(userinput == "2"):
                                        print("ID: ", end="")
                                        userinput = input()
                                        device.b_attached_id = int(userinput)
                                    elif(userinput == "3"):
                                        print("Canceled")
                                elif(device_type == "Output"):
                                    print("1. Attach device")
                                    print("2. Rename")
                                    print("3. Cancel")
                                    print("OPTION: ", end="")
                                    userinput = input()
                                    if(userinput == "1"):
                                        print("ID: ", end="")
                                        userinput = input()
                                        device.attached_id = int(userinput)
                                    elif(userinput == "2"):
                                        print("New name: ", end="")
                                        userinput = input()
                                        device.rename(userinput)
                                    elif(userinput == "3"):
                                        print("Canceled")
                                break
                            if(index == len(self.devices)-1):
                                print("Device not found")
                    except:
                        print("Invalid input")
            elif(userinput == '3'):
                print()
                print("DEVICES:")
                if(len(self.devices) == 0):
                    print("No devices found")
                else:
                    for device in self.devices:
                        if(device.getDeviceType() == "Output"):
                            print(str(device.id) + ": " +
                                  device.getDeviceType() + " ["+device.name+"]")
                        else:
                            print(str(device.id) + ": " +
                                  device.getDeviceType())
                print()
            elif(userinput == '4'):
                for device in self.devices:
                    if(device.getDeviceType() == "Output"):
                        device.setState(self.getOutput(device.attached_id))
                        device.output()
            elif(userinput == '5'):
                print("Shutting down")
                exit()
            else:
                print("Invalid option")

    def addDevice(self, device):
        device.setId(self.id)
        self.devices.append(device)
        self.id += 1


class Lever:
    'Lever/logic input'

    def __init__(self):
        self.state = 0
        self.deviceType = "Lever"
        self.id = 0

    def output(self):
        print("Lever: " + str(self.state))
        return self.state

    def setState(self, data):
        self.state = data
        print("New lever state: " + str(self.state))

    def getDeviceType(self):
        return self.deviceType

    def setId(self, id):
        self.id = id


class Not:
    'Logic not/inversion'

    def __init__(self):
        self.attached_id = -1
        self.deviceType = "Not"
        self.state = 0
        self.id = 0

    def getDeviceType(self):
        return self.deviceType

    def setState(self, data):
        self.state = data

    def output(self):
        if(self.state == 1):
            print("Not: " + str(0))
            return 0
        elif(self.state == 0):
            print("Not: " + str(1))
            return 1

    def setId(self, id):
        self.id = id


class And:
    'And logic gate'

    def __init__(self):
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.a = 0
        self.b = 0
        self.deviceType = "And"
        self.id = 0

    def output(self):
        if(self.a == 1 and self.b == 1):
            print("And: " + str(1))
            return 1
        else:
            print("And: " + str(0))
            return 0

    def setA(self, data):
        self.a = data
        print("And A new state: " + str(self.a))

    def setB(self, data):
        self.b = data
        print("And B new state: " + str(self.b))

    def getDeviceType(self):
        return self.deviceType

    def setId(self, id):
        self.id = id


class Or:
    'Or logic gate'

    def __init__(self):
        self.a = 0
        self.b = 0
        self.a_attached_id = -1
        self.b_attached_id = -1
        self.deviceType = "Or"
        self.id = 0

    def output(self):
        if(self.a == 1 or self.b == 1):
            print("Or: " + str(1))
            return 1
        else:
            print("Or: " + str(0))
            return 0

    def setA(self, data):
        self.a = data
        print("Or A new state: " + str(self.a))

    def setB(self, data):
        self.b = data
        print("Or B new state: " + str(self.b))

    def getDeviceType(self):
        return self.deviceType

    def setId(self, id):
        self.id = id


class Output:
    'Logic output'

    def __init__(self, name):
        self.attached_id = -1
        self.name = name
        self.deviceType = "Output"
        self.id = 0
        self.state = 0

    def setState(self, state):
        self.state = state

    def rename(self, new_name):
        self.name = new_name

    def output(self):
        print("Output [" + self.name + "]: " + str(self.state))
        return self.state

    def getDeviceType(self):
        return self.deviceType

    def setId(self, id):
        self.id = id


dm = DeviceManager()
dm.start()
