from typing import List
from model.coordinate import Coordinate2D
from model.displayable import Displayable


class Line(Displayable):

    def __constraint_check(self):
        if len(self.__coordinates) != 2:
            raise Exception("A line must have exactly two coordinates")
