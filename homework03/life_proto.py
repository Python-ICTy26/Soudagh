import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            grid = [
                [random.choice([0, 1]) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        return grid

    def draw_grid(self) -> None:
        grid = self.grid
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                color = pygame.Color("white")
                if grid[i][j] == 1:
                    color = pygame.Color("green")
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size
                    ),
                )
        return None

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
                    cells.append(self.grid[x][y])
            except IndexError:
                pass
        return cells

    def get_next_generation(self) -> Grid:
        grid = self.grid
        new_grid = [[0] * self.cell_width for _ in range(self.cell_height)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                neighbours = self.get_neighbours((i, j)).count(1)
                if grid[i][j] == 0 and neighbours == 3:
                    new_grid[i][j] = 1
                elif grid[i][j] == 1 and (neighbours == 2 or neighbours == 3):
                    new_grid[i][j] = 1
        return new_grid
