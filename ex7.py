#############################################
# FILE: ex7.py
# WRITER: eldad_chidra, eldadchidra
# EXERCISE: intro2cs ex7 2019
# DESCRIPTION: Recursive
#############################################


def print_to_n(n):
    """Prints Numbers 1 to n"""
    if n >= 1:
        print_to_n(n-1)
        print(n)
    elif n < 1:
        return


def print_reversed(n):
    """Prints Numbers n to 1"""
    if n < 1:
        return
    print(n)
    print_reversed(n-1)


def is_prime(n):
    """Gets number and returns True if Prime and False if not. Uses the function
    has_divisor_smaller_than"""
    if n <= 1:
        return False

    else:
        return has_divisor_smaller_than(n, int(n/2))


def has_divisor_smaller_than(n, i):
    if i > 1:
        if n % i == 0:
            return False
        return has_divisor_smaller_than(n, i-1)

    else:
        return True


def exp_n_x(n, x):
    """Exp. function to calculate the val of x. uses factorial (AZERET) at exp_n_x_helper function"""
    if n == 0 or x == 0:
        return 1
    return x ** n / exp_n_x_helper(n) + exp_n_x(n-1, x)


def exp_n_x_helper(n):
    """Factorial function"""
    if n == 0:
        return 1
    else:
        return n*exp_n_x_helper(n-1)


def play_hanoi(hanoi, n, src, dest, temp):
    """Resolves the Hanoi Game"""
    if n == 2:
        hanoi.move(src, temp)
        hanoi.move(src, dest)
        hanoi.move(temp, dest)
    elif n == 1:
        hanoi.move(src, dest)
    elif n <= 0:
        return
    else:
        play_hanoi(hanoi, n-1, src, temp, dest)
        hanoi.move(src, dest)
        play_hanoi(hanoi, n-1, temp, dest, src)


def print_sequences(char_list, n):
    """Prints the all sequences from list of chars. uses sequence_helper function."""
    for sequence in print_sequence_helper(char_list, n):
        print(sequence)


def print_sequence_helper(char_list, n):
    sequences = []

    if n == 0:
        return []

    elif n == 1:
        return char_list

    else:
        for i in char_list:
            for step_back in print_sequence_helper(char_list, n-1):
                sequences.append(i + step_back)
        return sequences


def print_no_repetition_sequences(char_list, n):
    """Prints the all sequences from list of chars with no repetition. uses no_repetition_sequences_helper."""
    for sequence in no_repetition_sequences_helper(char_list, n):
        print(sequence)


def no_repetition_sequences_helper(char_list, n):
    sequences = []

    if n == 0:
        return []

    elif n == 1:
        return char_list

    else:
        for i in char_list:
            for step_back in print_sequence_helper(char_list, n-1):
                sequences.append(i + step_back)

        return sequences


def parentheses(n):
    """Returns the valid sequences of parentheses. Uses the parentheses_helper function."""
    return parentheses_helper(n, n)


def parentheses_helper(n, in_par):
    last_result = []

    if n == 0:
        return []

    if in_par == 0:
        return []

    if in_par == 1:
        return ["()" * n]

    ex_par = parentheses_helper(n-1, in_par-2)

    for seq in parentheses_helper(n-1, in_par-1):
        if seq in ex_par:
            continue
        last_result.append("(" + seq + ")")

    for i in range(1, n):
        ex_par = parentheses_helper(n-i, in_par-1)
        for seq_2 in parentheses_helper(n-i, in_par):
            if seq_2 in ex_par:
                continue

            for seq_3 in parentheses_helper(i, in_par):
                if seq_2+seq_3 != last_result:
                    last_result.append(seq_2+seq_3)

                if seq_3+seq_2 != last_result:
                    last_result.append(seq_3+seq_2)

    return last_result + parentheses_helper(n, in_par-1)


def up_and_right(n, k):
    """Prints the all valid ways to move to the point n,k. uses up_and_right_helper function."""
    way = up_and_right_helper(n, k, 0, 0)

    for the_route in way:
        print(the_route)


def up_and_right_helper(n, k, x, y):
    moves = []
    up = [x, y+1]
    right = [x+1, y]

    if (n, k) == (x, y+1):
        return "u"

    if (n, k) == (x+1, y):
        return "r"

    if up[1] <= k:
        for way in up_and_right_helper(n, k, up[0], up[1]):
            moves.append("u"+way)

    if right[0] <= n:
        for way in up_and_right_helper(n, k, right[0], right[1]):
            moves.append("r"+way)

    return moves


def flood_fill(image, start):
    """Fills empty points at the start point and only at the points that were filled before"""

    image[start[0]][start[1]] = "*"
    rows = len(image)
    columns = len(image[0])

    up = [start[0]-1, start[1]]
    down = [start[0]+1, start[1]]
    right = [start[0], start[1]+1]
    left = [start[0], start[1]-1]

    if up[1] > 0 and image[up[0]][up[1]] == ".":
        flood_fill(image, up)

    if down[1] < rows and image[down[0]][down[1]] == ".":
        flood_fill(image, down)

    if right[0] < columns and image[right[0]][right[0]] == ".":
        flood_fill(image, right)

    if left[0] > 0 and image[left[0]][left[1]] == ".":
        flood_fill(image, left)

    image[start[0]][start[1]] = "*"