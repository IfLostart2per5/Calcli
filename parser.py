
from sly import Parser
from lexer import Lexel
from math import factorial
from utils import Consts, format_motor, normalize_number, clear_ends
from re import match
from inspect import isgenerator  
from random import randint
class undefined:
    def __str__(self) -> str:
        return 'undefined'

    def __repr__(self) -> str:
        return 'undefined()'


class GeneratorRepr:
    def __init__(self, mode, start_or_list, limit=None, step=1) -> None:
        if mode == "range":
            self._repr = list(range(start_or_list, limit, step))
            self.gen = (i for i in range(start_or_list, limit, step))
        elif mode == "list":
            self._repr = start_or_list
            self.gen = (i for i in start_or_list)
    def __repr__(self):
        return str(self._repr) + "@lazy_mode"


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

    @_('assign')
    def line(self, p):
        pass

    @_('relational')
    def line(self, p):
        return p.relational

    @_('condition')
    def line(self, p):
        return p.condition

    @_('empty')
    def line(self, p): pass

    @_('COMMENT')
    def line(self, p): pass


    @_('strexpr')
    def line(self, p):
        return p.strexpr

    @_('statement')
    def line(self, p):
        pass


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
            return normalize_number(p.term / p.fact)
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
    
    @_('RANDOM "(" term "," fact ")"')
    def term(self, p):
        return randint(p.term, p.fact)


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
            return normalize_number(p.fact ** p.prime)
        except ZeroDivisionError:
            print("Erro: zero não pode ser elevado a um número negativo.")

    @_('SQRT "(" prime ")"')
    def fact(self, p):
        try:
            return sqrt(p.prime)
        except ValueError:
            print("Erro: erro de dominio matematico.")
    
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
                print(f"Erro: não foi encontrado um valor chamado '{p.ID}'")
                



    @_('ID "[" expr "]"')
    def prime(self, p):
        try:
            return self.names[p.ID][p.expr]
        except TypeError:
            print("Erro: um número não suporta indexação!")
        except LookupError:
            print(f"Erro: não foi encontrado um valor chamado '{p.ID}'")
    @_('ID "[" ARROW "]"')
    def prime(self, p):
        try:
            if isinstance(self.names[p.ID], GeneratorRepr) and isgenerator(self.names[p.ID].gen):
                try:
                    return next(self.names[p.ID].gen)
                except StopIteration:
                    print("Erro: a expressão geradora acabou.")
                    del self.names[p.ID]
            else:
                print("Erro: a lista não está no modo tardio!")
        except LookupError:
            print(f"Erro: não foi emcontrado um valor chamado '{p.ID}'")

    @_('NUMBER')
    def number(self, p):
        return p.NUMBER

    @_('ID "=" value')
    def assign(self, p):
        if p.ID in self.const_names:
            print(f"Erro: o nome '{p.ID}' já foi declarado como uma constante.")
        else:
            self.names[p.ID] = p.value
        
    @_('POSTERIOR ID')
    def assign(self, p):
        self.names[p.ID] = undefined()

    @_('CONST ID "=" value')
    def assign(self, p):
        try:
            if p.ID in self.names.keys():
                print(f"Erro: o nome '{p.ID}' ja foi declarado como uma variavel.")
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

    @_('"(" expr ")" ARROW expr')
    def condition(self, p):
        if bool(p.expr0):
            return p.expr1

    @_('"(" expr ")" ARROW expr ":" expr')
    def condition(self, p):
        if bool(p.expr0):
            return p.expr1
        else:
            return p.expr2

    @_('"(" expr ")" ARROW expr ":" condition')
    def condition(self, p):
        if bool(p.expr0):
            return p.expr1
        else:
            return p.condition

    
    @_('expression')
    def value(self, p):
        return p.expression

    @_('lista')
    def value(self, p):
        return p.lista

    @_('expr')
    def expression(self, p):
        return p.expr

    @_('relational')
    def expression(self, p):
        return p.relational

    @_('strexpr')
    def expression(self, p):
        return p.strexpr

    @_('"{" expr RANGE expr "}"')
    def lista(self, p):
        return list(range(p.expr0, p.expr1))

    @_('"{" expr RANGE expr ARROW expr "}"')
    def lista(self, p):
        return list(range(p.expr0, p.expr1, p.expr2))

    @_('"{" expr RANGE expr "@" "}"')
    def lista(self, p):
        return GeneratorRepr("range", p.expr0, p.expr1)

    @_('"{" expr RANGE expr ARROW expr "@" "}"')
    def lista(self, p):
        return GeneratorRepr("range", p.expr0, p.expr1, p.expr2)

    @_('"{" empty "}"')
    def lista(self, p):
        return []


    @_('"{" elements "}"')
    def lista(self, p):
        return p.elements

    @_('"{" elements "@" "}"')
    def lista(self, p):
        return GeneratorRepr("list", p.elements)

    @_('')
    def empty(self, p):
        pass

    @_('expr "," elements')
    def elements(self, p):
        return [p.expr] + (p.elements)

    @_('expr')
    def elements(self, p):
        return [p.expr]

    @_('strexpr "," elements')
    def elements(self, p):
        return [p.strexpr] + (p.elements)

    @_('strexpr')
    def elements(self, p):
        return [p.strexpr]

    @_('WRITE "(" strexpr ")"')
    def statement(self, p):
        print(p.strexpr)

    @_('WRITE "(" expr ")"')
    def statement(self, p):
        print(p.expr)

    @_('DELETE ID')
    def statement(self, p):
        try:
            del self.names[p.ID]
        except LookupError:
            if p.ID in self.const_names:
                print(f"Erro: '{p.ID}' é uma constante, por tanto, não pode ser reatribuida.")
            else:
                print("Erro: não foi encontrado um valor chamado '{p.ID}'.")

    @_('APPEND "(" ID "," expression ")"')
    def statement(self, p):
        try:
            if type(self.names[p.ID]) is list:
                self.names[p.ID].append(p.expression)
            else:
                print('Erro: a função add não funciona com números e/ou strings!')
        except LookupError:
            print(f"Erro: não foi encontrado um valor chamado '{p.ID}'")

    @_('POP "(" ID ")"')
    def statement(self, p):
        try:
            if type(self.names[p.ID]) is list:
                return self.names[p.ID].pop()
            else:
                print("Erro: o método pop não funciona com números e/ou strings!")
        except LookupError:
            print(f"Erro: não foi encontrado um valor chamado '{p.ID}'")

    @_('POP "(" ID "," expr ")"')
    def statement(self, p):
        try:
            if type(self.names[p.ID]) is list:
                return self.names[p.ID].pop(p.expr)
            else:
                print("Erro: a função pop não funciona com números e/ou strings!")
        except LookupError:
            print(f"Erro: não foi encontrado um valor chamado '{p.ID}'")
        except IndexError:
            print("Erro: indices fora do intervalo")

    @_('CLEAR "(" ID ")"')
    def statement(self, p):
        try:
            if type(self.names[p.ID]) is list:
                self.names[p.ID] = []
            else:
                print("Erro: a função clear não funciona com números e/ou strings!")
        except LookupError:
            print(f"Erro: não foi encontrado um valor chamado '{p.ID}'")

    @_('DELETE ID "[" expr "]"')
    def statement(self, p):
        try:
            del self.names[p.ID][p.expr]
        except TypeError:
            print('Erro: um número não suporta indexação')
        

    @_('strexpr PLUS string')
    def strexpr(self, p):
        return p.strexpr + p.string 

    @_('string')
    def strexpr(self, p):
        return p.string

    @_('STRING')
    def string(self, p):
        return p.STRING

    @_('string REST "[" elements "]"')
    def string(self, p):
        try:
            return format_motor(p.string, p.elements)
        except ValueError:
            print("Erro: a quantidade de parametros e a quantidade de marcadores de formatação não são iguais!")






if __name__ == "__main__":
    yacc = Parsel(Lexel())
    try:

        while (data := input('(debug) \\> ')) != '.q':
        
            r = yacc.parse(yacc.lex.tokenize(data))
            print(r) if r is not None else None
    except KeyboardInterrupt as e:
        print(e)
    except EOFError:
        print("Tchau ;)")
