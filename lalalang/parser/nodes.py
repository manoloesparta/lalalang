from abc import ABC, abstractmethod


class Node(ABC):
    """
    This class represents every node that is
    part of the abstract syntax tree
    """

    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(Node):
    """
    These nodes are reserved only for the
    statements, meaning it won't produce any value.
    In la la lang there there are only two staments
    return and let.
    """

    @abstractmethod
    def statement_node(self) -> None:
        pass


class Expression(Node):
    """
    These nodes are reserved only for the
    expression, meaning it will produce a value. Aside
    from let and return everything is a expression.
    """

    @abstractmethod
    def expression_node(self) -> None:
        pass
