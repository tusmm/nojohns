from dataclasses import dataclass
from typing import NamedTuple, Self

from structures.board import Board, BOARD_HEIGHT, BOARD_WIDTH
from structures.direction import Direction

@dataclass
class Pawn:
    x: int
    y: int
    color: tuple[int, int, int]

    def move(self, offset: NamedTuple, direction: Direction, board: Board, pawns: list[Self]):
        new_x = self.x + offset.x
        new_y = self.y + offset.y

        current_cell = board.cells[Board.cartesian_to_id(self.x, self.y)]
        if (0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT and 
            all(not (new_x == pawn.x and new_y == pawn.y) for pawn in pawns) and
            current_cell.validate_direction(direction)):
            self.x = new_x
            self.y = new_y
    
