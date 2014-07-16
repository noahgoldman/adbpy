class MockSocket(object):

    def connect(self):
        self.connected = True

    def close(self):
        self.connected = False

    def send(self, message):
        return len(message)

    def recv(self, length):
        pass
