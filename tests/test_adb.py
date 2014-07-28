from mock import MagicMock, patch
import pytest

from adbpy.adb import Adb
from adbpy import Target, AdbError

@pytest.fixture
def adb():
    adb = Adb(())
    adb.socket = MagicMock()
    return adb

def test_get_transport():
    assert Adb._get_transport(Target.ANY) == "host:transport-any" 
    assert Adb._get_transport(Target.USB) == "host:transport-usb" 
    assert Adb._get_transport(Target.EMULATOR) == "host:transport-local" 
    assert Adb._get_transport("950a8ad5") == "host:transport:950a8ad5"

def test_adb_version(adb):
    adb.version()

    adb.socket.send.assert_called_once_with("host:version")

def test_adb_get_serialno_any(adb):
    adb.get_serialno(Target.ANY)
    adb.socket.send.assert_called_once_with("host:get-serialno")

def test_adb_get_serialno_serial(adb):
    adb.get_serialno("6097191b")
    adb.socket.send.assert_called_once_with("host-serial:6097191b:get-serialno")

def test_adb_get_product(adb):
    adb.get_product("950a8ad5")
    adb.socket.send.assert_called_once_with("host-serial:950a8ad5:get-product")

def test_adb_get_devpath(adb):
    adb.get_devpath(Target.USB)
    adb.socket.send.assert_called_once_with("host-usb:get-devpath")

def test_adb_get_state(adb):
    adb.get_state(Target.EMULATOR)
    adb.socket.send.assert_called_once_with("host-local:get-state")

def test_shell(adb):
    with patch.object(Adb, "_setup_target"):
        adb.shell("ls -l")
        adb.socket.send.assert_called_once_with("shell:ls -l")
        adb._setup_target.assert_called_once()

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

def test_devices(adb):
    adb.socket.receive = MagicMock(return_value="950a8ad5\tdevice\n")
    output = adb.devices()

    assert output == [("950a8ad5", "device")]

def test_start(adb):
    adb.process = MagicMock()
    adb.process.running = MagicMock(return_value=False)

    with pytest.raises(AdbError):
        adb.start()
