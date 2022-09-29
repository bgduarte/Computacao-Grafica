from model.world_object import WorldObject
from model.coordinate import Coordinate2D
from typing import List


class Window(WorldObject):

    def __init__(self, top_left: Coordinate2D, top_right: Coordinate2D, bottom_left: Coordinate2D):
        super().__init__(coordinates=[top_left, top_right, bottom_left])

    @property
    def top_left(self) -> Coordinate2D:
        return self._coordinates[0]

    @property
    def top_right(self) -> Coordinate2D:
        return self._coordinates[1]

    @property
    def bottom_left(self) -> Coordinate2D:
        return self._coordinates[2]

    @property
    def height(self) -> float:
        return Coordinate2D.distance(self.top_left, self.bottom_left)

    @property
    def width(self) -> float:
        return Coordinate2D.distance(self.top_left, self.top_right)

    # Returns the angle between the window up and the y-axis
    def _get_angle(self):
        pass

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")

