import numpy as np
from datetime import datetime
import os
import open3d as o3d


def get_dists(vert_source, vert_target):
    vert_source_0 = np.unique(vert_source[:, 0])
    vert_target_0 = np.unique(vert_target[:, 0])

    vert_source_1 = np.unique(vert_source[:, 1])
    vert_target_1 = np.unique(vert_target[:, 1])

    vert_source_0.sort()
    vert_source_1.sort()
    vert_target_0.sort()
    vert_target_1.sort()

    dist_0_all = np.maximum(vert_target_0[1] - vert_source_0[0], vert_source_0[1] - vert_target_0[0])
    dist_0_all = np.maximum(vert_target_0[1] - vert_target_0[0], dist_0_all)
    dist_0_all = np.maximum(vert_source_0[1] - vert_source_0[0], dist_0_all)

    dist_0 = (vert_source_0[1] - vert_source_0[0])\
        + (vert_target_0[1] - vert_target_0[0])\
        - dist_0_all

    dist_1_all = np.maximum(vert_target_1[1] - vert_source_1[0], vert_source_1[1] - vert_target_1[0])
    dist_1_all = np.maximum(vert_target_1[1] - vert_target_1[0], dist_1_all)
    dist_1_all = np.maximum(vert_source_1[1] - vert_source_1[0], dist_1_all)

    dist_1 = (vert_source_1[1] - vert_source_1[0])\
        + (vert_target_1[1] - vert_target_1[0])\
        - dist_1_all

    return dist_0, dist_1

def visualize(mesh_object):
    o3d.visualization.draw_geometries(mesh_object)
    return

def save_bricks(bricks_, str_path, str_file=None):
    # str_file does not contain format extension, .npy

    if not os.path.exists(str_path):
        os.makedirs(str_path)

    str_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    if str_file is None:
        str_file = 'bricks_{}'.format(str_time)

    str_save = os.path.join(str_path, str_file + '.npy')
    np.save(str_save, bricks_)

    return str_file

def load_bricks(str_path, str_file):
    # str_file does not contain format extension, .npy

    bricks_ = np.load(os.path.join(str_path, str_file + '.npy'))
    bricks_ = bricks_[()]

    return bricks_
