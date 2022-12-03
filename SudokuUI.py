""""
13 March 2021

Sudoku Solver UI by Erfan Paslar

"""

import eel  # For UI
from SudokuSolver import solve_sudoku, str2grid
from Sudoku import Sudoku

#### For UI ####
eel.init('.//UI')  # path of the webpage folder


@eel.expose
def solveIt(puzzle):
    try:
        grid = str2grid(puzzle)
        solution_set, done, info = solve_sudoku(
            grid, verbose=False, all_solutions=False)
        if not done:
            return ""

        # print(solution_set[0])
        return (solution_set[0])
    except IndexError:
        return ""


eel.start('index.html', size=(600, 640))