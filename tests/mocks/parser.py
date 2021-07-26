from lalalang.lexer import TokenType, Token
from lalalang.parser import Program, LetStatement, ReturnStatement, Identifier


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

IDENT_EXPRESSION = "foobar;"

INT_LITERAL = "5;"

PREFIX_EXPRESSIONS = [
    {
        "input": "!5;",
        "expected": ["!", 5],
    },
    {
        "input": "-10;",
        "expected": ["-", 10],
    },
]

INFIX_EXPRESSIONS = [
    {
        "input": "5 + 5;",
        "expected": [5, "+", 5],
    },
    {
        "input": "5 - 5;",
        "expected": [5, "-", 5],
    },
    {
        "input": "5 * 5;",
        "expected": [5, "*", 5],
    },
    {
        "input": "5 / 5;",
        "expected": [5, "/", 5],
    },
    {
        "input": "5 > 5;",
        "expected": [5, ">", 5],
    },
    {
        "input": "5 < 5;",
        "expected": [5, "<", 5],
    },
    {
        "input": "5 == 5;",
        "expected": [5, "==", 5],
    },
    {
        "input": "5 != 5;",
        "expected": [5, "!=", 5],
    },
]

PRECEDENCE_EXPRESSIONS = [
    {
        "input": "-a * b",
        "expected": "((- a) * b)",
    },
    {
        "input": "!-a",
        "expected": "(! (- a))",
    },
    {
        "input": "a + b + c",
        "expected": "((a + b) + c)",
    },
    {
        "input": "a * b * c",
        "expected": "((a * b) * c)",
    },
    {
        "input": "a * b / c",
        "expected": "((a * b) / c)",
    },
    {
        "input": "a + b / c",
        "expected": "(a + (b / c))",
    },
    {
        "input": "a + b * c + d / e - f",
        "expected": "(((a + (b * c)) + (d / e)) - f)",
    },
    {
        "input": "3 + 4; -5 * 5",
        "expected": "(3 + 4)((- 5) * 5)",
    },
    {
        "input": "5 > 4 == 3 < 4",
        "expected": "((5 > 4) == (3 < 4))",
    },
    {
        "input": "5 < 4 != 3 > 4",
        "expected": "((5 < 4) != (3 > 4))",
    },
]

BOOLEAN_EXPRESSION = [
    {
        "input": "true",
        "expected": "true",
    },
    {
        "input": "false",
        "expected": "false",
    },
    {
        "input": "3 > 5 == false",
        "expected": "((3 > 5) == false)",
    },
    {
        "input": "3 < 5 == true",
        "expected": "((3 < 5) == true)",
    },
]
