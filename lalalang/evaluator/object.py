from __future__ import annotations
from enum import Enum
from typing import Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from lalalang.parser.ast import Identifier, BlockStatement


class Object(ABC):
    """
    This is how we internally represent the objects in the
    interpreter in order to manipulate it
    """

    @abstractmethod
    def object_type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass


from lalalang.evaluator.environment import Environment  # Avoiding circular import


class ObjectType(Enum):
    """These are all the possible objects we can have"""

    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    RETURN_VALUE = "RETURN_VALUE"
    ERROR = "ERROR"
    FUNCTION = "FUNCTION"
    BUILTIN = "BUILTIN"


@dataclass
class Integer(Object):
    def __init__(self, value: int):
        self.value: int = value

    def object_type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)


@dataclass
class Boolean(Object):
    def __init__(self, value: bool):
        self.value: bool = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Boolean):
            return self.value == other.value
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Boolean):
            return self.value != other.value
        return False

    def object_type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return str(self.value).lower()


@dataclass
class Null(Object):
    def object_type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return "null"


@dataclass
class ReturnValue(Object):
    def __init__(self, value: Object):
        self.value: Object = value

    def object_type(self) -> ObjectType:
        return ObjectType.RETURN_VALUE

    def inspect(self) -> str:
        return self.value.inspect()


@dataclass
class Error(Object):
    def __init__(self, message: str):
        self.message: str = message

    def object_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return "ERROR: %s" % self.message


@dataclass
class Function(Object):
    def __init__(
        self, parameters: list[Identifier], body: BlockStatement, env: Environment
    ):
        self.env: Environment = env
        self.body: BlockStatement = body
        self.parameters: list[Identifier] = parameters

    def object_type(self) -> ObjectType:
        return ObjectType.FUNCTION

    def inspect(self) -> str:
        params: list[str] = [str(i) for i in self.parameters]
        return "fun(%s){\n\t%s\n}" % ("".join(params), str(self.body))


@dataclass
class Builtin(Object):
    def __init__(self, fun: Callable):
        self.fun: Callable = fun

    def object_type(self) -> ObjectType:
        return ObjectType.BUILTIN

    def inspect(self) -> str:
        return "Builtin function"
