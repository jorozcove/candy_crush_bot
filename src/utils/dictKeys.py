import numpy as np
from itertools import permutations

def get_dict_key(keys, values, val) -> str:
    """
    Returns the key of a dictionary given a value
    @param keys: list of keys
    @param values: list of values
    @param val: value to search

    @return: key of the dictionary
    """
    return list(keys)[list(values).index(val)]

def get_possible_combos(special_candies) -> list:
    """
    Returns a list of possible combos
    @param special_candies: list of special candies

    @return: list of possible combos
    """
    return list(permutations(special_candies, 2)) + [(candy, candy) for candy in special_candies]

def get_matrix() -> np.ndarray:
    """
    Returns a matrix of candies
    @return: matrix of candies
    """
    return np.array([['y', 'b', 'y', 'o_sh', 'y', 'y', 'b', 'r', 'o'],
        ['o', 'y', 'y', 'r', 'g', 'y', 'r', 'r', 'g'],
     ['g', 'r', 'o', 'b', 'r', 'b', 'o', 'b', 'b'],
     ['r', 'o', 'r', 'r', 'p', 'o', 'r', 'g', 'o'],
     ['g', 'b', 'p', 'y', 'g', 'y', 'b', 'y', 'g'],
     ['y', 'p', 'o', 'o', 'g', 'y', 'g', 'b', 'r'],
     ['p', 'p', 'g', 'p', 'p', 'r', 'r', 'y', 'b'],
     ['y', 'y', 'b', 'p', 'o', 'y', 'r', 'b', 'y'],
     ['p', 'b', 'y', 'y', 'o', 'p', 'p', 'y', 'y']], dtype=str)