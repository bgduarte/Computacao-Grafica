from model.coordinate import Coordinate, Coordinate3D
from typing import List, Literal
from utils.matrix_helper import MatrixHelper
from abc import ABC, abstractmethod


class WorldObject(ABC):
    _coordinates: List[Coordinate]

    def __init__(self, coordinates: List[Coordinate]) -> None:
        self._coordinates = coordinates
        self._constraint_check()

    def get_coordinates(self) -> List[Coordinate]:
        return self._coordinates

    @abstractmethod
    def _constraint_check(self):
        pass

    def rotate(self, angle, axis: Literal['x', 'y', 'z']='z'):
        self.transform([MatrixHelper.get_rotation_matrix(angle, axis)])

    def translate(self, movement_vector: Coordinate):
        self.transform([MatrixHelper.translation_matrix(Coordinate3D(movement_vector))])

    def scale(self, scale_vector: Coordinate3D):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])

    # Transforms polygon based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        for coord in self._coordinates:
            coord.transform(transformations_matrices)

    def get_center_coord(self) -> Coordinate3D:
        dimensions = self._coordinates[0].limit_size
        axis_sum = [0 for i in range(dimensions)]
        for coord in self._coordinates:
            for i in range(dimensions):
                axis_sum[i] += coord[i]

        l = float(len(self._coordinates))
        return Coordinate3D(Coordinate3D(axis_sum)*(1/l))

    def rotate_around_self(self, angle: float, axis: Literal['x', 'y', 'z'] = 'y'): # angle in degrees
        self.rotate_around_point(angle=angle, point=self.get_center_coord(), axis=axis)

    def scale_around_self(self, scale_vector: Coordinate3D):
        center_coord = self.get_center_coord()
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-center_coord),
            # Scale
            MatrixHelper.scale_matrix(scale_vector),
            # Translate back to the same position
            MatrixHelper.translation_matrix(center_coord)
        ])

    def rotate_around_point(self, angle: float, point: Coordinate3D, axis: Literal['x', 'y', 'z']): # angle in degrees
        translation_vector = point
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-translation_vector),
            # Rotates
            MatrixHelper.get_rotation_matrix(angle, axis),
            # Translate back to the same position
            MatrixHelper.translation_matrix(translation_vector)
        ])


