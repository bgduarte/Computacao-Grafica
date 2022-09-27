from typing import List
from model.coordinate import Coordinate2D
from model.displayable import Displayable

class Wireframe(Displayable):

    def _constraint_check(self):
        if len(self._coordinates) < 3:
            raise Exception("A wireframe have a least 3 coordinates")

    def _get_drawable_lines(self):
        lines = []
        size = (len(self._coordinates))
        for i in range(size):
            line = [self._coordinates[i], self._coordinates[(i+1)%size]]
            lines.append(line)
        return lines

    def _get_drawable_points(self):
        return self._coordinates
