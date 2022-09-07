from typing import List
from aux import Coordinate2D
from displayable import Displayable

class Wireframe(Displayable):
    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        super().__init__(name, coordinates)

    def __contraint_check(self):
        if len(self.__cordinates) < 3:
            raise Exception("A wireframe have a least 3 coordinates")