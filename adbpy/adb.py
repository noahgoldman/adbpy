from adbpy.socket import Socket
from adbpy import Target, AdbError
from adbpy.host_command import host_command
from adbpy.devices import parse_device_list

class Adb(object):

    def __init__(self, address=None):
        """
        Initialize an Adb object

        :param tuple address: The address of the Adb server in the form (host, port).
                              Defaults to ("localhost", 5037)
        """
        if address == None:
            # Default address
            address = ("localhost", 5037)

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

    def start(self):
        pass

    def devices(self):
        devices = None
        with self.socket.Connect():
            devices = self.command("host:devices")

        return parse_device_list(devices)

    def version(self):
        with self.socket.Connect():
            return self.command("host:version")

    def kill(self):
        with self.socket.Connect():
            try:
                return self.command_bool("host:kill")
            except RuntimeError:
                pass

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
