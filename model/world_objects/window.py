import math
import numpy
from typing import List, Literal, Tuple, Union

from model.world_object import WorldObject
from model.coordinate import Coordinate2D, Coordinate3D
from model.world_objects.displayable import Displayable
from utils.clipper import Clipper
from utils.matrix_helper import MatrixHelper


class Window(WorldObject):
    __clipping_method: Literal['liang_barsky', 'cohen_sutherland']

    def __init__(self, top_left: Coordinate3D, top_right: Coordinate3D, bottom_left: Coordinate3D,
                 center_back: Coordinate3D = None):
        super().__init__(coordinates=[top_left, top_right, bottom_left])
        if center_back is None:
            center_back = self.get_window_center() - self.view_vector
            self._coordinates.append(center_back)

    def clip_line(self, line: List[Coordinate3D]) -> Union[Tuple[Coordinate2D, Coordinate2D], None]:
        if self.__clipping_method == 'liang_barsky':
            return Clipper.liang_barsky_clip(line[0], line[1])
        elif self.__clipping_method == 'cohen_sutherland':
            return Clipper.cohen_sutherland_clip(line[0], line[1])

    def clip_point(self, point: Coordinate3D) -> Union[Coordinate3D, None]:
        return point if point.x >= -1 and point.x <= 1 and point.y >= -1 and point.y <= 1 else None

    def set_clipping_method(self, method: Literal['liang_barsky', 'cohen_sutherland']):
        self.__clipping_method = method

    @property
    def transformation_matrix(self) -> List[List[float]]:
        temp_window = Window(Coordinate3D(self.top_left.copy()),
                             Coordinate3D(self.top_right.copy()),
                             Coordinate3D(self.bottom_left.copy()),
                             Coordinate3D(self.center_back.copy()))

        matrix = []
        # Translate everything so the window is in the origin
        translation = -self.get_window_center()
        matrix.append(MatrixHelper.translation_matrix(translation))

        y_rotation = -(temp_window.view_vector.y_rotation_to_align_with_z())
        matrix.append(MatrixHelper.get_rotation_matrix(y_rotation, 'y'))
        temp_window.rotate(y_rotation, 'y')

        x_rotation = -(temp_window.view_vector.x_rotation_to_align_with_z())
        matrix.append(MatrixHelper.get_rotation_matrix(x_rotation, 'x'))
        temp_window.rotate(x_rotation, 'x')

        z_rotation = (-(temp_window.up.z_rotation_to_align_with_y()))
        matrix.append(MatrixHelper.get_rotation_matrix(z_rotation, 'z'))

        return matrix

    def coord_to_window_system(self, drawable: Displayable.Drawable) -> Displayable.Drawable:
        points = [self._transform_coord(p) for p in drawable.points]
        lines = [[self._transform_coord(line[0]), self._transform_coord(line[1])] for line in
                 drawable.lines]
        return self.clip(Displayable.Drawable(lines, points, drawable.color))

    def clip(self, drawable: Displayable.Drawable) -> Displayable.Drawable:
        # applies clipping and appends if clipped is not null
        for p in drawable.points:
            if p.z <= 0: return Displayable.Drawable([[]], [], drawable.color)
        points = [clipped_p for p in drawable.points if (clipped_p := self.clip_point(p)) is not None]
        lines = [clipped_l for line in drawable.lines if (clipped_l := self.clip_line(line)) is not None]
        # add missing line
        return Displayable.Drawable(lines, points, drawable.color)

    @property
    def top_left(self) -> Coordinate3D:
        return Coordinate3D(self._coordinates[0])

    @property
    def top_right(self) -> Coordinate3D:
        return Coordinate3D(self._coordinates[1])

    @property
    def bottom_left(self) -> Coordinate3D:
        return Coordinate3D(self._coordinates[2])

    @property
    def center_back(self) -> Coordinate3D:
        return Coordinate3D(self._coordinates[3])

    @property
    def view_vector(self)-> Coordinate3D:
        up = self.bottom_left - self.top_left
        left = self.top_left - self.top_right
        back = up * left
        return Coordinate3D(-back.normalize())

    @property
    def height(self) -> float:
        return Coordinate2D.distance(self.top_left, self.bottom_left)

    @property
    def width(self) -> float:
        return Coordinate2D.distance(self.top_left, self.top_right)

    @property
    def up(self) -> Coordinate3D:
        return Coordinate3D(-(self.bottom_left - self.top_left).normalize())

    @property
    def right(self) -> Coordinate3D:
        return Coordinate3D((self.top_right - self.top_left).normalize().copy())

    def move_left(self, amount):
        movement_vector = -self.right * amount * self.width
        self.translate(movement_vector)

    def move_right(self, amount):
        movement_vector = self.right * amount * self.width
        self.translate(movement_vector)

    def move_up(self, amount):
        movement_vector = self.up * amount * self.height
        self.translate(movement_vector)

    def move_down(self, amount):
        movement_vector = -self.up * amount * self.height
        self.translate(movement_vector)

    def move_forward(self, amount):
        movement_vector = -self.view_vector * amount
        self.translate(movement_vector)

    # Returns the angle between the window up and the y-axis
    def get_tilt_angle(self):
        y_axis: Coordinate2D = Coordinate2D.up()
        w_up: Coordinate2D = self.top_left - self.bottom_left
        return math.degrees(math.atan2(w_up.y * y_axis.x - w_up.x * y_axis.y, w_up.x * y_axis.x + w_up.y * y_axis.y))

    def get_center_coord(self) -> Coordinate3D:
        return self.get_window_center()

    def _transform_coord(self, coord: Coordinate3D):
        # TODO: Add projection calculation
        new_point = Coordinate3D(coord.copy())
        new_point.transform(self.transformation_matrix)

        new_point.x = new_point.x / (self.width * 0.5)
        new_point.y = new_point.y / (self.height * 0.5)
        return Coordinate3D(new_point)

    def get_window_center(self) -> Coordinate3D:
        center = self.bottom_left + ((self.top_left - self.bottom_left) * 0.5)
        return center + ((self.top_right - self.top_left) * 0.5)

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")
