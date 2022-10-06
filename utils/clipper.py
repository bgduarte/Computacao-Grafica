from typing import Tuple, Union
from model.coordinate import Coordinate2D

class Clipper:
    @staticmethod
    def _parametrize_liang_barsky(p, q):
        t1, t2 = 0, 1
        if p == 0: # parallel
            if q < 0:
                t1 = t2 + 1
        elif p < 0: # entering
            t1 = max(0, q/p)
        else: # exiting
            t2 = min(1, q/p)

        return t1, t2


    @staticmethod
    def liang_barsky_clip(point1: Coordinate2D, point2: Coordinate2D, 
            w_min: Coordinate2D = Coordinate2D(-1, -1), 
            w_max: Coordinate2D = Coordinate2D(1, 1)) -> Union[Tuple[Coordinate2D, Coordinate2D], None]:

        p1, q1 = -(point2.x - point1.x), point1.x - w_min.x # left
        p2, q2 = point2.x - point1.x, w_max.x - point1.x # right
        p3, q3 = -(point2.y - point1.y), point1.y - w_min.y # bottom
        p4, q4 = (point2.y - point1.y), w_max.y - point1.y # top

        ps = [p1, p2, p3, p4]
        qs = [q1, q2, q3, q4]
        x1, x2 = point1.x, point2.x
        y1, y2 = point1.y, point2.y

        for i in range(len(ps)):
            t1, t2 = Clipper._parametrize_liang_barsky(ps[i], qs[i])
            if t1 > t2:
                return None
            x1 = x1 + t1*(x2 - x1)
            x2 = x1 + t2*(x2 - x1)
            y1 = y1 + t1 * (y2 - y1)
            y2 = y1 + t2 * (y2 - y1)

        return Coordinate2D(x1, y1), Coordinate2D(x2, y2)
