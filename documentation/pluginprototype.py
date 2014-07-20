class PlugInTemplate:
	def __init__(self, app):
		self.app = app
		self.runlevel = 0 # runlevels are used to organize which plugins whould run first
		self.autorun = True # should it always run?
		self.dependencies = [] # what other plugins should it kick-off if it happens to run earlier
		self.has_run = False # has it run already?
		self.blob = b'' # a pointer to a binary string representing the file

	def set_blob(self, blob):
		self.blob = blob

	def load(self, pkl):
		pass

	def save(self):
		pass

	def get_data(self):
		pass

	def build_ui(self):
		pass

	def run(self):
		self.has_run = True #I should be the last bit of code in your plugin
		pass
