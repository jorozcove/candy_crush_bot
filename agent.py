from copy import deepcopy

class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None

    def set_game_matrix(self, matrix):
        self.game_matrix = matrix

    def decide_best_move(self, i, j, move):
        # Aquí se debe implementar la lógica para decidir el mejor movimiento
        # basado en la matriz del juego.
        # El movimiento debe ser guardado en el atributo best_move.

        # El movimiento debe ser una tupla de la forma (x, y, direction)
        # donde x e y son las coordenadas de la celda a mover y direction
        # es la dirección en la que se moverá la celda.
        # direction puede ser 'up', 'down', 'left' o 'right'.
        # Ejemplo: (0, 0, 'right') indica que la celda en la posición (0, 0)
        # se moverá hacia la derecha.
        # Algunas consideraciones:
        # - Dulces normales dan 60 puntos.
        # - Linea de 4 dulces da un dulce especial. 80 puntos.
        # - Linea de 5 dulces da un dulce de chocolate (Ñ) 100 puntos.
        # - Dulces especiales dan 120 puntos.
        # - Dulces con rayas horizontales eliminan la fila (nombre termina en _sh).
        # - Dulces con rayas verticales eliminan la columna (nombre termina en _sv).
        # - Dulces empaquetados eliminan todos los dulces alrededor (nombre termina en _p).
        # - Dulce de chocolate (Ñ) elimina todos los dulces del color que se intercambia. 150 puntos.
        # - Combo dulce empaquetado + dulce rayado elimina 3 filas y 3 columnas. 250 puntos.
        # - Combo dulce especial + chocolate (Ñ) 200 puntos.

        matrix = deepcopy(self.game_matrix) # Make a copy of the matrix

        score = 0
        new_pos = None

        # Make the move
        if move == "up":
            if i == 0:
                return 0, None
            matrix[i][j], matrix[i-1][j] = matrix[i-1][j], matrix[i][j]
            k = i-1
            m = j
        elif move == "down":
            if i == 8:
                return 0, None
            matrix[i][j], matrix[i+1][j] = matrix[i+1][j], matrix[i][j]
            k = i+1
            m = j
        elif move == "left":
            if j == 0:
                return 0, None
            matrix[i][j], matrix[i][j-1] = matrix[i][j-1], matrix[i][j]
            k = i
            m = j-1
        elif move == "right":
            if j == 8:
                return 0, None
            matrix[i][j], matrix[i][j+1] = matrix[i][j+1], matrix[i][j]
            k = i
            m = j+1
        
        # Check if there is a match
        if k < 7 and matrix[k][m] == matrix[k-1][m] == matrix[k+1][m]:
            score += 60
            new_pos = (i, j, move)
            return score, new_pos
        if k < 7 and (matrix[k][m] == matrix[k+1][m] == matrix[k+2][m]):
            score += 60
            new_pos = (i, j, move)
            return score, new_pos
        if m < 7 and matrix[k][m] == matrix[k][m-1] == matrix[k][m+1]:
            score += 60
            new_pos = (i, j, move)
            return score, new_pos
        if m < 7 and (matrix[k][m] == matrix[k][m+1] == matrix[k][m+2]):
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
        return self.best_move
