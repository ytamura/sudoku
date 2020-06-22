#!/usr/bin/env python
'''
sudoku.py

'''
import sys
import time
import numpy as np

from special_test_cases import TEST_CASE_2

matrix = TEST_CASE_2
puzzle = np.array(matrix)
n_rows, n_cols = puzzle.shape
assert n_rows == n_cols
L = n_rows
N = L**2
ORIG_PUZZLE = puzzle.copy()


def _check_rows(puzzle):
    for i in range(L):
        temp = []
        for j in range(L):
            x = puzzle[i, j]
            if x in temp:
                return False
            temp.append(x)
    return True


def _check_columns(puzzle):
    for i in range(L):
        temp = []
        for j in range(L):
            x = puzzle[j, i]
            if x in temp:
                return False
            temp.append(x)
    return True


def _check_squares(puzzle):
    '''Specific implementation for 3x3 3x3 squares [9x9]'''
    small_L = 3
    for i in range(small_L):
        I=i*3
        for j in range(small_L):
            J=j*3
            if sum(set(puzzle[I:I+3, J:J+3].flatten())) != 45:
                return False
    return True


def check_puzzle_valid(puzzle):
    if np.count_nonzero(puzzle) != N:
        return False
    if not _check_rows(puzzle):
        return False
    if not _check_columns(puzzle):
        return False
    if not _check_squares(puzzle):
        return False
    print('Valid!')
    return True


def _get_used_in_square(puzzle, i, j):
    i = int(i/3)*3
    j = int(j/3)*3
    square = puzzle[i:i+3, j:j+3]
    return square[square > 0]


def get_possible_numbers(puzzle, i, j):
    if ORIG_PUZZLE[i, j] > 0:
        return [ORIG_PUZZLE[i, j]]
    else:
        used_in_row = puzzle[i, puzzle[i, :] > 0]
        used_in_col = puzzle[puzzle[j, :] > 0, j]
        used_in_square = _get_used_in_square(puzzle, i, j)
        return (set(range(1, L+1)) -
                set(used_in_row) -
                set(used_in_col) -
                set(used_in_square))


def solve_puzzle(puzzle, n=0):
    '''Solve puzzle recursively.

    :param puzzle: puzzle, a 2D numpy array
    :param n: flattened index in puzzle

    :return: the solved puzzle or False
    '''
    i = int(n / L)
    j = n % L

    if n == N-1:
        if check_puzzle_valid(puzzle):
            return puzzle
        else:
            return False

    possibles = get_possible_numbers(puzzle, i, j)
    if len(possibles) == 0:
        return False
    else:
        # print('%s (%d,%d) %s' % (puzzle, i, j, possibles))
        for possible in possibles:
            puzzle[i, j] = possible
            sol = solve_puzzle(puzzle.copy(), n+1)
            if type(sol) != bool:
                return sol
    return False


def print_puzzle(puzzle, title=''):
    print(title)
    for row in puzzle:
        out_row = [str(x) if x > 0 else '-' for x in row]
        print('|%s|' % ' '.join(out_row))


if __name__ == '__main__':
    print_puzzle(puzzle, title='Puzzle')

    print('Solving...')
    start = time.time()
    solution = solve_puzzle(puzzle, 0)
    elapsed_time = time.time() - start
    print_puzzle(solution, title='Solution')
    print('Elapsed time: %ss' % elapsed_time)
