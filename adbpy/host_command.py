from adbpy import Target

def get_host_prefix(target):
    if target == Target.ANY:
        return "host:"
    elif target == Target.USB or target == Target.EMULATOR:
        return "host-{0}:".format(target)

    return "host-serial:{0}:".format(target)

def host_command(target, command):
    return get_host_prefix(target) + command
