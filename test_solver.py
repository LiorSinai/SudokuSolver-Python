from Sudoku import Sudoku
from solver import solve_sudoku, grid_equal, str2grid
import unittest


class SudokuSolverTest(unittest.TestCase):
    def check_solver(self):
        # check solver using manually solved puzzles
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
            solution_set, done, _ = solve_sudoku(puzzle, verbose=False, all_solutions=False)
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
            solution_set, done, _ = solve_sudoku(puzzle, verbose=False, all_solutions=False)
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
            solution_set, done, _ = solve_sudoku(puzzle, verbose=False, all_solutions=False)
            self.assertTrue(done)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))


    def solve_X_sudoku(self):
        puzzles = [
            (
                '060050200000000060532008000000049103000100050000000007005010008004000006000006500',
                '968751234741392865532468719257649183493187652186235497675914328814523976329876541'
            ),
            (
                '030040200520006700000000000080020170000070000050000003400000032000600000000080691',
                '638547219521936748749218365984325176362179584157864923496751832813692457275483691'
            )
        ]
        for puzzle, solution in puzzles:
            puzzle, solution = str2grid(puzzle), str2grid(solution)
            solution_set, done, info = solve_sudoku(puzzle, verbose=False, all_solutions=False, is_X_Sudoku=True)
            self.assertTrue(done)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))


    def solve_hyper_sudoku(self):
        puzzles = [
            # 711 solutions in general, 1 with hyper Sudoku
            (
                '...8..4..7.........4..9.........18....9....72....8..3931.....6...83542....7.1....',
                '951876423783542691246193758572931846839465172164287539315728964698354217427619385'
            ),
            (
            '.3.67.....5....98...4...7.3.........14...2.....38.1....6.....9..1.....5...9.3...4',
            '831679542756324981924185763678943125145762839293851476462518397317496258589237614'
            ),
            # 6836 solutions in general, 1 with hyper Sudoku
        ]
        for puzzle, solution in puzzles:
            puzzle, solution = str2grid(puzzle), str2grid(solution)
            solution_set, done, info = solve_sudoku(puzzle, verbose=False, all_solutions=False, is_hyper_Sudoku=True)
            self.assertTrue(done)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))

    def solve_hyper_sudoku_x(self):
        puzzles = [
            # From Hyper Sudoku X: 100 Hard Puzzles by Peter Ritmeester 
            # Many solutions in general, 747 X Sudoku solutions, 76 hyper Sudoku solutions, 1 Hyper X solution
            (
            '..4.............3....6.4.8..1......5..2.6....3.....87...9........5...........2...',
            '854329761627581934193674582918437625572968413346215879239756148785143296461892357'
            ),
        ]
        for puzzle, solution in puzzles:
            puzzle, solution = str2grid(puzzle), str2grid(solution)
            solution_set, done, info = solve_sudoku(
                puzzle, verbose=False, all_solutions=True, 
                is_hyper_Sudoku=True, is_X_Sudoku=True)
            self.assertTrue(done)
            self.assertEqual(len(solution_set), 1)
            solver_sol = str2grid(solution_set[0])
            self.assertTrue(grid_equal(solution, solver_sol))


def suite():
    "Set order of tests in ascending order of complexity and code required"
    suite = unittest.TestSuite()
    # smoke test
    suite.addTest(SudokuSolverTest('check_solver'))
    suite.addTest(SudokuSolverTest('check_solved_puzzles'))
    suite.addTest(SudokuSolverTest('solve_X_sudoku'))
    suite.addTest(SudokuSolverTest('solve_hyper_sudoku'))
    suite.addTest(SudokuSolverTest('solve_hyper_sudoku_x'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())