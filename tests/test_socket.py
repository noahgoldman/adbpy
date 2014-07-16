from unittest import TestCase

from adbpy.socket import Socket, int_to_hex, make_adb_message
from tests.mock_socket import MockSocket

class TestAdbCommand(TestCase):

    def test_int_to_hex(self):
        self.assertEqual(int_to_hex(2), "0002")
        self.assertEqual(int_to_hex(255), "00ff")
        self.assertEqual(int_to_hex(256), "0100")
        self.assertEqual(int_to_hex(100), "0064")
        self.assertEqual(int_to_hex(0), "0000")

    def test_int_to_hex_overflow(self):
        with self.assertRaises(ValueError):
            int_to_hex(65536)

    def test_message(self):
        msg = make_adb_message("host:track-devices")
        self.assertEqual(msg, "0012host:track-devices")

        msg = make_adb_message("host:serial:950a8ad5:list-forward")
        self.assertEqual(msg, "0021host:serial:950a8ad5:list-forward")
    
    def test_message_overflow(self):
        with self.assertRaises(ValueError):
            make_adb_message("x" * 65536)


class TestSocket(TestCase):

    def setUp(self):
        self.sock = MockSocket()
        self.mysock = Socket(self.sock)

    def test_send_normal_response(self):
        data_sent = [] 
        def send(message):
            data_sent.append(message)
            return len(message)

        self.sock.send = send

        data = "host:track-devices"

        self.mysock.send(data)

        self.assertEquals(1, len(data_sent))
        self.assertEquals(data, data_sent[0])

    def test_send_staggered_response(self):
        data_sent = [] 
        def send(message):
            data_sent.append(message[0])
            return 1

        self.sock.send = send
        data = "host:track-devices"

        self.mysock.send(data)

        self.assertEquals(len(data), len(data_sent))
        self.assertEquals(data, ''.join(data_sent))

    def test_send_failed_response(self):
        response_lengths = [0, 1]
        self.sock.send = lambda x: response_lengths.pop()

        with self.assertRaises(RuntimeError):
            self.mysock.send("long test string")

    def test_receive_fixed_length_full_response(self):
        data_to_recv = "0005"

        self.sock.recv = lambda x: data_to_recv

        data =  self.mysock.receive_fixed_length(4)
        self.assertEqual(data_to_recv, data)

    def test_receive_fixed_length_staggered_response(self):
        data_to_recv = "0005"
        split_data = list(data_to_recv)
        split_data.reverse()

        self.sock.recv = lambda x: split_data.pop()

        data =  self.mysock.receive_fixed_length(4)
        self.assertEqual(data_to_recv, data)

    def test_receive_failed_response(self):
        responses = ['', 'hi']
        self.sock.recv = lambda x: responses.pop()

        with self.assertRaises(RuntimeError):
            self.mysock.receive_fixed_length(100)
