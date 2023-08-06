
from sly import Lexer 
from utils import dynamic_parse, match
from re import match

class Lexel(Lexer):
    tokens = {NUMBER, PLUS, TIMES, DIV, SUB, POWER, REST, ID, DELETE, GE, LE, NE, GT, LT, EQ, ARROW, RANGE, CONST, SQRT, CUSTOMRT, PERHUNDRED, PERTHOUSAND, INPUT, COMMENT, POSTERIOR}

    literals = {'(', ')','!', '|', '=', ':', '[', ']','{', '}', ',', '@', ';'}
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = r"\d+(\.\d+)?i?"
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
        if t.value[3:].startswith('/%'):
            value = t.value[6:]
            key  = []
            value = []
            for char in value:
                if match('[a-z]', char):
                    key.append(char)
                elif match(r'\:', char):
                    continue
                elif match(r'[a-z]', char):
                    value.append(char)
                elif match(r"\%|\/", char):
                    pass

            key = ''.join(key)
            value = ''.join(value)

            if key == 'config-log':
                if value == '1':
                    with open('buffer', 'w') as f:
                        f.write('RECORD-LOG : TRUE')
                elif value == '0':
                    pass
                else:
                    raise RuntimeError('ERRO INTERNO: MÁ CONFIGURAÇÃO DO LOGGER')
            else:
                raise RuntimeError("ERRO INTERO: MÁ CONFIGURAÇÃO DO INTERPRETADOR")
        else:
            pass






    def error(self, t):
        raise ValueError("Bad character {!r} at line {} and index {}".format(t.value[0], self.lineno, self.index))
