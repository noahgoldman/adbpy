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
        return self.buffer.pop(0).encode("ascii")

    def set_buffer(self, data):
        self.buffer = random_split(data)
        self.buffer.append("")
        print(self.buffer)

def random_split(data):
    data_len = len(data)
    splits = random.randrange(data_len)  

    nums = list(map(lambda x: random.randrange(data_len), range(splits)))
    nums.insert(0, 0)
    nums.append(data_len-1)
    nums.sort()
    remove_close_nums(nums)

    return slice_list(data, nums)
    
def slice_list(data, points):
    output = []

    for i in range(len(points)-1):
        output.append(data[points[i]:points[i+1]])
    output.append(data[points[len(points)-1]:])

    return output

def remove_close_nums(nums):
    """
    Remove any items in the list that are the same number
    or are within 1 of each other.

    Assumes the input list is sorted
    """
    i = 0
    while i < len(nums)-1:
        if (nums[i] + 1) >= nums[i+1]:
            nums.pop(i+1)
        else:
            i += 1
