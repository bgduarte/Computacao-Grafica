from typing import List
import numpy as np
from model.transform_helper import TransformHelper


class Coordinate2D(List):

    def __init__(self, x, y: float):
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

    def __neg__(self):
        return Coordinate2D(-self.x, -self.y)

    def __add__(self, other):
        return Coordinate2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    # Transforms coordinate based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        matrix = self.copy()
        matrix.append(float(1))
        for t in transformations_matrices:
            matrix = np.matmul(matrix, t)

        # Defines the new coordinates, by removing the third element in the matrix
        self.x = matrix[0]
        self.y = matrix[1]

    def rotate(self, angle):
        self.transform([TransformHelper.rotation_matrix(angle)])

    def translate(self, movement_vector):
        self.transform([TransformHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector):
        self.transform([TransformHelper.scale_matrix(scale_vector)])
