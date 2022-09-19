from typing import List
from model.coordinate import Coordinate2D
from model.displayable import Displayable

class Wireframe(Displayable):
    def __constraint_check(self):
        if len(self.__coordinates) < 3:
            raise Exception("A wireframe have a least 3 coordinates")