from adbpy import Target

def get_host_prefix(target):
    if target in Target.__dict__.values():
        return target

    return "host-serial:{0}:".format(target)

def host_command(target, command):
    return get_host_prefix(target) + command
