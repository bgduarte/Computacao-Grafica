from viewport import Viewport
from displayable import Displayable
from dot import Dot
from wireframe import Wireframe
from line import Line
from typing import List, Literal
from enum import Enum
from aux import Coordinate2D



class Controller:
    __viewport: Viewport
    __displayFile: List[Displayable]
    OBJECT_TYPES = Enum('ObjectTypes', 'dot line wireframe')
    ZOOM_TYPES = Enum('ZoomTypes', 'in_ out')

    def __init__(self) -> None:
        from gui import Gui
        self.__gui = Gui(controller=self)
        canvas = self.__gui.create_canvas()
        self.__viewport = Viewport(canvas)
        self.__displayFile = []

    def run(self):
        self.__gui.run()
        while True:
            self.__gui.update()
            # TODO: draw not already drawed
            self.__viewport.draw(displayFile=self.__displayFile)


    def create_object(self, name: str, object_type: OBJECT_TYPES, coordinates: List[Coordinate2D]):
        # TODO: fix typing

        if (object_type == Controller.OBJECT_TYPES.dot.value):
            self.__displayFile.append(Dot(name, coordinates))
        elif (object_type == Controller.OBJECT_TYPES.line.value):
            self.__displayFile.append(Line(name, coordinates))
        elif (object_type == Controller.OBJECT_TYPES.wireframe.value):
            self.__displayFile.append(Wireframe(name, coordinates))

    def zoom(self, direction: ZOOM_TYPES):
        if direction == Controller.ZOOM_TYPES.in_.value:
            self.__viewport.zoom_in()
        else:
            self.__viewport.zoom_out()

    def navigate(self, direction: Literal['up', 'down', 'left', 'right']):
        self.__viewport.navigate(direction)
