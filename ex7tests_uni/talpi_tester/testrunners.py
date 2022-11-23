import copy
from importlib import import_module
import sys
import os
from io import StringIO

def peel(runners, modulename, fname, args=[], kwargs={}, options={}):
    return runners[-1](modulename, fname, args, kwargs,options,runners[:-1])

def base_runner(modulename, fname, args=[], kwargs={}, options={}, runners=[], tname=''):
    module = import_module(modulename)
    func = getattr(module, fname)
    return None,func(*args, **kwargs)

def check_args(modulename, fname, args=[], kwargs={}, options={}, runners=[base_runner]):
    args2 = copy.deepcopy(args)
    kwargs2 = copy.deepcopy(kwargs)
    code,res = peel(runners, modulename, fname, args, kwargs)
    if code:
        return code,res
    if not (args==args2 and kwargs==kwargs2): #good enough for now
        return ("modified", None)
    return None,res

def import_runner(modulename, fname, args=[], kwargs={}, options={},
                  resfilter=None,tname=''):
    if 'input' in options:
        return input_runner(modulename, fname, args, kwargs, options,tname)

    if 'output' in options:
        return print_runner(modulename, fname, args, kwargs, options,tname)

    check_input=options.pop('check_input') if 'check_input' in options else True
    resfilter=options.pop('resfilter') if 'resfilter' in options else None

    if check_input:
        runners = [base_runner,check_args]
    else:
        runners = [base_runner]
    code,res = peel(runners, modulename, fname, args, kwargs)
    if code:
        return code,res
    if resfilter:
        res = resfilter(res)
    return None,res

def print_runner(modulename, fname, args=[], kwargs={}, options={},tname=''):
    try:
        output=options.pop('output') if 'output' in options else None
        _stdout = sys.stdout
        tmpout = StringIO()
        sys.stdout = tmpout
        code,res = import_runner(modulename, fname, args, kwargs, options,
                                 tname=tname)
        if code:
            return code,res
        if output is None:
            if res is not None:
                return("wrong", 'return value should be None')
            res = tmpout.getvalue()
        else:
            o = tmpout.getvalue()
            if o != output:
                return("wrong", 'wrong string printed to stdout\nExpected: {0}\nactual: {1}'.format(output.replace("\n", "\\n"), o.replace("\n", "\\n")))

        return None,res
    finally:
        sys.stdout = _stdout


def flood_runner(modulename, fname, args=[], kwargs={}, options={}, tname=''):
    original = options.pop('original')
    args.insert(0, original)

    code,res = base_runner(modulename, fname, args, kwargs, options,
                             tname=tname)
    if code:
        return code,res

    else:
        output=options.pop('res')

        if original != output:
            return("wrong", 'wrong string printed to stdout\nExpected:\n{0}\n\nActual:\n{1}\n\n'.format("\n".join([str(i) for i in original]), "\n".join([str(i) for i in output])))

    return None,res


def sorted_print_runner(modulename, fname, args=[], kwargs={}, options={}, tname=''):
    try:
        output=options.pop('output') if 'output' in options else None
        _stdout = sys.stdout
        tmpout = StringIO()
        sys.stdout = tmpout
        code,res = import_runner(modulename, fname, args, kwargs, options,
                                 tname=tname)
        if code:
            return code,res
        if output is None:
            if res is not None:
                return("wrong", 'return value should be None')
            res = tmpout.getvalue()
        else:
            o = sorted(tmpout.getvalue().split("\n"))
            output = sorted(output.split("\n"))

            if "" in o and "" in output:
                o = o[1:]
                output = output[1:]

            if o != output:
                return("wrong", 'wrong string printed to stdout\nExpected: {0}\nActual: {1}\n(Order doesnt matter)'.format(output, o))

        return None,res
    finally:
        sys.stdout = _stdout


def input_runner(modulename, fname, args=[], kwargs={}, options={},tname=''):
    try:
        input=options.pop('input')
        _stdin = sys.stdin
        tmpin = StringIO(input)
        sys.stdin = tmpin
        code,res = import_runner(modulename, fname, args, kwargs, options,
                                 tname=tname)
        if code:
            return code,res
        if tmpin.read():
            return("inputerr", 'did not read all input')
        return None,res
    finally:
        sys.stdin = _stdin

def functionname_doc_runner(modulename, fname, args=[], kwargs={}, options={},tname=''):
    try:
        module = import_module(modulename)
    except:
        return None,"importfailed"
    if fname not in module.__dict__:
        return None,"notexist"
    if not callable(module.__dict__[fname]):
        return None,"notcallable"
    if not module.__dict__[fname].__doc__:
        return None, "Missing documentation of function"
    return None,True

def file_cmp_runner(modulename, fname, args=[], kwargs={}, options={}, runners=[], tname=''):
    module = import_module(modulename)
    find_words = getattr(module, "find_words_in_matrix")

    results = find_words(*args)

    cmp_file = options.pop('real_out')
    func_out = options.pop('user_out')

    write_to_out = getattr(module, "write_output_file")
    write_to_out(results, func_out)

    cmp_to = ""
    func_out_data =  ""
    with open(cmp_file, 'r') as f:
        cmp_to = f.read().strip("\n")

    with open(func_out, 'r') as f:
        func_out_data = f.read().strip("\n")

    return None, sorted(cmp_to.split("\n")) == sorted(func_out_data.split("\n"))


class Hanoi(object):
    def __init__(self, n):
        self.n = n
        self.src = [i for i in range(self.n)]
        self.dest = []
        self.temp = []
        self.moves = 0

    def move(self, src, dest):
        try:
            to_move = src.pop()
        except:
            raise Exception("TEST FAILED: You tried to move a disc from an empty pole!")
        if dest:
            if dest[-1] > to_move:
                raise Exception("TEST FAILED: You tried moving a disc onto a smaller one!")
        dest.append(to_move)
        self.moves += 1

    def check_finish(self):
        return self.dest == [i for i in range(self.n)]

    def good_on_moves(self):
        return self.moves == (2**self.n) - 1

    def get_poles_str(self):
        final = " s  t  d \n---------\n\n"

        length = max(len(self.src), len(self.temp), len(self.dest))

        for i in range(length):
            curr = ""
            real_index = length - 1 - i

            if real_index >= len(self.src):
                curr += " | "
            else:
                curr += " " + str(self.src[real_index]) + " "

            if real_index >= len(self.temp):
                curr += " | "
            else:
                curr += " " + str(self.temp[real_index]) + " "

            if real_index >= len(self.dest):
                curr += " | "
            else:
                curr += " " + str(self.dest[real_index]) + " "


            final += curr + "\n"

        final += " _  _  _ \n"
        return final


def hanoi_runner(modulename, fname, args=[], kwargs={}, options={}, tname=''):
    n = options.pop('n')
    game = Hanoi(n)

    args = [game, n, game.src, game.dest, game.temp]
    code,res = base_runner(modulename, fname, args, kwargs, options,
                             tname=tname)
    if code:
        return code,res

    else:
        if not game.check_finish():
            state = game.get_poles_str()
            return("wrong", "\nTEST FAILED\nYou did not complete the game.\nYour current state:\n{0}\n(0 is the largest disc, 1 is smaller, etc...)\n".format(game.get_poles_str()))

        if not game.good_on_moves():
            return("wrong", "\nTEST FAILED\nYou're not good on moves!\nThe game is solvable in {0} move(s), but it took you {1}!\n(However, you did complete the game)\n".format((2**game.n) - 1, game.moves))

    return None,res
