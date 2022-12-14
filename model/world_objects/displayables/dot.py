from model.world_objects.displayable import Displayable

class Dot(Displayable):
    def _constraint_check(self):
        if len(self._coordinates) != 1:
            raise Exception("A dot must have exactly one coordinate")

    def _get_drawable_lines(self):
        return []

    def _get_drawable_points(self):
        return self._coordinates
