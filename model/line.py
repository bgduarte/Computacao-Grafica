from typing import List
from model.coordinate import Coordinate2D
from model.displayable import Displayable


class Line(Displayable):

    def _constraint_check(self):
        if len(self._coordinates) != 2:
            raise Exception("A line must have exactly two coordinates")
    def _get_drawable_lines(self):
        return [self._coordinates]

    def _get__drawable_points(self):
        return self._coordinates
