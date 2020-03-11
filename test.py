import pygatt
import binascii

class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount



class myBle:
    ADDRESS_TYPE = pygatt.BLEAddressType.random
    read_characteristic = "0000xxxx-0000-1000-8000-00805f9b34fb"
    write_characteristic = "0000xxxx-0000-1000-8000-00805f9b34fb"
    notify_characteristic = "0000xxxxx-0000-1000-8000-00805f9b34fb"
    def __init__(self,device):
        self.device = device
        self.valueChanged = Event()
        self.checkdata = False

    def alert(self):
         self.valueChanged(self.checkdata)

    def write(self,data):
        self.device.write_char(self.write_characteristic,binascii.unhexlify(data))

    def notify(self,handle,data):
        self.checkdata = True

    def read(self):
        if(self.checkdata):
            self.read_data = self.device.char_read(uuid.UUID(self.read_characteristic))
            self.write(bytearray(b'\x10\x00'))
            self.checkdata = False
            return self.read_data
    def discover(self):
        return self.device.discover_characteristics().keys()

def triggerEvent(checkdata):
   print(str(checkdata))

ble = myBle(device)
ble.valueChanged += triggerEvent
ble.alert()