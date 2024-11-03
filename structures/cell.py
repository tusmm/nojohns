from enum import Enum
from dataclasses import dataclass
from typing import ClassVar, Optional, Union

import pygame
from pygame import Surface

from structures.direction import Direction

class Objective(Enum):
    EMPTY = 0
    EXIT = 1
    PRESSURE_PLATE = 2
    OXYGEN_TANK = 3
    ENEMY_SPAWNER = 4

@dataclass
class Cell:
    def _load_wall_images() -> dict[int, Surface]:
        images = {}
        MAX_WALL_PERMUTATIONS = 16
        for i in range(MAX_WALL_PERMUTATIONS):
            images[i] = pygame.image.load(f"assets/tiles/final{i}.png")
        return images
    images: ClassVar[dict[int, Surface]] = _load_wall_images()

    id: int 
    adjacency_matrix: list[int]
    objective: int

    def __init__(self, id: int, adjacency_matrix: Union[int, list[int]], objective: Optional[int] = Objective.EMPTY.value):
        self.id = id
        if isinstance(adjacency_matrix, int):
            self.adjacency_matrix = self.int_to_adjacency_matrix(adjacency_matrix)
        elif isinstance(adjacency_matrix, list):
            self.adjacency_matrix = adjacency_matrix
        self.objective = objective

    @staticmethod
    def int_to_adjacency_matrix(num: int) -> list[int]:
        matrix = [int(bit) for bit in bin(num)[2:]] 
        matrix = [0] * (4 - len(matrix)) + matrix
        return matrix

    @staticmethod
    def get_wall_image(adjacency_matrix: list[int]) -> Surface:
        index = 0
        for bit in adjacency_matrix:
            index = (index << 1) | bit
        return Cell.images[index]

    def validate_direction(self, direction: Direction) -> bool:
        return self.adjacency_matrix[direction.value] == 0

    def validate_objective(self, objective: Objective) -> bool:
        return self.objective == objective.value
