from dataclasses import dataclass

import pygame

from structures.board import Board, BOARD_HEIGHT, BOARD_WIDTH

@dataclass
class Pawn:
    x: int
    y: int

    def move(self, dx, dy, direction, board, pawns):
        new_x = self.x + dx
        new_y = self.y + dy

        current_cell = board.cells[Board.cartesian_to_id(self.x, self.y)]
        if (0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT and 
            all(not (new_x == pawn.x and new_y == pawn.y) for pawn in pawns) and
            current_cell.validate_direction(direction)):
            self.x = new_x
            self.y = new_y
    
