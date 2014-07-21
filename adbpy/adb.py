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

    def command_bool(self, data):
        self.socket.send(data)
        return self.socket.receive_fixed_length(4) == "OKAY"

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

    def get_product(self, target=Target.ANY):
        cmd = host_command(target, "get-product")
        with self.socket.Connect():
            return self.command(cmd)

    def get_serialno(self, target=Target.ANY):
        cmd = host_command(target, "get-serialno")
        with self.socket.Connect():
            return self.command(cmd)

    def get_devpath(self, target=Target.ANY):
        cmd = host_command(target, "get-devpath")
        with self.socket.Connect():
            return self.command(cmd)

    def get_state(self, target=Target.ANY):
        cmd = host_command(target, "get-state")
        with self.socket.Connect():
            return self.command(cmd)

    def forward(self, local, remote, target=Target.ANY, norebind=False):
        cmd_start = "forward:"
        if norebind:
            cmd_start += "norebind:"

        base_command = cmd_start + local + ";" + remote
        cmd = host_command(target, base_command)

        with self.socket.Connect():
            return self.command_bool(cmd)

    def kill_forward(self, local, target=Target.ANY):
        cmd = host_command(target, "killforward:" + local) 
        with self.socket.Connect():
            return self.command_bool(cmd)

    def kill_forward_all(self, target=Target.ANY):
        cmd = host_command(target, "killforward-all") 
        with self.socket.Connect():
            return self.command_bool(cmd)

    def shell(self, shell_cmd, target=Target.ANY):
        with self.socket.Connect():
            self.setup_target(target)
            self.socket.send("shell:" + shell_cmd)
            return self.socket.receive_until_end()
