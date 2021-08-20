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
