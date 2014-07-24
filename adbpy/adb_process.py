import subprocess
import socket

class AdbProcess(object):

    def __init__(self, path, address):
        self.started = False
        self.path = path
        self.address = address

    def start(self):
        cmd = "{0} -P {1} start-server".format(self.path, self.address[1])
        return subprocess.call(cmd, shell=True) == 0

    def started(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(address)
        except socket.error:
            return False

        return True
