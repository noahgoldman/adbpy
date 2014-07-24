from adbpy.socket import Socket
from adbpy import Target, AdbError
from adbpy.host_command import host_command
from adbpy.devices import parse_device_list
from adbpy.adb_process import AdbProcess

class Adb(object):

    def __init__(self, address=None, adb_path="adb"):
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
        self.process = AdbProcess(adb_path, address)

    def _command(self, data):
        self.socket.send(data)
        return self.socket.receive()

    def _command_bool(self, data):
        self.socket.send(data)
        return self.socket.receive_fixed_length(4) == "OKAY"

    @staticmethod
    def _get_transport(target):
        transport = ''
        if target in Target.__dict__.values():
            transport =  "-" + target
        else:
            # If the target was a serial
            transport = ":" + target
        return "host:transport" + transport

    def _setup_target(self, target):
        self.socket.send(Adb._get_transport(target))
        if self.socket.receive_fixed_length(4) != "OKAY":
            raise AdbError("Failed to change transport.  Verify that multiple devices "
                           "are not connected and that you chose the right target")

    def start(self):
        """
        Start the ADB server on the port specified in :py:attr:`Adb.address` during initialization.

        :raises: AdbError
        """
        self.process.start()
        if not self.process.started():
            raise AdbError("Failed to start Adb process")

    def devices(self):
        """
        Return a list of connected devices in the form (*serial*, *status*) where status can
        be any of the following:

        1. device
        2. offline
        3. unauthorized

        :returns: A list of tuples representing connected devices
        """
        devices = None
        with self.socket.Connect():
            devices = self._command("host:devices")

        return parse_device_list(devices)

    def version(self):
        with self.socket.Connect():
            return self._command("host:version")

    def kill(self):
        with self.socket.Connect():
            try:
                return self._command_bool("host:kill")
            except RuntimeError:
                pass

    def get_product(self, target=Target.ANY):
        cmd = host_command(target, "get-product")
        with self.socket.Connect():
            return self._command(cmd)

    def get_serialno(self, target=Target.ANY):
        cmd = host_command(target, "get-serialno")
        with self.socket.Connect():
            return self._command(cmd)

    def get_devpath(self, target=Target.ANY):
        cmd = host_command(target, "get-devpath")
        with self.socket.Connect():
            return self._command(cmd)

    def get_state(self, target=Target.ANY):
        cmd = host_command(target, "get-state")
        with self.socket.Connect():
            return self._command(cmd)

    def forward(self, local, remote, target=Target.ANY, norebind=False):
        cmd_start = "forward:"
        if norebind:
            cmd_start += "norebind:"

        base_command = cmd_start + local + ";" + remote
        cmd = host_command(target, base_command)

        with self.socket.Connect():
            return self._command_bool(cmd)

    def kill_forward(self, local, target=Target.ANY):
        cmd = host_command(target, "killforward:" + local)
        with self.socket.Connect():
            return self._command_bool(cmd)

    def kill_forward_all(self, target=Target.ANY):
        cmd = host_command(target, "killforward-all")
        with self.socket.Connect():
            return self._command_bool(cmd)

    def shell(self, shell_cmd, target=Target.ANY, timeout=None):
        with self.socket.Connect():
            self._setup_target(target)
            self.socket.send("shell:" + shell_cmd)
            return self.socket.receive_until_end(timeout)
