from copy import deepcopy

class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None

    def set_game_matrix(self, matrix):
        self.game_matrix = matrix

    def decide_best_move(self, i, j, move):
        # Aquí se implementa la lógica para decidir el mejor movimiento
        # basado en la matriz del juego.
        # El movimiento se guarda en el atributo best_move.

        # El movimiento es una tupla de la forma (x, y, direction)
        # donde x e y son las coordenadas de la celda a mover y direction
        # es la dirección en la que se moverá la celda.
        # direction puede ser 'up', 'down', 'left' o 'right'.
        # Ejemplo: (0, 0, 'right') indica que la celda en la posición (0, 0)
        # se moverá hacia la derecha.
        # Algunas consideraciones:
        # - Dulces normales dan 60 puntos.
        # - Dulces especiales dan 120 puntos.
        # - Dulces con rayas horizontales eliminan la fila (*_sh).
        # - Dulces con rayas verticales eliminan la columna (*_sv).
        # - Dulce de chocolate (Ñ) elimina todos los dulces del color que se intercambia.

        matrix = deepcopy(self.game_matrix) # Se hace una copia de la matriz

        score = 0
        new_pos = None

        # Se realiza el movimiento
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
        
        # Se verifica si hay una coincidencia
        match_conditions = [
            (k < 7 and matrix[k][m] == matrix[k-1][m] == matrix[k+1][m]),
            (k < 7 and matrix[k][m] == matrix[k+1][m] == matrix[k+2][m]),
            (m < 7 and matrix[k][m] == matrix[k][m-1] == matrix[k][m+1]),
            (m < 7 and matrix[k][m] == matrix[k][m+1] == matrix[k][m+2])
        ]

        if any(match_conditions):
            score += 60
            new_pos = (i, j, move)
            return score, new_pos

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
            raise Exception(FileNotFoundError("Game matrix not found"))
        self.compute_best_move()
        return self.best_move if self.best_move is not None else (0, 0, 'right')
