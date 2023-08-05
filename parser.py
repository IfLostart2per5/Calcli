from sly import Parser
from lexer import Lexel
from math import factorial, sqrt
from utils import Consts
from re import match

class undefined:
    def __str__(self) -> str:
        return 'undefined'

    def __repr__(self) -> str:
        return ''

class Parsel(Parser):

    tokens = Lexel.tokens

    literals = Lexel.literals 
    def __init__(self, lex):
        self.lex = lex
        self.names = {}
        self.const_names = Consts()
     


    @_('expr')
    def line(self, p):
        return p.expr

    @_('statement')
    def line(self, p):
        pass

    @_('relational')
    def line(self, p):
        return p.relational

    @_('condition')
    def line(self, p):
        return p.condition

    @_('loop')
    def line(self, p):
        return p.loop


    @_('expr PLUS term')
    def expr(self, p):
        return p.expr + p.term

    @_('expr SUB term')
    def expr(self, p):
        return p.expr - p.term

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES fact')
    def term(self, p):
        return p.term * p.fact

    @_('term DIV fact')
    def term(self, p):
        try:
            return p.term / p.fact 
        except ZeroDivisionError:
            print("Erro: Um número não pode ser dividido por 0, pois x / 0 é inválido, onde x pode ser qualquer número...")
            return undefined()


    @_('term REST fact')
    def term(self, p):
        try:
            return p.term % p.fact
        except ZeroDivisionError:
            print("Erro: Um número não pode ser dividido por 0, pois x / 0 é inválido, onde x pode ser qualquer número...")
            return undefined()



    @_('"|" fact "|"')
    def term(self, p):
        return abs(p.fact)

    @_('fact "!"')
    def term(self, p):
        return factorial(p.fact)

    @_('fact')
    def term(self, p):
        return p.fact

    @_('fact POWER prime')
    def fact(self, p):
        try:
            return p.fact ** p.prime
        except ZeroDivisionError:
            print("Erro: zero não pode ser elevado a um número negativo.")

    @_('SQRT "(" prime ")"')
    def fact(self, p):
        return sqrt(p.prime)
    
    @_('CUSTOMRT "(" prime "," prime ")"')
    def fact(self, p):
        return p.prime0 ** (p.prime1 ** -1)

    @_('PERHUNDRED "(" prime ")"')
    def fact(self, p):
        return p.prime / 100

    @_('PERTHOUSAND "(" prime ")"')
    def fact(self, p):
        return p.prime / 1000

    @_('prime')
    def fact(self, p):
        return p.prime

    @_('"(" expr ")"')
    def prime(self, p):
        return p.expr 

    @_('"(" SUB expr ")"')
    def prime(self, p):
        return -p.expr

    @_('INPUT "(" ")"')
    def prime(self, p):
        r = input("... ")
        return self.parse(self.lex.tokenize(r))

    @_('number')
    def prime(self, p):
        return p.number

    @_('ID')
    def prime(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            try:
                return self.const_names[p.ID]
            except LookupError:
                print(f"Valor {p.ID} não foi declarado")
                


    @_('DELETE ID')
    def prime(self, p):
        try:
            del self.names[p.ID]
        except KeyError:
            print(f"Variavel {p.ID} nao foi declarada")

    @_('ID "[" expr "]"')
    def prime(self, p):
        return self.names[p.ID][p.expr]

    @_('NUMBER')
    def number(self, p):
        return p.NUMBER

    @_('ID "=" value')
    def statement(self, p):
        if p.ID in self.const_names:
            print(f"O nome {p.ID} já foi declarado como uma constante.")
        else:
            self.names[p.ID] = p.value
        
        


    @_('CONST ID "=" value')
    def statement(self, p):
        try:
            if p.ID in self.names.keys():
                print(f"o nome {p.ID} ja foi declarado c    omo uma variavel.")
            else:
                self.const_names[p.ID] = p.value
        except ValueError:
            print("Erro: constantes não podem ser reatríbuidas!")


    @_('expr GE expr')
    def relational(self, p):
        return int(p.expr0 >= p.expr1)



    @_('expr LE expr')
    def relational(self, p):
        return int(p.expr0 <= p.expr1)

    @_('expr EQ expr')
    def relational(self, p):
        return int(p.expr0 == p.expr1)

    @_('expr NE expr')
    def relational(self, p):
        return int(p.expr0 != p.expr1)

    @_('expr GT expr')
    def relational(self, p):
        return int(p.expr0 > p.expr1)

    @_('expr LT expr')
    def relational(self, p):
        return int(p.expr0 < p.expr1)

    @_('"(" relational ")" ARROW expr')
    def condition(self, p):
        if bool(p.relational):
            return p.expr

    @_('"(" relational ")" ARROW expr ":" expr')
    def condition(self, p):
        if bool(p.relational):
            return p.expr0
        else:
            return p.expr1

    @_('"(" relational ")" ARROW expr ":" condition')
    def condition(self, p):
        if bool(p.relational):
            return p.expr
        else:
            return p.condition



    @_('"[" expr "," expr "," expr "]" ARROW line ')
    def loop(self, p):
        ran = range(p.expr0, p.expr1, p.expr2)
        for _ in ran:
            print(p.line)

    @_('expr')
    def value(self, p):
        return p.expr

    @_('relational')
    def value(self, p):
        return p.relational

    @_('"{" expr RANGE expr "}"')
    def value(self, p):
        return list(range(p.expr0, p.expr1))

    @_('"{" expr RANGE expr ARROW expr "}"')
    def value(self, p):
        return list(range(p.expr0, p.expr1, p.expr2))

    







if __name__ == "__main__":
    yacc = Parsel(Lexel())

    try:

        while (data := input('expression > ')) != '.q':
        
            r = yacc.parse(yacc.lex.tokenize(data))
            print(r) if r is not None else None
    except KeyboardInterrupt as e:
        print(e)
    except EOFError:
        print("Tchau ;)")
