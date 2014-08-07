from __future__ import absolute_import

import os
import subprocess
import socket

from adbpy.socket import Socket

class AdbProcess(object):

    def __init__(self, path, address):
        self.path = path
        self.address = address

    def start(self):
        null = open(os.devnull, 'w')
        cmd = '"{0}" -P {1} start-server'.format(self.path, self.address[1])
        return subprocess.call(cmd, shell=True, stdout=null) == 0

    def running(self):
        sock = Socket(self.address)
        try:
            sock.connect()
        except socket.error:
            return False

        return True
