import shlex
import copy
from exceptions import InvalidCommand, CDError, DownloadError, LSError
from colors import blue, bold
import io
from googleapiclient.http import MediaIoBaseDownload


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
		try:
			drive_cd(["cd", argv[1]], temp_state, driveapi)
		except Exception as e:
			raise LSError("ls: invalid directory path")
		drive_ls(["ls"], temp_state, driveapi)
	else:
		raise LSError("ls: too many arguments")

def drive_dl_internal(filename, state, driveapi):
	query = "name = '{}' and '{}' in parents".format(filename, state.top()['id'])
	files = driveapi.files().list(q = query, fields = "files(id)").execute().get('files', [])
	if len(files) > 1:
		raise DownloadError("dl: multiple files found")
	elif len(files) == 0:
		raise DownloadError("dl: file not found")
	else:
		file_id = files[0]['id']
		request = driveapi.files().get_media(fileId=file_id)
		fh = io.FileIO(filename, "wb")
		downloader = MediaIoBaseDownload(fh, request)
		done = False
		while done is False:
			status, done = downloader.next_chunk()
			print("Download {}%.".format(int(status.progress() * 100)))


def drive_dl(argv, state, driveapi):
	if len(argv) == 1:
		raise DownloadError("{}: please specify the file(s)".format(argv[0]))
	if len(argv) > 2:
		raise DownloadError("{}: too many arguments".format(argv[0]))

	try:
		index = argv[1].index('/')
		temp_state = copy.deepcopy(state)
		drive_cd(["cd", argv[1][:index]], temp_state, driveapi)
		filename = argv[1][index+1:]
		drive_dl_internal(filename, temp_state, driveapi)
	except ValueError as e:
		filename = argv[1]
		drive_dl_internal(filename, state, driveapi)
	except CDError as e:
		raise DownloadError("{}: invalid directory".format(argv[0]))



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
