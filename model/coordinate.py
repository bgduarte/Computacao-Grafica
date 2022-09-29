import math
from typing import List
from utils.matrix_helper import MatrixHelper
import numbers


class Coordinate2D(List):

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

    @property
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def __neg__(self):
        return Coordinate2D(-self.x, -self.y)

    def __add__(self, other):
        return Coordinate2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if not isinstance(other, numbers.Number):
            raise Exception(f'Coordinate can only be multiplied by numbers, not by {type(other)}')
        return Coordinate2D(self.x*other, self.y*other)

    @staticmethod
    def distance(coord1, coord2):
        return (coord2-coord1).length

    # Transforms coordinate based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        vector = self.copy()
        vector.append(float(1))
        for t in transformations_matrices:
            vector = MatrixHelper.dot(vector, t)

        # Defines the new coordinates, by removing the third element in the matrix
        self.x = vector[0]
        self.y = vector[1]

    def rotate(self, angle):
        self.transform([MatrixHelper.rotation_matrix(angle)])

    def translate(self, movement_vector):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])
