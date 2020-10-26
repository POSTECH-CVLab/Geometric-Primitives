import pytest
import numpy as np

from geometric_primitives import brick

def test_create_brick():
    brick_ = brick.Brick()

    assert brick_.get_position() == None
    assert brick_.get_direction() == 0
    assert brick_.get_vertices() == None

    size_upper, size_lower, height = brick_.get_size()
    assert np.all(size_upper == [2, 4])
    assert np.all(size_lower == [2, 4])
    assert height == 1

def test_set_position():
    brick_ = brick.Brick()

    assert brick_.get_position() == None

    pos = [1, 2, 1]
    brick_.set_position(pos)
    assert np.all(brick_.get_position() == np.array(pos))

    vertices = np.array([
        [2.0, 4.0, 1.0],
        [2.0, 0.0, 1.0],
        [0.0, 4.0, 1.0],
        [0.0, 0.0, 1.0],
        [2.0, 4.0, 2.0],
        [2.0, 0.0, 2.0],
        [0.0, 4.0, 2.0],
        [0.0, 0.0, 2.0],
    ])
    print(brick_.get_vertices())
    assert np.all(brick_.get_vertices() == vertices)

def test_set_direction():
    brick_ = brick.Brick()

    assert brick_.get_position() == None

    pos = [1, 2, 1]
    brick_.set_position(pos)
    brick_.set_direction(1)
    assert np.all(brick_.get_position() == np.array(pos))

    vertices = np.array([
        [3.0, 3.0, 1.0],
        [3.0, 1.0, 1.0],
        [-1.0, 3.0, 1.0],
        [-1.0, 1.0, 1.0],
        [3.0, 3.0, 2.0],
        [3.0, 1.0, 2.0],
        [-1.0, 3.0, 2.0],
        [-1.0, 1.0, 2.0],
    ])
    print(brick_.get_vertices())
    assert np.all(brick_.get_vertices() == vertices)

def test_set_configuration():
    brick_ = brick.Brick()

    assert brick_.get_position() == None

    pos = [5, -2, 3]
    direc = 1
    config = {
        'position': pos,
        'direction': direc
    }

    brick_.set_configuration(config)
    assert np.all(brick_.get_position() == np.array(pos))

    vertices = np.array([
        [7.0, -1.0, 3.0],
        [7.0, -3.0, 3.0],
        [3.0, -1.0, 3.0],
        [3.0, -3.0, 3.0],
        [7.0, -1.0, 4.0],
        [7.0, -3.0, 4.0],
        [3.0, -1.0, 4.0],
        [3.0, -3.0, 4.0],
    ])
    print(brick_.get_vertices())
    assert np.all(brick_.get_vertices() == vertices)
