from lalalang.lexer import TokenType, Token
from lalalang.parser import (
    Program, 
    LetStatement, 
    ReturnStatement, 
    Identifier
)


LET_STATEMENTS = """
    let x = 5;
    let y = 10;
    let foobar = 838383;
    let mia = 42;
"""

RETURN_STATEMENTS = """
    return 10;
    return 4 + 3;
    return add(5,6);
"""

LET_PROGRAM = Program.with_statements(
    [
        LetStatement(
            token=Token(TokenType.LET, "let"),
            name=Identifier(token=Token(TokenType.IDENT, "myVar"), value="myVar"),
            value=Identifier(
                token=Token(TokenType.IDENT, "anotherVar"), value="anotherVar"
            ),
        )
    ]
)

IDENT_EXPRESSION = "foobar;"

INT_LITERAL = "5;"