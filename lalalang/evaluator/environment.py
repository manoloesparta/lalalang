from lalalang.evaluator.object import Object


class Environment:
    @staticmethod
    def empty():
        return Environment(dict({}))

    def __init__(self, store: dict[str, Object]):
        self.store: dict[str, Object] = store

    def get_local(self, name: str) -> Object:
        return self.store.get(name)

    def set_local(self, name: str, val: Object) -> None:
        self.store[name] = val
        return val
