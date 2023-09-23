from copy import deepcopy
import itertools
import time
from threading import Thread
import numpy as np

class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None
        self.special_candies = ['Ñ', '_sv', '_sh', '_p']
        self.possible_combos = list(itertools.permutations(self.special_candies, 2)) + [(candy, candy) for candy in self.special_candies]
        self.combos = {}
        self.est_score = 0

    def set_game_matrix(self, matrix):
        self.game_matrix = matrix

    def decide_best_move(self, i: int, j: int, move: str):

        # Función auxiliar para calcular la puntuación y new_pos
        def update_score_and_pos(match_score):
            nonlocal score, new_pos
            score += match_score
            new_pos = (i, j, move)

        matrix = deepcopy(self.game_matrix)  # Hacer una copia de la matriz

        score = 0
        new_pos = None

        # Realizar el movimiento
        moves = {
            # "up": {"condition": i == 0, "swap": (i-1, j), "new_pos": (i-1, j)},
            "down": {"condition": i == 8, "swap": (i+1, j), "new_pos": (i+1, j)},
            # "left": {"condition": j == 0, "swap": (i, j-1), "new_pos": (i, j-1)},
            "right": {"condition": j == 8, "swap": (i, j+1), "new_pos": (i, j+1)}
        }

        if moves[move]["condition"]:
            return 0, None

        # Obtener movimientos que sean combos
        # print(moves[move]["swap"])
        if self.is_special_candy(matrix[moves[move]["swap"]]) and self.is_special_candy(matrix[i][j]):
            combo = self.get_combo(matrix[moves[move]["swap"]], matrix[i][j])

            if combo is not None:
                self.combos[(i, j, move)] = combo

                # Obtener la puntuación del combo
                score = self.score_combo(combo)
                update_score_and_pos(score)
            
        # Intercambiar dulces en la copia de la matriz
        matrix[i][j], matrix[moves[move]["swap"]] = matrix[moves[move]["swap"]], matrix[i][j]

        # Obtener la nueva posición
        k, m = moves[move]["new_pos"]
        
        # Obtener las coincidencias (lineas de 3, 4 o 5)
        matches = self.find_matches(matrix, k, m)

        # Mientras haya coincidencias, simular el resultado
        max_iterations = 15
        iterations = 0
        while matches and iterations < max_iterations:
            matches, matrix = self.simulate_result(matrix, k, m, update_score_and_pos)
            iterations += 1

        return score, new_pos
    
    def simulate_result(self, matrix, actual_row, actual_col, update_score_and_pos):
        """
            Having the matrix with the matches, remove the candies and drop the ones above

            matrix: The matrix with the matches
            actual_row: The row of the candy that was moved
            actual_col: The column of the candy that was moved
        """
        matches = self.find_matches(matrix, actual_row, actual_col, update_score_and_pos)
        # Replace the matches with "X"
        for match in matches:
            if match[2] is not None: 
                matrix[match[0:2]] = match[2] 
            else: matrix[match[0:2]] = 'X'
        # Drop the candies above
        for i in range(9):
            for j in range(9):
                if matrix[i][j] == 'X':
                    for k in range(i, 0, -1):
                        matrix[k][j] = matrix[k-1][j]
                    matrix[0][j] = '?'

        return matches, matrix

    def find_matches(self, matrix, actual_row, actual_col, update_score_and_pos = None):
        matches = []
        for i in range(9):
            row_mcc, row_matches = self.max_consecutive_candies(matrix[i])
            if update_score_and_pos is not None:
                count_dict = self.count_consecutive_candies(row_mcc)
                update_score_and_pos(count_dict['3'] * 60)
                update_score_and_pos(count_dict['4'] * 120)
                update_score_and_pos(count_dict['5'] * 200)
            for x in row_matches:
                for k in range(x[2], x[2]+x[1]):
                    if x[1] == 4 and (i, k) == (actual_row, actual_col) and len(x[0]) == 1 and x[0] != "Ñ": matches.append((i, k, f"{x[0]}_sh"))
                    elif x[1] == 5 and (i, k) == (actual_row, actual_col) and len(x[0]) == 1 and x[0] != "Ñ": matches.append((i, k, "Ñ"))
                    else: matches.append((i, k, None))
        for j in range(9):
            col_mcc, col_matches = self.max_consecutive_candies(matrix[:, j])
            if update_score_and_pos is not None:
                count_dict = self.count_consecutive_candies(col_mcc)
                update_score_and_pos(count_dict['3'] * 60)
                update_score_and_pos(count_dict['4'] * 120)
                update_score_and_pos(count_dict['5'] * 200)
            for x in col_matches:
                for k in range(x[2], x[2]+x[1]):
                    if x[1] == 4 and (k, j) == (actual_row, actual_col): matches.append((k, j, f"{x[0]}_sv"))
                    elif x[1] == 5 and (k, j) == (actual_row, actual_col): matches.append((k, j, "Ñ"))
                    else: matches.append((k, j, None))
        return set(matches)

    def max_consecutive_candies(self, arr):
        max_consecutive = {}
        matches = []
        current_variant = arr[0]
        if arr[0] != None:
            current_variant = arr[0][0]
        current_count = 1
        current_position = 0  # Añadir posición inicial

        for idx, variant in enumerate(arr[1:], start=1):  # Añadir índice a la enumeración
            # if variant == '?':
            #     # current_count = 0
            #     break
            if variant != None:
                variant = variant[0]  # El primer caracter es el color
            if variant == current_variant:
                current_count += 1
            else:
                max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
                matches.append((current_variant, current_count, current_position, current_position-current_count))  # Añadir posición de inicio y fin a las coincidencias
                current_variant = variant
                current_count = 1
                current_position = idx  # Actualizar la posición actual
        max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
        matches.append((current_variant, current_count, current_position, current_position + current_count - 1))  # Añadir posición de inicio y fin a las coincidencias

        #eliminar '?' de las coincidencias y del diccionario
        matches = list(filter(lambda x: x[0] != '?', matches))
        for key in list(max_consecutive.keys()):
            if key == '?':
                del max_consecutive[key]

        return max_consecutive, list(filter(lambda x: x[1] >=3, matches))

    def count_consecutive_candies(self, dictionary):
        count_consecutives = {
            '3': 0,
            '4': 0,
            '5': 0
        }
        
        for key, value in dictionary.items():
            if value == 3:
                count_consecutives['3'] += 1
            elif value == 4:
                count_consecutives['4'] += 1
            elif value == 5:
                count_consecutives['5'] += 1

        return count_consecutives

    def is_special_candy(self, candy):
        for special in self.special_candies:
            if candy!= None and candy.endswith(special):
                return True
        return False

    def get_combo(self, candy1, candy2):
        # print(">>>>>>>>>>", candy1, candy2)
        for combo in self.possible_combos:
            if candy1.endswith(combo[0]) and candy2.endswith(combo[1]):
                return combo[0] + combo[1]
            elif candy1.endswith(combo[1]) and candy2.endswith(combo[0]):
                return combo[1] + combo[0]
        return None 
    
    def score_combo(self, combo):
        if combo == 'ÑÑ':
            return 4740
        elif combo == 'Ñ_sv' or combo == 'Ñ_sh' or combo == '_svÑ' or combo == '_shÑ':
            return 3000
        elif combo == 'Ñ_p' or combo == '_pÑ':
            return 1440
        elif combo == '_sv_sv' or combo == '_sv_sh' or combo == '_sh_sv' or combo == '_sh_sh':
            return 1080
        elif combo == '_sv_p' or combo == '_p_sv' or combo == '_sh_p' or combo == '_p_sh':
            return 2160
        # elif combo == '_p_p':
        #     return 2160
        else:
            return 0

    def find_variant(self, color):
        color_where = np.where(self.game_matrix == color)
        if len(color_where[0]) > 0:
            return color_where[0][0], color_where[1][0]
        return None

    def chocolate_swap(self):
        pos = self.find_variant('Ñ')
        if pos != None:
            i, j = pos

            if i != 0:
                agent.best_move = (i, j, 'up')
            elif i != 8:
                agent.best_move = (i, j, 'down')
            elif j != 0:
                agent.best_move = (i, j, 'left')
            elif j != 8:
                agent.best_move = (i, j, 'right')

    def examine_possible_moves(self, i, j,  possible_moves, max_score=0):
        for move in possible_moves:
            score, new_pos = self.decide_best_move(i, j, move)

            if score >= max_score[0]:
                max_score[0] = score
                self.est_score = score
                self.best_move = new_pos

    def compute_best_move(self):
        start_time = time.time()
        max_score = [0]
        threads = []
        for i in range(9):
            for j in range(9):
                possible_moves = ['down', 'right']#['up', 'down', 'left', 'right']
                self.examine_possible_moves(i, j, possible_moves, max_score)
                # thread = Thread(target=self.examine_possible_moves, args=(i, j, possible_moves, max_score))
                # threads.append(thread)
                # thread.start()

        # for thread in threads:
        #     thread.join()
        
        # print("==================COMBOS==================")
        # print(self.combos)
        # print("===========================================")
        self.combos = {}
        # print("Time to compute best move: ", time.time() - start_time)

    def play(self):
        if self.game_matrix is None:
            raise Exception("Game matrix not found")
        self.compute_best_move()

        if self.best_move is None:
            self.chocolate_swap()

        print(f"Estimated score: {self.est_score} with move {self.best_move}")
        return self.best_move

if __name__ == '__main__': 
    pass