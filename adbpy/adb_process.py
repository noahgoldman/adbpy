from __future__ import absolute_import

import os
import subprocess
import socket

from adbpy.socket import Socket

DEFAULT_ADB_PORT = 5037

class AdbProcess(object):

    def __init__(self, path, address):
        self.path = path
        self.address = address

    def start(self):
        null = open(os.devnull, 'w')

        port_str = ""
        if self.address[1] != DEFAULT_ADB_PORT:
            port_str = "-P " + str(self.address[1])

        cmd = '"{0}" {1} start-server'.format(self.path, port_str)
        return subprocess.call(cmd, shell=True, stdout=null) == 0

    def running(self):
        sock = Socket(self.address)
        try:
            sock.connect()
        except socket.error:
            return False

        return True
