#!/usr/bin/env python3

from globals import pscmds
from globals import variables, commands

class AST():
    def __init__(self, parent = None, children = []):
        self.parent = parent
        self.children = children


class CMD(AST):
    def __init__(self, cmd, args = [], parent = None, children = []):
        super().__init__(parent, children)
        self.cmd = cmd
        self.args = args


class CTRL(AST):
    IF = 1
    WHILE = 2
    ELSE = 3
    ELIF = 4
    def __init__(self, ctype, condition = None, parent = None, children = [], alt = False):
        super().__init__(parent, children)
        self.ctype = ctype
        self.condition = condition
        self.alt = alt


class VAL(AST):
    VALUE = 1
    VAR = 2
    def __init__(self, vtype, value, parent = None, children = []):
        super().__init__(parent, children)
        self.vtype = vtype
        self.value = value

class BINOP(AST):
    def __init__(self, op, left, right, parent = None):
        super().__init__(parent)
        self.op = op
        self.left = left
        self.right = right

class ITEM(AST):
    STACK_A = 1
    STACK_B = 2
    def __init__(self, stack, index):
        self.stack = stack
        self.index = index

class LEN(AST):
    A = 1
    B = 2
    def __init__(self, stack):
        self.stack = stack

def parse_condition(line):
    toks = line.strip().split(' ')
    if len(toks) == 1:
        if toks[0] == "*A":
            return LEN(LEN.A)
        elif toks[0] == "*B":
            return LEN(LEN.B)
        elif toks[0].startswith("A["):
            if toks[0][-2].isdigit():
                return ITEM(ITEM.STACK_A, int(toks[0][2:-1]))
            else:
                return ITEM(ITEM.STACK_A, parse_condition(toks[0][2:-1]))
        elif toks[0].startswith("B["):
            if toks[0][-2].isdigit():
                return ITEM(ITEM.STACK_B, int(toks[0][2:-1]))
            else:
                return ITEM(ITEM.STACK_B, parse_condition(toks[0][2:-1]))
        elif toks[0][0] == "-" or toks[0][0].isdigit():
            return VAL(VAL.VALUE, int(toks[0]))
        else:
            return VAL(VAL.VAR, toks[0])
    elif len(toks) == 3:
        return BINOP(toks[1], parse_condition(toks[0]), parse_condition(toks[2]))
    return VAL(VAL.VALUE, True)


def generate_ast(lines):
    ast = AST(None, [])
    cur = ast
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        if line in pscmds:
            cur.children.append(CMD(line))
        elif line == "endif" or line == "endwhile":
            cur = cur.parent
        elif line == "else":
            cur = cur.parent
            cur.children[-1].alt = True
            cur.children.append(CTRL(CTRL.ELSE, None, cur, []))
            cur = cur.children[-1]
        elif line.startswith("if"):
            cur.children.append(CTRL(CTRL.IF, line[3:], cur, []))
            cur = cur.children[-1]
        elif line.startswith("elif"):
            cur = cur.parent
            cur.children[-1].alt = True
            cur.children.append(CTRL(CTRL.ELIF, line[5:], cur, []))
            cur = cur.children[-1]
        elif line.startswith("while"):
            cur.children.append(CTRL(CTRL.WHILE, line[6:], cur, []))
            cur = cur.children[-1]
        else:
            toks = line.split(" ")
            if toks[0] in commands:
                cur.children.append(CMD(toks[0], toks[1:], cur))
            elif len(toks) > 1 and toks[1] == "=":
                cur.children.append(CMD("var", toks, cur))
            elif len(toks) > 1 and toks[1] == "+=":
                cur.children.append(CMD("add", [toks[0], toks[2]], cur))
            elif len(toks) > 1 and toks[1] == "-":
                cur.children.append(CMD("sub", [toks[0], toks[2]], cur))
            elif len(toks) > 1 and toks[1] == "*=":
                cur.children.append(CMD("mul", [toks[0], toks[2]], cur))
            elif len(toks) > 1 and toks[1] == "/=":
                cur.children.append(CMD("div", [toks[0], toks[2]], cur))
            elif len(toks) > 1 and toks[1] == "%=":
                cur.children.append(CMD("mod", [toks[0], toks[2]], cur))

    return ast

def print_ast(ast, offset = 0):
    print(f"{' ' * offset}{type(ast)}: ")
    for child in ast.children:
        print_ast(child, offset + 2)
