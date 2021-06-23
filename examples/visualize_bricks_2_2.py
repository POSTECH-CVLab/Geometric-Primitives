import time
import copy

from geometric_primitives import brick
from geometric_primitives import bricks
from geometric_primitives import rules
from geometric_primitives import utils_io
from geometric_primitives import utils_meshes


brick_ = brick.Brick(size_upper=[2, 2], size_lower=[2, 2])
brick_.set_position([0, 0, 0])
brick_.set_direction(0)

bricks_ = bricks.Bricks(100, '1')
bricks_.add(brick_)

for ind in range(0, 10):
    brick_ = bricks_.sample()[0]
    bricks_.add(brick_)
    print(brick_.get_position(), brick_.get_direction())

    mesh_bricks, mesh_cubes = utils_meshes.get_mesh_bricks(bricks_, '2_2')
    utils_io.visualize(mesh_bricks)
