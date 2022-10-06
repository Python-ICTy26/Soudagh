import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    matrix = [values[i * len(values) // n : (i + 1) * len(values) // n] for i in range(n)]
    return matrix


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    a = []
    x = pos[0]
    y = pos[1]
    while x % 3 != 0:
        x -= 1
    while y % 3 != 0:
        y -= 1

    for i in range(x, x + int(len(grid) ** 0.25) + 2):
        for j in range(y, y + int(len(grid) ** 0.25) + 2):
            a.append(grid[i][j])
    return a


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return i, j
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    possible_values = set()
    for i in range(1, 10):
        str_i = str(i)
        if (
            str_i not in get_block(grid, pos)
            and str_i not in get_row(grid, pos)
            and str_i not in get_col(grid, pos)
        ):
            possible_values.add(str_i)
    return possible_values


def solve(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    else:
        values = find_possible_values(grid, pos)
        for i in values:
            grid[pos[0]][pos[1]] = i
            if solve(grid):
                return grid
            else:
                grid[pos[0]][pos[1]] = "."
    return []


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    if find_empty_positions(solution):
        return False

    for i in range(len(solution)):
        row = get_row(solution, (i, 0))
        col = get_col(solution, (0, i))
        block = get_block(solution, (i // len(solution), i % len(solution)))
        if len(row) != len(set(row)) or len(col) != len(set(col)) or len(block) != len(set(block)):
            return False
    return True


from random import randint


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    if N > 81:
        N = 81

    empty_pos = 81 - N
    pos = get_rand_row_col()

    grid = [["."] * 9 for _ in range(9)]
    grid[pos[0]][pos[1]] = str(randint(1, 9))
    grid = solve(grid)

    for i in range(empty_pos):
        pos = get_rand_row_col()
        while grid[pos[0]][pos[1]] == ".":
            pos = get_rand_row_col()
        grid[pos[0]][pos[1]] = "."
    return grid


def get_rand_row_col():
    return randint(0, 8), randint(0, 8)


if __name__ == "__main__":
    for fname in ["homework02/puzzle1.txt", "homework02/puzzle2.txt", "homework02/puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
