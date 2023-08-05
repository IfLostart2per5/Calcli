from sly import Lexer 
import re

class Lexel(Lexer):
    tokens = {NUMBER, PLUS, TIMES, DIV, SUB, POWER, REST, ID, DELETE, GE, LE, NE, GT, LT, EQ, ARROW, RANGE, CONST, SQRT, CUSTOMRT, PERHUNDRED, PERTHOUSAND, INPUT}

    literals = {'(', ')','!', '|', '=', ':', '[', ']','{', '}', ','}
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = r"\d+(\.\d+)?i?"
    ARROW = r"\-\>"
    RANGE = r"\.\.\."
    GE = r"\>="
    LE = r"\<="
    NE = r"\!="
    EQ = r"=="
    GT = r"\>"
    LT = r"\<"
    POWER = r"\^"
    PLUS = r'\+'
    TIMES = r'\*'
    DIV = r'\/'
    SUB = r'\-'
    REST = r"\%"
    DELETE = r"\#"
    CONST = r"\$"

    ID['sqrt'] = SQRT
    ID['ctrt'] = CUSTOMRT
    ID['perc'] = PERHUNDRED
    ID['perm'] = PERTHOUSAND
    ID['receive'] = INPUT 
    
    ignore = r" \t"
    ignore_newline = r"\n+"
    ignore_comment = r"\#\#.*"

    @_(r"\d+(\.\d+)?i?")
    def NUMBER(self, t):
        if '.' in t.value:
            t.value = float(t.value)
        elif 'i' in t.value:
            t.value = complex(t.value.replace('i', 'j'))
        else:
            t.value = int(t.value)

        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += 1
        return t






    def error(self, t):
        raise ValueError("Bad character {!r} at line {} and index {}".format(t.value[0], self.lineno, self.index))
