import time
import copy

from geometric_primitives import brick
from geometric_primitives import bricks
from geometric_primitives import rules
from geometric_primitives import utils_io
from geometric_primitives import utils_meshes


size_brick = [1, 2]

brick_ = brick.Brick(size_upper=size_brick, size_lower=size_brick)
brick_.set_position([0, 0, 0])
brick_.set_direction(0)

bricks_ = bricks.Bricks(100, 'mixed')
bricks_.add(brick_)

list_bricks = bricks_.get_possible_contacts(str_type=None)

for elem in list_bricks:
    bricks_copied = copy.deepcopy(bricks_)
    bricks_copied.add(elem)

    mesh_bricks, mesh_cubes = utils_meshes.get_mesh_bricks(bricks_copied)
    utils_io.visualize(mesh_bricks)
