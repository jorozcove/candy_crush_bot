from matrix import CandyMatrix
from python import Python, Dictionary
from time import now

struct Agent:
    var game_matrix: CandyMatrix
    var best_move: Tuple[Int, Int, String]
    var special_candies: PythonObject
    var possible_combos: PythonObject
    var np: PythonObject
    var combos: Dictionary

    fn __init__(inout self, rows:Int , cols: Int, matrix: CandyMatrix):
        self.best_move = (0, 0, String("up"))
        self.game_matrix = matrix
        self.combos = Python.dict()
        try:
            self.np = Python.import_module("numpy")
            self.special_candies = self.np.array(["Ñ", "_sv", "_sh", "_p"])
            let perm_utils = Python.import_module("dictKeys")
            self.possible_combos = perm_utils.get_possible_combos(self.special_candies)
        except:
            self.possible_combos = None

    fn decide_best_move(self, row: Int, col: Int, move: String) -> Tuple[Int, Tuple[Int, Int, String]]:
        fn update_score_and_pos(inout score: Int, inout new_pos: Tuple[Int, Int, String], match_score: Int):
            score += match_score
            new_pos = (row, col, move)

        var matrix = self.game_matrix

        return 10, (1, 2, String("up"))

    fn compute_best_move(inout self):
        let start_time = now()
        var max_score = 0
        for i in range(self.game_matrix.x):
            for j in range(self.game_matrix.y):
                try:
                    let possible_moves = self.np.array(["up", "down", "left", "right"])
                    for move in possible_moves:
                        let result = self.decide_best_move(i, j, move.to_string())
                        var score = result.get[0, Int]()
                        var new_pos = result.get[1, Tuple[Int, Int, String]]()
                        if score > max_score:
                            max_score = score
                            self.best_move = new_pos
                except:
                    continue
        
        print("==================COMBOS==================")
        try:
            print(self.combos.__str__())
        except:
            print("No combos found")
        print("===========================================")
        print("Time to compute best move: ", now() - start_time)

    fn play(self) raises -> Tuple[Int, Int, String]:
        if self.game_matrix.is_empty():
            raise Error("Matrix is empty")
        self.compute_best_move()
        return self.best_move

def get_value(m: PythonObject, row: Int, col: Int) -> PythonObject:
    return m[row][col]

fn fill_matrix(m:PythonObject, mx: CandyMatrix) raises -> None:
    for i in range(9):
        for j in range(9):
            let value = get_value(m, i, j).to_string()
            mx[i, j] = value

fn main()raises -> None:
    Python.add_to_path("/workspaces/candy_crush_bot/src/utils")
    let utils = Python.import_module("dictKeys")
    alias ROWS = 9
    alias COLS = 9
    let m = utils.get_matrix()
    let matrix = CandyMatrix(ROWS, COLS)
    fill_matrix(m, matrix)
    let agent = Agent(ROWS, COLS, matrix)
    print(agent.game_matrix.to_string())