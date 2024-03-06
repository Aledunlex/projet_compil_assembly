from collections import namedtuple

NumericLiteral = namedtuple("NumericLiteral", ('value',))
ExpressionStatement = namedtuple("ExpressionStatement", ('expression',))
BinaryExpression = namedtuple("BinaryExpression", ('left', 'operator', 'right'))
Identifier = namedtuple("Identifier", ('name',))
VariableDeclarator = namedtuple("VariableDeclarator", ('id', 'init'))
VariableDeclaration = namedtuple("VariableDeclaration", ('declarations', 'kind'))
StringLiteral = namedtuple("StringLiteral", ('value',))
NullLiteral = namedtuple("NullLiteral", ())
UpdateExpression = namedtuple("UpdateExpression", ('operator', 'prefix', 'argument'))
CallExpression = namedtuple("CallExpression", ('callee', 'arguments'))
BlockStatement = namedtuple("BlockStatement", ('body', 'directives'))
WhileStatement = namedtuple("WhileStatement", ('test', 'body'))
AssignmentExpression = namedtuple("AssignmentExpression", ('operator', 'left', 'right'))
IfStatement = namedtuple("IfStatement", ('test', 'consequent', 'alternate'))
ForStatement = namedtuple("ForStatement", ('init', 'test', 'update', 'body'))
BreakStatement = namedtuple("BreakStatement", ('label',))
ContinueStatement = namedtuple("ContinueStatement", ('label',))
MemberExpression = namedtuple("MemberExpression", ('object', 'property', 'computed'))
BooleanLiteral = namedtuple("BooleanLiteral", ('value',))
LogicalExpression = namedtuple("LogicalExpression", ('left', 'operator', 'right'))
ReturnStatement = namedtuple("ReturnStatement", ('argument',))
FunctionDeclaration = namedtuple("FunctionDeclaration", ('id', 'generator', 'expression', 'params', 'body', 'is_async'))
EmptyStatement = namedtuple("EmptyStatement", ())
SwitchCase = namedtuple("SwitchCase", ('consequent', 'test'))
SwitchStatement = namedtuple("SwitchStatement", ('discriminant', 'cases'))
UnaryExpression = namedtuple("UnaryExpression", ('operator', 'prefix', 'argument'))
ObjectProperty = namedtuple("ObjectProperty", ('method', 'shorthand', 'computed', 'key', 'value'))
ObjectExpression = namedtuple("ObjectExpression", ('properties',))
ThisExpression = namedtuple("ThisExpression", ())
NewExpression = namedtuple("NewExpression", ('callee', 'arguments'))
Program = namedtuple("Program", ('sourceType', 'body', 'directives'))
File = namedtuple("File", ('program',))