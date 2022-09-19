from math import pi
from typing import List
from math import cos, sin
from itertools import starmap
from operator import mul


class MatrixHelper:
    @staticmethod
    def degrees_to_radians(angle: float) -> float:
        return angle * (pi/180)

    @staticmethod
    def dot(vector: List[float], matrix: List[List[float]]) -> List[List[float]]:
        return [sum(starmap(mul, zip(vector, col))) for col in zip(*matrix)]

    @staticmethod
    # Receives a vector that represents the translation, returns a matrix to apply that operation
    def translation_matrix(v) -> List[List[float]]:
        return [
            [1,   0,   0],
            [0,   1,   0],
            [v.x, v.y, 1]
        ]

    @staticmethod
    def scale_matrix(s) -> List[List[float]]:
        return [
            [s.x, 0,  0],
            [0,  s.y, 0],
            [0,  0,   1]
        ]

    # Receives the angle in degrees and creates the rotation matrix
    @staticmethod
    def rotation_matrix(angle: float) -> List[List[float]]:
        a = MatrixHelper.degrees_to_radians(angle)
        return [
            [cos(a), -sin(a), 0],
            [sin(a),  cos(a), 0],
            [  0,       0,    1]
        ]