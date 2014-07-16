"""Socket connection classes for interacting with the ADB server directly"""

class Socket(object):
    """Implements the socket protocol for ADB"""

    MAX_RECV = 4096

    def __init__(self, socket):
        """Assign the socket"""
        self.socket = socket

    def connect(self):
        """Connect to the given socket"""
        self.socket.connect()

    def close(self):
        """Close the current socket"""
        self.socket.close()

    def send(self, data):
        """Send an formatted message to the ADB server"""
        total_sent = 0

        while total_sent < len(data):
            # Send only the bytes that haven't been
            # sent yet
            sent = self.socket.send(data[total_sent:])

            if sent == 0:
                self.close()
                raise RuntimeError("Socket connection dropped, "
                                   "send failed")
            total_sent += sent

    def receive_fixed_length(self, length):
        data = ''
        total_received = 0

        while total_received < length:
            chunk = self.socket.recv(min(length - total_received,
                                         self.MAX_RECV))
            if chunk == '':
                raise RuntimeError("Socket connection dropped, "
                                   "recv failed")
            data += chunk
            total_received += len(chunk)

        return data

    def receive(self):
        # Get the length of the incoming data
        data_length = receive_fixed_length(4)

        # Get the incoming data
        data = receive_fixed_length(data_length)

        return data

def make_adb_message(data):
    """
    Create a message formatted to the specifications
    of the ADB protocol.

    This is of the form "xxxx<data>" where xxxx is the length
    of the data as a 4 digit hex string

    Args:
        data    The data to be send

    Returns:
        A string to be sent to an ADB server
    """
    return int_to_hex(len(data)) + data

def int_to_hex(num):
    """
    Returns the integer formatted as a 4-digit hex string

    Args:
        num:    An integer to convert

    Returns:
        A 4 character hex string with no prefix
    """

    if num > 65535:
        raise ValueError("Maximum message length is 65535, "
                         "value of {} is too long".format(num))

    return "{0:04x}".format(num)
