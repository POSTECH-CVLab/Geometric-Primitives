import numpy as np
import copy

from geometric_primitives import brick
from geometric_primitives import rules
from geometric_primitives import utils_brick
from geometric_primitives import utils_bricks
from geometric_primitives import utils_validation


class Bricks:
    def __init__(self, max_bricks, brick_type, debug=False):
        self.max_bricks = max_bricks
        self.debug = debug
        self.bricks = []

        self.node_matrix = None
        self.adjacency_matrix = None
        self.edge_matrix = None
        self.degree_matrix = None

        self.brick_type = brick_type
        assert self.brick_type in ['mixed'] + copy.deepcopy(rules.ALL_TYPES)

    def get_bricks(self):
        return self.bricks

    def get_length(self):
        return len(self.bricks)

    def get_node_matrix(self):
        return self.node_matrix

    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    def get_edge_matrix(self):
        return self.edge_matrix

    def get_degree_matrix(self):
        return self.degree_matrix

    def get_vertices(self):
        bricks_ = self.get_bricks()

        vertices_all = []
        for brick_ in bricks_:
            vertices_all += list(brick_.get_vertices())

        vertices_all = np.array(vertices_all)
        vertices_all = np.unique(vertices_all, axis=0)

        return vertices_all

    def _validate_overlap_brick(self, brick_1, list_bricks):
        vert_1 = brick_1.get_vertices()
        min_max_1 = utils_validation.get_min_max_3d(vert_1)

        results = []

        for brick_2 in list_bricks:
            vert_2 = brick_2.get_vertices()
            min_max_2 = utils_validation.get_min_max_3d(vert_2)

            res = utils_validation.check_overlap_3d(min_max_1, min_max_2)

            results.append(res)

        if np.any(results):
            raise ValueError('Occur a brick overlap.')

    def _validate_contact_brick(self, brick_1):
        list_bricks = self.get_bricks()

        if len(list_bricks) == 0:
            return

        pos_1 = brick_1.get_position()
        vert_1 = brick_1.get_vertices()
        min_max_1 = utils_validation.get_min_max_3d(vert_1)

        results = []

        for brick_2 in list_bricks:
            pos_2 = brick_2.get_position()
            vert_2 = brick_2.get_vertices()

            res_ = 0

            if np.abs(pos_1[2] - pos_2[2]) == 1:
                min_max_2 = utils_validation.get_min_max_3d(vert_2)

                res = utils_validation.check_overlap_2d(min_max_1[:2], min_max_2[:2])
                if res: 
                    res_ = 1

            results.append(res_)

        if int(np.sum(results)) == 0:
            raise ValueError('Do not have a contact.')

    def _validate_origin_brick(self, brick_):
        pos = brick_.get_position()
        if pos[2] < 0:
            raise ValueError('Brick is located under an origin surface.')

    def _validate_overlap(self):
        len_bricks = self.get_length()
        list_bricks = self.get_bricks()

        for ind_1, brick_1 in enumerate(list_bricks):
            self._validate_overlap_brick(brick_1, list_bricks[ind_1+1:])

    def _validate_contact(self):
        len_bricks = self.get_length()
        list_bricks = self.get_bricks()

        if len_bricks <= 1:
            return
        else:
            reached = np.zeros(len_bricks)

            A = self.get_adjacency_matrix()
            A = np.triu(A)

            def check_contacts(ind_):
                for ind_elem, elem in enumerate(A[ind_]):
                    if elem == 1:
                        reached[ind_elem] = 1
                        check_contacts(ind_elem)

            check_contacts(0)
            reached[0] = 1

            if not np.sum(reached) == len_bricks:
                raise ValueError('Do not have a contact.')

    def _validate_origin(self):
        X = self.get_node_matrix()
        if X is not None and np.any(X[:, 3] < 0):
            raise ValueError('Brick is located under an origin surface.')

    def _validate_length(self):
        if self.get_length() > self.max_bricks:
            raise ValueError('Exceed the maximum number of bricks.')

    def validate_brick(self, brick_):
        self._validate_overlap_brick(brick_, self.get_bricks())
        self._validate_contact_brick(brick_)
        self._validate_origin_brick(brick_)

    def _validate_bricks(self, bricks_):
        bricks_validated = []
        for brick_ in bricks_:
            cur_bricks = copy.deepcopy(self)

            try:
                cur_bricks.add(brick_)
                bricks_validated.append(brick_)
            except Exception as e:
                pass

        return bricks_validated

    def validate_all(self):
        self._validate_overlap()
        self._validate_contact()
        self._validate_origin()
        self._validate_length()

    def add(self, brick_):
        if self.get_length() < self.max_bricks:
            self.validate_brick(brick_)
            self.bricks.append(brick_)

            _ = self.compute_node_matrix()
            _, _, _ = self.compute_adjacency_edge_degree_matrices()
        else:
            raise ValueError('Exceed the maximum number of bricks.')

    def get_possible_contacts(self, next_type=None):
        assert isinstance(next_type, (type(None), int))

        list_bricks = self.get_bricks()
        new_bricks = []

        for brick_ in list_bricks:
            cur_size = copy.deepcopy(brick_).get_size()
            cur_type = utils_brick.get_type(cur_size[0], cur_size[1], cur_size[2])

            if self.brick_type == 'mixed' and next_type is None:
                ind_rules = np.random.choice(len(rules.ALL_TYPES))
                next_type = rules.ALL_TYPES[ind_rules]
            elif self.brick_type == 'mixed' and next_type is not None:
                pass
            else:
                next_type = self.brick_type

            _, rules_, _ = utils_bricks.get_rules(cur_type, next_type)
            size_upper, size_lower, height = utils_brick.get_size(next_type)

            cur_position = brick_.get_position()
            cur_direction = brick_.get_direction()

            for rule in rules_:
                translations = rule['translations']
                direction = rule['direction']
                
                for trans in translations:
                    # upper
                    new_brick = brick.Brick(size_upper=size_upper, size_lower=size_lower)
                    new_brick.set_position(cur_position + np.concatenate((np.array(trans), [new_brick.height])))
                    new_brick.set_direction((cur_direction + direction) % 2)
                    if new_brick.get_position()[2] >= 0:
                        new_bricks.append(new_brick)

                    # lower
                    new_brick = brick.Brick(size_upper=size_upper, size_lower=size_lower)
                    new_brick.set_position(cur_position + np.concatenate((np.array(trans), [-1 * new_brick.height])))
                    new_brick.set_direction((cur_direction + direction) % 2)
                    if new_brick.get_position()[2] >= 0:
                        new_bricks.append(new_brick)

        new_bricks = self._validate_bricks(new_bricks)
        
        return new_bricks

    def _sample_one(self, next_type=None):
        assert isinstance(next_type, (type(None), int))

        list_bricks = self.get_bricks()
        ind_brick = np.random.choice(self.get_length())
        brick_sampled = list_bricks[ind_brick]

        cur_size = copy.deepcopy(brick_sampled).get_size()
        cur_type = utils_brick.get_type(cur_size[0], cur_size[1], cur_size[2])

        cur_position = brick_sampled.get_position()
        cur_direction = brick_sampled.get_direction()

        if self.brick_type == 'mixed' and next_type is None:
            ind_rules = np.random.choice(len(rules.ALL_TYPES))
            next_type = rules.ALL_TYPES[ind_rules]
        elif self.brick_type == 'mixed' and next_type is not None:
            pass
        else:
            next_type = self.brick_type

        _, rules_, probs_rules_ = utils_bricks.get_rules(cur_type, next_type)
        size_upper, size_lower, height = utils_brick.get_size(next_type)

        ind_rule = np.random.choice(len(rules_), p=probs_rules_)
        cur_rule = rules_[ind_rule]

        translations = copy.deepcopy(cur_rule['translations'])
        direction = copy.deepcopy(cur_rule['direction'])

        ind_trans = np.random.choice(len(translations))
        trans = translations[ind_trans]

        if cur_direction == 1:
            angle = np.pi * 3.0 / 2.0
            trans = np.dot(np.array([
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)],
                ]), trans)

        upper_lower = np.random.choice(2) * 2.0 - 1.0

        new_brick = brick.Brick(size_upper=size_upper, size_lower=size_lower)
        new_brick.set_position(cur_position + np.concatenate((np.array(trans), [new_brick.height * upper_lower])))
        new_brick.set_direction((cur_direction + direction) % 2)

        new_brick = self._validate_bricks([new_brick])

        if len(new_brick) == 0:
            return None
        else:
            return new_brick[0]

    def sample(self, num_samples=None, next_type=None):
        if num_samples is None:
            num_samples = 1

        possible_bricks = []
        while len(possible_bricks) <= num_samples:
            brick_sampled = self._sample_one(next_type=next_type)

            if brick_sampled is not None and utils_validation.check_duplicate(possible_bricks, brick_sampled):
                possible_bricks.append(brick_sampled)

        return possible_bricks

    def get_connection_type(self, brick_1, brick_2):
        # brick_1 is a yardstick.
        diff_direction = (brick_2.get_direction() + brick_1.get_direction()) % 2
        diff_position = (brick_2.get_position() - brick_1.get_position())[:2]

        if brick_1.get_direction() == 1:
            # TODO: check this.
            angle = np.pi * 3.0 / 2.0
            diff_position = np.dot(np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)],
            ]), diff_position)

        list_rules, _, _ = utils_bricks.get_rules(brick_1.get_type(), brick_2.get_type())

        ind = None
        num_ind = 0
        for rule in list_rules:
            if diff_direction == rule[1][0] and np.all(np.abs(diff_position - np.array(rule[1][1])) < 1e-4):
                ind = rule[0]
                num_ind += 1

        if not num_ind == 1:
#            print(brick_1.get_direction(), brick_2.get_direction())
#            print(num_ind, diff_direction, diff_position)
            raise ValueError('Invalid connection type.')

        assert ind > 0
        return ind

    def compute_node_matrix(self):
        bricks_ = self.get_bricks()
        len_bricks = self.get_length()

        if len_bricks > 0:
            X = np.zeros((len_bricks, 5))

            if len_bricks > 1:
                X[:len_bricks-1, :] = self.get_node_matrix()

            cur_type = bricks_[-1].get_type()
            cur_pos = bricks_[-1].get_position()
            cur_dir = bricks_[-1].get_direction()

            X[len_bricks-1, :] = np.array([cur_type, cur_pos[0], cur_pos[1], cur_pos[2], cur_dir])

            self.node_matrix = X

            return X
        else:
            return self.get_node_matrix()

    def compute_adjacency_edge_degree_matrices(self):
        bricks_ = self.get_bricks()
        len_bricks = self.get_length()

        if len_bricks > 0:
            A = np.zeros((len_bricks, len_bricks))
            D = np.zeros((len_bricks, len_bricks))
            E = np.zeros((len_bricks, len_bricks))

            for ind_1, brick_1 in enumerate(bricks_):
                for ind_2, brick_2 in enumerate(bricks_):
                    if ind_1 == ind_2:
                        E[ind_1, ind_2] = -1
                        continue

                    pos_1 = brick_1.get_position()
                    pos_2 = brick_2.get_position()
                    vert_1 = brick_1.get_vertices()
                    vert_2 = brick_2.get_vertices()
                    min_max_1 = utils_validation.get_min_max_3d(vert_1)
                    min_max_2 = utils_validation.get_min_max_3d(vert_2)

                    if np.abs(pos_1[2] - pos_2[2]) == 1 and utils_validation.check_overlap_2d(min_max_1[:2], min_max_2[:2]) == 1:
                        conn = self.get_connection_type(bricks_[ind_1], bricks_[ind_2])

                        A[ind_1, ind_2] = 1
                        D[ind_1, ind_1] += 1
                        E[ind_1, ind_2] = conn
                    else:
                        E[ind_1, ind_2] = 0

            self.adjacency_matrix = A
            self.edge_matrix = E
            self.degree_matrix = D

            assert np.all((E > 0) == A)
            assert np.all(np.sum(A, axis=0) == np.sum(D, axis=0))
            assert np.all(np.sum(A, axis=1) == np.sum(D, axis=1))

            return A, E, D
        else:
            return self.get_adjacency_matrix(), self.get_edge_matrix(), self.get_degree_matrix()

    def get_graph(self):
        X = self.get_node_matrix()
        A = self.get_adjacency_matrix()
        E = self.get_edge_matrix()
        D = self.get_degree_matrix()

        return X, A, E, D
