from init import driveinit
from colors import red, green, blue, bold
from repl_state import REPLState
from commands import parse_command

DEVELOPMENT_MODE = False

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
            command = input()
            parse_command(command, state, driveapi)
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            exit()
        except Exception as e:
            if DEVELOPMENT_MODE:
                raise e
            else:
                print(e)

if __name__ == '__main__':
    repl()
