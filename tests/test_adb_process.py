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
        subproc.assert_called_once_with(ADB_PATH + " -P " + str(DEFAULT_ADDRESS[1])
                                        + " start-server", shell=True)

def test_running(adb_proc):
    with patch.object(Socket, "connect", side_effect=socket.error()):
        assert adb_proc.running() == False

    with patch.object(Socket, "connect"):
        assert adb_proc.running() == True
