from tkinter import *
from typing import List, Literal
from model.world_objects.displayable import Displayable
from model.coordinate import Coordinate2D
from model.world_objects.window import Window


class Viewport:
    __canvas: Canvas
    __window: Window
    __world_origin: Coordinate2D

    LINE_WIDTH = 3
    POINT_WIDTH = 5

    ZOOM_AMOUNT = 1.1
    NAVIGATION_SPEED = 50

    def __init__(self, canvas: Canvas):
        self.__canvas = canvas
        self.__canvas.update()
        self.__window = Window([Coordinate2D(0, 0), Coordinate2D(self.get_width(), self.get_height())])
        self.__world_origin = Coordinate2D(0, 0)

    def __draw_line(self, coord1: Coordinate2D, coord2: Coordinate2D, color: str):
        coord1 = self.__tranform_coord(coord1)
        coord2 = self.__tranform_coord(coord2)
        self.__canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y,
                                  width=Viewport.LINE_WIDTH, fill=color)

    def __draw_point(self, coord: Coordinate2D, color: str):
        coord = self.__tranform_coord(coord)
        self.__canvas.create_oval(coord.x, coord.y, coord.x, coord.y,
                                  width=Viewport.POINT_WIDTH, outline=color)

    def __zoom(self, amount: float):
        # Add option to zoom irregularly in interface (different x t ammount)
        self.__window.scale_around_self(Coordinate2D(amount, amount))

    def __move_window(self, movement_vector: Coordinate2D):
        self.__window.translate(movement_vector)

    def __tranform_coord(self, coord: Coordinate2D) -> Coordinate2D:
        # TODO: change this to happen on window (new part)
        w_min = self.__window.get_coordinates()[0]
        w_max = self.__window.get_coordinates()[1]
        v_max = Coordinate2D(self.get_width(), self.get_height())
        v_min = self.__world_origin

        x = (coord.x - w_min.x) * (v_max.x - v_min.x) / (
                w_max.x - w_min.x)
        y = (1 - (coord.y - w_min.y) / (
                w_max.y - w_min.y)) * (v_max.y - v_min.y)
        return Coordinate2D(x, y)

    def get_window(self) -> Window:
        return self.__window

    def set_window(self, new_window: Window) -> None:
        self.__window = new_window

    def draw(self, display_file: List[Displayable]):
        # TODO: not redraw all every time
        self.__canvas.delete('all')
        for displayable in display_file:
            drawable = displayable.get_drawable()
            lines = drawable.lines
            points = drawable.points
            if lines:
                for line in lines:
                    self.__draw_line(coord1=line[0], coord2=line[1], color=drawable.color)

            for p in points:
                self.__draw_point(p, color=drawable.color)

        self.__canvas.update()

    def get_width(self) -> int:
        return self.__canvas.winfo_width()

    def get_height(self) -> int:
        return self.__canvas.winfo_height()

    def zoom_in(self) -> None:
        self.__zoom(1/Viewport.ZOOM_AMOUNT)

    def zoom_out(self) -> None:
        self.__zoom(Viewport.ZOOM_AMOUNT)

    def navigate(self, direction: Literal['up', 'down', 'left', 'right']):
        if direction == 'up':
            self.__move_window(Coordinate2D(0, Viewport.NAVIGATION_SPEED))
        elif direction == 'down':
            self.__move_window(Coordinate2D(0, -Viewport.NAVIGATION_SPEED))
        elif direction == 'left':
            self.__move_window(Coordinate2D(-Viewport.NAVIGATION_SPEED, 0))
        elif direction == 'right':
            self.__move_window(Coordinate2D(Viewport.NAVIGATION_SPEED, 0))
