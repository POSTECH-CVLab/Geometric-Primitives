from geometric_primitives.brick import Brick


obj_brick = Brick()
print(obj_brick)
print(obj_brick.size_upper)
print(obj_brick.size_lower)

obj_brick.set_position([1, 2, 3])
print(obj_brick.position)
print(obj_brick.vertices)

obj_brick.set_position([1, -2, 3])
print(obj_brick.position)
print(obj_brick.vertices)

print(obj_brick.get_vertices())
print(obj_brick.get_position())

config = {
    'position': [1, 4, 2],
    'direction': 1
}
obj_brick.set_configuration(config)

print(obj_brick.get_vertices())
print(obj_brick.get_position())
print(obj_brick.get_direction())
