""""
31 May 2020
Sudoku Solver

Solve many puzzles at once

"""

from solver import solve_sudoku, str2grid
from Sudoku import SudokuException
import time
from statistics import mean, stdev

def argmax(arr) -> int:
    pair = max(enumerate(arr), key=lambda pair: pair[1])
    return pair[0]


if __name__ == '__main__':
    folder = 'test/'

    file_name = 'top95.txt'  # top95.txt hardest.txt # from https://norvig.com/sudoku.html. 
    #file_name = 'ny.txt'   # from the New York Times
    #file_name = 'possiblesN.txt' # X-Sudoku https://www.geocaching.com/geocache/GC7MG6K_denombrements => 351/101793 solvable
    
    with open(folder + file_name, 'r') as f:
        puzzles = f.read().strip().split('\n')

    verbose       = False
    all_solutions = False
    is_X_Sudoku   = False

    t0 = time.time()
    metrics = {
        'times':      [],
        'calls':      [],
        'max depths': [],
        'nsolutions': []
    }
    num_solved = 0
    n_puzzles = len(puzzles)
    n_update = round(n_puzzles / 100) + 1
    for k, puzzle in enumerate(puzzles):
        if k % n_update == 0:
            print(f"{k + 1}/{len(puzzles)} ... {(k + 1)/len(puzzles):.5f}%")
        puzzle = str2grid(puzzle)
        tk0 = time.time()
        ## solve
        try:
            my_solution, done, info = solve_sudoku(
                puzzle, 
                verbose=verbose, 
                all_solutions=all_solutions,
                is_X_Sudoku=is_X_Sudoku,
                )
        except SudokuException:
            info = {
                'calls': 0,
                'max depth': 0,
                'nsolutions': 0,
            }
            done = 0
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
    print("nsolutions min-max, mean: %d-%d, %.1f %s %.1f "%(min(metric), max(metric), mean(metric), pm, stdev(metric)))
    print("total solutions: %d" % (sum(metric)))

    print(' ')
    metric = metrics['calls']
    k = argmax(metric)
    print("#puzzle, max calls, max depth: ", k, metric[k], metrics['max depths'][k])
    metric = metrics['max depths']
    k = argmax(metric)
    print("#puzzle, calls, max(max depth):", k, metrics['calls'][k], metric[k])