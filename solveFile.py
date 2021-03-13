""""
31 May 2020
Sudoku Solver

Solve many puzzles at once

"""

from Sudoku import Sudoku
from SudokuSolver import Sudoku, solveSudoku, grid_equal, str2grid, grid2str
import time
from statistics import mean, median, stdev

def argmax(arr) -> int:
    pair = max(enumerate(arr), key=lambda pair: pair[1])
    return pair[0]


if __name__ == '__main__':
    folder = 'test/'

    file_name = 'hardest.txt'  # top95.txt hardest.txt # from https://norvig.com/sudoku.html. 
    #file_name = 'ny.txt'   # from the New York Times
    
    with open(folder + file_name, 'r') as f:
        puzzles = f.read().strip().split('\n')

    verbose       = False
    all_solutions = False

    t0 = time.time()
    metrics = {
        'times':      [],
        'calls':      [],
        'max depths': [],
        'nsolutions': []
    }
    num_solved = 0
    for k, puzzle in enumerate(puzzles):
        # if k != 86:
        #     continue
        tk0 = time.time()
        ## solve
        puzzle = str2grid(puzzle)
        my_solution, done, info = solveSudoku(
            puzzle, 
            verbose=verbose, 
            all_solutions=all_solutions
            )
        # my_solution, done, info = solveSudokuBrute(puzzle)
        deltaTk = time.time() - tk0
        ## update metrics
        num_solved += done
        metrics['times'].append(deltaTk)
        metrics['calls'].append(info['calls'])
        metrics['max depths'].append(info['max depth'])
        metrics['nsolutions'].append(info['nsolutions'])
    deltaT = time.time() - t0

    pm ='\u00b1' #plus or minus symbol

    print(' ')
    print("%d/%d puzzles solved in %.5fs" % (num_solved, len(puzzles), deltaT))
    metric = metrics['times']
    print("time      min-max, mean: %.5fs-%.5fs, %.4fs %s %.4fs "%(min(metric), max(metric), mean(metric), pm, stdev(metric)))
    metric = metrics['calls']
    print("calls     min-max, mean: %d-%d, %.2f %s %.2f "%(min(metric), max(metric), mean(metric), pm, stdev(metric)))
    metric = metrics['max depths']
    print("max depth min-max, mean: %d-%d, %.2f %s %.2f "%(min(metric), max(metric), mean(metric), pm, stdev(metric)))
    metric = metrics['nsolutions']
    print("mnsolutions min-max, mean: %d-%d, %.1f %s %.1f "%(min(metric), max(metric), mean(metric), pm, stdev(metric)))

    print(' ')
    metric = metrics['calls']
    k = argmax(metric)
    print("#puzzle, max calls, max depth: ", k, metric[k], metrics['max depths'][k])
    metric = metrics['max depths']
    k = argmax(metric)
    print("#puzzle, calls, max(max depth):", k, metrics['calls'][k], metric[k])