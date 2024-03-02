""""

31 May 2020

Sudoku class

"""
from typing import List, Tuple, Set
from itertools import combinations

SIZE = 9
BOX_SIZE = 3


class Sudoku():
    def __init__(self, grid: List[List[int]], is_X_Sudoku=False, is_hyper_Sudoku=False, is_cross_Sudoku=False):
        n = len(grid)
        assert len(grid[0]) == n, "Grid is not square. n_rows=%d, n_columns=%d" % (n, len(grid[0]))
        self.grid = grid
        self.n = n
        self.groups = dict()
        self.create_rows_and_columns(n)
        self.create_boxes(n)
        if is_X_Sudoku:
            self.create_diagonals(n)
        if is_hyper_Sudoku:
            self.create_hyper_boxes()
        if is_cross_Sudoku:
            self.create_cross()
        # create reverse maps to groups
        self.cells = []
        for i in range(n):
            row = []
            for j in range(n):
                cell = []
                for g in self.groups.values():
                    if (i, j) in g:
                        cell.append(g)
                row.append(cell)
            self.cells.append(row)
        candidates = []
        for i in range(n):
            row = []
            for j in range(n):
                if grid[i][j] == 0:
                    row.append(self.find_options(i, j))
                else:
                    row.append(set())
            candidates.append(row)
        self.candidates = candidates

    def __repr__(self) -> str:
        repr = ''
        for row in self.grid:
            repr += str(row) + '\n'
        return repr

    def create_rows_and_columns(self, n):
        for c in range(n):
            row = [(c, j) for j in range(n)]
            col = [(i, c) for i in range(n)]
            self.groups[f'row {c}'] = row
            self.groups[f'column {c}'] = col

    def create_boxes(self, n):
        for i0 in range(0, n, BOX_SIZE):
            for j0 in range(0, n, BOX_SIZE):
                box = []
                for i in range(i0, i0 + BOX_SIZE):
                    for j in range(j0, j0 + BOX_SIZE):
                        box.append((i, j))
                self.groups[f'box ({i0},{j0})'] = box
        
    def create_diagonals(self, n):
        diag_top_left_to_bottom_right = [(i, i) for i in range(n)]
        diag_top_right_to_bottom_left = [(i, n - i - 1) for i in range(n)]
        self.groups['diagonal 0'] = diag_top_left_to_bottom_right
        self.groups['diagonal 1'] = diag_top_right_to_bottom_left

    def create_hyper_boxes(self):
        self.groups['box 1'] = [(i, j) for i in [1, 2, 3] for j in [1, 2, 3]]
        self.groups['box 2'] = [(i, j) for i in [1, 2, 3] for j in [5, 6, 7]]
        self.groups['box 3'] = [(i, j) for i in [5, 6, 7] for j in [1, 2, 3]]
        self.groups['box 4'] = [(i, j) for i in [5, 6, 7] for j in [5, 6, 7]]

    def create_cross(self):
        cross = {
            (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
            (4, 2), (4, 3), (4, 5), (4, 6)
        }
        self.groups['cross'] = cross
        # create a grid of viable candidates for each position


    def get_values(self, group: str):
        values = [self.grid[i][j] for (i, j) in self.groups[group]]
        return values
    
    def get_box_inds(self, r: int, c: int) -> List[Tuple[int, int]]:
        i0 = (r // BOX_SIZE) * BOX_SIZE  # get first row index
        j0 = (c // BOX_SIZE) * BOX_SIZE  # get first column index
        inds_box = self.groups[f'box ({i0},{j0})']
        return inds_box

    def get_neighbour_inds(self, r: int, c: int, flatten=False):
        neighbours = self.cells[r][c]
        if flatten:
            return list(set().union(*neighbours))
        return neighbours

    def find_options(self, r: int, c: int) -> Set:
        nums = set(range(1, SIZE + 1))
        used = set()
        for group in self.cells[r][c]:
            used |= set([self.grid[i][j] for (i, j) in group])
        valid = nums.difference(used)
        return valid

    @staticmethod
    def counting(arr: List[int], m=SIZE) -> List[int]:
        """ count occurrences in an array """
        count = [0] * (m + 1)
        for x in arr:
            count[x] += 1
        return count

    @staticmethod
    def all_unique(arr: List[int], m=SIZE) -> bool:
        """ verify that all numbers are used, and at most once """
        count = Sudoku.counting(arr, m=m)
        for c in count[1:]:  # ignore 0
            if c != 1:
                return False # not unique
        return True

    @staticmethod
    def no_duplicates(arr: List[int]):
        """ verify that no number is used more than once """
        count = Sudoku.counting(arr)
        for c in count[1:]:  # exclude 0:
            if c > 1:
                return False  # more than 1 of value
        return True

    @staticmethod
    def all_exist(arr: List[int]):
        """ verify that there is at least one of each number present """
        count = Sudoku.counting(arr)
        missing = None
        for num, c in enumerate(count[1:]):  # exclude 0:
            if c == 0:
                return False, num+1  # no value or candidate exists
        return True, missing

    def check_done(self) -> bool:
        """ check if each row/column/box only has unique elements"""
        # check rows
        for key in self.groups:
            if not Sudoku.all_unique(self.get_values(key)):
                return False
        return True
    
    def get_candidates(self, indices: List[Tuple[int, int]]):
        " get candidates within two corners of a rectangle/column/row"
        candidates = set()
        for (i, j) in indices:
                candidates = candidates | self.candidates[i][j]
        return candidates
    
    def get_candidates_box(self, start: Tuple[int, int], end: Tuple[int, int]):
        " get candidates within two corners of a rectangle/column/row"
        candidates = set()
        for i in range(start[0], end[0] + 1):
            for j in range(start[1], end[1] + 1):
                candidates = candidates | self.candidates[i][j]
        return candidates

    def check_possible(self):
        """ check if each row/column/box can have all unique elements"""
        # get rows
        for key, inds in self.groups.items():
            arr = [self.grid[i][j] for (i, j) in inds]
            if not Sudoku.no_duplicates(arr):
                raise SudokuException('Duplicate values in %s' % (key))
            arr += list(self.get_candidates(inds))
            possible, missing_num = Sudoku.all_exist(arr)
            if not possible:
                raise SudokuException('%d not placeable in %s' % (missing_num, key))
        return True

    ## ------- Candidate functions -------- ##
    def place_and_erase(self, r: int, c: int, x: int, constraint_prop=True):
        """ remove x as a candidate in the grid in this row, column and box"""
        # place candidate x
        self.grid[r][c] = x
        self.candidates[r][c] = set()
        # remove candidate x in neighbours
        inds_neighbours = self.get_neighbour_inds(r, c, flatten=True)
        erased = [(r, c)]  # set of indices for constraint propogration
        erased += self.erase([x], inds_neighbours, [])
        # constraint propagation, through every index that was changed
        while erased and constraint_prop:
            i, j = erased.pop()
            inds_neighbours = self.get_neighbour_inds(i, j, flatten=False)
            for inds in inds_neighbours:
                uniques = self.get_unique(inds, type=[1, 2, 3])
                for inds_combo, combo in uniques:
                    # passing back the erased here doesn't seem to be very helpful
                    self.set_candidates(combo, inds_combo)
                    erased += self.erase(combo, inds, inds_combo)
            inds_box = self.get_box_inds(i, j)
            pointers = self.pointing_combos(inds_box)
            for line, inds_pointer, num in pointers:
                erased += self.erase(num, line, inds_pointer)
        # keeps = self.box_line_reduction(inds_box) # doesn't work??
        # for inds_keep, nums in keeps:
        #     self.erase(nums, inds_box, inds_keep)

    def erase(self, nums: List[int], indices: List[Tuple[int, int]], keep: List[Tuple[int, int]]):
        """ erase nums as candidates in indices, but not in keep"""
        erased = []
        for i, j in indices:
            edited = False
            if ((i, j) in keep):
                continue
            for x in nums:
                if (x in self.candidates[i][j]):
                    self.candidates[i][j].remove(x)
                    edited = True
            if edited:
                erased.append((i, j))
        return erased

    def set_candidates(self, nums: List[int], indices: List[Tuple[int, int]]):
        """set candidates at indices. Remove all other candidates"""
        erased = []
        for i, j in indices:
            # beware triples where the whole triple is not in each box
            old = self.candidates[i][j].intersection(nums)
            if self.candidates[i][j] != old:
                self.candidates[i][j] = old.copy()
                erased.append((i, j))  # made changes here
        return erased

    def count_candidates(self, indices: List[Tuple[int, int]]):
        count = [[] for _ in range(self.n + 1)]
        # get counts
        for i, j in indices:
            for num in self.candidates[i][j]:
                count[num].append((i, j))
        return count

    def get_unique(self, indices: List[Tuple[int, int]], type=(0, 1, 2)):
        # See documentation at https://www.sudokuwiki.org/Hidden_Candidates
        groups = self.count_candidates(indices)
        uniques = []  # final set of unique candidates to return
        uniques_temp = {2: [], 3: []}  # potential unique candidates
        for num, group_inds in enumerate(groups):
            c = len(group_inds)
            if c == 1 and (1 in type):
                uniques.append((group_inds, [num]))
            if c == 2 and ((2 in type) or (3 in type)):
                uniques_temp[2].append(num)
            if c == 3 and (3 in type):
                uniques_temp[3].append(num)
        uniques_temp[3] += uniques_temp[2]
        # check for matching combos (both hidden and naked)
        for c in [2, 3]:
            if c not in type:
                continue
            # make every possible combination
            for combo in list(combinations(uniques_temp[c], c)):
                group_inds = set(groups[combo[0]])
                for k in range(1, c):
                    # if positions are shared, this will not change the length
                    group_inds = group_inds | set(groups[combo[k]])
                if len(group_inds) == c:
                    # unique combo (pair or triple) found
                    uniques.append((list(group_inds), combo))
        return uniques

    def pointing_combos(self, inds_box):
        # See documentation https://www.sudokuwiki.org/Intersection_Removal
        # inds_box should come from self.get_inds_box()
        groups = self.count_candidates(inds_box)
        pointers = []
        for num, indices in enumerate(groups):
            # need a pair or triple
            if len(indices) == 2 or len(indices) == 3:
                row_same, col_same = True, True
                i0, j0 = indices[0]
                for i, j in indices[1:]:
                    row_same = row_same and (i == i0)
                    col_same = col_same and (j == j0)
                if row_same:
                    line = [(i0, j) for j in range(self.n)]
                    pointers.append((line, indices, [num]))
                if col_same:
                    line = [(i, j0) for i in range(self.n)]
                    pointers.append((line, indices, [num]))
        return pointers

    def box_line_reduction(self, inds_box):
        # See documentation https://www.sudokuwiki.org/Intersection_Removal
        # inds_box should come from self.get_inds_box()
        keeps = []
        i0, j0 = inds_box[0]
        i1, j1 = min(i0 + BOX_SIZE, self.n - 1), min(j0 + BOX_SIZE, self.n - 1)
        # check rows
        for i in range(i0, i1 + 1):
            row = self.get_candidates_box((i, j0), (i, j1))
            line = self.get_candidates_box(
                (i, 0), (i, j0 - 1)) | self.get_candidates_box((i, j1 + 1), (i, self.n - 1))
            uniques = row.difference(line)
            if uniques:
                keeps.append(
                    ([(i, j) for j in range(j0, j1 + 1)], list(uniques)))
        # check columns
        for j in range(j0, j1 + 1):
            col = self.get_candidates_box((i0, j), (i1, j))
            line = self.get_candidates_box(
                (0, j), (i0 - 1, j)) | self.get_candidates_box((i1 + 1, j), (self.n - 1, j))
            uniques = col.difference(line)
            if uniques:
                keeps.append(
                    ([(i, j) for i in range(i0, i1 + 1)], list(uniques)))
        return keeps

    def flush_candidates(self) -> None:
        """set candidates across the whole grid, according to logical strategies"""
        # get indices for each set
        for _ in range(1):  # repeat this process in case changes are made
            # apply strategies
            for inds in self.groups.values():
                # hidden/naked singles/pairs/triples
                uniques = self.get_unique(inds, type=[1, 2])
                for inds_combo, combo in uniques:
                    self.erase(combo, inds, inds_combo)
                    self.set_candidates(combo, inds_combo)
            inds_boxes = [(inds) for (key, inds) in self.groups.items() if key.startswith('box')]
            for inds in inds_boxes:
                # pointing pairs
                pointers = self.pointing_combos(inds)
                for line, inds_pointer, num in pointers:
                    self.erase(num, line, inds_pointer)
                # box-line reduction
                # keeps = self.box_line_reduction(inds)
                # for inds_keep, nums in keeps:
                #     self.erase(nums, inds, inds_keep)
                    
class SudokuException(Exception):
    pass
