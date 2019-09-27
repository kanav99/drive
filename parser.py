import shlex
from commands.exceptions import InvalidCommand
from commands.cd import *
from commands.ls import *
from commands.dl import *

def parse_command(command, state, driveapi):
	argv = shlex.split(command)

	if len(argv) == 0:
		return

	if argv[0] == "cd":
		drive_cd(argv, state, driveapi)
	elif argv[0] == "ls":
		drive_ls(argv, state, driveapi)
	elif argv[0] == "download" or argv[0] == "dl":
		drive_dl(argv, state, driveapi)
	else:
		raise InvalidCommand("Not a valid command")
