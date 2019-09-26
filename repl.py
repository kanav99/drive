from init import driveinit
from colors import red, green, blue, bold
from repl_state import REPLState
from commands import parse_command
"""
Firing up the Drive Terminal
"""
def repl():
    state = REPLState()
    print((bold("Google Drive Terminal v0.0.1")))
    driveapi = driveinit()
    identifier = bold(green('drive:'))
    while True:
        try:
            print("{}{}$ ".format(identifier, bold(blue(state.get_pwd()))), end="")
            command = input().strip()
            parse_command(command, state, driveapi)
        except Exception as e:
            raise e

if __name__ == '__main__':
    repl()
