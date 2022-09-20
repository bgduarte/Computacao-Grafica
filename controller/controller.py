from view.viewport import Viewport
from model.display_file import ObservableDisplayFile
from model.displayable import Displayable
from model.dot import Dot
from model.wireframe import Wireframe
from model.line import Line
from typing import List, Literal
from enum import Enum
from model.coordinate import Coordinate2D
from view.gui import Gui


class Controller:
    ### Private attrs
    __viewport: Viewport

    ### Public attrs
    observable_display_file: ObservableDisplayFile

    # Constructor
    def __init__(self) -> None:
        self.observable_display_file = ObservableDisplayFile()

    ### Private methods
    def __create_interface(self) -> None:
        self.__gui = Gui(controller=self)
        canvas = self.__gui.create_canvas()
        self.__viewport = Viewport(canvas)
        self.observable_display_file.subscribe(self.__on_display_file_change)

    def __on_display_file_change(self, display_file: List[Displayable]) -> None:
        self.__viewport.draw(display_file)

    ### Public methods
    def run(self):
        self.__create_interface()
        self.__gui.run()
        while True:
            self.__gui.update()

    def create_object(self, name: str, color: str, object_type: Literal['dot', 'line', 'wireframe'], coordinates: List[Coordinate2D]):
        # color is '#rgb' or '#rrggbb'
        if object_type == 'dot':
            self.observable_display_file.append(Dot(name, color, coordinates))
        elif object_type == 'line':
            self.observable_display_file.append(Line(name, color, coordinates))
        elif object_type == 'wireframe':
            self.observable_display_file.append(Wireframe(name, color, coordinates))

    def zoom(self, direction: Literal['in', 'out']):
        if direction == 'in':
            self.__viewport.zoom_in()
        elif direction == 'out':
            self.__viewport.zoom_out()
        self.__viewport.draw(self.observable_display_file.displayables())

    def navigate(self, direction: Literal['up', 'down', 'left', 'right']):
        self.__viewport.navigate(direction)
        self.__viewport.draw(self.observable_display_file.displayables())

    def translate_object(self, displayable: Displayable, movement_vector: Coordinate2D) -> None:
        displayable.translate(movement_vector)
        self.__viewport.draw(self.observable_display_file.displayables())

    def scale_object(self, displayable: Displayable, scale_vector: Coordinate2D) -> None:
        displayable.scale_around_self(scale_vector)
        self.__viewport.draw(self.observable_display_file.displayables())
        
    def rotate_object(self, displayable: Displayable, angle: float,
                      relative_to: Literal['world', 'itself', 'coordinate'], center: Coordinate2D = None) -> None:
        if relative_to == 'world':
            displayable.rotate(angle)
        elif relative_to == 'itself':
            displayable.rotate_around_self(angle)
        elif relative_to == 'coordinate':
            displayable.rotate_around_point(angle, center)
        self.__viewport.draw(self.observable_display_file.displayables())