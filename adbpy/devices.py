import re

device_regex = re.compile(r'(\w+)\t(device|offline|unauthorized)')

def parse_device_list(device_list):
    return device_regex.findall(device_list)
