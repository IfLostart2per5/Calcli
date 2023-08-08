
import re

# self-explain... but him returns the string without your ends
def clear_ends(string):
    return string[1:-1]

# constants table. oh, im missing you, static typing languages <3<3
class Consts:
    def __init__(self) -> None:
        self.constants = {}

    def __getitem__(self, key):
        return self.constants[key]

    def __setitem__(self, key, value):
        if not (key in self.constants.keys()):
            self.constants[key] = value

        else:
            raise ValueError("Value already exists!")

    def __contains__(self, value):
        if value in self.constants.keys():
            return True
        else:
            return False

# normalize a floating point number into a integer, if him is a integer
def normalize_number(number: float | complex | int):
    if type(number) is complex:
        return number
    else:
        n = int(number)
        if n == number:
            return n
        else:
            return number

def parse(type_, string):
    return type_(string)

# auto parses a string into a numeric type
def dynamic_parse(string):
    if re.match(r'-?\d+', string):
        return parse(int, string)
    elif re.match(r'-?\d+\.\d+', string):
        return parse(float, string)
    elif re.match(r'-?\d+(\.\d+)(\+|-)\d+(\.\d+)i|\d(\.\d+)i', string, re.IGNORECASE):
        return parse(complex, string.replace('i', 'j'))

# format a string based in "$" markers
def format_motor(string, args):
    # the indexes to replace
    indexes = []

    # the index acumulator
    index_acc = -1
    for char in string:
        if char == "$":
            index_acc += 1
            indexes.append(index_acc)
        else:
            index_acc += 1
    
    formatters_count = string.count('$')
    
    # temporary mutable string
    temp_string_list = list(string)

    if formatters_count == len(args):
        for arg, index in zip(args, indexes):
            temp_string_list[index] = arg
    else:
        raise ValueError("Valores incompativeis!")
    # mounting the final string
    formatted = ''.join(map(lambda x: str(x), temp_string_list))

    del temp_string_list

    return formatted




if __name__ == "__main__":
    #testing
    print(format_motor("$ $ $", [2, 3, 4]))



