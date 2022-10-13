from model.world_objects.displayable import Displayable
from abc import ABC, abstractmethod

class Curve(Displayable):
    _resolution: int = 10  # number of lines that will be drawn per curve
    pass

    def _constraint_check(self):
        pass

    def _get_drawable_points(self):
        pass

    def _get_drawable_lines(self):
        pass

    @abstractmethod
    def _get_method_matrix(self):
        pass