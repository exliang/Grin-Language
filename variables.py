
# Module for creating and editing the variables dictionary

import sys


class Let:
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict):
        self.dict = variable_dict
        self.keywords_lst = keywords_lst
        self.tokens_lst = lst_of_grin_tokens
        self.labels_dict = labels_dict
        if self.tokens_lst[0].text() not in self.keywords_lst:  # if line starts w a label
            self.keyword = lst_of_grin_tokens[2].text()  # LET
            self.var_name = lst_of_grin_tokens[3].text()
            self.var_value = lst_of_grin_tokens[4].text()
        else:
            self.keyword = lst_of_grin_tokens[0].text()  # LET
            self.var_name = lst_of_grin_tokens[1].text()
            self.var_value = lst_of_grin_tokens[2].text()

    def add_var_to_dict(self):
        try:
            if self.var_value.isnumeric() or self.var_value.replace(".","").replace("-","").isnumeric() :  # var value is a number (int or float)
                if "." in self.var_value:  # float
                    if self.keyword == "DIV":
                        self.dict[self.var_name] = 0 / float(self.var_value)
                    elif self.keyword == "MULT":
                        self.dict[self.var_name] = 0 * float(self.var_value)
                    elif self.keyword == "SUB":
                        self.dict[self.var_name] = 0 - float(self.var_value)
                    else:  # ADD
                        self.dict[self.var_name] = float(self.var_value)
                else:  # int
                    if self.keyword == "DIV":
                        self.dict[self.var_name] = 0 // int(self.var_value)
                    elif self.keyword == "MULT":
                        self.dict[self.var_name] = 0 * int(self.var_value)
                    elif self.keyword == "SUB":
                        self.dict[self.var_name] = 0 - int(self.var_value)
                    else:  # ADD
                        self.dict[self.var_name] = int(self.var_value)
            elif isinstance(self.var_value, str):  # string
                var_value_stripped = self.var_value.strip('"')  # remove quotes
                if '"' not in self.var_value:   # unassigned variable (not string)
                    if var_value_stripped not in self.dict.keys():
                        self.dict[self.var_value] = 0
                        all_zeros = True
                        for value in self.dict.values():
                            if value != 0:
                                all_zeros = False
                        if self.keyword == "DIV" and all_zeros:
                            sys.exit("RunTimeError: cannot divide by 0")
                    elif var_value_stripped in self.dict.keys():
                        if self.keyword != "MULT":
                            self.dict[self.var_name] = 0
                elif var_value_stripped in self.dict.keys():  # check if the var_value is the var_name of another var
                    value_from_dict = self.dict[var_value_stripped]
                    self.dict[self.var_name] = value_from_dict
                else:  # var_value is just a string
                    self.dict[self.var_name] = var_value_stripped
        except Exception as e:
            sys.exit(f'Error: {e}')

class Add(Let):
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict):
        super().__init__(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)

    def add(self):
        try:
            for dict_var_name, dict_value in self.dict.items():
                both_float = isinstance(dict_value,float) and "." in self.var_value
                int_and_float = isinstance(dict_value,int) and "." in self.var_value
                float_and_int = isinstance(dict_value,float) and "." not in self.var_value
                both_int = isinstance(dict_value,int) and "." not in self.var_value

                if dict_var_name == self.var_name or dict_var_name == self.var_value:
                    if dict_var_name == self.var_value:
                        self.add_var_to_dict()
                    if ((type(dict_value) == int or type(dict_value) == float) and (self.var_value.replace("-","").isnumeric()
                            or self.var_value.replace(".","").replace("-", "").isnumeric())):  # ints & floats
                        if both_float or int_and_float:  # float + float or int + float
                            self.dict[self.var_name] = dict_value + float(self.var_value)
                        elif float_and_int or both_int:  # float + int or int + int
                            self.dict[self.var_name] = dict_value + int(self.var_value)
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
                    else:  # strings
                        value = self.var_value
                        self.var_value = self.var_value.strip('"')  # remove quotes
                        if '"' not in value and value not in self.dict.keys():  # value has been used before assignment
                            self.add_var_to_dict()
                        if self.var_value in self.dict.keys():  # check if the var_value is the var_name of another var
                            value_from_dict = self.dict[self.var_value]
                            self.dict[self.var_name] = self.dict[self.var_name] + value_from_dict
                        elif self.var_value not in self.dict.keys():  # var_value is just a string
                            self.dict[self.var_name] = dict_value + self.var_value
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
            else:  # break not hit means the variable has not been created yet, so it will be assigned a value of 0 which is the original var_value
                self.add_var_to_dict()
        except Exception as e:
            sys.exit(f'Error: {e}')

class Sub(Let):
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict):
        super().__init__(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)

    def subtract(self):
        try:
            for dict_var_name, dict_value in self.dict.items():
                both_float = isinstance(dict_value,float) and "." in self.var_value
                int_and_float = isinstance(dict_value,int) and "." in self.var_value
                float_and_int = isinstance(dict_value,float) and "." not in self.var_value
                both_int = isinstance(dict_value,int) and "." not in self.var_value

                if dict_var_name == self.var_name or dict_var_name == self.var_value:
                    if dict_var_name == self.var_value:
                        self.add_var_to_dict()
                    if ((type(dict_value) == int or type(dict_value) == float) and (self.var_value.isnumeric()
                            or self.var_value.replace(".","").replace("-", "").isnumeric())):  # ints & floats
                        if both_float or int_and_float:  # float + float or int + float
                            self.dict[self.var_name] = dict_value - float(self.var_value)
                        elif float_and_int or both_int:  # float + int or int + int
                            self.dict[self.var_name] = dict_value - int(self.var_value)
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
                    else:  # var names that are strings are var_value
                        value = self.var_value
                        self.var_value = self.var_value.strip('"')  # remove quotes
                        if '"' not in value and value not in self.dict.keys():  # value has been used before assignment
                            self.add_var_to_dict()
                        if self.var_value in self.dict.keys():  # check if the var_value is the var_name of another var
                            value_from_dict = self.dict[self.var_value]
                            self.dict[self.var_name] =  self.dict[self.var_name] - value_from_dict
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
            else:  # break not hit means the variable has not been created yet, so it will be assigned a value of 0 which is the original var_value
                self.add_var_to_dict()
        except Exception as e:
            sys.exit(f'Error: {e}')

class Mult(Let):
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict):
        super().__init__(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)

    def multiply(self):
        try:
            for dict_var_name, dict_value in self.dict.items():
                both_float = isinstance(dict_value,float) and "." in self.var_value
                int_and_float = isinstance(dict_value,int) and "." in self.var_value
                float_and_int = isinstance(dict_value,float) and "." not in self.var_value
                both_int = isinstance(dict_value,int) and "." not in self.var_value

                if dict_var_name == self.var_name or dict_var_name == self.var_value:
                    if dict_var_name == self.var_value:
                        self.add_var_to_dict()
                    if ((type(dict_value) == int or type(dict_value) == float) and (self.var_value.replace("-","").isnumeric()
                            or self.var_value.replace(".","").replace("-", "").isnumeric())):  # ints & floats
                        if both_float or int_and_float:  # float + float or int + float
                            self.dict[self.var_name] = dict_value * float(self.var_value)
                        elif float_and_int or both_int:  # float + int or int + int
                            self.dict[self.var_name] = dict_value * int(self.var_value)
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
                    else:  # strs
                        # var_value is a var name
                        value = self.var_value
                        self.var_value = self.var_value.strip('"')  # remove quotes
                        if '"' not in value and value not in self.dict.keys():  # value has been used before assignment
                            self.add_var_to_dict()
                        if self.var_value in self.dict.keys():  # check if the var_value is the var_name of another var
                            value_from_dict = self.dict[self.var_value]
                            self.dict[self.var_name] = self.dict[self.var_name] * value_from_dict

                        # int + str or str + int
                        elif type(dict_value) == str:
                            if self.var_value.replace("-","").isnumeric() and int(self.var_value) < 0:  # if one of the operands is a negative int
                                sys.exit("RunTimeError: negative multiplication of a string.")
                            else:
                                dict_value = dict_value.strip('"')  # remove quotes
                                self.dict[self.var_name] = dict_value * int(self.var_value)
                        elif type(self.var_value) == str:
                            if str(dict_value).replace("-","").isnumeric() and dict_value < 0:  # if one of the operands is a negative int
                                sys.exit("RunTimeError: negative multiplication of a string.")
                            else:
                                self.var_value = self.var_value.strip('"')  # remove quotes
                                self.dict[self.var_name] = dict_value * self.var_value
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
            else:  # break not hit means the variable has not been created yet, so it will be assigned a value of 0 which is the original var_value
                self.add_var_to_dict()
        except Exception as e:
            sys.exit(f'Error: {e}')

class Div(Let):
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict):
        super().__init__(lst_of_grin_tokens, variable_dict, keywords_lst, labels_dict)

    def divide(self):
        try:
            for dict_var_name, dict_value in self.dict.items():
                both_float = isinstance(dict_value,float) and "." in self.var_value
                int_and_float = isinstance(dict_value,int) and "." in self.var_value
                float_and_int = isinstance(dict_value,float) and "." not in self.var_value
                both_int = isinstance(dict_value,int) and "." not in self.var_value

                if dict_var_name == self.var_name or dict_var_name == self.var_value:
                    if dict_var_name == self.var_value:
                        self.add_var_to_dict()
                    if ((type(dict_value) == int or type(dict_value) == float) and (self.var_value.isnumeric()
                            or self.var_value.replace(".","").replace("-", "").isnumeric())):  # ints & floats
                        if both_float or int_and_float:  # float + float or int + float
                            self.dict[self.var_name] = dict_value / float(self.var_value)
                        elif float_and_int:  # float + int
                            self.dict[self.var_name] = dict_value / int(self.var_value)
                        elif both_int:  # int + int
                            self.dict[self.var_name] = dict_value // int(self.var_value)
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
                    else:  # var names that are strings are var_value
                        value = self.var_value
                        self.var_value = self.var_value.strip('"')  # remove quotes
                        if '"' not in value and value not in self.dict.keys():  # value has been used before assignment
                            self.add_var_to_dict()
                        if self.var_value in self.dict.keys():  # check if the var_value is the var_name of another var
                            value_from_dict = self.dict[self.var_value]
                            self.dict[self.var_name] = self.dict[self.var_name] / value_from_dict
                        else:  # invalid option
                            sys.exit("RunTimeError: invalid combination.")
                        break
            else:  # break not hit means the variable has not been created yet, so it will be assigned a value of 0 which is the original var_value
                self.add_var_to_dict()
        except ZeroDivisionError:
            sys.exit("RunTimeError: cannot divide by 0.")
        except Exception as e:
            sys.exit(f'Error: {e}')