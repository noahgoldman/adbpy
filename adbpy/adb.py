from adbpy.socket import Socket
from adbpy import Target
from adbpy.host_command import host_command

class Adb(object):

    def __init__(self, address):
        self.address = address 
        self.socket = Socket(address)

    def version(self):
        self.socket.connect()
        self.socket.send("host:version")
        return self.socket.receive()

    def get_serialno(self, target=Target.ANY):
        self.socket.connect()
        cmd = host_command(target, "get-serialno")
        self.socket.send(cmd)
        return self.socket.receive()
