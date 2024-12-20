
"""Test module for unittests for project3.py"""

import unittest
from project3 import *
from variables import *
from grin import *
from print_statement import *
from state import *
from input_keywords import *
import contextlib, io
from unittest.mock import patch

class Testing(unittest.TestCase):

    @patch('builtins.input')
    def test_while_loop(self, mock_input):
        mock_input.side_effect = ['2', 'test']  # so input doesnt' stop it from running
        statements_lst = ['Z: LET A 2', 'PRINT A', 'GOTO 2', 'GOTO 2 IF A > 0',
                          'GOSUB 3', 'ADD A 3', 'END', 'SUB A 1', 'MULT A 2', 'DIV A 4', 'RETURN', '.']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {}
        labels_dict = {}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        gosub_line_nums = []
        line_number = 1
        end_line_number = len(parsed_statements_lst)  # statements_lst
        labels_dict = create_labels_dict(parsed_statements_lst, labels_dict)
        try:
            main_loop(line_number, end_line_number, parsed_statements_lst, keywords_lst, variable_dict, labels_dict, gosub_line_nums)
        except SystemExit:  # END
            pass
        try:
            main()
        except SystemExit:
            pass

    @patch('builtins.input')
    def test_Input_class(self, mock_input):
        mock_input.side_effect = ['2', 'test']  # so input doesnt' stop it from running
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO", "GOSUB", "RETURN", "END"]

        # no label
        tokens_lst = list(parse(['INNUM A', '.']))[0]
        var_dict = {}
        inputt = Input(tokens_lst, var_dict, keywords_lst)

        # with label
        tokens_lst = list(parse(['Z: INSTR A', '.']))[0]
        var_dict = {}
        inputt = Input(tokens_lst, var_dict, keywords_lst)

    @patch('builtins.input')
    def test_Innum_class_int(self, mock_input):
        mock_input.side_effect = ['2', 'test']  # so input doesnt' stop it from running
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # no label
        tokens_lst = list(parse(['INNUM A', '.']))[0]
        var_dict = {}
        innum = Innum(tokens_lst, var_dict, keywords_lst)
        innum.add_num_to_var_dict()

    @patch('builtins.input')
    def test_Innum_class_float(self, mock_input):
        mock_input.side_effect = ['2.0', 'test']  # so input doesnt' stop it from running
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        # with label
        tokens_lst = list(parse(['Z: INNUM A', '.']))[0]
        var_dict = {}
        innum = Innum(tokens_lst, var_dict, keywords_lst)
        innum.add_num_to_var_dict()

    @patch('builtins.input')
    def test_Instr_class(self, mock_input):
        mock_input.side_effect = ['2', 'test']  # so input doesnt' stop it from running
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # no label
        tokens_lst = list(parse(['INSTR A', '.']))[0]
        var_dict = {}
        instr = Instr(tokens_lst, var_dict, keywords_lst)
        instr.add_str_to_var_dict()

        # with label
        tokens_lst = list(parse(['Z: INSTR A', '.']))[0]
        var_dict = {}
        instr = Instr(tokens_lst, var_dict, keywords_lst)

    def test_parse_statements_func(self):
        statements_lst = ['LET A "hi"', '.']
        self.assertEqual(len(parse_statements(statements_lst)), 1)
        self.assertEqual(len(parse_statements(statements_lst)[0]), 3)

    def test_create_labels_dict_func(self):
        statements_lst = ['Z: LET A "hi"', '.']
        tokens_lst = list(parse(statements_lst))
        labels_dict = create_labels_dict(tokens_lst, {})
        self.assertEqual(labels_dict, {1: 'Z'})

    def test_LET(self):
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO", "GOSUB", "RETURN", "END"]

        # value = str
        tokens_lst = list(parse(['LET A "hi"', '.']))[0]
        var_dict = {}
        Let(tokens_lst, var_dict, keywords_lst, {}).add_var_to_dict()
        assert 'A' in var_dict.keys() and "hi" in var_dict.values()

        # value = int
        tokens_lst = list(parse(['LET A 5', '.']))[0]
        var_dict = {}
        Let(tokens_lst, var_dict, keywords_lst, {}).add_var_to_dict()
        assert 'A' in var_dict.keys() and 5 in var_dict.values()

        # value (int) = var
        tokens_lst = list(parse(['LET A B', '.']))[0]
        var_dict = {'B': 4}
        Let(tokens_lst, var_dict, keywords_lst, {}).add_var_to_dict()
        assert 'A' in var_dict.keys() and 4 in var_dict.values()

        # value (str) = var
        tokens_lst = list(parse(['LET A B', '.']))[0]
        var_dict = {'B': "hi"}
        Let(tokens_lst, var_dict, keywords_lst, {}).add_var_to_dict()
        assert 'A' in var_dict.keys() and "hi" in var_dict.values()

        # starts w label
        tokens_lst = list(parse(['CZ: LET A B', '.']))[0]
        var_dict = {'B': "hi"}
        labels_dict = {1: 'CZ'}
        Let(tokens_lst, var_dict, keywords_lst, labels_dict).add_var_to_dict()
        assert 'A' in var_dict.keys() and "hi" in var_dict.values()

    def test_PRINT(self):
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # value is a var that's been pre-asssigned
        tokens_lst = list(parse(['PRINT A', '.']))[0]
        var_dict = {'A': 1}
        with contextlib.redirect_stdout(io.StringIO()) as output:
            print_keyword(tokens_lst, var_dict, keywords_lst)
        self.assertEqual(output.getvalue(), "1\n")

        # value is a var that's not been pre-asssigned
        tokens_lst = list(parse(['PRINT A', '.']))[0]
        var_dict = {}
        with contextlib.redirect_stdout(io.StringIO()) as output:
            print_keyword(tokens_lst, var_dict, keywords_lst)
        self.assertEqual(output.getvalue(), "0\n")

        # value is a str
        tokens_lst = list(parse(['PRINT "hi"', '.']))[0]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            print_keyword(tokens_lst, {}, keywords_lst)
        self.assertEqual(output.getvalue(), "hi\n")

        # value is an int
        tokens_lst = list(parse(['PRINT 3', '.']))[0]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            print_keyword(tokens_lst, {}, keywords_lst)
        self.assertEqual(output.getvalue(), "3\n")

        # starts w label
        tokens_lst = list(parse(['Z: PRINT 3', '.']))[0]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            print_keyword(tokens_lst, {}, keywords_lst)
        self.assertEqual(output.getvalue(), "3\n")

    def test_ADD(self):
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # var unassigned before adding
        tokens_lst = list(parse(['ADD A 5', '.']))[0]
        var_dict = {}
        add = Add(tokens_lst, var_dict, keywords_lst, {})
        add.add()
        assert 5 in var_dict.values() and 'A' in var_dict.keys()

        # var assigned before adding (int + int)
        tokens_lst = list(parse(['ADD A 5', '.']))[0]
        var_dict = {'A': 2}
        add = Add(tokens_lst, var_dict, keywords_lst, {})
        add.add()
        assert 7 in var_dict.values() and 'A' in var_dict.keys()

        # float + float
        tokens_lst = list(parse(['ADD A 5.0', '.']))[0]
        var_dict = {'A': 2.0}
        add = Add(tokens_lst, var_dict, keywords_lst, {})
        add.add()
        assert 7.0 in var_dict.values() and 'A' in var_dict.keys()

        # value is name of another var
        tokens_lst = list(parse(['ADD A B', '.']))[0]
        var_dict = {'A': 2.0, 'B': 1}
        add = Add(tokens_lst, var_dict, keywords_lst, {})
        add.add()
        assert 3.0 in var_dict.values() and 'A' in var_dict.keys()

        # value is a string
        tokens_lst = list(parse(['ADD A "llo"', '.']))[0]
        var_dict = {'A': "he"}
        add = Add(tokens_lst, var_dict, keywords_lst, {})
        add.add()
        assert "hello" in var_dict.values() and 'A' in var_dict.keys()

        # starts w label
        tokens_lst = list(parse(['Z: ADD A "llo"', '.']))[0]
        var_dict = {'A': "he"}
        labels_dict = {1: "Z"}
        add = Add(tokens_lst, var_dict, keywords_lst, labels_dict)
        add.add()
        assert "hello" in var_dict.values() and 'A' in var_dict.keys()

    def test_SUB(self):
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # starts a w label
        tokens_lst = list(parse(['Z: SUB A 5', '.']))[0]
        var_dict = {'A': 9}
        labels_dict = {1: "Z"}
        sub = Sub(tokens_lst, var_dict, keywords_lst, labels_dict)
        sub.subtract()
        assert 4 in var_dict.values() and 'A' in var_dict.keys()

        # float + int
        tokens_lst = list(parse(['Z: SUB A 5', '.']))[0]
        var_dict = {'A': 9.0}
        labels_dict = {1: "Z"}
        sub = Sub(tokens_lst, var_dict, keywords_lst, labels_dict)
        sub.subtract()
        assert 4.0 in var_dict.values() and 'A' in var_dict.keys()

        # int + float
        tokens_lst = list(parse(['Z: SUB A 5.0', '.']))[0]
        var_dict = {'A': 9}
        labels_dict = {1: "Z"}
        sub = Sub(tokens_lst, var_dict, keywords_lst, labels_dict)
        sub.subtract()
        assert 4.0 in var_dict.values() and 'A' in var_dict.keys()

        # var is unassigned before
        tokens_lst = list(parse(['SUB A 5', '.']))[0]
        var_dict = {}
        sub = Sub(tokens_lst, var_dict, keywords_lst, {})
        sub.subtract()
        assert -5 in var_dict.values() and 'A' in var_dict.keys()

        # value is another variable
        tokens_lst = list(parse(['SUB A B', '.']))[0]
        var_dict = {'A': 2.0, 'B': 1}
        sub = Sub(tokens_lst, var_dict, keywords_lst, {})
        sub.subtract()
        assert 1.0 in var_dict.values() and 'A' in var_dict.keys()

    def test_MULT(self):
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # starts w a label
        tokens_lst = list(parse(['Z: MULT A B', '.']))[0]
        var_dict = {'A': 2.0, 'B': 2}
        labels_dict = {1: "Z"}
        mult = Mult(tokens_lst, var_dict, keywords_lst, labels_dict)
        mult.multiply()
        assert 4.0 in var_dict.values() and 'A' in var_dict.keys()

        # int x int
        tokens_lst = list(parse(['MULT A 3', '.']))[0]
        var_dict = {'A': 2}
        mult = Mult(tokens_lst, var_dict, keywords_lst, {})
        mult.multiply()
        assert 6 in var_dict.values() and 'A' in var_dict.keys()

        # float x float
        tokens_lst = list(parse(['MULT A 3.0', '.']))[0]
        var_dict = {'A': 2.0}
        mult = Mult(tokens_lst, var_dict, keywords_lst, {})
        mult.multiply()
        assert 6.0 in var_dict.values() and 'A' in var_dict.keys()

        # int x str
        tokens_lst = list(parse(['MULT A 3', '.']))[0]
        var_dict = {'A': "hi"}
        mult = Mult(tokens_lst, var_dict, keywords_lst, {})
        mult.multiply()
        assert "hihihi" in var_dict.values() and 'A' in var_dict.keys()

        # str x int
        tokens_lst = list(parse(['MULT A "hi"', '.']))[0]
        var_dict = {'A': 3}
        mult = Mult(tokens_lst, var_dict, keywords_lst, {})
        mult.multiply()
        assert "hihihi" in var_dict.values() and 'A' in var_dict.keys()

        # var being used before assignment
        tokens_lst = list(parse(['MULT A 3.0', '.']))[0]
        var_dict = {}
        mult = Mult(tokens_lst, var_dict, keywords_lst, {})
        mult.multiply()
        assert 0 in var_dict.values() and 'A' in var_dict.keys()

        # negative multiplication
        try:
            tokens_lst = list(parse(['MULT A -3', '.']))[0]
            var_dict = {'A': "hi"}
            mult = Mult(tokens_lst, var_dict, keywords_lst, {})
            mult.multiply()
        except SystemExit:
            pass

        try:
            tokens_lst = list(parse(['MULT A "hi"', '.']))[0]
            var_dict = {'A': -3}
            mult = Mult(tokens_lst, var_dict, keywords_lst, {})
            mult.multiply()
        except SystemExit:
            pass

    def test_DIV(self):
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]

        # starts w a label
        tokens_lst = list(parse(['Z: DIV A 3.0', '.']))[0]
        var_dict = {'A': 6.0}
        labels_dict = {1: 'Z'}
        div = Div(tokens_lst, var_dict, keywords_lst, labels_dict)
        div.divide()
        assert 2.0 in var_dict.values() and 'A' in var_dict.keys()

        # float & int
        tokens_lst = list(parse(['DIV A 3', '.']))[0]
        var_dict = {'A': 6.0}
        div = Div(tokens_lst, var_dict, keywords_lst, {})
        div.divide()
        assert 2.0 in var_dict.values() and 'A' in var_dict.keys()

        # int & int
        tokens_lst = list(parse(['DIV A 3', '.']))[0]
        var_dict = {'A': 6}
        div = Div(tokens_lst, var_dict, keywords_lst, {})
        div.divide()
        assert 2 in var_dict.values() and 'A' in var_dict.keys()

        # var is used before assignment
        tokens_lst = list(parse(['DIV A 3', '.']))[0]
        var_dict = {}
        div = Div(tokens_lst, var_dict, keywords_lst, {})
        div.divide()
        assert 0 in var_dict.values() and 'A' in var_dict.keys()

        # value is another var
        tokens_lst = list(parse(['DIV A B', '.']))[0]
        var_dict = {'A': 6, 'B': 4.0}
        div = Div(tokens_lst, var_dict, keywords_lst, {})
        div.divide()
        assert 1.5 in var_dict.values() and 'A' in var_dict.keys()

        # testing system exit
        try:
            tokens_lst = list(parse(['DIV A 0', '.']))[0]
            var_dict = {'A': 6}
            div = Div(tokens_lst, var_dict, keywords_lst, {})
            div.divide()
        except SystemExit:
            pass

        try:
            tokens_lst = list(parse(['DIV A B', '.']))[0]
            var_dict = {'A': 6}
            div = Div(tokens_lst, var_dict, keywords_lst, {})
            div.divide()
        except SystemExit:
            pass

    def test_return_func(self):
        try:
            gosub_line_numbers = []
            return_keyword(gosub_line_numbers)
        except SystemExit:
            pass

    def test_get_operator_func(self):
        self.assertEqual(get_operator("="), "equal")
        self.assertEqual(get_operator("<>"), "not equal")
        self.assertEqual(get_operator("<"), "less than")
        self.assertEqual(get_operator("<="), "less than or equal")
        self.assertEqual(get_operator(">"), "greater than")
        self.assertEqual(get_operator(">="), "greater than or equal")
        self.assertEqual(get_operator("=="), "invalid operator")

    def test_determine_type_of_value1_and_value2(self):
        var_dict = {}

        # int, int
        value1, value2 = determine_type_of_value1_and_value2('5', '2', var_dict)
        self.assertEqual((value1, value2), (5,2))

        # float, float
        value1, value2 = determine_type_of_value1_and_value2('5.0', '2.0', var_dict)
        self.assertEqual((value1, value2), (5.0, 2.0))

        # str, str
        value1, value2 = determine_type_of_value1_and_value2('hi', 'bye', var_dict)
        self.assertEqual((value1, value2), ("hi", 'bye'))

        # var, var
        var_dict = {'A': 2, 'B': 3}
        value1, value2 = determine_type_of_value1_and_value2('A', 'B', var_dict)
        self.assertEqual((value1, value2), (2, 3))

class TestGoTo(unittest.TestCase):
    @patch('builtins.input')
    def test_goto_number(self, mock_input):
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        statements_lst = ['LET A 2', 'GOTO 2', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': 2}
        labels_dict = {}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst

        tokens_lst = parsed_statements_lst[line_number-1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number, keywords_lst)
        new_line_num = goto.goto_target()
        self.assertEqual(new_line_num, 4)

    @patch('builtins.input')
    def test_goto_label(self, mock_input):  #FIX THIS
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        statements_lst = ['LET A 2', 'GOTO "Z"', 'PRINT A', 'Z: LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': 2}
        labels_dict = {4: 'Z'}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst

        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target()
        self.assertEqual(new_line_num, 4)

    @patch('builtins.input')
    def test_goto_starts_with_label(self, mock_input):
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        statements_lst = ['LET A 2', 'Z: GOTO 2', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': 2}
        labels_dict = {2: 'Z'}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst

        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target()
        self.assertEqual(new_line_num, 4)

    @patch('builtins.input')
    def test_goto_var_num(self, mock_input):
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        statements_lst = ['LET A 2', 'GOTO A', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': 2}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst
        labels_dict = {1: "Z"}  # setting a random label so error doesn't occur when running

        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target()
        self.assertEqual(new_line_num, 4)

    @patch('builtins.input')
    def test_goto_var_str(self, mock_input):
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        statements_lst = ['LET A 2', 'GOTO A', 'PRINT A', 'Z: LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': "Z"}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst
        labels_dict = {4: "Z"}  # setting a random label so error doesn't occur when running

        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target()
        self.assertEqual(new_line_num, 4)

    @patch('builtins.input')
    def test_goto_invalid_target(self, mock_input):
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        statements_lst = ['LET A 2', 'GOTO A', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': (1,2,3)}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst
        labels_dict = {4: "Z"}  # setting a random label so error doesn't occur when running

        tokens_lst = parsed_statements_lst[line_number - 1]
        try:
            goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                        keywords_lst)
            new_line_num = goto.goto_target()
        except SystemExit:
            pass

    @patch('builtins.input')
    def test_goto_target_expression(self, mock_input):
        mock_input.side_effect = ['1', 'goto']  # so input doesnt' stop it from running

        # > (line num changes)
        statements_lst = ['LET A 2', 'GOTO 2 IF A > 0', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        variable_dict = {'A': 2}
        labels_dict = {}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        line_number = 2
        end_line_number = len(parsed_statements_lst)  # statements_lst

        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # > (line num doesn't change
        statements_lst = ['LET A 2', 'GOTO 2 IF A > 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 2)

        # < (line num doesn't change)
        statements_lst = ['LET A 2', 'GOTO 2 IF A < 0', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 2)

        # < (line num changes)
        statements_lst = ['LET A 2', 'GOTO 2 IF A < 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # = (line num changes)
        statements_lst = ['LET A 2', 'GOTO 2 IF A = 2', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # = (line num same)
        statements_lst = ['LET A 2', 'GOTO 2 IF A = 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 2)

        # <> (line num same)
        statements_lst = ['LET A 2', 'GOTO 2 IF A <> 2', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 2)

        # <> (line num changes)
        statements_lst = ['LET A 2', 'GOTO 2 IF A <> 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # <= (line num changes)
        statements_lst = ['LET A 2', 'GOTO 2 IF A <= 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # <= (line num same)
        statements_lst = ['LET A 2', 'GOTO 2 IF A <= 1', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 2)

        # >= (line num changes)
        statements_lst = ['LET A 2', 'GOTO 2 IF A >= 1', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # >= (line num same)
        statements_lst = ['LET A 2', 'GOTO 2 IF A >= 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 2)

        # starts w label
        statements_lst = ['LET A 2', 'Z: GOTO 2 IF A < 3', 'PRINT A', 'LET A 3']
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        labels_dict = {2: "Z"}
        goto = GoTo(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = goto.goto_target_expression()
        self.assertEqual(new_line_num, 4)

        # GOTO 0
        try:
            target_is_int('0', line_number, end_line_number)
        except SystemExit:
            pass

        # GOTO -#
        try:
            target_is_int('-3', line_number, end_line_number)
        except SystemExit:
            pass

        # GOTO 5 (not in program)
        try:
            target_is_int('5', line_number, end_line_number)
        except SystemExit:
            pass

        # GOTO label
        try:
            target_is_label('Z', {0:"Z"})
        except SystemExit:
            pass

        # GOTO label (label doesn't exist)
        try:
            target_is_label('Z', {})
        except SystemExit:
            pass

class TestGoSub(unittest.TestCase):
    def test_gosub_target_expression(self):
        gosub_line_nums = []
        variable_dict = {'A': 2}
        statements_lst = ['LET A 2', 'GOSUB 2 IF A < 3', 'PRINT A', 'LET A 3']
        line_number = 2
        parsed_statements_lst = parse_statements(statements_lst)
        tokens_lst = parsed_statements_lst[line_number - 1]
        labels_dict = {2: "Z"}
        keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO",
                        "GOSUB", "RETURN", "END"]
        end_line_number = len(parsed_statements_lst)
        gosub = GoSub(tokens_lst, variable_dict, labels_dict, line_number, end_line_number,
                    keywords_lst)
        new_line_num = gosub.gosub_target_expression(gosub_line_nums)
        self.assertEqual(new_line_num, 4)
