from copy import deepcopy

class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None

    def set_game_matrix(self, matrix):
        self.game_matrix = matrix

    def decide_best_move(self, i, j, move):
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
        matrix[i][j], matrix[moves[move]["swap"]] = matrix[moves[move]["swap"]], matrix[i][j]
        k, m = moves[move]["new_pos"]
        
        # Verificar coincidencias
        color = matrix[k][m]

        # Función auxiliar para calcular la puntuación y new_pos
        def update_score_and_pos(match_score):
            nonlocal score, new_pos
            score += match_score
            new_pos = (i, j, move)
            return True
        
        # Coincidencias horizontales
        if m >= 2 and matrix[k][m-2] == matrix[k][m-1] == matrix[k][m]:
            update_score_and_pos(80 if m >= 3 else 60)  # Línea de 4 o más
        elif m >= 1 and m <= 6 and matrix[k][m-1] == matrix[k][m] == matrix[k][m+1]:
            update_score_and_pos(80)  # Línea de 3 con medio
        elif m <= 5 and matrix[k][m] == matrix[k][m+1] == matrix[k][m+2]:
            update_score_and_pos(80 if m <= 4 else 60)  # Línea de 4 o más
        
        # Coincidencias verticales
        elif k >= 2 and matrix[k-2][m] == matrix[k-1][m] == matrix[k][m]:
            update_score_and_pos(80 if k >= 3 else 60)  # Línea de 4 o más
        elif k >= 1 and k <= 6 and matrix[k-1][m] == matrix[k][m] == matrix[k+1][m]:
            update_score_and_pos(80)  # Línea de 3 con medio
        elif k <= 5 and matrix[k][m] == matrix[k+1][m] == matrix[k+2][m]:
            update_score_and_pos(80 if k <= 4 else 60)  # Línea de 4 o más
        
        # Coincidencias de dulces especiales y combinaciones
        # elif color == 'Ñ':
        #     # Manejar dulce especial de chocolate
        #     # Añadir lógica aquí para priorizar el intercambio con otro dulce especial
        #     pass
        # elif color.endswith('_sv') or color.endswith('_sh') or color.endswith('_p'):
        #     # Manejar variantes de dulces especiales
        #     # Añadir lógica aquí para priorizar el intercambio con otro dulce especial
        #     pass

        return score, new_pos

    def compute_best_move(self):
        max_score = 0
        for i in range(9):
            for j in range(9):
                possible_moves = ['up', 'down', 'left', 'right']
                for move in possible_moves:
                    score, new_pos = self.decide_best_move(i, j, move)
                    if score >= max_score:
                        max_score = score
                        self.best_move = new_pos

    def play(self):
        if self.game_matrix is None:
            raise Exception("Game matrix not found")
        self.compute_best_move()
        return self.best_move
