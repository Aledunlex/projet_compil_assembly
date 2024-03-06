#!/usr/bin/env python3.10
# usage: ./C_gen3adresses.py <../exemples/file-compact.json>
import sys

from jsast import *
from utils import parse_program


class Generator:

    def __init__(self):
        self.index = 0
        self.index_loop = 0
        self.current = ""
        self.expression = ""
        self.func_dec = ""
        self.label_count = 0
        self.mem = dict()

    def gen(self, ast):
        match ast:
            case ExpressionStatement(exp):
                self.gen(exp)

            case BinaryExpression(e1, op, e2):
                self.gen(e1)
                strE1 = self.current
                self.gen(e2)
                strE2 = self.current
                self.current = f"temp_{self.index}"
                strE3 = self.current
                self.expression += f"movq {strE1}, {self.current}\n"
                self.index += 1
                self.current = f"temp_{self.index}"
                self.index += 1
                self.expression += f"movq {strE2}, {self.current}\n"
                if op == "+":
                    self.expression += f"addq {self.current}, {strE3}\n"
                elif op == "*":
                    self.expression += f"imulq {self.current}, {strE3}\n"
                elif op == "-":
                    self.expression += f"subq {self.current}, {strE3}\n"
                elif op == "==":
                    self.expression += f"je .L{self.label_count}\n"
                elif op == "!=":
                    self.expression += f"jne .L{self.label_count}\n"
                elif op == ">":
                    self.expression += f"jg .L{self.label_count}\n"
                elif op == ">=":
                    self.expression += f"jge .L{self.label_count}\n"
                elif op == "<":
                    self.expression += f"jl .L{self.label_count}\n"
                elif op == "<=":
                    self.expression += f"jle .L{self.label_count}\n"
                else:
                    self.expression += f"{op} pas implémenté dans BinaryExpression"
                self.current = strE3

            case NumericLiteral(val):
                self.current = f"temp_{self.index}"
                self.expression += f"movq ${val}, {self.current}\n"
                self.index += 1

            case BlockStatement(body, directives):
                for elmt in body:
                    self.gen(elmt)

            case VariableDeclarator(id, init):
                self.gen(init)
                strE = self.current
                self.expression += f"movq {strE}, temp_{self.index}\n"
                self.mem.update({id.name: f"temp_{self.index}"})
                self.index += 1

            case VariableDeclaration(dec, kind):
                for d in dec:
                    self.gen(d)

            case WhileStatement(test, body):
                self.expression += f"jmp .WHILE{self.index_loop}\n"
                self.expression += f".WHILE{self.index_loop}:\n"
                self.gen(test)
                self.expression += f"jae .ELSE{self.index_loop}\n"
                self.gen(body)
                self.expression += f"jmp .WHILE{self.index_loop}\n"
                self.expression += f".ELSE{self.index_loop}:\n"
                self.index_loop += 1

            case Identifier(name):
                if name in self.mem.keys():
                    self.current = self.mem[name]
                else:
                    return name

            case CallExpression(callee, args):
                for arg in args:
                    self.gen(arg)
                self.expression += f"call {callee.name}\n"

            case AssignmentExpression(op, left, right):
                match op:
                    case "+=":
                        exp = BinaryExpression(left, "+", right)
                        self.gen(exp)
                    case "-=":
                        exp = BinaryExpression(left, "-", right)
                        self.gen(exp)
                    case "=":
                        left_id = self.mem.get(left.name)
                        self.gen(right)
                        self.expression += f"movq {self.current}, {left_id}\n"

            case IfStatement(test, cons, alt):
                self.gen(test)
                self.label_count += 1
                self.expression += f"jmp .L{self.label_count}\n"
                self.expression += f".L{self.label_count - 1}:\n"

                if alt is not None:
                    self.gen(alt)
                self.label_count += 1
                self.expression += f".L{self.label_count - 1}:\n"
                self.gen(cons)

            case _ as e:
                raise NotImplementedError(e)


if __name__ == "__main__":
    ast = parse_program(sys.argv[1])
    generator = Generator()
    generator.func_dec += ".main:\n"
    generator.gen(ast)
    print(generator.func_dec)
    print(generator.expression)
