from typing import List
from aux import Coordinate2D
from displayable import Displayable


class Line(Displayable):
    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        super().__init__(name, coordinates)

    def __contraint_check(self):
        if len(self.get_coordinates()) != 2:
            raise Exception("A line must have exactly two coordinates")
