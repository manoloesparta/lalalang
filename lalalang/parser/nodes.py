from abc import ABC, abstractmethod


class Node(ABC):
    """
    This class represents every node that is
    part of the Abstract Syntax Tree
    """

    @abstractmethod
    def token_literal(self) -> str:
        pass


class Statement(Node):
    """
    These nodes are reserved only for the
    statements, meaning it won't produce any value
    """

    @abstractmethod
    def statement_node(self) -> None:
        pass


class Expression(Node):
    """
    These nodes are reserved only for the
    expression, meaning it will produce a value
    """

    @abstractmethod
    def expression_node(self) -> None:
        pass
