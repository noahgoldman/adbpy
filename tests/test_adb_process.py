import pytest
from mock import patch, call

from adbpy.adb_process import AdbProcess

ADB_PATH = "adb"

@pytest.fixture
def adb_proc():
    return AdbProcess(ADB_PATH)

def test_start(adb_proc):
    with patch("subprocess.call", return_value=0) as subproc:
        adb_proc.start()
        subproc.assert_called_once_with(ADB_PATH + " start-server", shell=True)
