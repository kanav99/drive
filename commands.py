import shlex
import copy
from exceptions import InvalidCommand, CDError
from colors import blue, bold

def drive_cd(argv, state, driveapi):

	if len(argv) != 2:
		raise CDError("cd: too many arguments")

	target_directory = argv[1]

	absolute_mode = (target_directory[0] == "/")

	if absolute_mode:
		parent = "root"
		folders = target_directory[1:].split("/")
	else:
		parent = state.top()["id"]
		folders = target_directory.split("/")

	temp_state = copy.deepcopy(state)

	for folder in folders:
		if folder == "" or folder == ".":
			continue

		if folder == "..":
			temp_state.pop()
			parent = temp_state.top()["id"]
			continue

		query = "name = '{}' and '{}' in parents and mimeType = 'application/vnd.google-apps.folder'".format(folder,parent)
		results = driveapi.files().list(q = query, pageSize = 1000, fields = "files(id)").execute()
		items = results.get('files', [])
		if not items:
			raise CDError("cd: no such file or directory")
		else:
			parent = items[0]['id']
			temp_state.push({"id": items[0]['id'], "name": folder})

	state.copy(temp_state)

def drive_ls(argv, state, driveapi):
	if len(argv) == 1:
		parent = state.top()["id"]
		query = "'{}' in parents".format(parent)
		results = driveapi.files().list(q = query, pageSize = 1000, fields = "files(name, mimeType)").execute()
		items = results.get('files', [])
		for item in items:
			if item['mimeType'] == 'application/vnd.google-apps.folder':
				print('{}'.format(blue(bold(item['name']))))
			else:
				print('{}'.format(item['name']))
	elif len(argv) == 2:
		temp_state = copy.deepcopy(state)
		drive_cd(["cd", argv[1]], temp_state, driveapi)
		drive_ls(["ls"], temp_state, driveapi)
	else:
		raise LSError("ls: too many arguments")

def parse_command(command, state, driveapi):
	argv = shlex.split(command)

	if len(argv) == 0:
		return

	if argv[0] == "cd":
		drive_cd(argv, state, driveapi)
	elif argv[0] == "ls":
		drive_ls(argv, state, driveapi)
	else:
		raise InvalidCommand("Not a valid command")
