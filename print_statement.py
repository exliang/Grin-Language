
# Module for the PRINT keyword

import sys


def print_keyword(lst_of_grin_tokens, variable_dict, keywords_lst):
    try:
        if lst_of_grin_tokens[0].text() not in keywords_lst:  # line is a label
            value_to_print = lst_of_grin_tokens[3].text()
        else:
            value_to_print = lst_of_grin_tokens[1].text()
        if value_to_print in variable_dict.keys():  # if value is a variable
            value_from_dict = variable_dict[value_to_print]
            print(value_from_dict)
        elif '"' not in value_to_print and not value_to_print.isnumeric():  # a var that hasn't been assigned yet
            print(0)
        else:  # value is a just a literal value
            if type(value_to_print) == str:
                value_to_print = value_to_print.replace('"','')  # get rid of quotes when printing
            print(value_to_print)
    except Exception as e:  # case not tested because exception is catched here just in case something goes wrong
        sys.exit(f"Error: {e}")

