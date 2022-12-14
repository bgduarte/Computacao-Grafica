from model.world_objects.displayables.curve import Curve
from utils.matrix_helper import MatrixHelper
from model.coordinate import Coordinate3D


class BezierCurve(Curve):
    def _constraint_check(self):
        length = len(self._coordinates)
        for i in range(3, len(self._coordinates)-1, 4):
            if self._coordinates[i] != self._coordinates[i+1]:
                raise Exception("Curves not connected")

        if length % 4 != 0 or length < 4:
            raise Exception("A bezier curve must have a least 4 points, "
                            "and the number of points must be multiple of 4")

    def _get_drawable_points(self):
        return self._coordinates[::4] + [self._coordinates[-1]]

    def _get_method_matrix(self):
        return [
            [-1, 3,-3, 1],
            [ 3,-6, 3, 0],
            [-3, 3, 0, 0],
            [ 1, 0, 0, 0]
                ]

    def _get_drawable_lines(self):
        lines = []
        Mb = self._get_method_matrix()

        points = []
        for i in range(int(len(self._coordinates) / 4)):  # for each curve (4 points)
            index = i*4
            Gx = [
                    [self._coordinates[index].x],
                    [self._coordinates[index + 1].x],
                    [self._coordinates[index + 2].x],
                    [self._coordinates[index + 3].x],
                 ]

            Gy = [
                [self._coordinates[index].y],
                [self._coordinates[index + 1].y],
                [self._coordinates[index + 2].y],
                [self._coordinates[index + 3].y],
            ]
            for j in range(self._resolution+1):  # for each point of the lines that has to be generated
                t = j / self._resolution
                T =[[t * t * t, t * t, t, 1]]

                x = MatrixHelper.mul(MatrixHelper.mul(T, Mb), Gx)[0][0]
                y = MatrixHelper.mul(MatrixHelper.mul(T, Mb), Gy)[0][0]

                points.append(Coordinate3D(x, y))

        return [[points[i], points[i+1]] for i in range(len(points)-1)]
