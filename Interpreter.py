from parser import Lexel, Parsel
from math import pi, e
class Interpreter:
    def __init__(self):
        self.main = Parsel(Lexel())
        self.main.const_names['i'] = 1j
        self.main.const_names['pi'] = pi
        self.main.const_names['euler'] = e 

    def run(self, expression):
        return self.main.parse(self.main.lex.tokenize(expression))


