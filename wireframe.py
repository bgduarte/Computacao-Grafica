from enum import Enum


class DrawableType(Enum):
    dot = 1
    line = 2
    wireframe = 3
    

class Drawable:
    # private attributes
    __name: str
    __drawable_type: DrawableType
    __coordinates: list

    def __init__(self, name: str, drawable_type: DrawableType) -> None:
        self.__name = name
        self.__drawable_type = drawable_type

    # private methods
    def __can_add_coordinates(self) -> bool:
        if self.__drawable_type == DrawableType.dot:
            return len(self.__coordinates) < 1
        elif self.__drawable_type == DrawableType.line:
            return len(self.__coordinates) < 2
        elif self.__drawable_type == DrawableType.wireframe:
            return True

    # public methods
    def add_coordinates(self, x, y):
        if self.__can_add_coordinates():
            self.__coordinates.append((x, y))
        else:
            raise Exception("Too many coordinates for this type")
        return self

    def get_coordinates(self) -> list:
        return self.__coordinates
