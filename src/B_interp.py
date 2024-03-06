#!/usr/bin/env python3.10
# usage: ./B_interp.py <../exemples/file-compact.json>
import sys

from jsast import *
from utils import parse_program


class Interpret:
    """Un interprète contient une pile d'environnements"""

    def __init__(self):
        self.stack = []
        self.add(Env())

    def add(self, env):
        self.stack.append(env)

    def remove(self, env):
        self.stack.pop(env)

    def isDeclared(self, var):
        for i in range(len(self.stack)):
            if var in self.stack[i].vals:
                return True
        return False

    def getValue(self, var):
        for i in range(len(self.stack)):
            if var in self.stack[i].vals:
                return self.stack[i].vals[var]

    def setValue(self, var, value, op):
        for i in range(len(self.stack)):
            if var in self.stack[i].vals:
                if op == "=":
                    self.stack[i].vals[var] = value
                elif op == "+=":
                    self.stack[i].vals[var] = self.interpEval(Identifier(var)) + value
                elif op == "-=":
                    self.stack[i].vals[var] = self.interpEval(Identifier(var)) - value

    def interpEval(self, ast):
        match ast:

            case BlockStatement(body, dir):
                return self.interpTransfo(ast)

            case UnaryExpression(op, prefix, arg):
                return self.interpEval(BinaryExpression(NumericLiteral(value=0), op, arg))

            case BinaryExpression(e1, "+", e2):
                return self.interpEval(e1) + self.interpEval(e2)

            case BinaryExpression(e1, "-", e2):
                return self.interpEval(e1) - self.interpEval(e2)

            case BinaryExpression(e1, "*", e2):
                return self.interpEval(e1) * self.interpEval(e2)

            case BinaryExpression(e1, "<", e2):
                return self.interpEval(e1) < self.interpEval(e2)

            case BinaryExpression(e1, "!=", e2):
                return self.interpEval(e1) != self.interpEval(e2)

            case BinaryExpression(e1, "==", e2):
                return self.interpEval(e1) == self.interpEval(e2)

            case StringLiteral(val):
                return val

            case NumericLiteral(val):
                return int(val)

            case ExpressionStatement(exp):
                return self.interpEval(exp)

            case Identifier(name):
                if self.isDeclared(name):
                    return self.getValue(name)
                else:
                    return name

            case VariableDeclarator(id, init):
                if (init is None):
                    return {self.interpEval(id): None}
                return {self.interpEval(id): self.interpEval(init)}

            case VariableDeclaration(dec, kind):
                return self.interpTransfo(ast)

            case NullLiteral():
                return None

            case WhileStatement(test, body):
                return self.interpTransfo(ast)

            case ForStatement(init, test, update, body):
                return self.interpTransfo(ast)

            case AssignmentExpression(op, l, r):
                return self.interpTransfo(ast)

            case CallExpression(ide, arg):
                if not isinstance(namedtuple, type(self.interpEval(ide))):
                    func = ide.name
                else:
                    func = self.interpEval(ide)
                if self.getValue(func) is None:
                    if "print" in func:
                        vals = [self.interpEval(var) for var in arg]
                        print(vals if len(vals) > 1 else vals[0])
                        return
                    raise NotImplementedError(f"Function {func} is not defined.")
                else:
                    try:
                        self.setValue(list(self.stack[-1:][0].vals.keys())[0], self.interpEval(arg[-1:][0]), "=")
                        return self.interpEval(self.getValue(func))
                    except ValueError as e:
                        return e.args[0]

            case IfStatement(test, cons, alt):
                return self.interpTransfo(ast)

            case ReturnStatement(arg):
                raise ValueError(self.interpEval(arg))

            case [ReturnStatement(arg)]:
                return self.interpEval(arg)

            case FunctionDeclaration(id, generator, expression, params, body, is_async):
                return self.interpTransfo(ast)

            case EmptyStatement():
                return

            case SwitchStatement(discriminant, cases):
                return self.interpTransfo(ast)

            case SwitchCase(cons, test):
                self.interpEval(cons)

            case _ as e:
                raise NotImplementedError(e)

    def interpTransfo(self, ast):
        match ast:
            case BlockStatement(body, directives):
                for elmt in body:
                    match elmt:
                        case BreakStatement(label):
                            break

                        case ContinueStatement(label):
                            continue

                        case _ as e:
                            self.interpEval(elmt)

            case VariableDeclaration(dec, kind):
                env = Env()
                for d in dec:
                    env.update(self.interpEval(d))
                self.add(env)

            case [Identifier(_)]:
                self.interpEval(ast)

            case FunctionDeclaration(id, generator, expression, params, body, is_async):
                # enregistre la fonction
                self.stack[0].update({self.interpEval(id): body})

                # enregistre les vars locales
                env = Env()
                for param in params:
                    env.update({self.interpEval(param): None})
                self.add(env)

            case WhileStatement(test, body):
                while self.interpEval(test):
                    self.interpTransfo(body)

            case SwitchStatement(discriminant, cases):
                dis = self.interpEval(discriminant)
                for case in cases:
                    if case.test:
                        if self.interpEval(case.test) == discriminant:
                            self.interpEval(case)
                self.interpEval(cases[-1])

            case ForStatement(init, test, update, body):
                if init is not None:
                    self.interpEval(init)
                while self.interpEval(test):
                    self.interpEval(update)
                    self.interpEval(body)

            case AssignmentExpression(op, Identifier(name), r):
                self.setValue(name, self.interpEval(r), op)

            case CallExpression(id, args):
                self.interpEval(ast)

            case IfStatement(test, cons, alt):
                if self.interpEval(test):
                    self.interpEval(cons)
                else:
                    if alt is not None:
                        self.interpEval(alt)

            case ReturnStatement(arg):
                self.interpEval(ast)

            case _ as e:
                raise NotImplementedError(e)


class Env:
    """Un environnement contient un set de dictionnaires attribuant à chaque variable une valeur"""

    def __init__(self):
        self.vals = dict()

    def update(self, dic):
        self.vals.update(dic)

    def pop(self, dic):
        self.vals.pop(dic)

    def __str__(self):
        return str(self.vals)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    interprete = Interpret()
    ast = parse_program(sys.argv[1])
    interprete.interpTransfo(ast)
