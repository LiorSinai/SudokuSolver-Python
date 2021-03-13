""""
13 March 2021

Sudoku Solver UI by Erfan Paslar

"""

import eel  # For UI
from SudokuSolver import solveSudoku, str2grid
from Sudoku import Sudoku

#### For UI ####
eel.init('.//UI')  # path of the webpage folder


@eel.expose
def solveIt(puzzle):
    try:
        puzzles = puzzle.strip().split('\n')
        max_calls, max_depth = [0, 0, -1], [0, 0, -1]  # [calls, max depth, k]
        mean_calls = 0
        for k, puzzle in enumerate(puzzles):
            puzzle = str2grid(puzzle)
            my_solution, done, info = solveSudoku(
                puzzle, verbose=False, all_solutions=False)
            mean_calls = (mean_calls * k + info['calls']) / (k + 1)
            max_calls = max(max_calls, [info['calls'], info['max depth'], k])
            if info['solutions'] > 1:
                print('error: puzzle %d has %d solution' %
                      (k, info['solutions']))
            if not done:
                return ""

        # print(info['solution set'][0])
        return (info['solution set'][0])
    except IndexError:
        return ""


eel.start('index.html', size=(600, 640))