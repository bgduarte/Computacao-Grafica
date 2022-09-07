from typing import List, Tuple
from displayable import Displayable
from aux import Coordinate2D

class Dot(Displayable):
    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        super().__init__(name, coordinates)

    def __contraint_check(self):
        if len(self.get_coordinates()) != 1:
            raise Exception("A dot must have exactly one coordinate")

