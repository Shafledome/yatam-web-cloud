import random
import string


def gen_random_key():
    letters_and_digits = string.ascii_letters + string.digits
    result = ''.join(random.choice(letters_and_digits) for i in range(16))
    return result
