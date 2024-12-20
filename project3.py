# The main module that executing the Grin interpreter.

import sys
from grin import *
from variables import *
from print_statement import *
from input_keywords import *
from state import *

def main() -> None:
    variable_dict = {}
    labels_dict = {}
    keywords_lst = ["LET", "PRINT", "INNUM", "INSTR", "ADD", "SUB", "MULT", "DIV", "GOTO", "GOSUB", "RETURN", "END", "IF"]
    gosub_line_nums = []

    line_number = 1
    statements_lst = create_statements_list()
    parsed_statements_lst = parse_statements(statements_lst)
    end_line_number = len(parsed_statements_lst)  # statements_lst
    labels_dict = create_labels_dict(parsed_statements_lst, labels_dict)  # statements_lst

    main_loop(line_number, end_line_number, parsed_statements_lst, keywords_lst, variable_dict, labels_dict, gosub_line_nums)

def main_loop(line_number, end_line_number, parsed_statements_lst, keywords_lst, variable_dict, labels_dict, gosub_line_nums):
    while line_number <= end_line_number:
        lst_of_grin_tokens = parsed_statements_lst[line_number - 1]

        if lst_of_grin_tokens[0].text() not in keywords_lst:  # if line starts w a label
            keyword = lst_of_grin_tokens[2].text()
        else:
            keyword = lst_of_grin_tokens[0].text()  # type of line (ex: LET, ADD, etc.)

        if keyword == "LET":
            let = Let(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)
            let.add_var_to_dict()
        elif keyword == "PRINT":
            print_keyword(lst_of_grin_tokens, variable_dict, keywords_lst)
        elif keyword == "INNUM":
            inputt = Innum(lst_of_grin_tokens, variable_dict, keywords_lst)
            inputt.add_num_to_var_dict()
        elif keyword == "INSTR":
            inputt = Instr(lst_of_grin_tokens, variable_dict, keywords_lst)
            inputt.add_str_to_var_dict()
        elif keyword == "ADD":
            add = Add(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)
            add.add()
        elif keyword == "SUB":
            subtract = Sub(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)
            subtract.subtract()
        elif keyword == "MULT":
            multiply = Mult(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)
            multiply.multiply()
        elif keyword == "DIV":
            divide = Div(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)
            divide.divide()
        elif keyword == "GOTO":
            goto = GoTo(lst_of_grin_tokens, variable_dict, labels_dict, line_number,
                        end_line_number, keywords_lst)
            if len(lst_of_grin_tokens) >= 2 and len(
                    lst_of_grin_tokens) <= 4:  # GOTO target or LABEL: GOTO target
                line_number = goto.goto_target()  # setting the new line number
            elif len(lst_of_grin_tokens) >= 6 and len(lst_of_grin_tokens) <= 8:
                previous_line_number = line_number
                line_number = goto.goto_target_expression()
                if line_number == previous_line_number:  # no effect bc comparison was false
                    line_number += 1
        elif keyword == "GOSUB":
            gosub = GoSub(lst_of_grin_tokens, variable_dict, labels_dict, line_number,
                          end_line_number, keywords_lst)
            if len(lst_of_grin_tokens) >= 2 and len(
                    lst_of_grin_tokens) <= 4:  # GOSUB target or LABEL: GOSUB target
                line_number = gosub.gosub_target(gosub_line_nums)
            elif len(lst_of_grin_tokens) >= 6 and len(lst_of_grin_tokens) <= 8:
                previous_line_number = line_number
                line_number = gosub.gosub_target_expression(gosub_line_nums)
                if line_number == previous_line_number:  # no effect bc comparison was false
                    line_number += 1
        elif keyword == "RETURN":
            line_number = return_keyword(gosub_line_nums)
        elif keyword == "END":
            sys.exit(0)
        if keyword != "GOTO" and keyword != "GOSUB" and keyword != "RETURN":
            line_number += 1  # increase line number after calling necessary module

def create_statements_list():
    # read inputs/lines of grin statements
    try:
        statements_list = []
        while True:
            statement = input().strip()
            if statement == ".":  # end of program reached
                statements_list.append(statement)
                break
            else:  # store the grin statement in an iterable
                statements_list.append(statement)
        return statements_list
    except Exception as e:
        sys.exit(f'Error: {e}')

def parse_statements(statements_lst):
    try:
        parsed_statments_lst = list(parse(statements_lst))
        return parsed_statments_lst
    except Exception as e:
        sys.exit(f'Error: {e}')

def create_labels_dict(statements_lst, labels_dict):
    try:
        for lst_of_grin_tokens in statements_lst:  # creating the labels dict   parse(statements_lst)
            labels_dict = store_labels(labels_dict, lst_of_grin_tokens)
        return labels_dict
    except Exception as e:
        sys.exit(f'Error: {e}')

if __name__ == '__main__':
    main()
