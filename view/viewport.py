from tkinter import *
from typing import List, Literal
from model.world_objects.displayable import Displayable
from model.coordinate import Coordinate2D, Coordinate3D
from model.world_objects.window import Window


class Viewport:
    __canvas: Canvas
    __window: Window
    __world_origin: Coordinate2D
    __border_width = 50

    LINE_WIDTH = 3
    POINT_WIDTH = 5

    ZOOM_AMOUNT = 1.1
    NAVIGATION_SPEED = 0.07
    WINDOW_ROTATION_AMOUNT = 15
    WINDOW_MOVEMENT_AMOUNT = 10

    def __init__(self, canvas: Canvas):
        self.__canvas = canvas
        self.__canvas.update()
        self.__window = Window(
            top_left=Coordinate3D(0, self.get_height(), 100),
            top_right=Coordinate3D(self.get_width(), self.get_height(), 100),
            bottom_left=Coordinate3D(0, 0, 100)
        )
        self.__world_origin = Coordinate2D(0, 0)
        self.__draw_viewport()

    def __draw_viewport(self):
        lines = [(-1, -1, 1, -1), (-1, 1, 1, 1), (-1, 1, -1, -1), (1, 1, 1, -1)]
        for x1, y1, x2, y2 in lines:
            self.__draw_line(
                Coordinate2D(x1, y1),
                Coordinate2D(x2, y2),
                '#f00',
                1
            )

    def __draw_line(self, coord1: Coordinate2D, coord2: Coordinate2D, color: str, line_width: int = None):
        if not line_width: line_width = Viewport.LINE_WIDTH
        coord1 = self.__tranform_coord(coord1)
        coord2 = self.__tranform_coord(coord2)
        self.__canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y,
                                  width=line_width, fill=color)

    def __draw_point(self, coord: Coordinate2D, color: str):
        coord = self.__tranform_coord(coord)
        self.__canvas.create_oval(coord.x, coord.y, coord.x, coord.y,
                                  width=Viewport.POINT_WIDTH, outline=color)

    def __zoom(self, amount: float):
        # Add option to zoom irregularly in interface (different x t ammount)
        self.__window.scale_around_self(Coordinate3D(amount, amount, amount))

    def __tranform_coord(self, coord: Coordinate2D) -> Coordinate2D:
        x = (coord[0] + 1)*0.5*self.get_width()
        y = (1 - (coord[1] + 1)*0.5) *self.get_height()
        x += self.__border_width
        y += self.__border_width
        return Coordinate2D(x, y)

    def set_clipping_method(self, method: Literal['liang_barsky', 'cohen_sutherland']):
        self.__window.set_clipping_method(method)

    def get_window(self) -> Window:
        return self.__window

    def set_window(self, new_window: Window) -> None:
        self.__window = new_window

    def draw(self, display_file: List[Displayable]):
        # TODO: not redraw all every time
        self.__canvas.delete('all')
        self.__draw_viewport()

        for displayable in display_file:
            drawable = self.__window.coord_to_window_system(displayable.get_drawable())
            drawable = self.__window.clip(drawable)
            for point in drawable.points:
                self.__draw_point(Coordinate2D(point), drawable.color)
            for line in drawable.lines:
                if line:
                    self.__draw_line(Coordinate2D(line[0]), Coordinate2D(line[1]), drawable.color)
            # TODO: FILL OBJECTS WITH COLOR
        self.__canvas.update()

    def get_width(self) -> int:
        return self.__canvas.winfo_width() - 2*self.__border_width

    def get_height(self) -> int:
        return self.__canvas.winfo_height() - 2*self.__border_width

    def zoom_in(self) -> None:
        self.__zoom(1/Viewport.ZOOM_AMOUNT)

    def zoom_out(self) -> None:
        self.__zoom(Viewport.ZOOM_AMOUNT)

    def navigate(self, direction: Literal['up', 'down', 'left', 'right', 'forward', 'backward']):
        amount = Viewport.NAVIGATION_SPEED
        if direction == 'up':
            self.__window.move_up(amount)
        elif direction == 'down':
            self.__window.move_down(amount)
        elif direction == 'left':
            self.__window.move_left(amount)
        elif direction == 'right':
            self.__window.move_right(amount)
        elif direction == 'forward':
            self.__window.move_forward(Viewport.WINDOW_MOVEMENT_AMOUNT)
        elif direction == 'backward':
            self.__window.move_forward(-Viewport.WINDOW_MOVEMENT_AMOUNT)
        
    def tilt(self, direction: Literal['up', 'down', 'left', 'right']) -> None:
        axis_vector: Coordinate3D = self.__window.up
        if direction == 'up' or direction == 'down':
            axis_vector = self.__window.right
        amount = Viewport.WINDOW_ROTATION_AMOUNT
        if direction == 'down' or direction == 'left':
            amount = -amount
        self.__window.rotate_around_self(amount, axis_vector=axis_vector)

    def rotate_window(self, direction: Literal['left', 'right']):
        amount = -Viewport.WINDOW_ROTATION_AMOUNT if direction == 'left' else Viewport.WINDOW_ROTATION_AMOUNT
        self.__window.rotate_around_point(angle=amount, point=self.__window.get_window_center(), axis_vector=self.__window.view_vector)
