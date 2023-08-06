import readline
import atexit
from Interpreter import Interpreter
from os import environ

def setup():
    readline.parse_and_bind('tab: complete')
    history = ".calcli_history"
    if environ.get('HOME') is not None:
        history = f"{environ.get('HOME')}/{history}"
    elif environ.get('USERPROFILE') is not None:
        history = f"{environ.get('USERPROFILE')}\\{history}"

    try:
        readline.read_history_file(history)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, history)
def read(prompt=""):
    return input(prompt)

setup()

try:
    interpreter: Interpreter = Interpreter()

    while True:
        expr = read("/>> ")
        r = interpreter.run(expr)
        print(r) if r is not None else None
except KeyboardInterrupt:
    print('Ctrl-C')
except EOFError:
    print('Tchau ;)')

