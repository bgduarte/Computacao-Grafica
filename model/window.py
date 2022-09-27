from model.world_object import WorldObject


class Window(WorldObject):

    def _constraint_check(self):
        if len(self._coordinates) != 2:
            raise Exception("A window must have exactly two coordinates")