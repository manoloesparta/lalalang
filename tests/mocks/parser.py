from lalalang.lexer import TokenType, Token
from lalalang.parser import Program, LetStatement, ReturnStatement, Identifier


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

PREFIX_EXPRESSIONS = [
    {
        "input": "!5;",
        "output": ["!", 5],
    },
    {
        "input": "-10;",
        "output": ["-", 10],
    },
]

INFIX_EXPRESSIONS = [
    {
        "input": "5 + 5;",
        "output": [5, "+", 5],
    },
    {
        "input": "5 - 5;",
        "output": [5, "-", 5],
    },
    {
        "input": "5 * 5;",
        "output": [5, "*", 5],
    },
    {
        "input": "5 / 5;",
        "output": [5, "/", 5],
    },
    {
        "input": "5 > 5;",
        "output": [5, ">", 5],
    },
    {
        "input": "5 < 5;",
        "output": [5, "<", 5],
    },
    {
        "input": "5 == 5;",
        "output": [5, "==", 5],
    },
    {
        "input": "5 != 5;",
        "output": [5, "!=", 5],
    },
]

PRECEDENCE_EXPRESSIONS = [
    {
        "input": "-a * b",
        "output": "((- a) * b)",
    },
    {
        "input": "!-a",
        "output": "(! (- a))",
    },
    {
        "input": "a + b + c",
        "output": "((a + b) + c)",
    },
    {
        "input": "a * b * c",
        "output": "((a * b) * c)",
    },
    {
        "input": "a * b / c",
        "output": "((a * b) / c)",
    },
    {
        "input": "a + b / c",
        "output": "(a + (b / c))",
    },
    {
        "input": "a + b * c + d / e - f",
        "output": "(((a + (b * c)) + (d / e)) - f)",
    },
    {
        "input": "3 + 4; -5 * 5",
        "output": "(3 + 4)((- 5) * 5)",
    },
    {
        "input": "5 > 4 == 3 < 4",
        "output": "((5 > 4) == (3 < 4))",
    },
    {
        "input": "5 < 4 != 3 > 4",
        "output": "((5 < 4) != (3 > 4))",
    },
]
