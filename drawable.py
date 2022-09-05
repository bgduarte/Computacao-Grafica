from enum import Enum
from typing import List
from aux import Coordinate2D

class DrawableType(Enum):
    dot = 1
    line = 2
    wireframe = 3
    
class Drawable:
    # private attributes
    __name: str
    __type: DrawableType
    __coordinates: List[Coordinate2D]

    def __init__(self, name: str, drawable_type: DrawableType) -> None:
        self.__name = name
        self.__type = drawable_type

    # private methods
    def __can_add_coordinates(self) -> bool:
        if self.__type == DrawableType.dot:
            return len(self.__coordinates) < 1
        elif self.__type == DrawableType.line:
            return len(self.__coordinates) < 2
        elif self.__type == DrawableType.wireframe:
            return True

    # public methods
    def add_coordinates(self, x, y):
        if self.__can_add_coordinates():
            self.__coordinates.append(Coordinate2D(x, y))
        else:
            raise Exception("Too many coordinates for this type")
        return self

    def get_coordinates(self) -> List[Coordinate2D]:
        return self.__coordinates
