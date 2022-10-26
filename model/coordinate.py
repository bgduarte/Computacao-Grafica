import math
from typing import List
from utils.matrix_helper import MatrixHelper
import numbers
from abc import abstractmethod


class Coordinate(List):
    limit_size = -1

    def __init__(self, x):
        super().__init__(x[0:self.limit_size])


    def __neg__(self):
        return type(self)([-e for e in self])

    def __add__(self, other):
        result = []
        for i in range(len(self)):
            result.append(self[i] + other[i])
        return type(self)(result)

    def __sub__(self, other):
        return self.__add__(-other)

    @property
    def length(self):
        result = 0
        for e in self:
            result += e*e
        return math.sqrt(result)

    def __mul__(self, other):
        if not isinstance(other, numbers.Number):
            raise Exception(f'Coordinate can only be multiplied by numbers, not by {type(other)}')
        return type(self)([e*other for e in self])

    def normalize(self):
        return type(self)([e/self.length for e in self])

    @staticmethod
    def distance(coord1, coord2) -> float:
        return (coord2-coord1).length

    @classmethod
    def up(cls):
        up =  []
        for i in range(cls.limit_size):
            up.append(0 if i != 1 else 1)

        return cls(up)

        # Transforms coordinate based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        vector = self.copy()
        vector.append(float(1))
        for t in transformations_matrices:
            vector = MatrixHelper.dot(vector, t)

        # Defines the new coordinates, by removing the third element in the matrix
        for i in range(len(self)):
            self[i] = vector[i]

    def rotate(self, angle):
        self.transform([MatrixHelper.rotation_matrix(angle)])

    def translate(self, movement_vector):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])


class Coordinate2D(Coordinate):
    limit_size = 2
    def __init__(self, x, y: float = None):
        if isinstance(x, list):
            super(Coordinate2D, self).__init__(x)
        else:
            super(Coordinate2D, self).__init__([x, y])

    @property
    def x(self):
        return self.__getitem__(0)

    @x.setter
    def x(self, value: float):
        self[0] = value

    @property
    def y(self):
        return self.__getitem__(1)

    @y.setter
    def y(self, value: float):
        self[1] = value


class Coordinate3D(Coordinate2D):
    limit_size = 3
    
    def __init__(self, x, y: float = None, z: float = None):
        if isinstance(x, list):
            super(Coordinate3D, self).__init__(x)
        else:
            super(Coordinate3D, self).__init__([x, y, z])

    @property
    def z(self):
        return self.__getitem__(2)

    @z.setter
    def z(self, value: float):
        self[2] = value