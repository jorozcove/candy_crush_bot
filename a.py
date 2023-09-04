from src.Agents.agent_v3 import Agent
import numpy as np

# def max_consecutive_variants(arr):
#     max_consecutive = {}
#     current_variant = arr[0]
#     current_count = 1

#     for char in arr[1:]:
#         if char == current_variant:
#             current_count += 1
#         else:
#             max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
#             current_variant = char
#             current_count = 1
#     max_consecutive[current_variant] = max(max_consecutive.get(current_variant, 0), current_count)
#     return max_consecutive

# # Ejemplo de uso
# arr = ['y', 'o', 'o', 'o', 'y', 'y', 'p', 'o', 'o']
# print("Lista:", arr)
# result = max_consecutive_variants(arr)
# print("Máximas consecutivas:", result)


# #function that counts the number of =3, =4 and =5 consecutive candies, use the result from the previous function
# #example result: {'y': 2, 'o': 3, 'p': 1}
# def count_consecutive_candies(dictionary):
#     count_consecutives = {
#         '3': 0,
#         '4': 0,
#         '5': 0
#     }
    
#     for key, value in dictionary.items():
#         if value == 3:
#             count_consecutives['3'] += 1
#         elif value == 4:
#             count_consecutives['4'] += 1
#         elif value == 5:
#             count_consecutives['5'] += 1

#     return count_consecutives

# # Ejemplo de uso
# result = count_consecutive_candies(result)
# print("Consecutivos:", result)

ROWS = 9
COLS = 9
LEFT, RIGHT, TOP, BOTTOM = 0, 1, 2, 3

def findMatch(board, r, c, direction):
    matchLength = 0
    if (direction == LEFT):
        while (c > 0):
            cur = board[r][c]
            nxt = board[r][c-1]
            if (cur == nxt):
                matchLength += 1
                c -=1
            else:
                break
    if (direction == RIGHT):
        while (c < COLS-1):
            cur = board[r][c]
            nxt = board[r][c+1]
            if (cur == nxt):
                matchLength += 1
                c +=1
            else:
                break
    if (direction == TOP):
        while (r > 0):
            cur = board[r][c]
            nxt = board[r-1][c]
            if (cur == nxt):
                matchLength += 1
                r -=1
            else:
                break
    if (direction == BOTTOM):
        while (r < ROWS-1):
            cur = board[r][c]
            nxt = board[r+1][c]
            if (cur == nxt):
                matchLength += 1
                r +=1
            else:
                break
    return matchLength + 1

def findMatches(board, minMatch):
    matched = []
    exclude = ('X', '?')
    for r in range(ROWS):
        for c in range(COLS):
            if (c >= minMatch-1 and (board[r][c] not  in exclude)):
                match = findMatch(board, r, c, LEFT)
                if (match >= minMatch):
                    matched += [(r, x) for x in range(c, c-match, -1)]

            if (c <= COLS-minMatch and (board[r][c] not in exclude)):
                match = findMatch(board, r, c, RIGHT)
                if (match >= minMatch):
                    matched += [(r, x) for x in range(c, c+match)]

            if (r >= minMatch-1 and (board[r][c] not in exclude)):
                match = findMatch(board, r, c, TOP)
                if (match >= minMatch):
                    matched += [(x, c) for x in range(r, r-match, -1)]

            if (r <= ROWS-minMatch and (board[r][c] not in exclude)):
                match = findMatch(board, r, c, BOTTOM)
                if (match >= minMatch):
                    matched += [(x, c) for x in range(r, r+match)]
    return set(matched)

matrix = np.array([
    ['y', 'g', 'p', 'p', 'g', 'p', 'g', 'b', 'p'],
    ['r', 'r', 'y', 'o', 'r', 'r', 'r', 'g', 'g'],
    ['r', 'b', 'y', 'p', 'y', 'p', 'y', 'y', 'y'],
    ['y', 'r', 'p', 'g', 'o', 'p', 'y', 'o', 'r'],
    ['o', 'p', 'b', 'b', 'r', 'o', 'r', 'y', 'g'],
    ['r', 'p', 'o', 'b', 'o', 'b', 'p', 'g', 'y'],
    ['p', 'y', 'g', 'p', 'y', 'y', 'g', 'r', 'b'],
    ['b', 'y', 'p', 'b', 'y', 'o', 'b', 'o', 'o'],
    ['o', 'b', 'y', 'o', 'b', 'o', 'y', 'g', 'p']
], dtype="U4")


# print(sorted(findMatches(matrix, 3), key=lambda x: x[0]))

# print(">>>>>>>>>")

agent = Agent()
agent.set_game_matrix(matrix)

matches = agent.find_matches(matrix, 1, 6)
print(sorted(matches , key=lambda x: x[0]))

while matches:
    matches, matrix = agent.simulate_result(matrix, 1, 6)