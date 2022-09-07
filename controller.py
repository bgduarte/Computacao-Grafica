from viewport import Viewport
from displayable import Displayable
from dot import Dot
from line import Line
from typing import List
from enum import Enum
from aux import Coordinate2D



class Controller:
    __viewport: Viewport
    __displayFile: List[Displayable]
    OBJECT_TYPES = Enum('ObjectTypes', 'dot line wireframe')

    def __init__(self) -> None:
        from gui import Gui
        self.__gui = Gui(controller=self)
        canvas = self.__gui.create_canvas()
        self.__viewport = Viewport(canvas)

        self.__displayFile = []

    def run(self):
        self.__viewport.draw(displayFile=self.__displayFile)
        self.__gui.run()

    def create_object(self, name: str, object_type: OBJECT_TYPES, coordinates: List[Coordinate2D]):
        # TODO: fix typing
        
        if (object_type == Controller.OBJECT_TYPES.dot):
            self.__displayFile.append(Dot(name, coordinates))
        elif (object_type == Controller.OBJECT_TYPES.line):
            self.__displayFile.append(Line(name, coordinates))
        elif (object_type == Controller.OBJECT_TYPES.wireframe):
            self.__displayFile.append(Displayable(name, coordinates))


