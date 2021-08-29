from lalalang.evaluator.evaluator import *
from lalalang.evaluator.object import *


INTEGER = [
    {
        "input": "314",
        "expected": "314",
    },
    {
        "input": "016",
        "expected": "16",
    },
]

BOOLEAN = [
    {
        "input": "true",
        "expected": "true",
    },
    {
        "input": "false",
        "expected": "false",
    },
]

PREFIX = [
    {
        "input": "-5",
        "expected": "-5",
    },
    {
        "input": "--5",
        "expected": "5",
    },
    {
        "input": "!true",
        "expected": "false",
    },
    {
        "input": "!false",
        "expected": "true",
    },
]

INFIX = [
    {
        "input": "5 + 4",
        "expected": "9",
    },
    {
        "input": "13 * 2 + 6",
        "expected": "32",
    },
    {
        "input": "(5 + 2) * 3",
        "expected": "21",
    },
    {
        "input": "(3 / 3) * 3",
        "expected": "3",
    },
    {
        "input": "10 - (4 + 2)",
        "expected": "4",
    },
    {
        "input": "10 - 20",
        "expected": "-10",
    },
    {
        "input": "10 % 2",
        "expected": "0",
    },
]

LOGICAL = [
    {
        "input": "true || false",
        "expected": "true",
    },
    {
        "input": "false || false",
        "expected": "false",
    },
    {
        "input": "false && true",
        "expected": "false",
    },
    {
        "input": "true && true",
        "expected": "true",
    },
]

CONDITIONALS = [
    {
        "input": "if(5 == 5) { 3 }",
        "expected": "3",
    },
    {
        "input": "if(10 < 3) { 4 } else { 5 }",
        "expected": "5",
    },
    {
        "input": "if(5 != 5) { 3 }",
        "expected": "null",
    },
]

RETURN = [
    {
        "input": "let a = 5*8;return 10;",
        "expected": "10",
    },
    {
        "input": "return 2; return 3;",
        "expected": "2",
    },
    {
        "input": "if(1 == 1){ if(1 == 1) { return 1; } return 0; }",
        "expected": "1",
    },
]

ERRORS = [
    {
        "input": "-true",
        "expected": "ERROR: Unknown operator -ObjectType.BOOLEAN",
    },
    {
        "input": "10 + false",
        "expected": "ERROR: Type missmatch ObjectType.INTEGER + ObjectType.BOOLEAN",
    },
    {
        "input": "false + false",
        "expected": "ERROR: Unkown operator ObjectType.BOOLEAN + ObjectType.BOOLEAN",
    },
    {
        "input": "a",
        "expected": "ERROR: Identifier not found: a",
    },
    {
        "input": "return x",
        "expected": "ERROR: Identifier not found: x",
    },
]

FUNCTION_CALLS = [
    {
        "input": "let a = fun(x) { x + 1 }; a(2)",
        "expected": "3",
    },
    {
        "input": "let b = fun() { false }; b()",
        "expected": "false",
    },
    {
        "input": "let c = fun(x) { if(x > 0) { return 1; } return 2; }; c(1)",
        "expected": "1",
    },
]

ENVIRONMENT = [
    {
        "input": "let a = 10; let b = 5; a + b;",
        "expected": "15",
    },
    {
        "input": "let a = 10; let f = fun() { return a; }; f()",
        "expected": "10",
    },
    {
        "input": "let x = 10; let f = fun() { let y = 3; return x + y; }; f()",
        "expected": "13",
    },
]

BUILTINS = [
    {
        "input": "print(10)",
        "expected": "null",
    },
    {
        "input": "println(10)",
        "expected": "null",
    },
    {
        "input": '"Universe: " + toString(10)',
        "expected": "Universe: 10",
    },
]

NULLS = [
    {
        "input": "null",
        "expected": "null",
    },
    {
        "input": "let a = null; a;",
        "expected": "null",
    },
    {
        "input": "let a = if(false) { 1 }; a;",
        "expected": "null",
    },
]

STRINGS = [
    {
        "input": '"Feliz jueves!"',
        "expected": "Feliz jueves!",
    },
    {
        "input": 'let a = "b"; a;',
        "expected": "b",
    },
    {
        "input": 'let b = fun() { return "b"; }; b()',
        "expected": "b",
    },
    {
        "input": '"a" + "b"',
        "expected": "ab",
    },
    {
        "input": '"a" + "b" + "c"',
        "expected": "abc",
    },
    {
        "input": '"feliz" + " " + "jueves"',
        "expected": "feliz jueves",
    },
]
