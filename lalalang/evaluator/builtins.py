from lalalang.evaluator.evaluator import NULL
from lalalang.evaluator.object import Object, Builtin, Function, Error, Integer


def _println(*args: Object):
    """Internal representation of println function"""
    if len(args) != 1:
        return Error("It must recieve one parameter")

    print(args[0].inspect())
    return NULL


def _print(*args: Object):
    """Internal representation of print function"""
    if len(args) != 1:
        return Error("It must recieve one parameter")

    print(args[0].inspect(), end="")
    return NULL


BUILTINS: dict[str, Object] = {
    "println": Builtin(_println),
    "print": Builtin(_print),
}
