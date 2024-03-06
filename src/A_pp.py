#!/usr/bin/env python3.10
# usage: ./A_pp.py <../exemples/file-compact.json>
import sys

from jsast import *
from utils import parse_program


def pretty_print(ast, level=0):
    expression = "\t" * level

    match ast:
        case ExpressionStatement(exp):
            expression += pretty_print(exp) + ";\n"

        case BinaryExpression(e1, op, e2):
            match e1:
                case BinaryExpression(e3, "+", e4):
                    expression += "("
                    expression += pretty_print(e3)
                    expression += " + "
                    expression += pretty_print(e4)
                    expression += ")"
                case BinaryExpression(e3, "-", e4):
                    expression += "("
                    expression += pretty_print(e3)
                    expression += " - "
                    expression += pretty_print(e4)
                    expression += ")"

            expression += pretty_print(e1)
            expression += " " + op + " "
            expression += pretty_print(e2)

        case StringLiteral(val):
            expression += '"'
            expression += val
            expression += '"'

        case NumericLiteral(val):
            expression += str(val)

        case BlockStatement(body, _):
            expression = ""
            for elmt in body:
                expression += pretty_print(elmt, level)

        case VariableDeclarator(id, init):
            expression += pretty_print(id)
            if init is not None:
                expression += " = "
                expression += pretty_print(init)

        case VariableDeclaration(dec, kind):
            expression += kind + " "
            for i, d in enumerate(dec):
                if 0 < i < len(dec):
                    expression += ", "
                expression += pretty_print(d)

            expression += ";\n"

        case Identifier(name):
            expression += name

        case NullLiteral():
            expression += "null"

        case WhileStatement(test, body):
            expression += "while ("
            expression += pretty_print(test)
            expression += ") {\n"
            expression += pretty_print(body, level + 1)
            expression += ("\t" * level) + "}\n"

        case AssignmentExpression(op, l, r):
            expression += pretty_print(l)
            expression += " " + op + " "
            expression += pretty_print(r)

        case CallExpression(callee, arguments):
            expression += pretty_print(callee)
            expression += "("
            for i, a in enumerate(arguments):
                if 0 < i < len(arguments):
                    expression += ", "
                expression += pretty_print(a)

            expression += ")"

        case IfStatement(test, cons, alt):
            expression += "if ("
            expression += pretty_print(test)
            expression += ") {\n"
            expression += pretty_print(cons, level + 1)
            expression += ("\t" * level) + "}\n"
            if alt is not None:
                expression += "else {\n "
                expression += pretty_print(alt, level + 1)
                expression += ("\t" * level) + "}\n"

        case UnaryExpression(op, prefix, arg):
            if prefix is True:
                if op == "-" or op == "/":
                    expression += f"({op} {pretty_print(arg)})"
                else:
                    expression += f"{op} {pretty_print(arg)}"

        case ForStatement(init, test, update, body):
            expression += "for ("
            if init is not None:
                expression += pretty_print(init) + "; "
            expression += pretty_print(test) + "; "
            expression += pretty_print(update) + ";"
            expression += ') '
            expression += "{\n"
            expression += pretty_print(body, level + 1)
            expression += ("\t" * level) + "}\n"

        case BreakStatement(_):
            expression += "break;\n"

        case ContinueStatement(_):
            expression += "continue;\n"

        case FunctionDeclaration(id, _, _, params, body, _):
            expression += "function "
            expression += pretty_print(id) + " ("
            for i, p in enumerate(params):
                if 0 < i < len(params):
                    expression += ", "
                expression += pretty_print(p)
            expression += ") { \n"
            expression += pretty_print(body, level + 1)
            expression += ("\t" * level) + "}\n"

        case ReturnStatement(arg):
            expression += "return "
            expression += pretty_print(arg)
            expression += ";\n"

        case SwitchStatement(discrimant, cases):
            expression += "switch (" + pretty_print(discrimant) + ") {\n"
            for i, c in enumerate(cases):
                expression += pretty_print(c, level + 1)
            expression += ("\t" * level) + "}\n"

        case SwitchCase(cons, test):
            if test is not None:
                expression += "case " + pretty_print(test) + " :\n"
            else:
                expression += "default : \n"
            for c in cons:
                expression += pretty_print(c, level + 1) + "\n"

        case LogicalExpression(l, op, r):
            expression += pretty_print(l)
            expression += " " + op + " "
            expression += pretty_print(r)

        case EmptyStatement():
            pass

        case _ as e:
            raise NotImplementedError(e)

    if expression.endswith("\n\n"):
        expression = expression
    return expression


if __name__ == "__main__":
    ast = parse_program(sys.argv[1])
    print(pretty_print(ast))
