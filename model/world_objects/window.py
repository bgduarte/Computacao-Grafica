import math
from typing import List, Literal, Tuple, Union

from model.world_object import WorldObject
from model.coordinate import Coordinate2D
from model.world_objects.displayable import Displayable
from utils.clipper import Clipper


class Window(WorldObject):
    __clipping_method: Literal['liang_barsky']

    def __init__(self, top_left: Coordinate2D, top_right: Coordinate2D, bottom_left: Coordinate2D):
        self.__clipping_method = 'liang_barsky'
        super().__init__(coordinates=[top_left, top_right, bottom_left])

    def clip_line(self, line: List[Coordinate2D]) -> Union[Tuple[Coordinate2D, Coordinate2D], None]:
        if self.__clipping_method == 'liang_barsky':
            return Clipper.liang_barsky_clip(line[0], line[1])

    def clip_point(self, point: Coordinate2D) -> Union[Coordinate2D, None]:
        return point if point.x >= -1 and point.x <= 1 and point.y >= -1 and point.y <= 1 else None

    # def coord_to_window_system(self, displayables: List[Displayable]):
    #     displayables_copy = displayables.copy()
    #     lines = []
    #     points = []
    #     for displayable in displayables_copy:
    #         drawable = displayable.get_drawable()
    #         for p in drawable.points:
    #             new_point = self._transform_coord(p)
    #             new_point = self.clip_point(new_point)
    #             if new_point:
    #                 points.append(new_point)
    #         for line in drawable.lines:
    #             transformed_line = [
    #                 self._transform_coord(line[0]),
    #                 self._transform_coord(line[1])
    #             ]
    #             clipped_line = self.clip_line(transformed_line)
    #             if clipped_line:
    #                 lines.append(clipped_line)
    #     return Displayable.Drawable(lines=lines, points=points, color='#000')
    def set_clipping_method(self, method: Literal['liang_barsky']):
        self.__clipping_method = method

    def coord_to_window_system(self, drawable: Displayable.Drawable) -> Displayable.Drawable:
        points = [self._transform_coord(p) for p in drawable.points]
        lines = [[self._transform_coord(line[0]), self._transform_coord(line[1])] for line in drawable.lines]
        return Displayable.Drawable(lines, points, drawable.color)


    def clip(self, drawable: Displayable.Drawable) -> Displayable.Drawable:
        # applies clipping and appends if clipped is not null
        points = [clipped_p for p in drawable.points if (clipped_p := self.clip_point(p)) is not None]
        lines = [clipped_l for line in drawable.lines if (clipped_l := self.clip_line(line)) is not None]
        return Displayable.Drawable(lines, points, drawable.color)

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

    def move_left(self, amount):
        movement_vector = -(self.top_right - self.top_left).normalize() * amount * self.width
        self.translate(movement_vector)

    def move_right(self, amount):
        movement_vector = (self.top_right - self.top_left).normalize() * amount * self.width
        self.translate(movement_vector)

    def move_up(self, amount):
        movement_vector = -(self.bottom_left - self.top_left).normalize() * amount * self.height
        self.translate(movement_vector)

    def move_down(self, amount):
        movement_vector = (self.bottom_left - self.top_left).normalize() * amount * self.height
        self.translate(movement_vector)

    # Returns the angle between the window up and the y-axis
    def _get_angle(self):
        y_axis: Coordinate2D = Coordinate2D.up()
        w_up: Coordinate2D = self.top_left-self.bottom_left
        # TODO: change this approach
        return math.degrees(math.atan2(w_up.y*y_axis.x - w_up.x*y_axis.y, w_up.x*y_axis.x + w_up.y*y_axis.y))

    def _transform_coord(self, coord: Coordinate2D):
        new_point = Coordinate2D(coord.copy())
        new_point.translate(-self.get_window_center())
        new_point.rotate(self._get_angle())
        new_point.x = new_point.x / (self.width * 0.5)
        new_point.y = new_point.y / (self.height * 0.5)
        return new_point

    def get_window_center(self) -> Coordinate2D:
        center = self.bottom_left + ((self.top_left-self.bottom_left)*0.5)
        return center + ((self.top_right - self.top_left)*0.5)

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")
