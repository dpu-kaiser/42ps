#!/usr/bin/env python3

stack_a = []
stack_b = []

pscmd_count = 0

variables = {}
commands = [
    "var",
    "inc",
    "dec",
    "input",
    "clear",
    "print",
    "add",
    "sub",
    "mul",
    "div",
    "mod",
    "lshift",
    "rshift",
]

pscmds = (
    "pa",
    "pb",
    "sa",
    "sb",
    "ss",
    "ra",
    "rb",
    "rr",
    "rra",
    "rrb",
    "rrr",
)
