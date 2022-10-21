import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        curses.resizeterm(self.life.rows + 2, self.life.cols + 2)
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        grid = self.life.curr_generation
        for i in range(len(grid)):
            line = ""
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    line += "*"
                else:
                    line += " "
            screen.addstr(i + 1, 1, line)

    def run(self) -> None:
        while self.life.is_changing and self.life.is_max_generations_exceeded:
            screen = curses.initscr()
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            time.sleep(1)
        curses.endwin()
