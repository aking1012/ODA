from ODA.documentation.pluginprototype import PlugInTemplate

class PlugIn(PlugInTemplate):
	def __init__(self, app):
		super().__init__(app)
		self.fileid_event_queue = []
	def register(self, match, callback):
		self.fileid_event_queue.append([match, callback])