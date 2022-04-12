from geometric_primitives import brick
from geometric_primitives import bricks
from geometric_primitives import rules
from geometric_primitives import utils_io
from geometric_primitives import utils_meshes


list_rules = rules.LIST_RULES_2_4
print(list_rules)

def assemble(list_conns):
    bricks_ = bricks.Bricks(10000, 0)

    z = 0
    dir_cur = 0

    brick_ = brick.Brick()
    brick_.set_position([0, 0, z])
    brick_.set_direction(dir_cur)

    bricks_.add(brick_)

    for conn in list_conns:
        z += 1
        print(list_rules[conn])

        dir_cur = (dir_cur + list_rules[conn][1][0]) % 2

        brick_ = brick.Brick()
        brick_.set_position(list_rules[conn][1][1] + [z])
        brick_.set_direction(dir_cur)

        bricks_.add(brick_)

    return bricks_


if __name__ == '__main__':
    list_conns = [45, 45, 45, 45]
    bricks_ = assemble(list_conns)

    mesh_bricks, mesh_cubes = utils_meshes.get_mesh_bricks(bricks_)
    utils_io.visualize(mesh_bricks)

    list_conns = [0, 45, 30, 45]
    bricks_ = assemble(list_conns)

    mesh_bricks, mesh_cubes = utils_meshes.get_mesh_bricks(bricks_)
    utils_io.visualize(mesh_bricks)
