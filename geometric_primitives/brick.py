import numpy as np


class Brick:
    # TODO: position is on integer grid, it makes vertex coordinates to real numbers.
    def __init__(self, size_upper=[2, 4], size_lower=[2, 4], height=1):
        self.size_upper = np.array(size_upper)
        self.size_lower = np.array(size_lower)
        self.height = 1
        self.position = None
        self.direction = 0
        self.vertices = None

        assert np.all(self.size_upper == self.size_lower)

    def get_size(self):
        return self.size_upper, self.size_lower, self.height

    def _set_vertices(self):
        assert self.position is not None

        vertices = []
        signs = np.array([
            [1.0, 1.0],
            [1.0, -1.0],
            [-1.0, 1.0],
            [-1.0, -1.0],
        ])

        for elem in signs:
            size_lower = self.size_lower
            if self.get_direction() == 1:
                # TODO: make it smarter
                size_lower = np.array([size_lower[1], size_lower[0]])

            trans = elem * size_lower / 2
            trans = np.concatenate((trans, np.array([0.0])))
            vertices.append(self.get_position() + trans)

        for elem in signs:
            size_upper = self.size_upper
            if self.get_direction() == 1:
                size_upper = np.array([size_upper[1], size_upper[0]])

            trans = elem * size_upper / 2
            trans = np.concatenate((trans, np.array([float(self.height)])))
            vertices.append(self.get_position() + trans)

        vertices = np.array(vertices)
        self.vertices = np.array(vertices)

        assert len(self.vertices) == 8

    def get_vertices(self):
        return self.vertices

    def set_position(self, pos):
        assert len(pos) == 3

        self.position = np.array(pos)
        self._set_vertices()

    def get_position(self):
        return self.position

    def set_direction(self, direc):
        assert direc in [0, 1]

        self.direction = direc
        self._set_vertices()

    def get_direction(self):
        return self.direction

    def set_configuration(self, pos_direc):
        assert isinstance(pos_direc, dict)

        pos = pos_direc['position']
        direc = pos_direc['direction']

        self.set_position(pos)
        self.set_direction(direc)

    def get_position_direction(self):
        return np.concatenate((
            self.get_position(),
            np.array([self.get_direction()])
        ))
