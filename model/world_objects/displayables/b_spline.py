from model.world_objects.displayables.curve import Curve
from utils.matrix_helper import MatrixHelper
from typing import List
from model.coordinate import Coordinate2D


class BSpline(Curve):

    def _constraint_check(self):
        pass  # TODO: implement this

    def _get_drawable_points(self):
        return self._coordinates  # TODO: improve this

    def _get_method_matrix(self):
        return [
            [-1 / 6, 3 / 6, -3 / 6, 1 / 6],
            [3 / 6, -1, 3 / 6, 0],
            [-3 / 6, 0, 3 / 6, 0],
            [1 / 6, 4 / 6, 1 / 6, 0]
        ]

    def forward_differences(self, number_of_points: int,
                           Dx: List[List[float]], Dy: List[List[float]]) -> List[List[Coordinate2D]]:
        x = Dx[0][0]
        y = Dy[0][0]
        old_x = x
        old_y = y
        lines = []
        for i in range(0, number_of_points):
            x += Dx[1][0]
            Dx[1][0] += Dx[2][0]
            Dx[2][0] += Dx[3][0]

            y += Dy[1][0]
            Dy[1][0] += Dy[2][0]
            Dy[2][0] += Dy[3][0]
            lines.append([Coordinate2D(old_x, old_y), Coordinate2D(x, y)])

            old_x = x
            old_y = y


        return lines

    def _get_drawable_lines(self):
        lines = []
        Mbs = self._get_method_matrix()

        fi = 1/self._resolution

        Efi = [
            [0, 0, 0, 1],
            [fi * fi * fi, fi * fi, fi, 0],
            [6 * fi * fi * fi, 2 * fi * fi, 0, 0],
            [6 * fi * fi * fi, 0, 0, 0]
        ]

        for i in range(0, len(self._coordinates) -3):
            Gx = [
                [self._coordinates[i].x],
                [self._coordinates[i+1].x],
                [self._coordinates[i+2].x],
                [self._coordinates[i+3].x],
            ]
            Cx = MatrixHelper.mul(Mbs, Gx)
            Dx = MatrixHelper.mul(Efi, Cx)

            Gy = [
                [self._coordinates[i].y],
                [self._coordinates[i+1].y],
                [self._coordinates[i+2].y],
                [self._coordinates[i+3].y],
            ]
            Cy = MatrixHelper.mul(Mbs, Gy)
            Dy = MatrixHelper.mul(Efi, Cy)

            lines += (self.forward_differences(number_of_points=self._resolution, Dx=Dx, Dy=Dy))

        return lines
