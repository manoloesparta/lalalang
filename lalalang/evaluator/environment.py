from __future__ import annotations
from lalalang.evaluator.object import Object


class Environment:
    """
    The environment is just a table with the list of identifiers
    and its values associated, it has also a outer environment since
    we can access global values
    """

    @staticmethod
    def empty():
        return Environment(dict({}), None)

    def __init__(self, store: dict[str, Object], outer: Environment):
        self.store: dict[str, Object] = store
        self.outer: Environment = outer

    def get_local(self, name: str) -> Object:
        value: Object = self.store.get(name)
        if not value and self.outer != None:
            value = self.outer.get_local(name)
        return value

    def set_local(self, name: str, val: Object) -> Object:
        self.store[name] = val
        return val
