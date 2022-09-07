from tkinter import *
from typing import List
from displayable import Displayable
from dot import Dot
from line import Line


class Viewport:
    __canvas: Canvas

    LINE_WIDTH = 3
    LINE_COLOR = "black"

    POINT_WIDTH = 5
    POINT_COLOR = "black"

    def __init__(self, canvas: Canvas):
        self.__canvas = canvas

    def __drawLine(self, coord1, coord2):
        self.__canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y,
                                  width=Viewport.LINE_WIDTH, fill=Viewport.LINE_COLOR)

    def __draw_point(self, coord):
        self.__canvas.create_oval(coord.x, coord.y, coord.x, coord.y,
                                  width=Viewport.POINT_WIDTH, fill=Viewport.POINT_COLOR)

    def draw(self, displayFile: List[Displayable]):
        for displayable in displayFile:

            coordinates = displayable.get_coordinates()
            for i in range(len(coordinates)):
                # Transform coordinate

                # Draw point
                self.__draw_point(coordinates[i])

                # Draw line
                if i < len(coordinates) - 1:
                    self.__drawLine(coordinates[i], coordinates[i + 1])
                else:
                    if not isinstance(displayable, Dot) and not isinstance(displayable, Line):
                        self.__drawLine(coordinates[i], coordinates[0])