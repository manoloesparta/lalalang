from lalalang.evaluator.evaluator import NULL
from lalalang.evaluator.object import *


def _print_line(*args: Object) -> Object:
    """Internal representation of println function"""
    if len(args) != 1:
        return Error("It must recieve one parameter")

    print(args[0].inspect())
    return NULL


def _print(*args: Object) -> Object:
    """Internal representation of print function"""
    if len(args) != 1:
        return Error("It must recieve one parameter")

    print(args[0].inspect(), end="")
    return NULL


def _to_string(*args: Object) -> Object:
    """Convert an integer to a string"""
    if len(args) != 1:
        return Error("It must recieve one parameter")

    number: Object = args[0]

    if not isinstance(number, Integer):
        return Error("It must be an integer")

    return String(str(number.value))


BUILTINS: dict[str, Object] = {
    "println": Builtin(_print_line),
    "print": Builtin(_print),
    "toString": Builtin(_to_string),
}
