from __future__ import annotations
from math import pi
from typing import List, TYPE_CHECKING, Literal
from math import cos, sin
from itertools import starmap
from operator import mul

if TYPE_CHECKING:
    from model.coordinate import Coordinate3D


class MatrixHelper:
    @staticmethod
    def degrees_to_radians(angle: float) -> float:
        return angle * (pi/180)

    @staticmethod
    def dot(vector: List[float], matrix: List[List[float]]) -> List[List[float]]:
        return [sum(starmap(mul, zip(vector, col))) for col in zip(*matrix)]

    @staticmethod
    def cross(vector:List[float], vector2:List[float]) -> List[float]:
        dimension = len(vector)
        result = []
        for i in range(dimension):
            result.append(0)
            for j in range(dimension):
                if j != i:
                    for k in range(dimension):
                        if k != i:
                            if k > j:
                                result[i] += vector[j] * vector2[k]
                            elif k < j:
                                result[i] -= vector[j] * vector2[k]
        return result


    @staticmethod
    def mul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        c = []
        for i in range(0, len(a)):
            temp = []
            for j in range(0, len(b[0])):
                s = 0
                for k in range(0, len(a[0])):
                    s += a[i][k] * b[k][j]
                temp.append(s)
            c.append(temp)
        return c

    @staticmethod
    # Receives a vector that represents the translation, returns a matrix to apply that operation
    def translation_matrix(v: Coordinate3D) -> List[List[float]]:
        return [
            [1,   0,   0,  0],
            [0,   1,   0,  0],
            [0,   0,   1,  0],
            [v.x, v.y, v.z, 1]
        ]

    @staticmethod
    def scale_matrix(s: Coordinate3D) -> List[List[float]]:
        return [
            [s.x, 0,  0, 0],
            [0,  s.y, 0, 0],
            [0,  0, s.z, 0],
            [0,  0, 0,  1]
        ]

    # Receives the angle in degrees and creates the rotation matrix
    @staticmethod
    def rotation_matrix_x(angle: float) -> List[List[float]]:
        a = MatrixHelper.degrees_to_radians(angle)
        return [
            [1, 0, 0, 0],
            [0, cos(a), sin(a), 0],
            [0, -sin(a), cos(a), 0],
            [0, 0, 0, 1],
        ]

    @staticmethod
    def rotation_matrix_y(angle: float) -> List[List[float]]:
        a = MatrixHelper.degrees_to_radians(angle)
        return [
            [cos(a), 0, -(sin(a)), 0],
            [0, 1, 0, 0],
            [sin(a), 0, cos(a), 0],
            [0, 0, 0, 1],
        ]

    @staticmethod
    def rotation_matrix_z(angle: float) -> List[List[float]]:
        a = MatrixHelper.degrees_to_radians(angle)
        return [
            [cos(a), sin(a), 0, 0],
            [-sin(a), cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]

    @staticmethod
    def get_rotation_matrix(angle, axis: Literal['x', 'y', 'z']):
        if axis == 'x':
            return MatrixHelper.rotation_matrix_x(angle)
        elif axis == 'y':
            return MatrixHelper.rotation_matrix_y(angle)
        elif axis == 'z':
            return MatrixHelper.rotation_matrix_z(angle)
        else:
            raise Exception('kjgnrksjgn')
7