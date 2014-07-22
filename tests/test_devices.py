from adbpy.devices import parse_device_list

def test_parse_device():
    input = "1ccb04bb\tdevice\n"
    expected = [("1ccb04bb", "device")]
    assert parse_device_list(input) == expected

    input = "1ccb04bb\tdevice\n950a8ad5\tunauthorized\n"
    expected = [("1ccb04bb", "device"), ("950a8ad5", "unauthorized")]
    assert parse_device_list(input) == expected

    input = ""
    expected = []
    assert parse_device_list(input) == expected

    input = "1ccb04bb\tdevice\n950a8ad5\tunauthorized\n1234567\toffline\n"
    expected = [
        ("1ccb04bb", "device"),
        ("950a8ad5", "unauthorized"),
        ("1234567", "offline"),
    ]
    assert parse_device_list(input) == expected
