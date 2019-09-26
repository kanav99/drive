import copy

class REPLState:
	"""docstring for ClassName"""
	def __init__(self):
		self.stack = []

	def get_pwd(self):
		path = "/"
		for folder in self.stack:
			path = path + folder["name"] + "/"
		return path

	def pop(self):
		return self.stack.pop()

	def push(self, path):
		self.stack.append(path)

	def clear(self):
		self.stack.clear()

	def top(self):
		if len(self.stack) == 0:
			return {"name": "", "id": "root"}
		return self.stack[len(self.stack) - 1]

	def copy(self, state):
		self.stack = copy.deepcopy(state.stack)
