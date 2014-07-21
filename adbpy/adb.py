from adbpy.socket import Socket
from adbpy import Target
from adbpy.host_command import host_command

class Adb(object):

    def __init__(self, address):
        self.address = address 
        self.socket = Socket(address)

    def command(self, data):
        self.socket.connect()
        self.socket.send(data)
        return self.socket.receive()

    def version(self):
        return self.command("host:version")

    def get_serialno(self, target=Target.ANY):
        cmd = host_command(target, "get-serialno")
        return self.command(cmd)

    def shell(self, shell_cmd, target=Target.ANY):
        cmd = host_command(target, "shell " + shell_cmd)
        return command(cmd)

