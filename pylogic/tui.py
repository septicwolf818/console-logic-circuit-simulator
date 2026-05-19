import sys

_ANSI = sys.stdout.isatty()

class _C:
    if _ANSI:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        BOLD = '\033[1m'
        DIM = '\033[2m'
        RESET = '\033[0m'
    else:
        GREEN = RED = YELLOW = CYAN = BOLD = DIM = RESET = ''

def green(t): return f"{_C.GREEN}{t}{_C.RESET}"
def red(t):   return f"{_C.RED}{t}{_C.RESET}"
def yellow(t):return f"{_C.YELLOW}{t}{_C.RESET}"
def cyan(t):  return f"{_C.CYAN}{t}{_C.RESET}"
def bold(t):  return f"{_C.BOLD}{t}{_C.RESET}"
def dim(t):   return f"{_C.DIM}{t}{_C.RESET}"

def on(val):
    return green('*') if val else red('o')

def bit(val):
    return green('1') if val else red('0')

def rule(char='-', width=58):
    return dim(char * width)

def menu(title, items, status=None, subtitle=None):
    print()
    if subtitle:
        print(f"  {bold(cyan(title))}  {dim(subtitle)}")
    else:
        print(f"  {bold(cyan(title))}")
    if status:
        print(f"  {dim(status)}")
    print(f"  {rule()}")
    for k, v in items:
        print(f"    {green(k)} {v}")
    print(f"  {rule()}")
    print(f"  {dim('Select: ')}", end="")
