import numpy as np


def check_overlap_1d(min_max_1, min_max_2):
    assert isinstance(min_max_1, tuple)
    assert isinstance(min_max_2, tuple)

    return min_max_1[1] > min_max_2[0] and min_max_2[1] > min_max_1[0]

def check_overlap_2d(min_max_1, min_max_2):
    assert len(min_max_1) == 2
    assert len(min_max_2) == 2

    return check_overlap_1d(min_max_1[0], min_max_2[0]) and check_overlap_1d(min_max_1[1], min_max_2[1])

def check_overlap_3d(min_max_1, min_max_2):
    assert len(min_max_1) == 3
    assert len(min_max_2) == 3

    return check_overlap_1d(min_max_1[0], min_max_2[0]) and check_overlap_1d(min_max_1[1], min_max_2[1]) and check_overlap_1d(min_max_1[2], min_max_2[2])

def get_min_max_3d(vertices):
    min_max = [
        (np.min(vertices[:, 0]), np.max(vertices[:, 0])),
        (np.min(vertices[:, 1]), np.max(vertices[:, 1])),
        (np.min(vertices[:, 2]), np.max(vertices[:, 2]))
    ]

    return min_max

def check_duplicate(bricks_, brick_):
    for cur_brick in bricks_:
        if np.all(cur_brick.get_position() == brick_.get_position()) and cur_brick.get_direction() == brick_.get_direction():
            return False
    return True
