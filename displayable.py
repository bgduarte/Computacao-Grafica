from typing import List, Tuple
from aux import Coordinate2D

class Displayable:
    # private attributes
    __name: str
    __coordinates: List[Coordinate2D]

    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        self.__name = name
        self.__coordinates = coordinates
        self.__contraint_check()
        if not issubclass(type(self), Displayable):
            raise Exception("Displayable is a base class, it is no supposed to be instantiated")

    # public methods
    def add_coordinate(self, x, y):
        self.__coordinates.append(Coordinate2D(x, y))
        self.__contraint_check()

    def get_coordinates(self) -> List[Coordinate2D]:
        return self.__coordinates

    def __contraint_check(self):
        pass