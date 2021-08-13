from __future__ import annotations
from enum import Enum
from typing import Callable
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import Token, TokenType
from lalalang.parser.precedence import PRECEDENCES, ExpressionPrecedence
from lalalang.parser.ast import *


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.current_token: Token = Token.empty()
        self.peek_token: Token = Token.empty()
        self.statements: list[Statement] = []
        self.errors: list[str] = []
        self.prefix_parse_funs: dict[TokenType, Callable] = dict({})
        self.infix_parse_funs: dict[TokenType, Callable] = dict({})
        self._setup()

    def __repr__(self):
        conversion: list[str] = [repr(i) for i in self.statements]
        return "\n".join(conversion)

    def __str__(self):
        conversion: list[str] = [str(i) for i in self.statements]
        return "".join(conversion)

    def parse_program(self) -> Program:
        """
        This is the main method that will traverse the tokens and generate
        the respective abstract syntax tree
        """
        program: Program = Program()
        while not self._current_token_is(TokenType.EOF):
            statement: Statement = self._parse_statement()
            if statement:
                program.add_statement(statement)
            self._next_token()
        return program

    def _setup(self) -> None:
        """Some stuff that needs to be ready at the construction of this class"""
        self._register_prefix_fun(TokenType.IDENT, self._parse_identifier)
        self._register_prefix_fun(TokenType.INT, self._parse_integer_literal)
        self._register_prefix_fun(TokenType.BANG, self._parse_prefix_expression)
        self._register_prefix_fun(TokenType.MINUS, self._parse_prefix_expression)
        self._register_prefix_fun(TokenType.TRUE, self._parse_boolean)
        self._register_prefix_fun(TokenType.FALSE, self._parse_boolean)
        self._register_prefix_fun(TokenType.LPAREN, self._parse_grouped_expression)
        self._register_prefix_fun(TokenType.IF, self._parse_if_expression)
        self._register_prefix_fun(TokenType.FUNCTION, self._parse_function_literal)

        self._register_infix_fun(TokenType.PLUS, self._parse_infix_expression)
        self._register_infix_fun(TokenType.MINUS, self._parse_infix_expression)
        self._register_infix_fun(TokenType.SLASH, self._parse_infix_expression)
        self._register_infix_fun(TokenType.ASTERISK, self._parse_infix_expression)
        self._register_infix_fun(TokenType.EQ, self._parse_infix_expression)
        self._register_infix_fun(TokenType.NOT_EQ, self._parse_infix_expression)
        self._register_infix_fun(TokenType.LT, self._parse_infix_expression)
        self._register_infix_fun(TokenType.GT, self._parse_infix_expression)
        self._register_infix_fun(TokenType.LPAREN, self._parse_call_expression)

        self._next_token()
        self._next_token()

    def _next_token(self) -> None:
        """This helps us moving arround the lexer to watch one token ahead"""
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def _parse_statement(self) -> Statement:
        """Here are the conditionals to handle any statements defined by us"""
        if self._current_token_is(TokenType.LET):
            return self._parse_let_statement()
        elif self._current_token_is(TokenType.RETURN):
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_let_statement(self) -> LetStatement:
        """Parse the let statement"""
        statement: LetStatement = LetStatement.empty()
        statement.token = self.current_token

        if not self._peek_expected(TokenType.IDENT):
            return None

        statement.name = Identifier(self.current_token, self.current_token.literal)

        if not self._peek_expected(TokenType.ASSIGN):
            return None

        self._next_token()
        statement.value = self._parse_expression(ExpressionPrecedence.LOWEST)

        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_return_statement(self) -> ReturnStatement:
        """Pase the return statement"""
        statement: ReturnStatement = ReturnStatement.empty()
        statement.token = self.current_token

        self._next_token()

        statement.return_value = self._parse_expression(ExpressionPrecedence.LOWEST)
        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_expression_statement(self) -> ExpressionStatement:
        """Parse the expression statement"""
        statement: ExpressionStatement = ExpressionStatement.empty()
        statement.expression = self._parse_expression(ExpressionPrecedence.LOWEST)

        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_expression(self, precedence: ExpressionPrecedence) -> Expression:
        """
        This is the main method that contains explicitly pratt
        parsing, it is a recursive algorithm which decides about
        infix and prefix parsing functions.
        """
        prefix: Callable = self.prefix_parse_funs.get(self.current_token.token_type)
        if not prefix:
            self._no_prefix_parsing_error(self.current_token.token_type)
            return None

        left_expression: Expression = prefix()

        while (
            not self._peek_token_is(TokenType.SEMICOLON)
            and precedence < self._peek_precendence()
        ):
            infix: Callable = self.infix_parse_funs.get(self.peek_token.token_type)
            if not infix:
                return left_expression

            self._next_token()
            left_expression = infix(left_expression)

        return left_expression

    def _parse_identifier(self) -> Identifier:
        """Parse any identifier (e.g variable and function names)"""
        return Identifier(self.current_token, self.current_token.literal)

    def _parse_integer_literal(self) -> IntegerLiteral:
        """Parse an integer literal (the actual number)"""
        literal: IntegerLiteral = IntegerLiteral.empty()
        literal.token = self.current_token
        try:
            number: int = int(self.current_token.literal)
        except ValueError:
            self.errors.append(
                "Could not parse %s as integer" % self.current_token.literal
            )
        literal.value = number
        return literal

    def _parse_boolean(self) -> BooleanLiteral:
        """Parse boolean expression"""
        return BooleanLiteral(
            self.current_token, self._current_token_is(TokenType.TRUE)
        )

    def _parse_grouped_expression(self) -> Expression:
        """Parse any grouped expression (any expression with more than one operator)"""
        self._next_token()
        expression: Expression = self._parse_expression(ExpressionPrecedence.LOWEST)
        if self._peek_expected(TokenType.RPAREN):
            return expression
        return None

    def _parse_if_expression(self) -> IfExpression:
        """Parse if expressions"""
        expression: IfExpression = IfExpression.empty()
        expression.token = self.current_token

        if not self._peek_expected(TokenType.LPAREN):
            return None

        self._next_token()
        expression.condition = self._parse_expression(ExpressionPrecedence.LOWEST)

        if not self._peek_expected(TokenType.RPAREN):
            return None

        if not self._peek_expected(TokenType.LBRACE):
            return None

        expression.consequence = self._parse_block_statement()

        if self._peek_token_is(TokenType.ELSE):
            self._next_token()

            if not self._peek_expected(TokenType.LBRACE):
                return None

            expression.alternative = self._parse_block_statement()

        return expression

    def _parse_block_statement(self) -> BlockStatement:
        """Parse the block statements (consequent and alternatives of if expressions)"""
        block: BlockStatement = BlockStatement.empty()
        block.statements = []

        self._next_token()

        while not self._current_token_is(
            TokenType.RBRACE
        ) and not self._current_token_is(TokenType.EOF):
            statement = self._parse_statement()

            if statement:
                block.statements.append(statement)

            self._next_token()

        return block

    def _parse_function_literal(self) -> FunctionLiteral:
        """Parse the name, parameters and body of a function"""
        literal: FunctionLiteral = FunctionLiteral.empty()
        literal.token = self.current_token

        if not self._peek_expected(TokenType.LPAREN):
            return None

        literal.parameters = self._parse_function_parameters()

        if not self._peek_expected(TokenType.LBRACE):
            return None

        literal.body = self._parse_block_statement()
        return literal

    def _parse_function_parameters(self) -> list[Identifier]:
        """Parse the function parameters"""
        identifiers: list[Identifier] = []

        if self._peek_token_is(TokenType.RPAREN):
            self._next_token()
            return identifiers

        self._next_token()

        ident: Identifier = Identifier(self.current_token, self.current_token.literal)
        identifiers.append(ident)

        while self._peek_token_is(TokenType.COMMA):
            self._next_token()
            self._next_token()
            ident = Identifier(self.current_token, self.current_token.literal)
            identifiers.append(ident)

        if not self._peek_expected(TokenType.RPAREN):
            return None

        return identifiers

    def _parse_call_expression(self, function: Expression) -> CallExpression:
        """Parse a call expression (function call)"""
        expression: CallExpression = CallExpression.empty()
        expression.function = function
        expression.token = self.current_token
        expression.arguments = self._parse_call_arguments()
        return expression

    def _parse_call_arguments(self) -> list[Expression]:
        """Parse the call arguments"""
        arguments: list[Expression] = []

        if self._peek_token_is(TokenType.RPAREN):
            self._next_token()
            return arguments

        self._next_token()
        arguments.append(self._parse_expression(ExpressionPrecedence.LOWEST))

        while self._peek_token_is(TokenType.COMMA):
            self._next_token()
            self._next_token()
            arguments.append(self._parse_expression(ExpressionPrecedence.LOWEST))

        if not self._peek_expected(TokenType.RPAREN):
            return None

        return arguments

    def _parse_prefix_expression(self) -> PrefixExpression:
        """We return the prefix expression of our current token"""
        expression: PrefixExpression = PrefixExpression.empty()
        expression.token = self.current_token
        expression.operator = self.current_token.literal

        self._next_token()
        expression.right = self._parse_expression(ExpressionPrecedence.PREFIX)

        return expression

    def _parse_infix_expression(self, left: Expression) -> InfixExpression:
        """We return the infix expression of our current token"""
        expression: InfixExpression = InfixExpression.empty()
        expression.token = self.current_token
        expression.operator = self.current_token.literal
        expression.left = left

        precedence: ExpressionPrecedence = self._current_precedence()
        self._next_token()
        expression.right = self._parse_expression(precedence)

        return expression

    def _no_prefix_parsing_error(self, token_type: TokenType) -> None:
        """Add this error message whenever a prefix expression is unrecognized"""
        message = "No prefix function to parse %s" % token_type
        self.errors.append(message)

    def _current_precedence(self) -> ExpressionPrecedence:
        """Gets the precendence of the current token"""
        precendence: ExpressionPrecedence = PRECEDENCES.get(
            self.current_token.token_type
        )
        if not precendence:
            return ExpressionPrecedence.LOWEST
        return precendence

    def _current_token_is(self, token_type: TokenType) -> bool:
        """Check if the current token is a specific TokenType"""
        return self.current_token.token_type == token_type

    def _peek_token_is(self, token_type: TokenType) -> bool:
        """Check if the next token is a specific TokenType"""
        return self.peek_token.token_type == token_type

    def _peek_error(self, token_type: TokenType) -> None:
        """Add error message of unexpected tokens"""
        message: str = "Expected type %s, got %s" % (
            token_type,
            self.peek_token.token_type,
        )
        self.errors.append(message)

    def _peek_precendence(self) -> ExpressionPrecedence:
        """Gets the precedence of the peek token"""
        precedence: ExpressionPrecedence = PRECEDENCES.get(
            self.peek_token.token_type, ExpressionPrecedence.LOWEST
        )
        return precedence

    def _peek_expected(self, token_type: TokenType) -> bool:
        """This helper method is for checking if next token has the expected TokenType"""
        if self._peek_token_is(token_type):
            self._next_token()
            return True
        self._peek_error(token_type)
        return False

    def _register_prefix_fun(self, token_type: TokenType, fun: Callable) -> None:
        """Associate a token type with a function for the prefix statements"""
        self.prefix_parse_funs[token_type] = fun

    def _register_infix_fun(self, token_type: TokenType, fun: Callable) -> None:
        """Associate a token type with a function for the infix statements"""
        self.infix_parse_funs[token_type] = fun
