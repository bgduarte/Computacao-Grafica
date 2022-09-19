from controller.controller import Controller
from model.coordinate import Coordinate2D
from model.wireframe import Wireframe


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
        square  = Wireframe(name = f'Square {self.__square_count}', coordinates=points)
        self.__controller.observable_display_file.append(square)
        self.__square_count += 1
        return square


def main():
    controller = Controller()
    helper = DebugHelper(controller)
    ## Place what you want to test here (display doesn't update automatically,
    # you need to trigger by using the interface)
    square1 = helper.create_square(position=(100, 100), size=30)
    square2 = helper.create_square(position=(100, 100), size=30)
    square3 = helper.create_square(position=(100, 100), size=30)
    square4 = helper.create_square(position=(100, 100), size=30)
    square2.rotate_around_point(15, Coordinate2D(100, 100))
    square3.rotate_around_point(30, Coordinate2D(100, 100))
    square4.rotate_around_point(45, Coordinate2D(100, 100))
    #square2.scale_around_self(Coordinate2D(2, 2))
    #square2.translate(Coordinate2D(15, 0))

    ##
    helper.run()

if __name__ == "__main__":
    main()