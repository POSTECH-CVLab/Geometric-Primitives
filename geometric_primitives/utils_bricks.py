import numpy as np
import copy

from geometric_primitives import brick
from geometric_primitives import bricks
from geometric_primitives import rules
from geometric_primitives import utils_brick


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
    num_types = np.unique(X[:, 0]).shape[0]

    if num_types == 1:
        brick_type = np.unique(X[:, 0])[0]
    else:
        brick_type = 'mixed'

    list_bricks = []
    for bx, ba in zip(X, A):
        size_upper, size_lower, height = utils_brick.get_size(bx[0])

        brick_ = brick.Brick(size_upper, size_lower, height)
        brick_.set_position(bx[1:4])
        brick_.set_direction(bx[4])

        list_bricks.append(brick_)

    bricks_ = Bricks(len(list_bricks), brick_type)
    bricks_.bricks = list_bricks
    try:
        bricks_.validate_all()
    except:
        bricks_ = None

    return bricks_

def get_rules(cur_type, next_type):
    if cur_type == 0 and next_type == 0:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_2_4)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_2_4)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_2_4)
    elif cur_type == 1 and next_type == 1:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_2_2)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_2_2)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_2_2)
    elif cur_type == 2 and next_type == 2:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_1_2)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_1_2)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_1_2)
    elif cur_type == 0 and next_type == 1:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_24_22)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_24_22)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_24_22)
    elif cur_type == 0 and next_type == 2:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_24_12)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_24_12)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_24_12)
    elif cur_type == 1 and next_type == 0:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_22_24)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_22_24)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_22_24)
    elif cur_type == 1 and next_type == 2:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_22_12)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_22_12)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_22_12)
    elif cur_type == 2 and next_type == 0:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_12_24)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_12_24)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_12_24)
    elif cur_type == 2 and next_type == 1:
        list_rules_ = copy.deepcopy(rules.LIST_RULES_12_22)
        rules_ = copy.deepcopy(rules.RULE_CONTACTS_12_22)
        probs_rules_ = copy.deepcopy(rules.PROBS_CONTACTS_12_22)
    else:
        raise ValueError('Invalid cur_type and next_type.')

    return list_rules_, rules_, probs_rules_
