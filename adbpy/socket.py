"""Socket connection classes for interacting with the ADB server directly"""

from __future__ import absolute_import
from __future__ import unicode_literals
import socket
from contextlib import contextmanager
import select
import time

class Socket(object):
    """Implements the socket protocol for ADB"""

    MAX_RECV = 4096

    def __init__(self, address):
        """Assign the socket"""
        self.address = address
        self.socket = None
        self.connected = False

    @contextmanager
    def Connect(self):
        """
        Context manager to handle a socket
        """
        self.connect()
        yield
        self.close()

    def connect(self):
        """Connect to the given socket"""
        if not self.connected:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.address)
            self.connected = True

    def close(self):
        """Close the current socket"""
        self.socket.close()
        self.connected = False

    def send(self, data):
        """Send a formatted message to the ADB server"""
        self._send_data(int_to_hex(len(data)))

        self._send_data(data)

    def _send_data(self, data):
        """Send data to the ADB server"""
        total_sent = 0

        while total_sent < len(data):
            # Send only the bytes that haven't been
            # sent yet
            sent = self.socket.send(data[total_sent:].encode("ascii"))

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
                                            self.MAX_RECV)).decode("ascii")

            if chunk == '':
                self.close()
                raise RuntimeError("Socket connection dropped, "
                                   "recv failed")

            data += chunk
            total_received += len(chunk)

        return data

    def receive(self):
        # Get the response status
        status = self.receive_fixed_length(4)

        if status != "OKAY" and status != "FAIL":
            raise SocketError("Socket communication failed: "
                              "the server did not return a valid response")

        # Get the length of the incoming data
        data_length_str = self.receive_fixed_length(4)
        data_length = int(data_length_str, 16)

        # Get the incoming data
        data = self.receive_fixed_length(data_length)

        if status != "OKAY":
            raise SocketError("Previous command failed with: " + data)

        self.close()
        return data

    def receive_until_end(self, timeout=None):
        """
        Reads and blocks until the socket closes

        Used for the "shell" command, where STDOUT and STDERR
        are just redirected to the terminal with no length
        """
        if self.receive_fixed_length(4) != "OKAY":
            raise SocketError("Socket communication failed: "
                              "the server did not return a valid response")

        # The time at which the receive starts
        start_time = time.clock()

        output = ""

        while True:
            if timeout is not None:
                self.socket.settimeout(timeout - (time.clock() - start_time))
            
            chunk = ''
            try:
                chunk = self.socket.recv(4096).decode("ascii")
            except socket.timeout:
                return output            

            if not chunk:
                return output

            output += chunk

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

class SocketError(Exception):
    pass
