from lalalang.parser.ast import *
from lalalang.evaluator.object import *
from lalalang.evaluator.environment import Environment

# References
TRUE: Boolean = Boolean(True)
FALSE: Boolean = Boolean(False)
NULL: Null = Null()

from lalalang.evaluator.builtins import BUILTINS


def eval_3lang(node: Node, env: Environment) -> Object:
    """
    This is executing a tree walk interpreter, doing a
    postorder traverse over the ast
    """

    # Statements
    if isinstance(node, Program):
        return eval_program(node, env)

    elif isinstance(node, ExpressionStatement):
        return eval_3lang(node.expression, env)

    elif isinstance(node, BlockStatement):
        return eval_block_statement(node, env)

    elif isinstance(node, ReturnStatement):
        value = eval_3lang(node.return_value, env)
        if is_error(value):
            return value
        return ReturnValue(value)

    elif isinstance(node, LetStatement):
        value = eval_3lang(node.value, env)
        if is_error(value):
            return value
        return env.set_local(node.name.value, value)

    # Expressions
    elif isinstance(node, PrefixExpression):
        right = eval_3lang(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)

    elif isinstance(node, InfixExpression):
        left = eval_3lang(node.left, env)
        if is_error(left):
            return left

        right = eval_3lang(node.right, env)
        if is_error(right):
            return right

        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, IfExpression):
        condition = eval_3lang(node.condition, env)
        if is_error(condition):
            return condition
        return eval_if_expression(node, env)

    elif isinstance(node, Identifier):
        return eval_identifier(node, env)

    elif isinstance(node, CallExpression):
        fun = eval_3lang(node.function, env)
        if is_error(fun):
            return fun

        args: list[Object] = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]

        return apply_function(fun, args)

    # Internal objects
    elif isinstance(node, IntegerLiteral):
        return Integer(node.value)

    elif isinstance(node, BooleanLiteral):
        return boolean_reference(node.value)

    elif isinstance(node, FunctionLiteral):
        params: list[Identifier] = node.parameters
        body: BlockStatement = node.body
        return Function(params, body, env)

    return None


def eval_program(root: Program, env: Environment) -> Object:
    """
    The root of every program is a list of statements, not
    the ast nodes, we need to start from the root
    """
    for statement in root.statements:
        result: Object = eval_3lang(statement, env)

        if isinstance(result, ReturnValue):
            return result.value

        elif isinstance(result, Error):
            return result

    return result


def eval_block_statement(block: BlockStatement, env: Environment) -> Object:
    """
    This is somewhat similar to eval_program except that is
    looking for any value to return and stop in the statement
    """
    for statement in block.statements:
        if result := eval_3lang(statement, env):
            rt: ObjectType = result.object_type()
            if rt == ObjectType.RETURN_VALUE or rt == ObjectType.ERROR:
                return result
    return result


def eval_prefix_expression(operator: str, right: Object) -> Object:
    """We support evaluating the two only prefix operators"""
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_operator_expression(right)
    return Error("Unknown operator %s %s" % (operator, right.object_type()))


def eval_bang_operator_expression(right: Object) -> Object:
    """
    If the object is null or false, it should evaluate to true, any
    othe expression or object should be false
    """
    if right in [FALSE, NULL]:
        return TRUE
    return FALSE


def eval_minus_operator_expression(right: Object) -> Object:
    """Just reverse the value is already in the object"""
    if isinstance(right, Integer):
        return Integer(-right.value)

    return Error("Unknown operator -%s" % right.object_type())


def eval_infix_expression(operator: str, left: Object, right: Object) -> Object:
    """Main method for evaluating infix expression"""
    if left.object_type() != right.object_type():
        return Error(
            "Type missmatch %s %s %s"
            % (left.object_type(), operator, right.object_type())
        )

    if isinstance(left, Integer) and isinstance(right, Integer):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return boolean_reference(left == right)
    elif operator == "!=":
        return boolean_reference(left != right)

    return Error(
        "Unknown operator %s %s %s"
        % (left.object_type(), operator, right.object_type())
    )


def eval_integer_infix_expression(operator: str, left: Object, right: Object) -> Object:
    """
    Here we evaulate relational and arithmetic operations
    with integers
    """
    if not (isinstance(left, Integer) and isinstance(right, Integer)):
        return NULL

    left_value: int = left.value
    right_value: int = right.value

    # Arithmetic
    if operator == "+":
        return Integer(left_value + right_value)
    elif operator == "-":
        return Integer(left_value - right_value)
    elif operator == "*":
        return Integer(left_value * right_value)
    elif operator == "/":
        return Integer(left_value // right_value)

    # Relational
    elif operator == "<":
        return boolean_reference(left_value < right_value)
    elif operator == ">":
        return boolean_reference(left_value > right_value)
    elif operator == "==":
        return boolean_reference(left_value == right_value)
    elif operator == "!=":
        return boolean_reference(left_value != right_value)

    return Error(
        "Unkown operator %s %s %s" % (left.object_type(), operator, right.object_type())
    )


def eval_if_expression(expression: IfExpression, env: Environment) -> Object:
    """
    Here we parse the condition and depending on the result we
    execute the consequence or alternative
    """
    predicate: Object = eval_3lang(expression.condition, env)

    if is_truthy(predicate):
        return eval_3lang(expression.consequence, env)
    elif expression.alternative is not None:
        return eval_3lang(expression.alternative, env)

    return NULL


def is_truthy(obj: Object) -> bool:
    """Here we check which kind of objects evaluate to true or false"""
    if obj in [NULL, FALSE]:
        return False
    return True


def eval_identifier(node: Identifier, env: Environment) -> Object:
    """Check if the name has a value associated in the environment"""
    if value := env.get_local(node.value):
        return value

    if proc := BUILTINS.get(node.value):
        return proc

    return Error("Identifier not found: %s" % node.value)


def eval_expressions(expressions: list[Expression], env: Environment) -> list[Object]:
    """Here we evaluate a bunch of expressions and keep track of them"""
    result: list[Object] = []
    for exp in expressions:
        evaluated = eval_3lang(exp, env)
        if is_error(evaluated):
            return [evaluated]
        result.append(evaluated)
    return result


def boolean_reference(value: bool) -> Boolean:
    """Return the Boolean reference instead of creating new value"""
    if value:
        return TRUE
    return FALSE


def apply_function(function: Object, args: list[Object]) -> Object:
    """
    We get the current environment and the outer one to run the
    body of the function with its parameters
    """
    if isinstance(function, Function):
        extended_env: Environment = extend_function_env(function, args)
        evaluated: Object = eval_3lang(function.body, extended_env)

        if isinstance(evaluated, ReturnValue):
            return evaluated.value
        return evaluated

    elif isinstance(function, Builtin):
        return function.fun(*args)

    return Error("Not a function: %s" % function.object_type())


def extend_function_env(function: Function, args: list[Object]) -> Environment:
    """Add the outer env to the local one"""
    env: Environment = Environment(dict({}), function.env)

    for index, param in enumerate(function.parameters):
        env.set_local(param.value, args[index])

    return env


def is_error(obj: Object) -> bool:
    """Helper method to check whenever an exception occurs"""
    if obj:
        return obj.object_type() == ObjectType.ERROR
    return False
