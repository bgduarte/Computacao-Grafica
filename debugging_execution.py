from controller.controller import Controller
from model.coordinate import Coordinate3D
from model.world_objects.displayables.b_spline import BSpline
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
        position = Coordinate3D(position[0], position[1])
        points = [
            position,
            Coordinate3D(position.x + size, position.y),
            Coordinate3D(position.x + size, position.y + size),
            Coordinate3D(position.x , position.y + size),
        ]
        square  = Wireframe(name = f'Square {self.__square_count}', coordinates=points, color='#000')
        self.__controller.observable_display_file.append(square)
        self.__square_count += 1
        return square

    def create_dot(self, position: tuple):
        coord = Coordinate3D(position[0], position[1], 0)
        dot = Dot(name="Dot1", color='#000', coordinates=[coord])
        self.__controller.observable_display_file.append(dot)
        return dot

    def create_line(self, position: tuple, position2: tuple):
        coord = Coordinate3D(position[0], position[1], 0)
        coord2 = Coordinate3D(position2[0], position2[1], 0)
        line = Line(name="Dot1", color='#000', coordinates=[coord, coord2])
        self.__controller.observable_display_file.append(line)
        return line

    def create_bezier_curve(self, coords: List[Coordinate3D]):
        curve = BezierCurve(coordinates=coords, name="Curve", color='#000')
        self.__controller.observable_display_file.append(curve)
        return curve

    def create_spline_curve(self, coords: List[Coordinate3D]):
        curve = BSpline(coordinates=coords, name="Curve", color='#000')
        self.__controller.observable_display_file.append(curve)
        return curve


def main():
    controller = Controller()
    helper = DebugHelper(controller)
    ## Place what you want to test here (display doesn't update automatically,
    # you need to trigger by using the interface)
    square1 = helper.create_square(position=(100, 100), size=30)
    dot = helper.create_dot(position=(100,100))
    curve = helper.create_spline_curve([
        Coordinate3D(100,100),
        Coordinate3D(200, 100),
        Coordinate3D(300, 200),
        Coordinate3D(400, 100),
        Coordinate3D(500, 100),
        Coordinate3D(600, 100),
    ])
    line = helper.create_line((100, 100), (100, 200))
    #square1.scale_around_self(Coordinate2D(2, 2))
    #square1.translate(Coordinate2D(15, 0))
    #square1.rotate_around_self(15)

    ##
    helper.run()

if __name__ == "__main__":
    main()