from unittest.mock import patch
from unittest import TestCase
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import TokenType, Token


class TestLexer(TestCase):
    def test_lexer_with_source_code(self):
        source_code = """
            let pi = 314;
            fun area(ratio) {
                pi + ratio + ratio;
            }
        """
        expected_tokens = [
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "pi"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "314"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.FUNCTION, "fun"),
            Token(TokenType.IDENT, "area"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "ratio"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENT, "pi"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "ratio"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.IDENT, "ratio"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_delimeters(self):
        source_code = "(){},;"
        expected_tokens = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_control(self):
        source_code = "~`^"
        expected_tokens = [
            Token(TokenType.ILLEGAL, "~"),
            Token(TokenType.ILLEGAL, "`"),
            Token(TokenType.ILLEGAL, "^"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_operators(self):
        source_code = "+="
        expected_tokens = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.ASSIGN, "="),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_identifiers(self):
        source_code = "someone in the crowd"
        expected_tokens = [
            Token(TokenType.IDENT, "someone"),
            Token(TokenType.IDENT, "in"),
            Token(TokenType.IDENT, "the"),
            Token(TokenType.IDENT, "crowd"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_numbers(self):
        source_code = "314 217 161"
        expected_tokens = [
            Token(TokenType.INT, "314"),
            Token(TokenType.INT, "217"),
            Token(TokenType.INT, "161"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_keywords(self):
        source_code = "let fun"
        expected_tokens = [
            Token(TokenType.LET, "let"),
            Token(TokenType.FUNCTION, "fun"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_correct_string_format(self):
        token = Token(TokenType.EOF, "")
        self.assertEqual(str(token), 'Token(TokenType.EOF, "")')

    def compare_results(self, source_code, expected_tokens):
        lex = Lexer(source_code)
        for token in expected_tokens:
            current = lex.next_token()
            self.assertEqual(token.token_type, current.token_type)
            self.assertEqual(token.literal, current.literal)
