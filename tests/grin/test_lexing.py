# Unit tests for the provided grin.lexing module.


from grin.lexing import to_tokens, GrinLexError, KEYWORDS
from grin.location import GrinLocation
from grin.token import GrinTokenKind, GrinToken
import unittest



class TestGrinLexing(unittest.TestCase):
    def assertNoTokens(self, line: str) -> None:
        tokens = list(to_tokens(line, 1))
        self.assertEqual(len(tokens), 0)


    def assertOneToken(
            self, line: str, kind: GrinTokenKind, text: str, *,
            value: object = None) -> None:
        tokens = list(to_tokens(line, 1))
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind(), kind)
        self.assertEqual(tokens[0].text(), text)
        self.assertEqual(tokens[0].value(), value)


    def assertTokens(self, line: str, line_number: int, *tokens: GrinToken) -> None:
        expected_tokens = list(tokens)
        actual_tokens = list(to_tokens(line, line_number))

        self.assertEqual(len(actual_tokens), len(expected_tokens))

        for actual, expected in zip(actual_tokens, expected_tokens):
            self.assertEqual(actual, expected)


    def assertLexError(self, line: str, column_number: int) -> None:
        with self.assertRaises(GrinLexError) as context:
            list(to_tokens(line, 1))

        expected_location = GrinLocation(1, column_number)
        self.assertEqual(context.exception.location(), expected_location)


    def test_empty_lines_have_no_tokens(self):
        self.assertNoTokens('')


    def test_lines_with_only_spaces_have_no_tokens(self):
        self.assertNoTokens('      ')


    def test_can_recognize_keywords(self):
        for keyword in KEYWORDS:
            with self.subTest(keyword = keyword):
                tokens = list(to_tokens(keyword, 1))
                self.assertEqual(len(tokens), 1)
                self.assertNotEqual(tokens[0].kind(), GrinTokenKind.IDENTIFIER)
                self.assertEqual(tokens[0].text(), keyword)
                self.assertEqual(tokens[0].value(), keyword)


    def test_can_recognize_identifiers_when_not_keywords(self):
        for identifier in ('BOO', 'U2', 'THIS1ISTHELAST1'):
            with self.subTest(identifier = identifier):
                self.assertOneToken(identifier, GrinTokenKind.IDENTIFIER, identifier, value = identifier)


    def test_can_recognize_string_literals(self):
        for text in ('"Boo"', '"Hello Boo!"'):
            with self.subTest(text = text):
                self.assertOneToken(text, GrinTokenKind.LITERAL_STRING, text, value = text[1:-1])


    def test_unterminated_string_literals_are_disallowed(self):
        unterminated = '"This does not end'
        self.assertLexError(unterminated, len(unterminated) + 1)


    def test_can_recognize_integers(self):
        for line, value in (('11', 11), ('7', 7), ('0', 0), ('-11', -11), ('-7', -7)):
            with self.subTest(line = line, value = value):
                self.assertOneToken(line, GrinTokenKind.LITERAL_INTEGER, line, value = value)


    def test_can_recognize_floats(self):
        for line, value in (
                ('11.25', 11.25), ('7.0', 7), ('0.75', 0.75),
                ('-11.25', -11.25), ('-7.0', -7), ('5.', 5)):
            with self.subTest(line = line, value = value):
                self.assertOneToken(line, GrinTokenKind.LITERAL_FLOAT, line, value = value)


    def test_cannot_recognize_negation_without_digits(self):
        for invalid in ('-', '-abc'):
            with self.subTest(invalid = invalid):
                self.assertLexError(invalid, 2)


    def test_can_recognize_colon(self):
        self.assertOneToken(':', GrinTokenKind.COLON, ':')


    def test_can_recognize_dot(self):
        self.assertOneToken('.', GrinTokenKind.DOT, '.')


    def test_can_recognize_comparison_operators(self):
        self.assertOneToken('=', GrinTokenKind.EQUAL, '=')
        self.assertOneToken('<>', GrinTokenKind.NOT_EQUAL, '<>')
        self.assertOneToken('<', GrinTokenKind.LESS_THAN, '<')
        self.assertOneToken('<=', GrinTokenKind.LESS_THAN_OR_EQUAL, '<=')
        self.assertOneToken('>', GrinTokenKind.GREATER_THAN, '>')
        self.assertOneToken('>=', GrinTokenKind.GREATER_THAN_OR_EQUAL, '>=')


    def test_invalid_characters_are_disallowed(self):
        for invalid in ('!', '%', '$', '~'):
            with self.subTest(invalid = invalid):
                self.assertLexError(invalid, 1)


    def test_can_recognize_sequences_of_tokens(self):
        line = 'START:   LET NAME "Boo"'

        self.assertTokens(
            line, 1,
            GrinToken(
                kind = GrinTokenKind.IDENTIFIER, text = 'START', value = 'START',
                location = GrinLocation(1, 1)),
            GrinToken(
                kind = GrinTokenKind.COLON, text = ':',
                location = GrinLocation(1, 6)),
            GrinToken(
                kind = GrinTokenKind.LET, text = 'LET', value = 'LET',
                location = GrinLocation(1, 10)),
            GrinToken(
                kind = GrinTokenKind.IDENTIFIER, text = 'NAME', value = 'NAME',
                location = GrinLocation(1, 14)),
            GrinToken(
                kind = GrinTokenKind.LITERAL_STRING, text = '"Boo"', value = 'Boo',
                location = GrinLocation(1, 19)))



if __name__ == '__main__':
    unittest.main()
