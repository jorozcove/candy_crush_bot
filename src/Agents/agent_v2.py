from copy import deepcopy
import itertools
import time

class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None
        self.special_candies = ['Ñ', '_sv', '_sh', '_p']
        self.possible_combos = list(itertools.permutations(self.special_candies, 2)) + [(candy, candy) for candy in self.special_candies]
        self.combos = {}

    def set_game_matrix(self, matrix):
        self.game_matrix = matrix

    def decide_best_move(self, i, j, move):

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
            "up": {"condition": i == 0, "swap": (i-1, j), "new_pos": (i-1, j)},
            "down": {"condition": i == 8, "swap": (i+1, j), "new_pos": (i+1, j)},
            "left": {"condition": j == 0, "swap": (i, j-1), "new_pos": (i, j-1)},
            "right": {"condition": j == 8, "swap": (i, j+1), "new_pos": (i, j+1)}
        }

        if moves[move]["condition"]:
            return 0, None

        # Obtener movimientos que sean combos
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
        
        candy = matrix[k][m]
        
        # Coincidencias horizontales
        count_dict = self.count_consecutive_candies(self.max_consecutive_candies(matrix[k]))
        update_score_and_pos(count_dict['3'] * 60)
        update_score_and_pos(count_dict['4'] * 100)
        update_score_and_pos(count_dict['5'] * 150)

        # count_dict = self.count_consecutive_candies(self.max_consecutive_candies(matrix[i]))
        # update_score_and_pos(count_dict['3'] * 60)
        # update_score_and_pos(count_dict['4'] * 100)
        # update_score_and_pos(count_dict['5'] * 150)

        # Coincidencias verticales
        count_dict = self.count_consecutive_candies(self.max_consecutive_candies(matrix[:, m]))
        update_score_and_pos(count_dict['3'] * 60)
        update_score_and_pos(count_dict['4'] * 100)
        update_score_and_pos(count_dict['5'] * 150)

        # count_dict = self.count_consecutive_candies(self.max_consecutive_candies(matrix[:, j]))
        # update_score_and_pos(count_dict['3'] * 60)
        # update_score_and_pos(count_dict['4'] * 100)
        # update_score_and_pos(count_dict['5'] * 150)
        

        return score, new_pos

    def max_consecutive_candies(self, arr):
        max_consecutive = {}
        current_variant = arr[0]
        if arr[0] != None:
            current_variant = arr[0][0]
        current_count = 1

        for variant in arr[1:]:
            if variant != None:
                variant = variant[0] # El primer caracter es el color
            if variant == current_variant:
                current_count += 1
            else:
                max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
                current_variant = variant
                current_count = 1
        max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
        return max_consecutive

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
        print(">>>>>>>>>>", candy1, candy2)
        for combo in self.possible_combos:
            if candy1.endswith(combo[0]) and candy2.endswith(combo[1]):
                return combo[0] + combo[1]
            elif candy1.endswith(combo[1]) and candy2.endswith(combo[0]):
                return combo[1] + combo[0]
        return None 
    
    def score_combo(self, combo):
        if combo == 'ÑÑ':
            return 1000
        elif combo == 'Ñ_sv' or combo == 'Ñ_sh' or combo == '_svÑ' or combo == '_shÑ':
            return 800
        elif combo == 'Ñ_p' or combo == '_pÑ':
            return 500
        elif combo == '_sv_sv' or combo == '_sv_sh' or combo == '_sh_sv' or combo == '_sh_sh':
            return 400
        elif combo == '_sv_p' or combo == '_p_sv' or combo == '_sh_p' or combo == '_p_sh':
            return 1300
        elif combo == '_p_p':
            return 350
        else:
            return 0           

    def compute_best_move(self):
        start_time = time.time()
        max_score = 0
        for i in range(9):
            for j in range(9):
                possible_moves = ['up', 'down', 'left', 'right']
                for move in possible_moves:
                    score, new_pos = self.decide_best_move(i, j, move)

                    if score >= max_score:
                        max_score = score
                        self.best_move = new_pos
        
        print("==================COMBOS==================")
        print(self.combos)
        print("===========================================")
        self.combos = {}
        print("Time to compute best move: ", time.time() - start_time)

    def play(self):
        if self.game_matrix is None:
            raise Exception("Game matrix not found")
        self.compute_best_move()
        return self.best_move


# # Coincidencias horizontales
# if m >= 2 and matrix[k][m-2] == matrix[k][m-1] == matrix[k][m]:
#     update_score_and_pos(80 if m >= 3 else 60)  # Línea de 4 o más
# elif m >= 1 and m <= 6 and matrix[k][m-1] == matrix[k][m] == matrix[k][m+1]:
#     update_score_and_pos(80)  # Línea de 3 con medio
# elif m <= 5 and matrix[k][m] == matrix[k][m+1] == matrix[k][m+2]:
#     update_score_and_pos(80 if m <= 4 else 60)  # Línea de 4 o más

# # Coincidencias verticales
# elif k >= 2 and matrix[k-2][m] == matrix[k-1][m] == matrix[k][m]:
#     update_score_and_pos(80 if k >= 3 else 60)  # Línea de 4 o más
# elif k >= 1 and k <= 6 and matrix[k-1][m] == matrix[k][m] == matrix[k+1][m]:
#     update_score_and_pos(80)  # Línea de 3 con medio
# elif k <= 5 and matrix[k][m] == matrix[k+1][m] == matrix[k+2][m]:
#     update_score_and_pos(80 if k <= 4 else 60)  # Línea de 4 o más


# Coincidencias de dulces especiales y combinaciones
# elif color == 'Ñ':
#     # Manejar dulce especial de chocolate
#     # Añadir lógica aquí para priorizar el intercambio con otro dulce especial
#     pass
# elif color.endswith('_sv') or color.endswith('_sh') or color.endswith('_p'):
#     # Manejar variantes de dulces especiales
#     # Añadir lógica aquí para priorizar el intercambio con otro dulce especial
#     pass

