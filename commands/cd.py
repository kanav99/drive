import copy
from commands.exceptions import CDError


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
