from model.coordinate import Coordinate3D
from model.coordinate import Coordinate2D
import unittest

class Coordinate2DTest(unittest.TestCase):

    def test_add_coords(self):
        coord1 = Coordinate2D(10, 20)
        coord2 = Coordinate2D(5, 10)
        result = coord1 + coord2
        assert result.x == coord1.x + coord2.x
        assert result.y == coord1.y + coord2.y

    def test_neg_coord(self):
        coord1 = Coordinate2D(10, 20)
        result = -coord1
        assert result.x == -coord1.x
        assert result.y == -coord1.y

    def test_sub_coord(self):
        coord1 = Coordinate2D(10, 20)
        coord2 = Coordinate2D(5, 10)
        result = coord1 - coord2
        assert result.x == coord1.x - coord2.x
        assert result.y == coord1.y - coord2.y

    def test_lenght_coord(self):
        coord1 = Coordinate2D(3, 4)
        result = coord1.length
        assert result == 5


    def test_mul_coord(self):
        coord1 = Coordinate2D(10, 20)
        result = coord1*20
        assert result.x == 20*coord1.x
        assert result.y == 20*coord1.y

    def test_normalize_coord(self):
        coord1 = Coordinate2D(10, 20)
        result = coord1.normalize()
        assert round(result.length) == 1


    def test_distance_coord(self):
        coord1 = Coordinate2D(10, 20)
        coord2 = Coordinate2D(10, 10)
        result = Coordinate2D.distance(coord1, coord2)
        assert result == 10

    def test_up_coord(self):
        assert Coordinate2D.up() == [0,1]

class Coordinate3DTest(unittest.TestCase):

    def test_add_coords(self):
        coord1 = Coordinate3D(10, 20, 30)
        coord2 = Coordinate3D(5, 10, 15)
        result = coord1 + coord2
        assert result.x == coord1.x + coord2.x
        assert result.y == coord1.y + coord2.y
        assert result.z == coord1.z + coord2.z

    def test_neg_coord(self):
        coord1 = Coordinate3D(10, 20, 30)
        result = -coord1
        assert result.x == -coord1.x
        assert result.y == -coord1.y
        assert result.z == -coord1.z

    def test_sub_coord(self):
        coord1 = Coordinate3D(10, 20, 30)
        coord2 = Coordinate3D(5, 10, 15)
        result = coord1 - coord2
        assert result.x == coord1.x - coord2.x
        assert result.y == coord1.y - coord2.y
        assert result.z == coord1.z - coord2.z

    def test_lenght_coord(self):
        coord1 = Coordinate3D(0, 3, 4)
        result = coord1.length
        assert result == 5


    def test_mul_coord(self):
        coord1 = Coordinate3D(10, 20, 30)
        result = coord1*20
        assert result.x == 20*coord1.x
        assert result.y == 20*coord1.y
        assert result.z == 20 * coord1.z

    def test_normalize_coord(self):
        coord1 = Coordinate3D(10, 20, 45)
        result = coord1.normalize()
        assert round(result.length) == 1


    def test_distance_coord(self):
        coord1 = Coordinate3D(10, 20, 30)
        coord2 = Coordinate3D(10, 10, 30)
        result = Coordinate3D.distance(coord1, coord2)
        assert result == 10

    def test_up_coord(self):
        assert Coordinate3D.up() == [0,1,0]