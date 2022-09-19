from typing import List
from model.coordinate import Coordinate2D
from utils.matrix_helper import  MatrixHelper
# Abstract class
class Displayable:
    # private attributes
    __name: str
    __coordinates: List[Coordinate2D]

    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        self.__name = name
        self.__coordinates = coordinates
        self.__constraint_check()
        if not issubclass(type(self), Displayable):
            raise Exception("Displayable is an abstract class, it is not supposed to be instantiated")

    # public methods
    def add_coordinate(self, x, y):
        self.__coordinates.append(Coordinate2D(x, y))
        self.__constraint_check()

    def get_coordinates(self) -> List[Coordinate2D]:
        return self.__coordinates
    
    def get_name(self) -> str:
        return self.__name

    def __constraint_check(self):
        pass

    def rotate(self, angle):
        self.transform([MatrixHelper.rotation_matrix(angle)])

    def translate(self, movement_vector: Coordinate2D):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector: Coordinate2D):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])

    # Transforms polygon based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        print(f'beforeCoord:{self.__coordinates}')
        for coord in self.__coordinates:
            coord.transform(transformations_matrices=transformations_matrices)
        print(f'afterCoord:{self.__coordinates}')

    def get_center_coord(self):
        sum_x = 0
        sum_y = 0
        for coord in self.__coordinates:
            sum_x += coord.x
            sum_y += coord.y

        l = float(len(self.__coordinates))
        return Coordinate2D(sum_x/l, sum_y/l)

    def rotate_around_self(self, angle: float): # angle in degrees
        self.rotate_around_point(angle=angle, point=self.get_center_coord())

    def scale_around_self(self, scale_vector: Coordinate2D):
        center_coord = self.get_center_coord()
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-center_coord),  # TODO: investigate translation backwards
            # Scale
            MatrixHelper.scale_matrix(scale_vector),
            # Translate back to the same position
            MatrixHelper.translation_matrix(center_coord)
        ])

    def rotate_around_point(self, angle: float, point: Coordinate2D): # angle in degrees
        translation_vector = point
        print(MatrixHelper.translation_matrix(translation_vector))
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-translation_vector),
            # Rotates
            MatrixHelper.rotation_matrix(angle),
            # Translate back to the same position
            MatrixHelper.translation_matrix(translation_vector)
        ])
