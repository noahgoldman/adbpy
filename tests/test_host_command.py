from adbpy.host_command import get_host_prefix, host_command
from adbpy import Target

def test_get_host_prefix():
    assert get_host_prefix(Target.ANY) == Target.ANY
    assert get_host_prefix(Target.USB) == Target.USB

    assert get_host_prefix("950a8ad5") == "host-serial:950a8ad5:"

def test_command():
    assert host_command(Target.ANY, "test") == "host:test"
    assert host_command(Target.EMULATOR, "testing") == "host-local:testing"

    assert host_command("950a8ad5", "testing again") == "host-serial:950a8ad5:testing again"
