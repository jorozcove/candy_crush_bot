from copy import deepcopy

class Agent:
    def __init__(self):
        self.game_matrix = None
        self.best_move = None

    def set_game_matrix(self, matrix):
        self.game_matrix = matrix

    def decide_best_move(self, i, j, move):
        matrix = deepcopy(self.game_matrix)  # Make a copy of the matrix

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
        
        # Check for matches
        color = matrix[k][m]

        # Helper function to calculate score and new_pos
        def update_score_and_pos(match_score):
            nonlocal score, new_pos
            score += match_score
            new_pos = (i, j, move)
            return True
        
        # Horizontal matches
        if m >= 2 and matrix[k][m-2] == matrix[k][m-1] == matrix[k][m]:
            update_score_and_pos(80 if m >= 3 else 60)  # Line of 4 or more
        elif m >= 1 and m <= 6 and matrix[k][m-1] == matrix[k][m] == matrix[k][m+1]:
            update_score_and_pos(80)  # Line of 3 with middle
        elif m <= 5 and matrix[k][m] == matrix[k][m+1] == matrix[k][m+2]:
            update_score_and_pos(80 if m <= 4 else 60)  # Line of 4 or more
        
        # Vertical matches
        elif k >= 2 and matrix[k-2][m] == matrix[k-1][m] == matrix[k][m]:
            update_score_and_pos(80 if k >= 3 else 60)  # Line of 4 or more
        elif k >= 1 and k <= 6 and matrix[k-1][m] == matrix[k][m] == matrix[k+1][m]:
            update_score_and_pos(80)  # Line of 3 with middle
        elif k <= 5 and matrix[k][m] == matrix[k+1][m] == matrix[k+2][m]:
            update_score_and_pos(80 if k <= 4 else 60)  # Line of 4 or more
        
        # # Special candy matches and combinations
        # elif color == 'Ñ':
        #     # Handle chocolate special candy
        #     # Add logic here to prioritize swapping with another special candy
        #     pass
        # elif color.endswith('_sv') or color.endswith('_sh') or color.endswith('_p'):
        #     # Handle special candy variants
        #     # Add logic here to prioritize swapping with another special candy
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
