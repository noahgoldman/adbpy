import pytest
import socket

from adbpy.adb import Adb
from adbpy import Target

DEFAULT_ADDRESS = ("localhost", 5037)

def adb_active():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((DEFAULT_ADDRESS))
    except socket.error:
        return False

    return True

@pytest.fixture
def adb():
    return Adb(DEFAULT_ADDRESS)

@pytest.mark.skipif(not adb_active(), reason="Adb is not running")
class TestAdbFunctional:

    def test_version(self, adb):
        version = adb.version()

        assert len(version) == 4

        # Adb version should be around 30-40
        assert int(version, 16) < 50

    def test_get_serialno(self, adb):
        serialno = adb.get_serialno(Target.ANY)
        assert serialno is not ''
