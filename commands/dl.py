import copy
import io
from googleapiclient.http import MediaIoBaseDownload
from commands.exceptions import DownloadError


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
