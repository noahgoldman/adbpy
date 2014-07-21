from adbpy.socket import Socket
from adbpy import Target, AdbError
from adbpy.host_command import host_command

class Adb(object):

    def __init__(self, address):
        self.address = address 
        self.socket = Socket(address)

    def command(self, data):
        self.socket.send(data)
        return self.socket.receive()

    @staticmethod
    def get_transport(target):
        if target in Target.__dict__.values(): 
            return "host:transport-" + target
        else:
            # If the target was a serial
            return "host:transport:" + target

    def setup_target(self, target):
        self.socket.send(Adb.get_transport(target))
        if self.socket.receive_fixed_length(4) != "OKAY":
            raise AdbError("Failed to change transport")

    def version(self):
        with self.socket.Connect():
            return self.command("host:version")

    def get_serialno(self, target=Target.ANY):
        with self.socket.Connect():
            cmd = host_command(target, "get-serialno")
            return self.command(cmd)

    def shell(self, shell_cmd, target=Target.ANY):
        with self.socket.Connect():
            self.setup_target(target)
            self.socket.send("shell:" + shell_cmd)
            return self.socket.receive_until_end()
