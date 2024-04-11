#!/usr/bin/env python3
from parser import generate_ast, print_ast
from interpreter import eval_ast
from globals import variables, stack_a, stack_b
import globals


def eval_lines(lines):
    ast = generate_ast(lines)
    #print_ast(ast)
    eval_ast(ast)
    ast.children.clear()
    #print(variables)
    print("A:", stack_a)
    print("B:", stack_b)
    print(f"Executed {globals.pscmd_count} push_swap commands")

def repl():
    code = []
    next_line = input("(42PS) > ")
    while (next_line != "exit"):
        while (next_line != "run" and next_line != ";"):
            code.append(next_line)
            next_line = input("(42PS) > ")
            if (next_line == "exit"):
                return
        eval_lines(code)
        code.clear()
        next_line = input("(42PS) > ")

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 0:
        print("42ps v0.1")
    elif len(sys.argv) == 1:
        repl()
    elif len(sys.argv) == 2:
        with open(sys.argv[1], "r") as file:
            lines = file.readlines()
            eval_lines(lines)
    else:
        pass
