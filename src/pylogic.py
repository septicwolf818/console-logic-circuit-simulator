import sys
from device_manager import DeviceManager

if __name__ == "__main__":
    DM = DeviceManager()
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        DM.start_gui()
    else:
        DM.start()
