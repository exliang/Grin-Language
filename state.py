
# Module for managing the program's state

import sys


class Go:
    def __init__(self, lst_of_grin_tokens, variable_dict, labels_dict, line_number, end_line_number, keyword_lst):
        self.target = lst_of_grin_tokens[1].text()
        self.tokens_lst = lst_of_grin_tokens
        self.var_dict = variable_dict
        self.labels_dict = labels_dict
        self.curr_line_number = line_number
        self.end_line_number = end_line_number
        self.keywords_lst = keyword_lst

class GoTo(Go):
    def __init__(self, lst_of_grin_tokens, variable_dict, labels_dict, line_number, end_line_number, keyword_lst):
        super().__init__(lst_of_grin_tokens, variable_dict, labels_dict, line_number, end_line_number, keyword_lst)

    def goto_target(self):
        # returns the new line number whether target is an int or label
        try:
            if self.tokens_lst[0].text() not in self.keywords_lst:  # starts w label
                self.target = self.tokens_lst[3].text()
            if self.target.replace("-","").isnumeric():  # target = pos or neg int
                return target_is_int(self.target, self.curr_line_number, self.end_line_number)
            elif not self.target.replace("-","").isnumeric():  # target = string
                if self.target.replace('"','') in self.labels_dict.values():  # check if the target is a label
                    return target_is_label(self.target, self.labels_dict)
                elif self.target in self.var_dict.keys():  # target is a var name
                    value = self.var_dict[self.target]
                    if type(value) == int:  # var value is int
                        return target_is_int(value, self.curr_line_number, self.end_line_number)
                    elif type(value) == str:  # var value is str (label)
                        if value in self.labels_dict.values():  # check if the target is a label
                            return target_is_label(value, self.labels_dict)
                    else:
                        sys.exit("RunTimeError: variable value is not an integer or a string.")  # label was not found in dict
                else:
                    sys.exit("RunTimeError: target is not a label or a variable name.")
            else:  # target is not an int or a label (string)
                sys.exit("RunTimeError: target is not an int or a string.")
        except Exception as e:
            sys.exit(f'ERROR: {e}')

    def goto_target_expression(self):
        try:
            if self.tokens_lst[0].text() not in self.keywords_lst:  # starts w label
                value1 = self.tokens_lst[5].text()
                operator = self.tokens_lst[6].text()
                value2 = self.tokens_lst[7].text()
            else:
                value1 = self.tokens_lst[3].text()
                operator = self.tokens_lst[4].text()
                value2 = self.tokens_lst[5].text()
            valid_values = [(int,int), (float,float), (int,float), (float,int), (str,str)]
            value1, value2 = determine_type_of_value1_and_value2(value1, value2, self.var_dict)
            if (type(value1), type(value2)) in valid_values: # check that value1 and value2 are the correct types
                if type(value1) == str:
                    value1 = value1.replace('"','')
                if type(value2) == str:
                    value2 = value2.replace('"', '')
                if get_operator(operator) == "equal":
                    if value1 == value2:
                        return self.goto_target()
                    else:  # return original line_number
                        return self.curr_line_number
                elif get_operator(operator) == "not equal":
                    if value1 != value2:
                        return self.goto_target()
                    else:
                        return self.curr_line_number
                elif get_operator(operator) == "less than":
                    if value1 < value2:
                        return self.goto_target()
                    else:
                        return self.curr_line_number
                elif get_operator(operator) == "less than or equal":
                    if value1 <= value2:
                        return self.goto_target()
                    else:
                        return self.curr_line_number
                elif get_operator(operator) == "greater than":
                    if value1 > value2:
                        return self.goto_target()
                    else:
                        return self.curr_line_number
                elif get_operator(operator) == "greater than or equal":
                    if value1 >= value2:
                        return self.goto_target()
                    else:
                        return self.curr_line_number
                else:  # invalid operator
                    sys.exit("RunTimeError: invalid operator for value1 and value2.")
            else:  # invalid combination of values
                sys.exit("RunTimeError: invalid combination for value1 and value2.")
        except Exception as e:
            sys.exit(f'Error: {e}')

class GoSub(Go):
    def __init__(self, lst_of_grin_tokens, variable_dict, labels_dict, line_number, end_line_number, keyword_lst):
        super().__init__(lst_of_grin_tokens, variable_dict, labels_dict, line_number, end_line_number, keyword_lst)

    def gosub_target(self, gosub_line_nums):
        # add the next line after teh GOSUB statement to the front fo the list when a GOSUB statement is executed
        try:
            gosub_line_nums.insert(0,self.curr_line_number+1)
            return GoTo(self.tokens_lst, self.var_dict, self.labels_dict, self.curr_line_number, self.end_line_number, self.keywords_lst).goto_target()
        except Exception as e:
            sys.exit(f'Error: {e}')

    def gosub_target_expression(self, gosub_line_nums):
        try:
            gosub_line_nums.insert(0, self.curr_line_number + 1)
            return GoTo(self.tokens_lst, self.var_dict, self.labels_dict, self.curr_line_number, self.end_line_number, self.keywords_lst).goto_target_expression()
        except Exception as e:
            sys.exit(f'Error: {e}')

def return_keyword(gosub_line_nums):
    # go back to the most recent line number, which is the first eelm in the list then remove the elem (return new line_number)
    try:
        recent_line_number = gosub_line_nums[0]
        gosub_line_nums.pop(0)
        return recent_line_number
    except IndexError:
        sys.exit("RunTimeError: return statement was hit before a GOSUB was encountered.")
    except Exception as e:
        sys.exit(f'Error: {e}')

def store_labels(labels_dict, lst_of_grin_tokens):
    # {line_number: label_name}
    try:
        for i in range(len(lst_of_grin_tokens)):
            token1 = lst_of_grin_tokens[i]
            if i != len(lst_of_grin_tokens) - 1:
                token2 = lst_of_grin_tokens[i+1]
                if token2.text() == ":":  # this means token1 was a label
                    line_num_of_label = token1.location().line()
                    labels_dict[line_num_of_label] = token1.text()
        return labels_dict
    except Exception as e:
        sys.exit(f'Error: {e}')

def target_is_int(target, curr_line_number, end_line_number):
    try:
        if int(target) == 0:  # GOTO 0 is not permitted
            sys.exit("RunTimeError: cannot jump to the current line number.")
        new_line_number = curr_line_number + int(target)
        if new_line_number <= 0:
            sys.exit("RunTimeError: cannot jump to line number 0 or a negative line number.")
        elif new_line_number >= end_line_number + 2:
            sys.exit("RunTimeError: cannot jump to a line not in the program.")
        return new_line_number
    except Exception as e:
        sys.exit(f'Error: {e}')

def target_is_label(target, labels_dict):
    try:
        for line_num, label_name in labels_dict.items():
            if label_name == target.replace('"',''):  # get rid of quotes in target
                if line_num == 0:  # GOTO 0 is not permitted
                    sys.exit("RunTimeError: cannot jump to the current line number.")
                new_line_num = line_num
                return new_line_num
        sys.exit("Error: label does not exist.")  # label was not found in dict
    except Exception as e:
        sys.exit(f'Error: {e}')

def get_operator(operator):
    if operator == "=":
        return "equal"
    elif operator == "<>":
        return "not equal"
    elif operator == "<":
        return "less than"
    elif operator == "<=":
        return "less than or equal"
    elif operator == ">":
        return "greater than"
    elif operator == ">=":
        return "greater than or equal"
    else:
        return "invalid operator"

def determine_type_of_value1_and_value2(value1, value2, variable_dict):
    try:
        if value1.replace('-','').isnumeric():  # int
            value1 = int(value1)
        elif value1.replace('-','').replace('.','').isnumeric():  # float
            value1 = float(value1)
        elif not value1.replace('-', '').replace('.', '').isnumeric():  # value1 = str or var
            if value1 in variable_dict.keys():  # value1 = var
                value1 = variable_dict[value1]
            elif value1 not in variable_dict.keys():  # value1 = str
                value1 = str(value1)
        else:
            sys.exit("RunTimeError: value1 is not a valid option.")

        if value2.replace('-','').isnumeric():  # int
            value2 = int(value2)
        elif value2.replace('-','').replace('.','').isnumeric():  # float
            value2 = float(value2)
        elif not value2.replace('-','').replace('.','').isnumeric():  # value2 = str or var
            if value2 in variable_dict.keys():  # value1 = var
                value2 = variable_dict[value2]
            elif value2 not in variable_dict.keys():  # value1 = str
                value2 = str(value2)
        else:
            sys.exit("RunTimeError: value2 is not a valid option.")

        return value1, value2
    except Exception as e:
        sys.exit(f'Error: {e}')