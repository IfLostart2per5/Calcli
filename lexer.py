
from sly import Lexer 
from utils import dynamic_parse, clear_ends
from re import match


class Lexel(Lexer):
    tokens = {NUMBER, PLUS, TIMES, DIV, SUB, POWER, REST, ID, DELETE, GE, LE, NE, GT, LT, EQ, ARROW, RANGE, CONST, SQRT, CUSTOMRT, PERHUNDRED, PERTHOUSAND, INPUT, COMMENT, POSTERIOR, STRING}

    literals = {'(', ')','!', '|', '=', ':', '[', ']','{', '}', ',', '@', ';'}
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = r"\d+(\.\d+)?i?"
    STRING = r'"(.*?)"'
    ARROW = r"\-\>"
    RANGE = r"\.\.\."
    COMMENT = r"\#\#.*"
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
    ID['post'] = POSTERIOR
    
    ignore = r" \t"
    ignore_newline = r"\n+"

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

    @_(r'\#\#.*')
    def COMMENT(self, t):
        pass 

    @_(r'"(.*?)"')
    def STRING(self, t):
        t.value = clear_ends(t.value)
        return t


    def error(self, t):
        raise ValueError("Bad character {!r} at line {} and index {}".format(t.value[0], self.lineno, self.index))


if __name__ == "__main__":
    lex = Lexel()
    while True:
        try:
            r = input('(debug) />>')
            for tk in lex.tokenize(r):
                print(f"type = '{tk.type}' value = '{tk.value}'")
        except EOFError:
            break
