import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.speed = speed

        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size

        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        grid = self.life.curr_generation
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                color = pygame.Color('white')
                if grid[i][j] == 1:
                    color = pygame.Color('green')
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        cell_pos = (x // self.cell_size, y // self.cell_size)
                        self.life.curr_generation[cell_pos[1]][cell_pos[0]] = abs(self.life.curr_generation[cell_pos[1]][cell_pos[0]] - 1)
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()

            if not paused:
                self.draw_grid()
                self.draw_lines()
                self.life.step()
                pygame.display.flip()

                if not (self.life.is_max_generations_exceeded and self.life.is_changing):
                    break
                clock.tick(self.speed)
        pygame.quit()


