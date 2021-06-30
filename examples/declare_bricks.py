import time
import copy

from geometric_primitives import brick
from geometric_primitives import bricks
from geometric_primitives import rules


brick1 = brick.Brick()
brick2 = brick.Brick()
brick3 = brick.Brick()

brick1.set_position([0, 0, 0])
brick1.set_direction(0)

brick2.set_position([1, -2, 1])
brick2.set_direction(1)

brick3.set_position([-1, -3, 1])
brick3.set_direction(0)

bricks_ = bricks.Bricks(6, '0')
bricks_.add(brick1)
bricks_.add(brick2)

brick1 = brick.Brick()

brick1.set_position([0, 0, 0])
brick1.set_direction(0)

bricks_ = bricks.Bricks(6, '0')
bricks_.add(brick1)

bricks_._validate_overlap()
bricks_.get_possible_contacts()

def stack(bricks):
    possible_bricks = bricks.get_possible_contacts()
    new_bricks = []

    for possible_brick in possible_bricks:
        copy_bricks = copy.deepcopy(bricks)
        copy_bricks.add(possible_brick)

        copy_bricks.validate_all()
        X, A, E, D = copy_bricks.get_graph()

        new_bricks.append(copy_bricks)

    return new_bricks
    
list_bricks = [bricks_]

for ind in range(0, 4):
    time_start = time.time()
    new_list_bricks = []

    num_bricks = 0
    for bricks_ in list_bricks:
        cur_list_bricks = stack(bricks_)
        num_bricks += len(cur_list_bricks)
        if ind < 3:
            new_list_bricks += cur_list_bricks

    list_bricks = new_list_bricks
    print(num_bricks)
    time_end = time.time()
    print('time consumed: ', time_end - time_start, 'sec.')
