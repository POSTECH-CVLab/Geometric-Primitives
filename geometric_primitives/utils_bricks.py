import numpy as np
import copy

from geometric_primitives import brick
from geometric_primitives import bricks


def align_bricks(bricks_):
    list_bricks = bricks_.get_bricks()

    list_positions = []
    for brick_ in list_bricks:
        list_positions.append(brick_.get_position())
    positions = np.array(list_positions)

    trans = np.array([
        np.min(positions[:, 0]),
        np.min(positions[:, 1]),
        np.min(positions[:, 2]),
    ])

    list_bricks_new = []
    for brick_ in list_bricks:
        position_new = copy.deepcopy(brick_.get_position())
        direction_new = copy.deepcopy(brick_.get_direction())

        position_new -= trans

        brick_new = brick.Brick()
        brick_new.set_position(position_new)
        brick_new.set_direction(direction_new)
        list_bricks_new.append(brick_new)

    bricks_aligned = bricks.Bricks(bricks_.get_length())
    bricks_aligned.bricks = list_bricks_new
    bricks_aligned.validate_all()

    return bricks_aligned

def align_bricks_to_origin(bricks_):
    list_bricks = bricks_.get_bricks()

    list_positions = []
    for brick_ in list_bricks:
        list_positions.append(brick_.get_position())
    positions = np.array(list_positions)
    bottoms = np.where(positions[:, 2] == np.min(positions[:, 2]))[0]
    ind_origin = np.random.choice(bottoms, 1)
    ind_origin = ind_origin[0]

    brick_origin = copy.deepcopy(list_bricks[ind_origin])

    list_bricks_new = []
    for brick_ in list_bricks:
        position_new = copy.deepcopy(brick_.get_position())
        direction_new = copy.deepcopy(brick_.get_direction())

        position_new -= brick_origin.get_position()

        if brick_origin.get_direction() == 1:
            angle_rotated = np.pi * 1.0 / 2.0
            position_new_ = copy.deepcopy(position_new)
            position_new_.astype(np.float)
            position_new.astype(np.float)

            position_new[0] = np.round(np.cos(angle_rotated) * position_new_[0]) - np.round(np.sin(angle_rotated) * position_new_[1])
            position_new[1] = np.round(np.sin(angle_rotated) * position_new_[0]) + np.round(np.cos(angle_rotated) * position_new_[1])

            position_new = np.round(position_new)

            direction_new = (direction_new + brick_origin.get_direction()) % 2

        brick_new = brick.Brick()
        brick_new.set_position(position_new)
        brick_new.set_direction(direction_new)
        list_bricks_new.append(brick_new)

    bricks_aligned = bricks.Bricks(bricks_.get_length())
    bricks_aligned.bricks = list_bricks_new
    bricks_aligned.validate_all()

    return bricks_aligned

def convert_to_bricks(X, A):
    list_bricks = []
    for bx, ba in zip(X, A):
        brick_ = brick.Brick()
        brick_.set_position(bx[:3])
        brick_.set_direction(bx[3])

        list_bricks.append(brick_)

    bricks_ = Bricks(len(list_bricks))
    bricks_.bricks = list_bricks
    try:
        bricks_.validate_all()
    except:
        bricks_ = None

    return bricks_
