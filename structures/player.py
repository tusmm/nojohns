from dataclasses import dataclass

from structures.board import Board
from structures.direction import Direction
from structures.pawn import Pawn

@dataclass
class Player:
    pawn_index: int
    pawns: list[Pawn]
    possible_movement: set[Direction]

    def __init__(self, pawn_index: int, pawns: list[Pawn], possible_movement: set[Direction]):
        self.pawn_index = pawn_index
        self.pawns = pawns
        self.possible_movement = possible_movement

    def move(self, direction: Direction, board: Board):
        if direction in self.possible_movement:
            pawns = self.pawns.copy()
            pawns.pop(self.pawn_index)
            self.pawns[self.pawn_index].move(Direction.get_coordinate_offset(direction), direction, board, pawns)
   
    def rotate_pawn(self):
        self.pawn_index = (self.pawn_index + 1) % len(self.pawns)