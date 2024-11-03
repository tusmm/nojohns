from collections import namedtuple
from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def get_coordinate_offset(self):
        match self:
            case Direction.NORTH:
                return Coordinate(0, -1)
            case Direction.EAST:
                return Coordinate(1, 0)
            case Direction.SOUTH:
                return Coordinate(0, 1)
            case Direction.WEST:
                return Coordinate(-1, 0)

Coordinate = namedtuple('Coordinate', ['x', 'y'])