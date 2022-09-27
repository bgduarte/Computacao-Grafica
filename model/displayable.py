from typing import List
from model.coordinate import Coordinate2D
from dataclasses import dataclass
from model.world_object import WorldObject
from abc import abstractmethod


# Abstract class
class Displayable(WorldObject):
    # private attributes
    _name: str
    _color: str

    @dataclass
    class Drawable:
        lines: List[List[Coordinate2D]]
        points: List[Coordinate2D]
        color: str

    def __init__(self, name: str, color: str, coordinates: List[Coordinate2D]) -> None:
        # color is '#rgb' or '#rrggbb'
        super().__init__(coordinates=coordinates)
        self._name = name
        self._color = color
        self._constraint_check()
        if not issubclass(type(self), Displayable):
            raise Exception("Displayable is an abstract class, it is not supposed to be instantiated")
    
    def get_name(self) -> str:
        return self._name
    
    def get_color(self) -> str:
        return self._color

    def set_color(self, color: str) -> None:
        # color is '#rgb' or '#rrggbb'
        self._color = color

    def get_drawable(self):
        return Displayable.Drawable(
            lines=self._get_drawable_lines(),
            points=self._get_drawable_points(),
            color=self._color)

    @abstractmethod
    def _get_drawable_lines(self):
        pass

    @abstractmethod
    def _get_drawable_points(self):
        pass
