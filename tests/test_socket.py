from unittest import TestCase
import pytest

from adbpy.socket import Socket, int_to_hex, make_adb_message
from tests.mock_socket import MockSocket

def test_int_to_hex():
    assert int_to_hex(2) == "0002"
    assert int_to_hex(255) == "00ff"
    assert int_to_hex(256) == "0100"
    assert int_to_hex(100) == "0064"
    assert int_to_hex(0) == "0000"

def test_int_to_hex_overflow():
    with pytest.raises(ValueError):
        int_to_hex(65536)

def test_message():
    msg = make_adb_message("host:track-devices")
    assert msg == "0012host:track-devices"

    msg = make_adb_message("host:serial:950a8ad5:list-forward")
    assert msg == "0021host:serial:950a8ad5:list-forward"

def test_message_overflow():
    with pytest.raises(ValueError):
        make_adb_message("x" * 65536)

@pytest.fixture
def socket():
    return Socket(MockSocket())

def test_send_normal_response(socket):
    data_sent = [] 
    def send(message):
        data_sent.append(message)
        return len(message)

    socket.socket.send = send

    data = "host:track-devices"

    socket.send(data)

    assert len(data_sent) == 1
    assert data == data_sent[0]

def test_send_staggered_response(socket):
    data_sent = [] 
    def send(message):
        data_sent.append(message[0])
        return 1

    socket.socket.send = send
    data = "host:track-devices"

    socket.send(data)

    assert len(data) == len(data_sent)
    assert data == ''.join(data_sent)

def test_send_failed_response(socket):
    response_lengths = [0, 1]
    socket.socket.send = lambda x: response_lengths.pop()

    with pytest.raises(RuntimeError):
        socket.send("long test string")

def test_receive_fixed_length_full_response(socket):
    data_to_recv = "0005"

    socket.socket.recv = lambda x: data_to_recv

    data = socket.receive_fixed_length(4)
    assert data_to_recv == data

def test_receive_fixed_length_staggered_response(socket):
    data_to_recv = "0005"
    split_data = list(data_to_recv)
    split_data.reverse()

    socket.socket.recv = lambda x: split_data.pop()

    data = socket.receive_fixed_length(4)
    assert data_to_recv == data

def test_receive_failed_response(socket):
    responses = ['', 'hi']
    socket.socket.recv = lambda x: responses.pop()

    with pytest.raises(RuntimeError):
        socket.receive_fixed_length(100)
