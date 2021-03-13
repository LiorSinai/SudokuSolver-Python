""""

31 May 2020

Sudoku Solver

"""

from Sudoku import Sudoku
from SudokuSolver import Sudoku, solveSudoku, grid_equal, str2grid, grid2str
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
            self.assertFalse(s.check_possible()[0])
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
            self.assertTrue(s.check_possible()[0])


    def check_solver(self):
        # check sovler using manually solved puzzles
        # easy Sudokus (no backtracking required). From New York Times, 31 May 2020 - 2 June 2020
        puzzles = [
            (
                '280070309600104007745080006064830100102009800000201930006050701508090020070402050',
                '281576349693124587745983216964835172132749865857261934426358791518697423379412658'
            ),
            (
                '910780200027001894684000300000846001740059080009000050106093008000500706002070130',
                '913784265527361894684925317235846971741259683869137452176493528398512746452678139'
            )
            
        ]
        for puzzle, solution in puzzles:
            puzzle, solution = list(map(str2grid, [puzzle, solution]))
            solution_set, done, _ = solveSudoku(puzzle, verbose=False, all_solutions=False)
            self.assertTrue(done)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))
        # medium to hard Sudoku (some backtracking). From New York Times, 31 May 2020 - 2 June 2020
        puzzles = [
            (
                '100020400035040900704000001800000000091032080000100097070900600000000000000450000',
                '189327465235641978764895321827569143491732586653184297372918654546273819918456732'
            ),
            (
                '000832067000600200800700010010020000509004700000008000007000940000005000402000500',
                '195832467743651298826749315318927654569314782274568139657283941931475826482196573'
            ),
            (
                '000010030009005008804006025000000600008004000120087000300900200065008000900000000',
                '752819436639245718814736925473592681598164372126387549387951264265478193941623857'
            )
        ]
        for puzzle, solution in puzzles:
            puzzle, solution =list(map(str2grid, [puzzle, solution]))
            solution_set, done, _ = solveSudoku(puzzle, verbose=False, all_solutions=False)
            self.assertTrue(done)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))


    def check_solved_puzzles(self):
        # these puzzles were sovled with the solver. This is to check solutions still hold.
        puzzles = [
            # from https://dev.to/aspittel/how-i-finally-wrote-a-sudoku-solver-177g
            (   
                # very easy puzzle
                '530070000600195000098000060800060003400803001700020006060000280000419005000080079', 
                '534678912672195348198342567859761423426853791713924856961537284287419635345286179'
             ),
            # https://www.nytimes.com/puzzles/sudoku/
            (
                '106000050070030004090005200002060007000108000047020000000000803003200006000000002' , 
                '186742359275839164394615278812564937639178425547923681721456893953281746468397512'
            ),
            # Arto Inkala Puzzles from  https://norvig.com/sudoku.html
            (   
                # not that hard actually
                '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.', 
                '859612437723854169164379528986147352375268914241593786432981675617425893598736241'
            ),
            (   
                # have to make at least 3 guesses
                '..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..', 
                '145327698839654127672918543496185372218473956753296481367542819984761235521839764'
            ),
            (   
                # have to make at least 3 guesses
                '800000000003600000070090200050007000000045700000100030001000068008500010090000400', 
                '812753649943682175675491283154237896369845721287169534521974368438526917796318452'
            ),
            # 17 clue puzzle from https://theconversation.com/good-at-sudoku-heres-some-youll-never-complete-5234
            (
                #  1 unique solution. Very fun to do
                '000700000100000000000430200000000006000509000000000418000081000002000050040000300', 
                '264715839137892645598436271423178596816549723759623418375281964982364157641957382'
            ),
            # 17 clue puzzle from  https://cracking-the-cryptic.web.app/sudoku/PMhgbbQRRb
            (
                '029000400000500100040000000000042000600000070500000000700300005010090000000000060', 
                '329816457867534192145279638931742586684153279572968314796321845418695723253487961'
            ), 
             # https://www.sudokuwiki.org/Weekly_Sudoku.asp
            (   # May 24 2020 Extreme -> requires multiple diabolical+extreme strategies
                '003100720700000500050240030000720000006000800000014000060095080005000009049002600', 
                '693158724724963518851247936538726491416539872972814365267495183385671249149382657'
            ),
            (   
                #403 'unsolvable' - no known logical solution
                '100200000065074800070006900004000000050008704000030000000000600080000057006007089',
                '138259476965374821472186935824761593653928714791435268517893642389642157246517389'
            ),
            (   
                #404 'unsolvable' - no known logical solution
                '400009200000010080005400006004200001050030060700005300500007600090060000002800007',
                '468579213279613485135428796384296571951734862726185349513947628897362154642851937'
            ),
            (
                # June 7 2020 Extreme
                '080001206000020000020305040060010900002050400008000010030704050000030000406100080',
                '785941236143628795629375841564213978912857463378469512231784659897536124456192387'
            )
        ]
        for puzzle, solution in puzzles:
            puzzle, solution = str2grid(puzzle), str2grid(solution)
            solution_set, done, _ = solveSudoku(puzzle, verbose=False, all_solutions=False)
            self.assertTrue(done)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))


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
    # end game
    suite.addTest(SudokuTest('check_done'))
    # smoke test
    suite.addTest(SudokuTest('check_solver'))
    suite.addTest(SudokuTest('check_solved_puzzles'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())