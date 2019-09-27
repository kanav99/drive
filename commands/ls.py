import copy
from commands.exceptions import LSError
from commands.cd import drive_cd
from colors import bold, blue


def drive_ls(argv, state, driveapi):
	if len(argv) == 1:
		parent = state.top()["id"]
		query = "'{}' in parents".format(parent)
		results = driveapi.files().list(q = query, pageSize = 1000, fields = "files(name, mimeType)").execute()
		items = results.get('files', [])
		for item in items:
			if item['mimeType'] == 'application/vnd.google-apps.folder':
				# print('{}'.format(blue(bold(item['name']))))
				print(f'{blue(bold(item["name"]))}')
			else:
				# print('{}'.format(item['name']))
				print(f'{item["name"]}')
	elif len(argv) == 2:
		temp_state = copy.deepcopy(state)
		try:
			drive_cd(["cd", argv[1]], temp_state, driveapi)
		except Exception as e:
			raise LSError("ls: invalid directory path")
		drive_ls(["ls"], temp_state, driveapi)
	else:
		raise LSError("ls: too many arguments")
