from lalalang.lexer.token import TokenType, Token
from lalalang.parser.ast import Program, LetStatement, ReturnStatement, Identifier


CONSTRUCTED_PROGRAM = Program.with_statements(
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

LET_STATEMENTS = [
    {
        "input": "let xyz = 412;",
        "expected": ["xyz", "412"],
    },
    {
        "input": "let variable = value;",
        "expected": ["variable", "value"],
    },
    {
        "input": "let i = 0;",
        "expected": ["i", "0"],
    },
]

RETURN_STATEMENTS = [
    {
        "input": "return 5;",
        "expected": "5",
    },
    {
        "input": "return 1000;",
        "expected": "1000",
    },
    {
        "input": "return hello;",
        "expected": "hello",
    },
]

IDENT_EXPRESSION = [
    {
        "input": "another;",
        "expected": "another",
    },
    {
        "input": "day;",
        "expected": "day",
    },
    {
        "input": "of;",
        "expected": "of",
    },
    {
        "input": "sun;",
        "expected": "sun",
    },
]

INT_LITERALS = [
    {
        "input": "5;",
        "expected": 5,
    },
    {
        "input": "314;",
        "expected": 314,
    },
    {
        "input": "278;",
        "expected": 278,
    },
]

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
]

GROUPED_EXPRESSIONS = [
    {
        "input": "1 + (2 + 3) + 4",
        "expected": "((1 + (2 + 3)) + 4)",
    },
    {
        "input": "(5 + 5) * 2",
        "expected": "((5 + 5) * 2)",
    },
    {
        "input": "2 / (5 + 5)",
        "expected": "(2 / (5 + 5))",
    },
    {
        "input": "-(5 + 5)",
        "expected": "(- (5 + 5))",
    },
    {
        "input": "!(true == true)",
        "expected": "(! (true == true))",
    },
]

IF_EXPRESSIONS = [
    {
        "input": "if (x < y) { x }",
        "expected": ["(x < y)", "x", "None"],
    },
    {
        "input": "if (x > y) { x } else { y }",
        "expected": ["(x > y)", "x", "y"],
    },
]

FUNCTION_LITERALS = [
    {
        "input": "fun(x, y) { x + y; }",
        "expected": ["fun(x,y) (x + y)", "(x + y)"],
    },
    {
        "input": "fun(x) { x - x; }",
        "expected": ["fun(x) (x - x)", "(x - x)"],
    },
]

CALL_EXPRESSIONS = [
    {
        "input": "start(fire);",
        "expected": ["start", "start(fire)"],
    },
    {
        "input": "city(of,2,stars);",
        "expected": ["city", "city(of, 2, stars)"],
    },
    {
        "input": "planet(1,2);",
        "expected": ["planet", "planet(1, 2)"],
    },
]
