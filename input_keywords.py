
# Module for the INNUM and INSTR keywords

import sys


class Input:
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst):
        self.dict = variable_dict
        if lst_of_grin_tokens[0].text() not in keywords_lst:  # starts w label
            self.keyword = lst_of_grin_tokens[2].text()  # INNUM or INSTR
            self.var_name = lst_of_grin_tokens[3].text()
        else:
            self.keyword = lst_of_grin_tokens[0].text()  # INNUM or INSTR
            self.var_name = lst_of_grin_tokens[1].text()
        self.var_value = input().strip()

class Innum(Input):
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst):
        super().__init__(lst_of_grin_tokens, variable_dict, keywords_lst)

    def add_num_to_var_dict(self):
        try:
            if self.var_value.isnumeric() or self.var_value.replace("-","").isnumeric():  # pos & neg int
                self.dict[self.var_name] = int(self.var_value)
            elif self.var_value.replace(".","").replace("-","").isnumeric():  # pos & neg float
                self.dict[self.var_name] = float(self.var_value)
            else:  # invalid option
                sys.exit("RunTimeError: invalid combination.")
        except Exception as e:
            sys.exit(f'Error: {e}')

class Instr(Input):
    def __init__(self, lst_of_grin_tokens, variable_dict, keywords_lst):
        super().__init__(lst_of_grin_tokens, variable_dict, keywords_lst)

    def add_str_to_var_dict(self):
        try:
            self.dict[self.var_name] = self.var_value
        except Exception as e:
            sys.exit(f'Error: {e}')