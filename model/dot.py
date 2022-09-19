from typing import List, Tuple
from model.displayable import Displayable
from model.coordinate import Coordinate2D

class Dot(Displayable):
    def __constraint_check(self):
        if len(self.__coordinates) != 1:
            raise Exception("A dot must have exactly one coordinate")