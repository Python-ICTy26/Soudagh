import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        cell_neighbours = [[-1, -1], [1, 1], [0, 1], [1, 0], [-1, 1], [1, -1], [-1, 0], [0, -1]]

        for c in cell_neighbours:
            c[0] += cell[0]
            c[1] += cell[1]

        for c in cell_neighbours:
            x, y = c
            try:
                if x >= 0 and y >= 0:
                    cells.append(self.curr_generation[x][y])
            except IndexError:
                pass
        return cells

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(False)

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j)).count(1)
                if self.curr_generation[i][j] == 0 and neighbours == 3:
                    new_grid[i][j] = 1
                elif self.curr_generation[i][j] == 1 and (neighbours == 2 or neighbours == 3):
                    new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations < self.generations:
            return False
        return True

    @property
    def is_changing(self) -> bool:
        for i in range(self.rows):
            if self.prev_generation[i] != self.curr_generation[i]:
                return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        f = open(filename, "r")
        grid = []
        for i, line in enumerate(f):
            grid.append([])
            for c in line[:-1]:
                grid[i].append(int(c))

        game_from_file = GameOfLife(size=(len(grid), len(grid[0])), randomize=False)
        game_from_file.curr_generation = grid
        return game_from_file

    def save(self, filename: pathlib.Path) -> None:
        f = open(filename, "w")
        for i in self.curr_generation:
            for c in i:
                f.write(str(c))
            f.write("\n")
