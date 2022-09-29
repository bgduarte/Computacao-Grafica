from model.world_object import WorldObject
from model.coordinate import Coordinate2D
from typing import List


class Window(WorldObject):
    # angle between window up vector and the y-axis
    _angle: float

    def __init__(self, coordinates: List[Coordinate2D], angle: float=None):
        super().__init__(coordinates=coordinates)
        self._angle = angle if angle else 0

    def _constraint_check(self):
        if len(self._coordinates) != 2:
            raise Exception("A window must have exactly two coordinates")




