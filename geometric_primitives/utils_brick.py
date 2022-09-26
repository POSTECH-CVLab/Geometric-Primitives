import numpy as np


def get_type(size_upper, size_lower, height):
    if np.all(size_upper == [2, 4]) and np.all(size_lower == [2, 4]) and height == 1:
        return 0
    elif np.all(size_upper == [2, 2]) and np.all(size_lower == [2, 2]) and height == 1:
        return 1
    elif np.all(size_upper == [1, 2]) and np.all(size_lower == [1, 2]) and height == 1:
        return 2
    else:
        raise ValueError('Not supported size.')

def get_size(brick_type):
    if brick_type == 0:
        size_upper = size_lower = [2, 4]
        height = 1
    elif brick_type == 1:
        size_upper = size_lower = [2, 2]
        height = 1
    elif brick_type == 2:
        size_upper = size_lower = [1, 2]
        height = 1
    else:
        raise ValueError('Not supported brick_type.')

    return size_upper, size_lower, height
