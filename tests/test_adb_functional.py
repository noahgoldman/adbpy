import socket
import random

import pytest
from mock import patch

from adbpy.adb import Adb
from adbpy import Target, AdbError
from adbpy.adb_process import AdbProcess

from .utils import random_ascii

DEFAULT_ADDRESS = ("localhost", 5037)

def adb_active():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((DEFAULT_ADDRESS))
    except socket.error:
        return False

    return True

def num_devices():
    if adb_active():
        a = Adb(DEFAULT_ADDRESS)
        return len(a.devices())

@pytest.fixture
def adb():
    # Restart ADB
    adb = Adb(DEFAULT_ADDRESS)
    adb.kill()

    proc = AdbProcess("adb", DEFAULT_ADDRESS)
    proc.start()
    return adb

@pytest.mark.skipif(not adb_active(), reason="Adb is not running")
class TestAdbFunctional:

    def test_start_adb(self, adb):
        adb.kill()
        adb.start()

        adb.kill()
        with patch.object(AdbProcess, "running", return_value=False):
            with pytest.raises(AdbError):
                adb.start()

    def test_version(self, adb):
        version = adb.version()

        assert len(version) == 4

        # Adb version should be around 30-40
        assert int(version, 16) < 50

    def test_get_serialno(self, adb):
        serialno = adb.get_serialno(Target.ANY)
        assert serialno is not ''

    @pytest.mark.skipif(num_devices() != 1, reason="Only one device can be present.")
    def test_shell(self, adb):
        data = "test"
        assert adb.shell('echo "{0}"'.format(data)) == data + "\r\n"

    @pytest.mark.skipif(num_devices() != 1, reason="Only one device can be present.")
    def test_shell_timeout(self, adb):
        assert adb.shell('echo "hi"; sleep 0.2; echo "ho"', timeout=0.1) == "hi\r\n"

    @pytest.mark.skipif(num_devices() != 1, reason="Only one device can be present.")
    def test_forward(self, adb):
        port1 = "tcp:" + str(random.randint(0, 9999))
        port2 = "tcp:" + str(random.randint(0, 9999))
        output = adb.forward(port1, port2)
        assert output

        output = adb.forward(port1, port2, norebind=True)
        assert not output

        output = adb.kill_forward(port1) 
        assert output

        output = adb.kill_forward(port1) 
        assert not output

        output = adb.kill_forward_all()
        assert output
