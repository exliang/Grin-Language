# Unit tests for the provided grin.parsing module.


from grin.lexing import to_tokens
from grin.location import GrinLocation
from grin.parsing import parse, GrinParseError
import unittest



class TestGrinParsing(unittest.TestCase):
    def assertCanParseLine(self, line: str) -> None:
        tokens = list(to_tokens(line, 1))
        parsed = list(parse([line]))
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0], tokens)


    def assertParseError(self, line: str, column_number: int) -> None:
        with self.assertRaises(GrinParseError) as context:
            list(parse([line]))

        self.assertEqual(context.exception.location(), GrinLocation(1, column_number))


    def test_cannot_parse_empty_statements(self):
        empties = ['', '    ']

        for empty in empties:
            with self.subTest(empty = empty):
                self.assertParseError(empty, len(empty) + 1)


    def test_cannot_parse_statements_not_beginning_with_keyword(self):
        for invalid in ('4 < 5', '"Boo"'):
            with self.subTest(invalid = invalid):
                self.assertParseError(invalid, 1)


    def test_can_parse_valid_variable_update(self):
        keywords = ['LET', 'ADD', 'SUB', 'MULT', 'DIV']

        operand_sequences = [
            'AGE 13',
            'NAME "Boo"',
            'PERCENTAGE 999.75',
            'NAME OTHERNAME'
        ]

        for keyword in keywords:
            for operand_sequence in operand_sequences:
                with self.subTest(keyword = keyword, operand_sequence = operand_sequence):
                    self.assertCanParseLine(f'{keyword} {operand_sequence}')


    def test_cannot_parse_variable_update_with_extra_tokens(self):
        self.assertParseError('LET X 3 "Boo"', 9)


    def test_cannot_parse_variable_update_with_missing_tokens(self):
        errors = ['ADD X', 'ADD']

        for error in errors:
            with self.subTest(error = error):
                self.assertParseError(error, len(error) + 1)


    def test_cannot_parse_variable_update_with_invalid_target(self):
        self.assertParseError('LET 3 4', 5)


    def test_cannot_parse_variable_update_with_invalid_source(self):
        self.assertParseError('LET X =', 7)


    def test_can_parse_print_statement(self):
        lines = [
            'PRINT NAME',
            'PRINT 13',
            'PRINT 999.75',
            'PRINT "Boo"'
        ]

        for line in lines:
            with self.subTest(line = line):
                self.assertCanParseLine(line)


    def test_cannot_parse_print_statement_with_extra_tokens(self):
        self.assertParseError('PRINT NAME "Boo"', 12)


    def test_cannot_parse_print_statement_with_missing_tokens(self):
        self.assertParseError('PRINT', 6)


    def test_cannot_parse_print_statement_with_invalid_source(self):
        self.assertParseError('PRINT END', 7)


    def test_can_parse_input_statements(self):
        lines = [
            'INNUM X',
            'INNUM BOO',
            'INSTR X',
            'INSTR BOO'
        ]

        for line in lines:
            with self.subTest(line = line):
                self.assertCanParseLine(line)


    def test_cannot_parse_input_statement_with_extra_tokens(self):
        lines = [
            'INNUM VALUE 13',
            'INSTR VALUE "Boo"'
        ]

        for line in lines:
            with self.subTest(line = line):
                self.assertParseError(line, 13)


    def test_cannot_parse_input_statement_with_missing_tokens(self):
        for line in ['INNUM', 'INSTR']:
            with self.subTest(line = line):
                self.assertParseError(line, 6)


    def test_cannot_parse_input_statement_with_invalid_target(self):
        for line in ['INNUM 3', 'INSTR 3']:
            with self.subTest(line = line):
                self.assertParseError(line, 7)


    def test_can_parse_jump_statements_without_condition(self):
        keywords = ['GOTO', 'GOSUB']
        targets = ['13', '"Boo"', 'XYZ']

        for keyword in keywords:
            for target in targets:
                with self.subTest(keyword = keyword, target = targets):
                    self.assertCanParseLine(f'{keyword} {target}')


    def test_can_parse_jump_statements_with_condition(self):
        keywords = ['GOTO', 'GOSUB']
        values = ['13', '999.75', '"Boo"', 'XYZ']
        operators = ['=', '<>', '<', '<=', '>', '>=']

        for keyword in keywords:
            for value1 in values:
                for operator in operators:
                    for value2 in values:
                        with self.subTest(
                                keyword = keyword, value1 = value1,
                                operator = operator, value2 = value2):
                            self.assertCanParseLine(f'{keyword} 3 IF {value1} {operator} {value2}')


    def test_cannot_parse_jump_statements_with_extra_tokens(self):
        self.assertParseError('GOTO 3 IF 4 < 5 "Boo"', 17)


    def test_cannot_parse_jump_statements_with_missing_tokens(self):
        errors = [
            'GOTO',
            'GOSUB 3 IF',
            'GOTO 3 IF X',
            'GOTO 3 IF X <'
        ]

        for error in errors:
            with self.subTest(error = error):
                self.assertParseError(error, len(error) + 1)


    def test_cannot_parse_jump_statements_with_invalid_target(self):
        self.assertParseError('GOTO 35.5', 6)


    def test_cannot_parse_jump_statements_with_invalid_left_source(self):
        self.assertParseError('GOTO 3 IF DIV < 5', 11)


    def test_cannot_parse_jump_statements_with_invalid_comparison_operator(self):
        self.assertParseError('GOTO 3 IF X Y Z', 13)


    def test_cannot_parse_jump_statements_with_invalid_right_source(self):
        self.assertParseError('GOTO 3 IF 5 < DIV', 15)


    def test_can_parse_no_operand_statements(self):
        keywords = ['RETURN', 'END']

        for keyword in keywords:
            with self.subTest(keyword = keyword):
                self.assertCanParseLine(keyword)


    def test_parsing_stops_when_dot_encountered(self):
        lines = list(parse(['RETURN', '.', 'RETURN']))
        self.assertEqual(len(lines), 1)
        self.assertEqual(len(lines[0]), 1)


    def test_can_parse_valid_statement_with_label(self):
        statements = [
            'LET AGE 13',
            'RETURN',
            'PRINT "Boo"'
        ]

        for statement in statements:
            with self.subTest(statement = statement):
                self.assertCanParseLine(f'START: {statement}')


    def test_cannot_parse_label_without_statement(self):
        invalid = 'LABEL:'
        self.assertParseError(invalid, len(invalid) + 1)



if __name__ == '__main__':
    unittest.main()
