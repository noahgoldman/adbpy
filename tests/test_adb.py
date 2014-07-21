from mock import MagicMock, patch
import pytest

from adbpy.adb import Adb
from adbpy import Target

@pytest.fixture
def adb():
    adb = Adb(())
    adb.socket = MagicMock()
    return adb

def test_adb_version(adb):
    adb.version()

    adb.socket.send.assert_called_once_with("host:version")

def test_adb_get_serialno_any(adb):
    adb.get_serialno(Target.ANY)
    adb.socket.send.assert_called_once_with("host:get-serialno")

def test_adb_get_serialno_serial(adb):
    adb.get_serialno("6097191b")
    adb.socket.send.assert_called_once_with("host-serial:6097191b:get-serialno")

def test_shell(adb):
    with patch.object(Adb, "setup_target"):
        adb.shell("ls -l")
        adb.socket.send.assert_called_once_with("shell:ls -l")
        adb.setup_target.assert_called_once()

def test_forward(adb):
    device_id = "950a8ad5"
    adb.forward("tcp:6001", "tcp:36001", device_id, norebind=False)

    adb.socket.send.assert_called_once_with("host-serial:950a8ad5:"
                                            "forward:tcp:6001;"
                                            "tcp:36001")

def test_forward_rebind(adb):
    device_id = "950a8ad5"
    adb.forward("tcp:6001", "tcp:36001", device_id, norebind=True)

    adb.socket.send.assert_called_once_with("host-serial:950a8ad5:"
                                            "forward:norebind:"
                                            "tcp:6001;tcp:36001")
