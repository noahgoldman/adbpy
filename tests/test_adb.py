from mock import MagicMock
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
