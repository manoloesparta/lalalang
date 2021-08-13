from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum


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


class ObjectType(Enum):
    """These are all the possible objects we can have"""

    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"


class Integer(Object):
    def __init__(self, value: int):
        self.value: int = value

    def object_type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):
    def __init__(self, value: bool):
        self.value = value

    def object_type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return str(self.value)


class Null(Object):
    def object_type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return "null"
