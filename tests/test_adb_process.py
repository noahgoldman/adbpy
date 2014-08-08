import socket

import pytest
from mock import patch, call

from adbpy.adb_process import AdbProcess
from adbpy.socket import Socket

ADB_PATH = "adb"

DEFAULT_ADDRESS = ("localhost", 5037)

@pytest.fixture
def adb_proc():
    return AdbProcess(ADB_PATH, DEFAULT_ADDRESS)

def test_start(adb_proc):
    with patch("subprocess.call", return_value=0) as subproc:
        adb_proc.start()
        assert "start-server" in subproc.call_args[0][0]

def test_start_alternate_port(adb_proc):
    adb_proc.address = ("localhost", 5040)
    with patch("subprocess.call", return_value=0) as subproc:
        adb_proc.start()
        assert "5040" in subproc.call_args[0][0]
        assert "start-server" in subproc.call_args[0][0]

def test_running(adb_proc):
    with patch.object(Socket, "connect", side_effect=socket.error()):
        assert adb_proc.running() == False

    with patch.object(Socket, "connect"):
        assert adb_proc.running() == True
