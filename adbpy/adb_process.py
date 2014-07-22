import subprocess

class AdbProcess(object):

    def __init__(self, path):
        self.started = False
        self.path = path

    def start(self):
        return subprocess.call(self.path + " start-server", shell=True) == 0
