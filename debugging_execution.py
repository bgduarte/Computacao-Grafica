from controller.controller import Controller
from model.coordinate import Coordinate2D
from model.world_objects.displayables.wireframe import Wireframe
from model.world_objects.displayables.line import Line
from model.world_objects.displayables.dot import Dot
from model.world_objects.displayables.bezier_curve import BezierCurve
from typing import List



class DebugHelper:

    def __init__(self, controller: Controller):
        self.__controller = controller
        self.__square_count = 0

    def run(self):
        self.__controller.run()

    def create_square(self, size: float, position: tuple):
        position = Coordinate2D(position[0], position[1])
        points = [
            position,
            Coordinate2D(position.x + size, position.y),
            Coordinate2D(position.x + size, position.y + size),
            Coordinate2D(position.x , position.y + size),
        ]
        square  = Wireframe(name = f'Square {self.__square_count}', coordinates=points, color='#000')
        self.__controller.observable_display_file.append(square)
        self.__square_count += 1
        return square

    def create_dot(self, position: tuple):
        coord = Coordinate2D(position[0], position[1])
        dot = Dot(name="Dot1", color='#000', coordinates=[coord])
        self.__controller.observable_display_file.append(dot)
        return dot

    def create_line(self, position: tuple, position2: tuple):
        coord = Coordinate2D(position[0], position[1])
        coord2 = Coordinate2D(position2[0], position2[1])
        line = Line(name="Dot1", color='#000', coordinates=[coord, coord2])
        self.__controller.observable_display_file.append(line)
        return line

    def create_bezier_curve(self, coords: List[Coordinate2D]):
        curve = BezierCurve(coordinates=coords, name="Curve", color='#000')
        self.__controller.observable_display_file.append(curve)
        return curve


def main():
    controller = Controller()
    helper = DebugHelper(controller)
    ## Place what you want to test here (display doesn't update automatically,
    # you need to trigger by using the interface)
    #square1 = helper.create_square(position=(100, 100), size=30)
    #dot = helper.create_dot(position=(400,400))
    curve = helper.create_bezier_curve([
        Coordinate2D(100,0),
        Coordinate2D(100, 100),
        Coordinate2D(0,100),
        Coordinate2D(0, 0),
        Coordinate2D(0, 0),
        Coordinate2D(0, -100),
        Coordinate2D(-100, -70),
        Coordinate2D(-30, 0),

    ])
    line = helper.create_line((100, 100), (100, 200))
    #square1.scale_around_self(Coordinate2D(2, 2))
    #square1.translate(Coordinate2D(15, 0))
    #square1.rotate_around_self(15)

    ##
    helper.run()

if __name__ == "__main__":
    main()