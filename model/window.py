import math

from model.world_object import WorldObject
from model.coordinate import Coordinate2D


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
        y_axis: Coordinate2D = Coordinate2D.up()
        w_up: Coordinate2D = self.top_left-self.bottom_left
        return math.degrees(math.atan2(w_up.y*y_axis.x - w_up.x*y_axis.y, w_up.x*y_axis.x + w_up.y*y_axis.y))

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")
