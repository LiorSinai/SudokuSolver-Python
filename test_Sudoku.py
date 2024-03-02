""""

31 May 2020

Sudoku Solver

"""

from Sudoku import Sudoku, SudokuException
from solver import grid_equal
from str2grid import str2grid
import unittest


class SudokuTest(unittest.TestCase):
    #def setup(self):
    def check_unique_test(self):
        s = Sudoku([[1]])
        arr = [1,2 ,3, 4, 5]
        self.assertTrue(s.no_duplicates(arr))
        arr = [1,2 ,2, 1]
        self.assertFalse(s.no_duplicates(arr))
        arr = [i for i in range(10)]    
        self.assertTrue(s.no_duplicates(arr))
        arr += [9]
        self.assertFalse(s.no_duplicates(arr))


    def check_row_test(self):
        grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                [2, 0, 0, 0, 0, 0, 0, 0, 0], 
                [3, 3, 0, 0, 0, 0, 0, 0, 0], 
                [4, 0, 0, 0, 0, 0, 0, 0, 0], 
                [5, 0, 0, 0, 0, 0, 0, 0, 0],
                [6, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 0, 0],
                [9, 0, 0, 0, 0, 0, 0, 0, 0]]
        s = Sudoku(grid)
        self.assertTrue(s.no_duplicates(grid[0]))
        self.assertTrue(s.no_duplicates(grid[1]))
        self.assertFalse(s.no_duplicates(grid[2]))


    def check_col_test(self):
        grid = [[1, 9, 3, 4, 5, 6, 7, 8, 9],
                 [2, 8, 1, 0, 0, 0, 0, 0, 0], 
                 [3, 7, 2, 0, 0, 0, 0, 0, 0], 
                 [4, 6, 3, 0, 0, 0, 0, 0, 0], 
                 [5, 5, 4, 0, 0, 0, 0, 0, 0],
                 [6, 4, 5, 0, 0, 0, 0, 0, 0],
                 [7, 3, 6, 0, 0, 0, 0, 0, 0],
                 [8, 2, 7, 0, 0, 0, 0, 0, 0],
                 [9, 1, 8, 0, 0, 0, 0, 0, 0]]
        s = Sudoku(grid)
        self.assertEqual(s.get_col(0), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertTrue(s.no_duplicates(s.get_col(0)))
        self.assertEqual(s.get_col(1), [9, 8, 7, 6, 5, 4, 3, 2, 1])
        self.assertTrue(s.no_duplicates(s.get_col(1)))
        self.assertEqual(s.get_col(3), [4, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(s.no_duplicates(s.get_col(3)))
        self.assertEqual(s.get_col(2), [3, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertFalse(s.no_duplicates(s.get_col(2)))

    
    def check_box_test(self):
        grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [4, 5, 6, 0, 0, 0, 0, 0, 0], 
                 [7, 8, 9, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 1, 2, 2, 0, 0, 0], 
                 [0, 0, 0, 4, 5, 6, 0, 0, 0],
                 [0, 0, 0, 7, 8, 8, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        s = Sudoku(grid)
        # different indices for the upper left box:
        box = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(s.get_box(0,0), box)
        self.assertEqual(s.get_box(1,2), box)
        self.assertEqual(s.get_box(2,2), box)
        self.assertTrue(s.no_duplicates(s.get_box(0, 0)))
        # different indices for the middle box:
        box = [1, 2, 2, 4, 5, 6, 7, 8, 8]
        self.assertEqual(s.get_box(4,4), box)
        self.assertEqual(s.get_box(3,3), box)
        self.assertEqual(s.get_box(3,5), box)
        self.assertFalse(s.no_duplicates(s.get_box(4, 4)))

    
    def find_options_test(self):
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        s = Sudoku(grid)
        self.assertEqual(s.find_options(0, 2), {1, 2, 4})
        self.assertEqual(s.find_options(4, 4), {5})
        self.assertEqual(s.find_options(5, 1), {1, 5})
        self.assertEqual(s.find_options(8, 6), {1, 3, 4, 6})


    def candidates_test(self):
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        candidates = [
            [set(), set(), {1, 2, 4}, {2, 6}, set(), {8, 2, 4, 6}, {8, 1, 4, 9}, {1, 2, 4, 9}, {8, 2, 4}],
            [set(), {2, 4, 7}, {2, 4, 7}, set(), set(), set(), {8, 3, 4, 7}, {2, 3, 4}, {8, 2, 4, 7}],
            [{1, 2}, set(), set(), {2, 3}, {3, 4}, {2, 4}, {1, 3, 4, 5, 7}, set(), {2, 4, 7}],
            [set(), {1, 2, 5}, {1, 2, 5, 9}, {9, 5, 7}, set(), {1, 4, 7}, {9, 4, 5, 7}, {9, 2, 4, 5}, set()],
            [set(), {2, 5}, {9, 2, 5, 6}, set(), {5}, set(), {9, 5, 7}, {9, 2, 5}, set()],
            [set(), {1, 5}, {1, 3, 5, 9}, {9, 5}, set(), {1, 4}, {8, 9, 4, 5}, {9, 4, 5}, set()],
            [{1, 3, 9}, set(), {1, 3, 4, 5, 7, 9}, {3, 5, 7}, {3, 5}, {7}, set(), set(), {4}],
            [{2, 3}, {8, 2, 7}, {2, 3, 7}, set(), set(), set(), {3, 6}, {3}, set()],
            [{1, 2, 3}, {1, 2, 4, 5}, {1, 2, 3, 4, 5}, {2, 3, 5, 6}, set(), {2, 6}, {1, 3, 4, 6}, set(), set()]
        ]
        s = Sudoku(grid)
        self.assertTrue(grid_equal(candidates, s.candidates))
        # test uniques
        inds = [(0, j) for j in range(9)] # no unique candidates
        #self.assertEqual(s.get_unique(inds), [])
        self.assertEqual(s.get_unique(inds, type=[1]), [] )
        inds = [(7, j) for j in range(9)] # uniques: 8 at (7, 1)  and 6 at (7, 6)
        #self.assertEqual(s.get_unique(inds), [([(7, 6)], [6]), ([(7, 1)], [8])] ) #[(6, (7, 6)), (8, (7, 1))])
        self.assertEqual(s.get_unique(inds, type=[1]), [([(7, 6)], [6]), ([(7, 1)], [8])] )
        inds = s.get_box_inds(5, 6)  # middle right box. unique 8 at (5,6)
        #self.assertEqual(s.get_unique(inds), [([(5, 6)], [8])])
        self.assertEqual(s.get_unique(inds, type=[1]), [([(5, 6)], [8])] )
        # test erase function
        s.place_and_erase(0, 2, 1, constraint_prop=False) 
        self.assertEqual(s.candidates[0], [set(), set(), set(), {2, 6}, set(), {8, 2, 4, 6}, {8, 4, 9}, {2, 4, 9}, {8, 2, 4}])
        col = [s.candidates[i][2] for i in range(9)]
        self.assertEqual(col, [set(), {2, 4, 7}, set(), {2, 5 ,9}, {2, 5, 6, 9}, {3, 5, 9}, {3, 4, 5, 7, 9}, {2, 3, 7}, {2, 3, 4, 5}])


    def candidates_advanced(self):
        grid = [
            [0, 8, 0, 0, 0, 1, 2, 0, 6],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 2, 0, 3, 0, 5, 0, 4, 0],
            [0, 6, 0, 0, 1, 0, 9, 0, 0],
            [0, 0, 2, 0, 5, 0, 4, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 1, 0],
            [0, 3, 0, 7, 0, 4, 0, 5, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [4, 0, 6, 1, 0, 0, 0, 8, 0]
        ] # June 7 Extreme 'https://www.sudokuwiki.org
        s = Sudoku(grid)
        candidates = [
            [{9, 3, 5, 7}, set(), {3, 4, 5, 7, 9}, {9, 4}, {9, 4, 7}, set(), set(), {9, 3, 7}, set()],
            [{1, 3, 5, 6, 7, 9}, {1, 4, 5, 7, 9}, {1, 3, 4, 5, 7, 9}, {8, 9, 4, 6}, set(), {8, 9, 6, 7}, {1, 3, 5, 7, 8}, {9, 3, 7}, {1, 3, 5, 7, 8, 9}],
            [{1, 9, 6, 7}, set(), {1, 9, 7}, set(), {8, 9, 6, 7}, set(), {8, 1, 7}, set(), {8, 1, 9, 7}],
            [{3, 5, 7}, set(), {3, 4, 5, 7}, {8, 2, 4}, set(), {8, 2, 3, 7}, set(), {2, 3, 7}, {2, 3, 5, 7, 8}],
            [{1, 3, 9, 7}, {1, 9, 7}, set(), {8, 9, 6}, set(), {3, 6, 7, 8, 9}, set(), {3, 6, 7}, {8, 3, 7}],
            [{9, 3, 5, 7}, {9, 4, 5, 7}, set(), {9, 2, 4, 6}, {9, 4, 6, 7}, {2, 3, 6, 7, 9}, {3, 5, 6, 7}, set(), {2, 3, 5, 7}],
            [{8, 1, 2, 9}, set(), {1, 9}, set(), {8, 9, 6}, set(), {1, 6}, set(), {1, 2, 9}],
            [{1, 2, 5, 7, 8, 9}, {1, 5, 9, 7}, {1, 5, 9, 7}, {2, 5, 6, 8, 9}, set(), {8, 9, 2, 6}, {1, 6, 7}, {9, 2, 6, 7}, {1, 2, 4, 7, 9}],
            [set(), {9, 5, 7}, set(), set(), {9}, {9, 2}, {3, 7}, set(), {9, 2, 3, 7}]
        ]
        self.assertTrue(grid_equal(candidates, s.candidates))
        inds = [(i, 0) for i in range(9)]
        #self.assertEqual(s.get_pairs(inds), [([(6, 0), (7, 0)], (2, 8))])
        uniques = s.get_unique(inds, type=[2])[0]
        uniques[0].sort()
        self.assertEqual(uniques, ([(6, 0), (7, 0)], (2, 8)) )
        grid = [
            [0, 0, 0, 0, 0, 1, 0, 3, 0],
            [2, 3, 1, 0, 9, 0, 0, 0, 0],
            [0, 6, 5, 0, 0, 3, 1, 0, 0],
            [6, 7, 8, 9, 2, 4, 3, 0, 0],
            [1, 0, 3, 0, 5, 0, 0, 0, 6],
            [0, 0, 0, 1, 3, 6, 7, 0, 0],
            [0, 0, 9, 3, 6, 0, 5, 7, 0],
            [0, 0, 6, 0, 1, 9, 8, 4, 3],
            [3, 0, 0, 0, 0, 0, 0, 0, 0]
        ] # https://www.sudokuwiki.org/Hidden_Candidates#HP
        s = Sudoku(grid)
        inds = [(0, j) for j in range(9)]
        uniques = s.get_unique(inds, type=[3])[0]
        uniques[0].sort()
        self.assertEqual(uniques, ([(0, 3), (0, 6), (0, 8)], (2, 5, 6)) )
        s.candidates[0][8] = {2, 5}
        inds = [(i, 8) for i in range(9)]
        uniques = s.get_unique(inds, type=[3])[0]
        uniques[0].sort()
        self.assertEqual(uniques, ([(1, 8), (2, 8), (5, 8)], (4, 8, 7)) )
        

    def check_done(self):
        # Easy 
        puzzle = '280070309600104007745080006064830100102009800000201930006050701508090020070402050'
        solution= '281576349693124587745983216964835172132749865857261934426358791518697423379412658'
        puzzle, solution = str2grid(puzzle), str2grid(solution)
        s = Sudoku(puzzle)
        self.assertFalse(s.check_done())
        s = Sudoku(solution)
        self.assertTrue(s.check_done())
        # Medium
        puzzle = '100020400035040900704000001800000000091032080000100097070900600000000000000450000'
        solution = '189327465235641978764895321827569143491732586653184297372918654546273819918456732'
        puzzle, solution = str2grid(puzzle), str2grid(solution)
        s = Sudoku(puzzle)
        self.assertFalse(s.check_done())
        s = Sudoku(solution)
        self.assertTrue(s.check_done())


    def impossible_test(self):
        # impossible
        puzzles = [
            # From https://norvig.com/sudoku.html  -> column 4, no 1 possible because of triple 5-6 doubles and triple 1s
            '.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........',  
            # obvious doubles
            '12.......34...............5...........5..........................................',  
            '11.......34...............5......................................................',
        ]
        for puzzle in puzzles:
            puzzle = str2grid(puzzle)
            s = Sudoku(puzzle)
            s.flush_candidates()
            self.assertRaises(SudokuException, s.check_possible)
        # possible
        puzzles = [
            '280070309600104007745080006064830100102009800000201930006050701508090020070402050',  
            '000010030009005008804006025000000600008004000120087000300900200065008000900000000',  
            '1.....................................5..........................................',
        ]
        for puzzle in [puzzles[1]]:
            puzzle = str2grid(puzzle)
            s = Sudoku(puzzle)
            s.flush_candidates()
            self.assertTrue(s.check_possible())

    def impossible_x_test(self):
        # impossible
        puzzles = [
            # two 2s on a diagonal
            '060050200000000060532008000000049103000100050000000007005010008004000006000006502',  
            # two 7s on a diagonal
            '030040200520006700000000000080020170000070000050000003407000032000600000000080691',
        ]
        for puzzle in puzzles:
            puzzle = str2grid(puzzle)
            s = Sudoku(puzzle, is_X_Sudoku=False)
            s.flush_candidates()
            self.assertTrue(s.check_possible())
            # now try with X-Sudoku rules:
            s = Sudoku(puzzle, is_X_Sudoku=True)
            s.flush_candidates()
            self.assertRaises(SudokuException, s.check_possible)
        # possible
        puzzles = [
            '030040200520006700000000000080020170000070000050000003400000032000600000000080691',  
            '060050200000000060532008000000049103000100050000000007005010008004000006000006500',  
        ]
        for puzzle in [puzzles[1]]:
            puzzle = str2grid(puzzle)
            s = Sudoku(puzzle)
            s.flush_candidates()
            self.assertTrue(s.check_possible())


def suite():
    "Set order of tests in ascending order of complexity and code required"
    suite = unittest.TestSuite()
    # basic checks
    suite.addTest(SudokuTest('check_unique_test'))
    suite.addTest(SudokuTest('check_row_test'))
    suite.addTest(SudokuTest('check_col_test'))
    suite.addTest(SudokuTest('check_box_test'))
    # find options
    suite.addTest(SudokuTest('find_options_test'))
    # candidates
    suite.addTest(SudokuTest('candidates_test'))
    suite.addTest(SudokuTest('candidates_advanced'))
    suite.addTest(SudokuTest('impossible_test'))
    suite.addTest(SudokuTest('impossible_x_test'))
    # end game
    suite.addTest(SudokuTest('check_done'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())