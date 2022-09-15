import numpy as np


class TransformHelper:

    @staticmethod
    # Receives a vector that represents the translation, returns a matrix to apply that operation
    def translation_matrix(v) -> list:
        return [
            [1,   0,   0],
            [0,   1,   0],
            [v.x, v.y, 1]
        ]

    @staticmethod
    def scale_matrix(s ):
        return [
            [s.x, 0,  0],
            [0,  s.y, 0],
            [0,  0,   1]
        ]

    # Receives the angle in degrees and creates the rotation matrix
    @staticmethod
    def rotation_matrix(angle: float):
        a = np.deg2rad(angle)
        return [
            [np.cos(a), -np.sin(a), 0],
            [np.sin(a),  np.cos(a), 0],
            [0,          0,         1]
        ]