
from re import match, IGNORECASE
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

def dynamic_parse(string):
    if match(r'-?\d+', string):
        return parse(int, string)
    elif match(r'-?\d+\.\d+', string):
        return parse(float, string)
    elif match(r'-?\d+(\.\d+)(\+|-)\d+(\.\d+)i|\d(\.\d+)i', string, IGNORECASE):
        return parse(complex, string.replace('i', 'j'))

