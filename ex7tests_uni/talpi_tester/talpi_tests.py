from .autotest import TestSet

from . import testrunners

import sys
from importlib import import_module
from io import StringIO
import copy

defaults = {'modulename':'ex7',
            'runner':testrunners.functionname_doc_runner,
            'ans':[True],
            }

def unordered(exp,ans):
    try:
        return type(exp)==type(ans) and sorted(exp) == sorted(ans)
    except TypeError:
        return False


exp_mat = \
[['*','*','*','*','*'],
['*','.','*','.','*'],
['*','.','*','.','*'],
['*','*','*','*','*']]

exp_mat_res00 = \
[['*','*','*','*','*'],
['*','.','*','.','*'],
['*','.','*','.','*'],
['*','*','*','*','*']]

exp_mat_res11 = \
[['*','*','*','*','*'],
['*','*','*','.','*'],
['*','*','*','.','*'],
['*','*','*','*','*']]


cases = {s:{'fname':s} for s in ('print_to_n',
                                 'print_reversed',
                                 'is_prime',
                                 'exp_n_x',
                                 'play_hanoi',
                                 'print_sequences',
                                 'print_no_repetition_sequences',
                                 'parentheses',
                                 'up_and_right',
                                 'flood_fill',)
     }

cases_2 = {
    "print_to_n_5": {
        "fname": "print_to_n",
        "args": [5],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": "1\n2\n3\n4\n5\n"}
    },

    "print_to_n_7": {
        "fname": "print_to_n",
        "args": [7],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": "1\n2\n3\n4\n5\n6\n7\n"}
    },

    "print_to_n_1": {
        "fname": "print_to_n",
        "args": [1],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": "1\n"}
    },

    "print_to_n_0": {
        "fname": "print_to_n",
        "args": [0],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": ""}
    },

    "print_to_n_negative": {
        "fname": "print_to_n",
        "args": [-3],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": ""}
    },

    "print_to_n_reversed_5": {
        "fname": "print_reversed",
        "args": [5],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": "5\n4\n3\n2\n1\n"}
    },

    "print_to_n_reversed_7": {
        "fname": "print_reversed",
        "args": [7],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": "7\n6\n5\n4\n3\n2\n1\n"}
    },

    "print_to_n_reversed_1": {
        "fname": "print_reversed",
        "args": [1],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": "1\n"}
    },

    "print_to_n_reversed_0": {
        "fname": "print_reversed",
        "args": [0],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": ""}
    },

    "print_to_n_reversed_negative": {
        "fname": "print_reversed",
        "args": [-3],
        "ans": [None],
        "runner": testrunners.print_runner,
        "options": {"output": ""}
    },

    "is_prime_2": {
        "fname": "is_prime",
        "args": [2],
        "ans": [True],
        "runner": testrunners.base_runner,
    },

    "is_prime_3": {
        "fname": "is_prime",
        "args": [3],
        "ans": [True],
        "runner": testrunners.base_runner,
    },

    "is_prime_97": {
        "fname": "is_prime",
        "args": [97],
        "ans": [True],
        "runner": testrunners.base_runner,
    },

    "is_prime_91": {
        "fname": "is_prime",
        "args": [91],
        "ans": [False],
        "runner": testrunners.base_runner,
    },

    "is_prime_75": {
        "fname": "is_prime",
        "args": [75],
        "ans": [False],
        "runner": testrunners.base_runner,
    },

    "is_prime_333": {
        "fname": "is_prime",
        "args": [333],
        "ans": [False],
        "runner": testrunners.base_runner,
    },

    "is_prime_1": {
        "fname": "is_prime",
        "args": [1],
        "ans": [False],
        "runner": testrunners.base_runner,
    },

    "is_prime_0": {
        "fname": "is_prime",
        "args": [0],
        "ans": [False],
        "runner": testrunners.base_runner,
    },

    "is_prime_negative": {
        "fname": "is_prime",
        "args": [-1],
        "ans": [False],
        "runner": testrunners.base_runner,
    },

    "exp_n_x_10_0": {
        "fname": "exp_n_x",
        "args": [10, 0],
        "ans": [1],
        "runner": testrunners.base_runner,
    },

    "exp_n_x_2_3": {
        "fname": "exp_n_x",
        "args": [3, 3],
        "ans": [((3**0)/1) + ((3**1)/1) + ((3**2)/2) + (3**3)/6],
        "runner": testrunners.base_runner,
    },

    "exp_n_x_negative": {
        "fname": "exp_n_x",
        "args": [2, -1],
        "ans": [1/1 -1/1 + 1/2],
        "runner": testrunners.base_runner,
    },

    "print_sequences_3": {
        "fname": "print_sequences",
        "args": [["a", "b", "c"], 3],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "aaa\naab\naac\naba\naca\nabb\nabc\nacb\nacc\nbaa\nbab\nbac\nbba\nbca\nbbb\nbbc\nbcb\nbcc\ncaa\ncab\ncac\ncba\ncca\ncbb\ncbc\nccb\nccc\n"}
    },

    "print_sequences_1": {
        "fname": "print_sequences",
        "args": [["a", "b", "c"], 1],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "a\nb\nc\n"}
    },


    "print_sequences_0": {
        "fname": "print_sequences",
        "args": [["a", "b", "c"], 0],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": ""}
    },

    "print_sequences_one_char": {
        "fname": "print_sequences",
        "args": [["d"], 4],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "dddd\n"}
    },

    "print_sequences_no_repeat_3": {
        "fname": "print_no_repetition_sequences",
        "args": [["a", "b", "c"], 3],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "abc\nacb\nbca\nbac\ncab\ncba\n"}
    },

    "print_sequences_no_repeat_1": {
        "fname": "print_no_repetition_sequences",
        "args": [["a", "b", "c"], 1],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "a\nb\nc\n"}
    },


    "print_sequences_no_repeat_0": {
        "fname": "print_no_repetition_sequences",
        "args": [["a", "b", "c"], 0],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": ""}
    },

    "print_sequences_no_repeat_one_char": {
        "fname": "print_no_repetition_sequences",
        "args": [["d"], 4],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": ""}
    },


    "parantheses_1": {
        "fname": "parentheses",
        "args": [1],
        "ans": [["()"]],
        "runner": testrunners.base_runner,
        'comparemethod': unordered
    },

    "parantheses_2": {
        "fname": "parentheses",
        "args": [2],
        "ans": [["(())", "()()"]],
        "runner": testrunners.base_runner,
        'comparemethod': unordered
    },

    "parantheses_3": {
        "fname": "parentheses",
        "args": [3],
        "ans": [['()()()', '()(())', '(())()', '(()())', '((()))']],
        "runner": testrunners.base_runner,
        'comparemethod': unordered
    },

    "parantheses_4": {
        "fname": "parentheses",
        "args": [4],
        "ans": [['()()()()', '()()(())', '()(())()', '()(()())', '()((()))', '(())()()', '(())(())', '(()())()', '(()()())', '(()(()))', '((()))()', '((())())', '((()()))', '(((())))']],
        "runner": testrunners.base_runner,
        'comparemethod': unordered
    },

    "up_and_right_1": {
        "fname": "up_and_right",
        "args": [2, 1],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "rru\nurr\nrur\n"}
    },

    "up_and_right_0": {
        "fname": "up_and_right",
        "args": [0, 0],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": ""}
    },

    "up_and_right_1_0": {
        "fname": "up_and_right",
        "args": [1, 0],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": "r\n"}
    },

    "up_and_right_neg": {
        "fname": "up_and_right",
        "args": [-1, -1],
        "ans": [None],
        "runner": testrunners.sorted_print_runner,
        "options": {"output": ""}
    },

    "flood_1_1": {
        "fname": "flood_fill",
        "args": [(1, 1)],
        "ans": [None],
        "runner": testrunners.flood_runner,
        "options": {"original": copy.deepcopy(exp_mat), "res": exp_mat_res11}
    },

    "flood_0_0": {
        "fname": "flood_fill",
        "args": [(0, 0)],
        "ans": [None],
        "runner": testrunners.flood_runner,
        "options": {"original": copy.deepcopy(exp_mat), "res": exp_mat_res00}
    },

    "hanoi1": {
        "fname": "play_hanoi",
        "ans": [None],
        "runner": testrunners.hanoi_runner,
        "options": {"n": 1}
    },

    "hanoi2": {
        "fname": "play_hanoi",
        "ans": [None],
        "runner": testrunners.hanoi_runner,
        "options": {"n": 2}
    },

    "hanoi5": {
        "fname": "play_hanoi",
        "ans": [None],
        "runner": testrunners.hanoi_runner,
        "options": {"n": 5}
    },

    "hanoi9": {
        "fname": "play_hanoi",
        "ans": [None],
        "runner": testrunners.hanoi_runner,
        "options": {"n": 9}
    },

    "hanoi0": {
        "fname": "play_hanoi",
        "ans": [None],
        "runner": testrunners.hanoi_runner,
        "options": {"n": 0}
    },
}


for k,v in cases_2.items():
    cases[k] = v

tsets = {'ex7':TestSet({},cases),
}
