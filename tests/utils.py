import random
import string

def random_ascii(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
