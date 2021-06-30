import numpy as np
import numpy.matlib
import os
import copy

import open3d as o3d

from geometric_primitives import bricks


path_unit_primitives = '../unit_primitives'
str_cube = 'cube.stl'
str_2_4 = '3001.stl'
str_2_2 = '3003.stl'
str_1_2 = '3004.stl'

path_brick_0 = os.path.join(path_unit_primitives, str_2_4)
path_brick_1 = os.path.join(path_unit_primitives, str_2_2)
path_brick_2 = os.path.join(path_unit_primitives, str_1_2)

mesh_bricks_unit = [
    o3d.io.read_triangle_mesh(path_brick_0),
    o3d.io.read_triangle_mesh(path_brick_1),
    o3d.io.read_triangle_mesh(path_brick_2),
]

dividers_1 = [
    2,
    2,
    1,
]
dividers_2 = [
    4,
    2,
    2,
]
subtractors_3 = [
    6.27,
    6.27,
    6.27,
]


def preprocess(model, color):
    min_bound = model.get_min_bound()
    max_bound = model.get_max_bound()
    center = min_bound + (max_bound - min_bound) / 2.0
    scale = 1.0

    vertices = np.asarray(model.vertices)
    vertices -= np.matlib.repmat(center, len(model.vertices), 1)
    model.vertices = o3d.utility.Vector3dVector(vertices / scale)

    angle = -np.pi / 2.0
    model.rotate(np.array([
        [1.0, 0.0, 0.0],
        [0.0, np.cos(angle), -np.sin(angle)],
        [0.0, np.sin(angle), np.cos(angle)],
    ]))

    angle = np.pi / 2.0
    model.rotate(np.array([
        [np.cos(angle), -np.sin(angle), 0.0],
        [np.sin(angle), np.cos(angle), 0.0],
        [0.0, 0.0, 1.0],
    ]))

#    model.transform(np.array([
#        [0.735, 0, 0, 0],
#        [0, 1.4775, 0, 0],
#        [0, 0, 0.445, 0],
#        [0, 0, 0, 1],
#    ]))

    model.paint_uniform_color(color)

    return model

def get_cube(color):
    path_cube = os.path.join(path_unit_primitives, str_cube)

    mesh_cube = o3d.io.read_triangle_mesh(path_cube)
    mesh_cube = preprocess(mesh_cube, color)

    mesh_cube.translate(np.array([
        [0],
        [0],
        [0]
    ]))

    mesh_cube.transform(np.array([
        [0.735, 0, 0, 0],
        [0, 1.4775, 0, 0],
        [0, 0, 0.445, 0],
        [0, 0, 0, 1],
    ]))

    return mesh_cube

def get_voxel(color):
    path_cube = os.path.join(path_unit_primitives, str_cube)

    mesh_cube = o3d.io.read_triangle_mesh(path_cube)
    mesh_cube = preprocess(mesh_cube, color)

    mesh_cube.translate(np.array([
        [0],
        [0],
        [0]
    ]))

    mesh_cube.transform(np.array([
        [0.5, 0, 0, 0],
        [0, 0.5, 0, 0],
        [0, 0, 0.5, 0],
        [0, 0, 0, 1],
    ]))

    return mesh_cube

def choose_brick_info(brick_):
    ind = int(bricks.get_cur_type(brick_))

    mesh_brick = copy.deepcopy(mesh_bricks_unit[ind])
    divider_1 = copy.deepcopy(dividers_1[ind])
    divider_2 = copy.deepcopy(dividers_2[ind])
    subtractor_3 = copy.deepcopy(subtractors_3[ind])

    return mesh_brick, divider_1, divider_2, subtractor_3

def get_mesh_bricks(bricks_):
    mesh_bricks = []
    mesh_cubes = []

    for ind_brick, brick_ in enumerate(bricks_.get_bricks()):
        color = np.random.RandomState(43 * ind_brick).rand(3)
        ind = int(bricks.get_cur_type(brick_))

        mesh_brick, divider_1, divider_2, subtractor_3 = choose_brick_info(brick_)
        mesh_brick = preprocess(mesh_brick, color)

        if ind == 1:
            vertices = np.asarray(mesh_brick.vertices)
            vertices += np.matlib.repmat([0.0, 2.8, 2.8], len(mesh_brick.vertices), 1)
            mesh_brick.vertices = o3d.utility.Vector3dVector(vertices)
        elif ind == 2:
            vertices = np.asarray(mesh_brick.vertices)
            vertices += np.matlib.repmat([0.0, 2.1, 2.1], len(mesh_brick.vertices), 1)
            mesh_brick.vertices = o3d.utility.Vector3dVector(vertices)

#        mesh_cube = get_cube(color)

        bound_min = mesh_brick.get_min_bound()
        bound_max = mesh_brick.get_max_bound()

        unit_axis_1 = (bound_max[0] - bound_min[0]) / divider_1
        unit_axis_2 = (bound_max[1] - bound_min[1]) / divider_2
        unit_axis_3 = (bound_max[2] - bound_min[2]) - subtractor_3

        pos = brick_.get_position()
        direc = brick_.get_direction()
        mesh_brick.translate(np.array([
            [unit_axis_1 * pos[0]], 
            [unit_axis_2 * pos[1]], 
            [unit_axis_3 * pos[2]]
        ]))
        mesh_brick.rotate(mesh_brick.get_rotation_matrix_from_xyz((0.0, 0.0, np.pi / 2.0 * direc)))

        '''
        mesh_cube.translate(np.array([
            [unit_axis_1 * pos[0]], 
            [unit_axis_2 * pos[1]], 
            [unit_axis_3 * pos[2]]
        ]))

        mesh_cube.rotate(mesh_cube.get_rotation_matrix_from_xyz((0.0, 0.0, np.pi / 2.0 * direc)))
        '''

        mesh_bricks.append(mesh_brick)
#        mesh_cubes.append(mesh_cube)

    return mesh_bricks, mesh_cubes

def get_mesh_voxels(voxels_):
    len_voxels = voxels_.get_length()
    mesh_voxels = []

    for ind_bricks in range(1, len_voxels + 1):
        color = np.random.RandomState(42 * ind_bricks).rand(3)

        mesh_voxel = get_voxel(color)
        mesh_voxels.append(mesh_voxel)

    mesh_voxel = mesh_voxels[0]
    bound_min = mesh_voxel.get_min_bound()
    bound_max = mesh_voxel.get_max_bound()
    unit_axis_1 = (bound_max[0] - bound_min[0]) + 0.03
    unit_axis_2 = (bound_max[1] - bound_min[1]) + 0.03
    unit_axis_3 = (bound_max[2] - bound_min[2]) + 0.03

    print(unit_axis_1)
    print(unit_axis_2)
    print(unit_axis_3)

    for voxel, mesh_voxel in zip(voxels_.get_voxels(), mesh_voxels):
        pos = voxel.get_position()
        direc = voxel.get_direction()
        mesh_voxel.translate(np.array([
            [unit_axis_1 * pos[0]], 
            [unit_axis_2 * pos[1]], 
            [unit_axis_3 * pos[2]]
        ]))
#        mesh_voxel.rotate(mesh_voxel.get_rotation_matrix_from_xyz((0.0, 0.0, np.pi / 2.0 * direc)))

    return mesh_voxels
