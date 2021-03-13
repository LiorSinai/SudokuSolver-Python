""""

31 May 2020

Sudoku Solver

"""

from copy import deepcopy, copy
from typing import List, Tuple, Set
import random
import time

from Sudoku import Sudoku, SIZE


def grid_equal(A, B):
    """ Check if 2 grids are equal or not"""
    n = len(A)
    if n != len(B):
        return False
    for i in range(n):
        for j in range(n):
            if A[i][j] != B[i][j]:
                return False
    return True

def get_nonempty(A):
    n = len(A)
    m = len(A[0])
    nonempty = []
    for nm in range(n*m):
        i = nm // n
        j = nm % m
        if A[i][j] != 0:
            nonempty.append(nm)
    return nonempty

def flatten(grid):
    arr = []
    for row in grid:
        arr.extend(row)
    return arr

def unflatten(arr: List[int], n=9):
    grid = []
    for i in range(0, len(arr), n):
        grid.append(arr[i:i+n])
    return grid

def arr2str(arr):
    string = ''
    for digit in arr:
        string += str(digit)
    return string

def str2arr(string):
    arr = []
    end = string.find('-')
    end = len(string) if end == -1 else end
    for c in string[0:end]:
        if c == '.':
            arr.append(0)
        else:
            arr.append(int(c))
    return arr  # [int(c) for c in string]

def grid2str(grid: List[List[int]]) -> str:
    return arr2str(flatten(grid))

def str2grid(string: str) -> List[List[int]]:
    return unflatten(str2arr(string))

def print_grid(grid: List[List[int]]) -> None:
        repr = ''
        for row in grid:
            repr += str(row) + '\n'
        print(repr[:-1])

def solveSudokuBrute(grid):
    """
    Only uses backtracking. Very slow, especially on hard puzzles
    """
    def solve(game, depth=0, ij=0):
        nonlocal calls, depth_max
        calls += 1
        depth_max = depth if depth > depth_max else depth_max
        solved = False
        while not solved:
            if ij == 81:
                solved = game.check_done()
                return game.grid, solved
            i = ij // 9
            j = ij % 9
            if game.grid[i][j] == 0:
                # backtracking check point:
                options = game.find_options(i, j)
                if len(options) == 0:
                    return game.grid, False  # this call is going nowhere
                for y in options:
                    game_next = deepcopy(game)
                    game_next.grid[i][j] = y
                    game_next.place_and_erase(i, j, y)
                    grid_final, solved = solve(
                        game_next, ij=ij+1, depth=depth+1)
                    if solved:
                        break
                return grid_final, solved
            ij += 1

        return game.grid, solved

    calls, depth_max = 0, 0
    game = Sudoku(grid)
    grid, solved = solve(game, depth=0, ij=0)

    info = {'calls': calls, 'max depth': depth_max, 'solutions': 1}
    return grid, solved, info


def solveSudoku(grid, num_boxes=SIZE, verbose=True, all_solutions=False):
    """
    idea based on https://dev.to/aspittel/how-i-finally-wrote-a-sudoku-solver-177g
    Try each step until failure, and repeat:
    1) write numbers with only have 1 option
    2) write candidates with only 1 option/ 2 pairs
    3) with multiple options, take a guess and branch (backtrack)
    """
    def solve(game, depth=0, progress_factor=1):
        nonlocal calls, depth_max, progress, progress_update, update_increment
        calls += 1
        depth_max = max(depth, depth_max)
        solved = False
        while not solved:
            solved = True  # assume solved
            edited = False  # if no edits, either done or stuck
            for i in range(game.n):
                for j in range(game.n):
                    if game.grid[i][j] == 0:
                        solved = False
                        options = game.candidates[i][j]
                        if len(options) == 0:
                            progress += progress_factor
                            return False  # this call is going nowhere
                        elif len(options) == 1:  # Step 1
                            game.place_and_erase(
                                i, j, list(options)[0])  # Step 2
                            # game.flush_candidates() # full grid cleaning
                            edited = True
            if not edited:  # changed nothing in this round -> either done or stuck
                if solved:
                    progress += progress_factor
                    solution_set.append(grid2str(game.grid.copy()))
                    return True
                else:
                    # Find the box with the least number of options and take a guess
                    # The place_and_erase() call changes this dynamically
                    min_guesses = (game.n + 1, -1)
                    for i in range(game.n):
                        for j in range(game.n):
                            options = game.candidates[i][j]
                            if len(options) < min_guesses[0] and len(options) > 1:
                                min_guesses = (len(options), (i, j))
                    i, j = min_guesses[1]
                    options = game.candidates[i][j]
                    # backtracking check point:
                    progress_factor *= (1/len(options))
                    for y in options:
                        game_next = deepcopy(game)
                        game_next.place_and_erase(i, j, y)
                        # game_next.flush_candidates() # full grid cleaning
                        solved = solve(
                            game_next, depth=depth+1, progress_factor=progress_factor)
                        if solved and not all_solutions:
                            break  # return 1 solution
                        if verbose and progress > progress_update:
                            print("%.1f" % (progress*100), end='...')
                            progress_update = (
                                (progress//update_increment) + 1) * update_increment
                    return solved
        return solved

    calls, depth_max = 0, 0
    progress, update_increment, progress_update = 0.0, 0.01, 0.01
    solution_set = []

    game = Sudoku(grid)
    game.flush_candidates()  # check for obvious candidates

    possible, message = game.check_possible()
    if not possible:
        print('Error on board. %s' % message)
        info = {
            'calls': calls,
            'max depth': depth_max,
            'nsolutions': len(solution_set),
        }
        return solution_set, False, info

    if verbose:
        print("solving: ", end='')
    solve(game, depth=0)
    if verbose:
        print("100.0")
    solved = (len(solution_set) >= 1)

    info = {
        'calls': calls,
        'max depth': depth_max,
        'nsolutions': len(solution_set),
        }
    return solution_set, solved, info


if __name__ == '__main__':
    # from https://www.sudokuwiki.org/Weekly_Sudoku.asp
    # 404 'unsolvable'
    puzzle   = '400009200000010080005400006004200001050030060700005300500007600090060000002800007'
    #solution = '468579213279613485135428796384296571951734862726185349513947628897362154642851937'
    # puzzle[0] = 0  # multiple solutions -> 411 solutions

    ## https://theconversation.com/good-at-sudoku-heres-some-youll-never-complete-5234
    # 17 clue puzzle: minimum number of clues for a unique solution to be possible
    #puzzle   ='000700000100000000000430200000000006000509000000000418000081000002000050040000300' #-> 1 unique solution. Very fun to do
    #puzzle  ='000000000100000000000430200000000006000509000000000418000081000002000050040000300' # -> 76_215 solutions

    ## impossible 
    # From https://norvig.com/sudoku.html  -> column 4, no 1 possible because of triple 5-6 doubles and triple 1s
    #puzzle = '.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........'
    ## obvious exclusion
    #puzzle = '12.......34...............5...........5..........................................'
    ## obvious duplicate
    #puzzle =  '11.......34...............5......................................................'

    grid = str2grid(puzzle)
    ## make multiple solutions
    nonempty = get_nonempty(grid)
    for ij in random.sample(nonempty, k=0): #k=number of values to set to zero
        i = ij // 9
        j = ij % 9
        grid[i][j] = 0

    solution = solution if 'solution' in locals() else None

    verbose       = False
    all_solutions = False

    t0 = time.time()
    print_grid(grid)
    nclues = 81 - puzzle.count('.') - puzzle.count('0')
    print("num clues: %d" % nclues)
    ## solve
    solution_set, done, info = solveSudoku(
        grid, 
        verbose=verbose, 
        all_solutions=all_solutions
        )
     # solver_solution, done, info = solveSudokuBrute(puzzle)
    deltaT = time.time() - t0
    print(' ')
    print("total time: %.5fs" % (deltaT))
    for key in ['calls', 'max depth', 'nsolutions']:
        print("%-14s: %d" % (key, info[key]))

    if done:
        solver_grid = str2grid(solution_set[0])
        if solution:
            grid_solution = str2grid(solution)  
            print("The solution is correct: ", grid_equal(solver_grid, grid_solution))
        print_grid(solver_grid)