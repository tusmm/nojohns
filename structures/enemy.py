from collections import deque
from dataclasses import dataclass

import pygame

from structures.board import Board
from structures.direction import Direction, Offset
from structures.pawn import Pawn

COOLDOWN = 100 

@dataclass
class Enemy:
    x: int
    y: int
    enabled: bool
    last_move_tick: int

    def interact(self, board: Board, pawns: list[Pawn]):
        if self.enabled:
            if pygame.time.get_ticks() - self.last_move_tick >= COOLDOWN:
                self.last_move_tick = pygame.time.get_ticks()
                self.move(board, pawns)
        else:
            self.enabled = True
            self.last_move_tick = pygame.time.get_ticks()

    def move(self, board: Board, pawns: list[Pawn]):
        # Move the enemy towards the nearest pawn with breadth-first search
        goals = [Offset(pawn.x, pawn.y) for pawn in pawns]
        queue = []
        visited = {Offset(self.x, self.y): Offset(self.x, self.y)}
        queue.append(Offset(self.x, self.y))
        
        while queue:
            current = queue.pop(0)
            if current in goals:
                break

            current_cell = board.cells[Board.cartesian_to_id(current.x, current.y)]
            for direction in Direction:
                offset = Direction.get_coordinate_offset(direction)
                if current_cell.adjacency_matrix[direction.value] == 0:
                    neighbor = Offset(current.x + offset.x, current.y + offset.y)
                    if neighbor not in visited:
                        visited[neighbor] = current
                        queue.append(neighbor)

        while visited[current] != current:
            current = visited[current]
        self.x, self.y = current.x, current.y 

