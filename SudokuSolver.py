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

def solveSudokuBrute(grid):
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
    # idea based on https://dev.to/aspittel/how-i-finally-wrote-a-sudoku-solver-177g
    # Try each step until failure, and repeat:
    # 1) write numbers with only have 1 option
    # 2) write candidates with only 1 option/ 2 pairs
    # 3) with multiple options, take a guess and branch (backtrack)
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
                        #options = game.find_options(i, j)
                        if len(options) == 0:
                            progress += progress_factor
                            return game.grid, False  # this call is going nowhere
                        elif len(options) == 1:  # Step 1
                            #game.grid[i][j] = list(options)[0]
                            game.place_and_erase(
                                i, j, list(options)[0])  # Step 2
                            # game.flush_candidates() # full grid cleaning
                            edited = True
            if not edited:  # changed nothing in this round -> either done or stuck
                if solved:
                    progress += progress_factor
                    solution_set.append(grid2str(game.grid.copy()))
                    #print(len(solution_set), solution_set[-1])
                    return game.grid, True
                else:
                    # Find the box with the least number of options and take a guess
                    # The erase() changes this dynamically in the previous for loop
                    min_guesses = (game.n + 1, -1)
                    for i in range(game.n):
                        for j in range(game.n):
                            options = game.candidates[i][j]
                            #options = game.find_options(i, j)
                            if len(options) < min_guesses[0] and len(options) > 1:
                                min_guesses = (len(options), (i, j))
                    i, j = min_guesses[1]
                    options = game.candidates[i][j]
                    #options = game.find_options(i, j)
                    # backtracking check point:
                    progress_factor *= (1/len(options))
                    for y in options:
                        game_next = deepcopy(game)
                        #game_next.grid[i][j] = y
                        game_next.place_and_erase(i, j, y)
                        # game_next.flush_candidates() # full grid cleaning
                        grid_final, solved = solve(
                            game_next, depth=depth+1, progress_factor=progress_factor)
                        if solved and not all_solutions:
                            break  # return 1 solution
                        if progress > progress_update and verbose:
                            print("%.1f" % (progress*100), end='...')
                            progress_update = (
                                (progress//update_increment) + 1) * update_increment
                    return grid_final, solved
        return game.grid, solved

    calls, depth_max = 0, 0
    progress, update_increment, progress_update = 0, 0.01, 0.01
    solution_set = []

    game = Sudoku(grid)
    game.flush_candidates()  # check for obvious candidates

    possible, message = game.check_possible()
    if not possible:
        print('Error on board. %s' % message)
        info = {
            'calls': calls,
            'max depth': depth_max,
            'solutions': len(solution_set),
            'solution set': solution_set
        }
        return grid, False, info

    grid_final, solved = solve(game, depth=0)

    if len(solution_set) >= 1:
        solved = True
        grid_final = unflatten(str2arr(solution_set[0]))

    info = {
        'calls': calls,
        'max depth': depth_max,
        'solutions': len(solution_set),
        'solution set': solution_set}
    return grid_final, solved, info


if __name__ == '__main__':
    # from https://dev.to/aspittel/how-i-finally-wrote-a-sudoku-solver-177g
    # very easy puzzle
    # puzzle = '530070000600195000098000060800060003400803001700020006060000280000419005000080079'
    # solution = '530070000600195000098000060800060003400803001700020006060000280000419005000080079'

    # from https://www.sudokuwiki.org/Weekly_Sudoku.asp
    # puzzle = '100200000065074800070006900004000000050008704000030000000000600080000057006007089' #403 'unsolvable' - no known logical solution
    # 404 'unsolvable'
    # puzzle = '400009200000010080005400006004200001050030060700005300500007600090060000002800007'
    # puzzle[0] = 0  # multiple solutions -> 411 solutions
    # puzzle = '080001206000020000020305040060010900002050400008000010030704050000030000406100080' # June 7 Extreme
    # May 24 Extreme -> requires multiple diabolical+extreme strategies
    # puzzle = '003100720700000500050240030000720000006000800000014000060095080005000009049002600'
    # solution = '693158724724963518851247936538726491416539872972814365267495183385671249149382657'

    # https://www.nytimes.com/puzzles/sudoku/
    #puzzle   = '106000050070030004090005200002060007000108000047020000000000803003200006000000002'
    #solution = '186742359275839164394615278812564937639178425547923681721456893953281746468397512'

    # https://norvig.com/sudoku.html
    # puzzle = '.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........'  # impossible puzzle with no solution -> column 4, no 1 possible because of triple 5-6 doubles and triple 1s
    # Arto Inkala Puzzles
    # puzzle =   '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'  # not that hard actually
    #solution = '859612437723854169164379528986147352375268914241593786432981675617425893598736241'
    # puzzle =   '..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..' # have to make at least 3 guesses
    #solution = '145327698839654127672918543496185372218473956753296481367542819984761235521839764'
    # have to make at least 3 guesses
    # puzzle = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'
    # solution = '812753649943682175675491283154237896369845721287169534521974368438526917796318452'

    # https://theconversation.com/good-at-sudoku-heres-some-youll-never-complete-5234
    # 17 clue puzzle: minimum number of clues for a unique solution to be possible
    # puzzle   ='000700000100000000000430200000000006000509000000000418000081000002000050040000300' #-> 1 unique solution. Very fun to do
    # puzzle   ='000000000100000000000430200000000006000509000000000418000081000002000050040000300'# -> 76215 solutions
    #solution ='264715839137892645598436271423178596816549723759623418375281964982364157641957382'
    # https://cracking-the-cryptic.web.app/sudoku/PMhgbbQRRb
    #puzzle =   '029000400000500100040000000000042000600000070500000000700300005010090000000000060'
    #solution = '329816457867534192145279638931742586684153279572968314796321845418695723253487961'

    # find non-zero entries
    #nonempty = get_nonempty(puzzle)
    # nonempty = 81 - puzzle.count('.') - puzzle.count('0')
    # print("num clues: %d" % nonempty)
    # make multiple solutions
    # for ij in random.sample(nonempty, k=0):
    #     i = ij // 9
    #     j = ij % 9
    #     puzzle[i][j] = 0

    # puzzles = [puzzle]
    # solutions = [solution]

    # from https://norvig.com/sudoku.html. Solver at https://www.sudokuwiki.org/sudoku.htm can solve 67, but not 6
    # file_name = 'sudoku_top95' + '.txt'

    # file_name = 'sudoku_hardest'  +'.txt' # from https://norvig.com/sudoku.html
    # file_name = 'Sudoku_NY' +'.txt'  # from the New York Times
    # with open(file_name, 'r') as f:
    #     puzzles = f.read().strip().split('\n')
    # eel.
    puzzles = "52...6.........7.13...........4..8..6......5...........418.........3..2...87.....".strip().split('\n')
    # t0 = time.time()
    # max_t = [0, -1]  # time, k
    max_calls, max_depth = [0, 0, -1], [0, 0, -1]  # [calls, max depth, k]
    num_solved = 0
    mean_calls = 0
    for k, puzzle in enumerate(puzzles):
        # for k, puzzle in enumerate([puzzles[86]]):
        # print
        #S = Sudoku(str2grid(puzzle))
        # print(S)
        # solve
        # tk0 = time.time()
        puzzle = str2grid(puzzle)
        my_solution, done, info = solveSudoku(
            puzzle, verbose=False, all_solutions=False)
        #my_solution, done, info = solveSudokuBrute(puzzle)
        # deltaTk = time.time() - tk0
        num_solved += done
        # update average
        mean_calls = (mean_calls * k + info['calls']) / (k + 1)
        # set maximums
        # max_t = max(max_t, [deltaTk, k])
        max_calls = max(max_calls, [info['calls'], info['max depth'], k])
        # max_depth = max(max_depth, [info['calls'],
        # info['max depth'], k], key=lambda x: x[1])
        if info['solutions'] > 1:
            print('error: puzzle %d has %d solution' % (k, info['solutions']))
    # deltaT = time.time() - t0
    # print(' ')
    # print("number solved: %d/%d" % (num_solved, len(puzzles)))
    # print("total time: %.5fs; average time: %.5fs," %
    #       (deltaT, deltaT/len(puzzles)))
    # print("max time, # puzzle ", max_t)
    # print("max calls, depth, # puzzle:", max_calls)
    # print("calls, max(max depth), # puzzle:", max_depth)
    # print("average calls: %.1f" % mean_calls)

    # print(' ')
    # print("Solutions:", info['solutions'])
    # solution = str2grid(solutions[k])
    # print("The solution is correct: ", grid_equal(my_solution, solution))
    # S = Sudoku(my_solution)
    # print(S)
    print(info['solution set'][0])
