from ODA.documentation.pluginprototype import PlugInTemplate

class PlugIn(PlugInTemplate):

	def __init__(self, app):
		super().__init__(app)
		self.autorun = False

	def run(self):
		print("Trying to run the queue")
		try:
			for key, val in self.app.core.plugin_manager.plugins['conditional_plugin_registry'].fileid_event_queue:
				#this is a nasty hack until I implement a full list for selection
				if key in self.app.core.plugin_manager.plugins['fileid'].info['type'][0]:
					val()
		except:
			pass