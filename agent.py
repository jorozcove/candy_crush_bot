class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None

    def receive_game_matrix(self, matrix):
        """
        Recibe la matriz del juego y la guarda en el atributo game_matrix.
        matrix: Matriz del juego.
        [ [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy],
            [candy, candy, candy, candy, candy, candy, candy, candy, candy, candy] ]
        (candy types:
            red, blue, green, orange, purple, yellow, red_sh, blue_sh, green_sh, orange_sh, purple_sh, yellow_sh,
            red_sv, blue_sv, green_sv, orange_sv, purple_sv, yellow_sv, red_p, blue_p, green_p, orange_p, purple_p, yellow_p,
            Ñ
        )
        """
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
        # - Dulces especiales dan 120 puntos.
        # - Dulces con rayas horizontales eliminan la fila (*_sh).
        # - Dulces con rayas verticales eliminan la columna (*_sv).
        # - Dulce de chocolate (Ñ) elimina todos los dulces del color que se intercambia.

        self.compute_best_move()

    def compute_best_move(self, matrix):
        self.receive_game_matrix(matrix)
        max_score = 0
        for i in range(9):
            for j in range(9):
                possible_moves = ['up', 'down', 'left', 'right']
                for move in possible_moves:
                    score, new_pos = self.decide_best_move(i, j, move)
                    if score > max_score:
                        max_score = score
                        self.best_move = new_pos

    def play(self):
        if self.game_matrix is None:
            raise Exception("No se ha recibido ninguna matriz de juego.")
        self.decide_best_move()
        return self.best_move
