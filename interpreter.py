#!/usr/bin/env python3
from parser import AST, CMD, CTRL, VAL, BINOP, ITEM, LEN, parse_condition
from globals import variables, pscmds, stack_a, stack_b, pscmd_count
import globals

if_false = False

def exec_pscmd(cmd):
    match cmd:
        case "pa":
            if len(stack_b) > 0:
                stack_a.insert(0, stack_b.pop(0))
        case "pb":
            if len(stack_a) > 0:
                stack_b.insert(0, stack_a.pop(0))
        case "sa":
            if len(stack_a) > 1:
                stack_a[0], stack_a[1] = stack_a[1], stack_a[0]
        case "sb":
            if len(stack_b) > 1:
                stack_b[0], stack_b[1] = stack_b[1], stack_b[0]
        case "ss":
            exec_pscmd("sa")
            exec_pscmd("sb")
        case "ra":
            if len(stack_a) > 0:
                stack_a.append(stack_a.pop(0))
        case "rb":
            if len(stack_b) > 0:
                stack_b.append(stack_b.pop(0))
        case "rr":
            exec_pscmd("ra")
            exec_pscmd("rb")
        case "rra":
            if len(stack_a) > 0:
                stack_a.insert(0, stack_a.pop())
        case "rrb":
            if len(stack_b) > 0:
                stack_b.insert(0, stack_b.pop())
        case "rrr":
            exec_pscmd("rra")
            exec_pscmd("rrb")
    globals.pscmd_count += 1


def get_item(ast):
    if type(ast.index) == int:
        if ast.stack == ITEM.STACK_A and len(stack_a) > ast.index:
            return stack_a[ast.index]
        elif ast.stack == ITEM.STACK_B and len(stack_b) > ast.index:
            return stack_b[ast.index]
        else:
            return None
    else:
        ast.index = eval_ast(ast.index)
        return eval_ast(ast)



def exec_cmd(cmd):
    if cmd.cmd in pscmds:
        exec_pscmd(cmd.cmd)
        return
    match cmd.cmd:
        case "var":
            if len(cmd.args) == 1:
                variables[cmd.args[0]] = None
            elif len(cmd.args) == 3 and cmd.args[1] == "=":
                if cmd.args[2] == "*A":
                    variables[cmd.args[0]] = len(stack_a)
                elif cmd.args[2] == "*B":
                    variables[cmd.args[0]] = len(stack_b)
                elif cmd.args[2].startswith("A["):
                    variables[cmd.args[0]] = get_item(ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1])))
                elif cmd.args[2].startswith("B["):
                    variables[cmd.args[0]] = get_item(ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1])))
                elif cmd.args[2] in variables:
                    variables[cmd.args[0]] = variables[cmd.args[2]]
                else:
                    variables[cmd.args[0]] = int(cmd.args[2])
        case "inc":
            variables[cmd.args[0]] += 1
        case "dec":
            variables[cmd.args[0]] -= 1
        case "input":
            for arg in cmd.args:
                stack_a.append(int(arg))
        case "clear":
            stack_a.clear()
            stack_b.clear()
        case "print":
            if len(cmd.args) == 1:
                if cmd.args[0] in variables:
                    print(variables[cmd.args[0]])
                elif cmd.args[0] == "A":
                    print("A:", stack_a)
                elif cmd.args[0] == "B":
                    print("B:", stack_b)
                else:
                    print(cmd.args[0])
        case "add":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] + len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] + len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] + get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] + get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] + int(cmd.args[1]))
        case "sub":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] - len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] - len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] - get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] - get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] - int(cmd.args[1]))
        case "mul":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] * len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] * len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] * get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] * get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] * int(cmd.args[1]))
        case "div":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] / len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] / len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] / get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] / get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] / int(cmd.args[1]))
        case "mod":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] % len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] % len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] % get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] % get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] % int(cmd.args[1]))
        case "lshift":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] << len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] << len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] << get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] << get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] << int(cmd.args[1]))
        case "rshift":
            if len(cmd.args) == 2:
                if cmd.args[1] == "*A":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] >> len(stack_a))
                elif cmd.args[1] == "*B":
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] >> len(stack_b))
                elif cmd.args[1].startswith("A["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] >> get_item(
                        ITEM(ITEM.STACK_A, parse_condition(cmd.args[2][2:-1]))))
                elif cmd.args[1].startswith("B["):
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] >> get_item(
                        ITEM(ITEM.STACK_B, parse_condition(cmd.args[2][2:-1]))))
                else:
                    variables[cmd.args[0]] = int(variables[cmd.args[0]] >> int(cmd.args[1]))


def eval_ast(ast):
    global if_false
    if type(ast) == VAL:
        if ast.vtype == VAL.VAR:
            return variables[ast.value]
        else:
            return ast.value
    elif type(ast) == BINOP:
        left = eval_ast(ast.left)
        right = eval_ast(ast.right)
        if ast.op == "==":
            return left == right
        elif ast.op == "!=":
            return left != right
        elif ast.op == "<":
            if left == None and right != None:
                return True
            elif right == None:
                return False
            else:
                return left < right
        elif ast.op == "<=":
            if left == None:
                return True
            elif right == None:
                return False
            else:
                return left <= right
        elif ast.op == ">":
            if left == None and right != None:
                return False
            elif right == None:
                return True
            else:
                return left > right
        elif ast.op == ">=":
            if right == None:
                return True
            elif left == None:
                return False
            else:
                return left >= right
    elif type(ast) == CMD:
        exec_cmd(ast)
    elif type(ast) == CTRL:
        condition = parse_condition(ast.condition)
        match ast.ctype:
            case CTRL.IF:
                if eval_ast(condition):
                    for child in ast.children:
                        eval_ast(child)
                elif ast.alt:
                    if_false = True
            case CTRL.WHILE:
                while eval_ast(condition):
                    for child in ast.children:
                        eval_ast(child)
            case CTRL.ELSE:
                if if_false:
                    if_false = False
                    for child in ast.children:
                        eval_ast(child)
            case CTRL.ELIF:
                if if_false:
                    if_false = False
                    if eval_ast(condition):
                        for child in ast.children:
                            eval_ast(child)
                    elif ast.alt:
                        if_false = True
    elif type(ast) == ITEM:
        return get_item(ast)
    elif type(ast) == LEN:
        if ast.stack == LEN.A:
            return len(stack_a)
        elif ast.stack == LEN.B:
            return len(stack_b)
        # elif ast.stack == ITEM.STACK_B:
        #     ast.index = eva
        #     return stack_b[eval_ast(ast.index)]
        # else:
        #     return None


    else:
        for child in ast.children:
            eval_ast(child)