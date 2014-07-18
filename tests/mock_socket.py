import random

class MockSocket(object):

    def __init__(self):
        self.input = ""

    def connect(self):
        self.connected = True

    def close(self):
        self.connected = False

    def send(self, message):
        self.input += message

    def recv(self, length):
        return self.buffer.pop(0)

    def set_buffer(self, data):
        self.buffer = random_split(data)

def random_split(data):
    data_len = len(data)
    splits = random.randrange(data_len)  

    nums = set(map(lambda x: random.randrange(data_len), range(splits)))
    return slice_list(data, nums)
    
def slice_list(data, points):
    output = []
    output.append(data[:points[0]])

    for i in range(len(points)-1):
        output.append(data[points[i]:points[i+1]])
    output.append(data[points[len(points)-1]:])

    return output
