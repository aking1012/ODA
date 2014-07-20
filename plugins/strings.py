from ODA.documentation.pluginprototype import PlugInTemplate
import re

class PlugIn(PlugInTemplate):
	def __init__(self, app):
		super().__init__(app)
		self.box = 'strings_tab_box'
		self.runlevel = 1
	
	def set_blob(self, blob):
		self.blob = str(blob).lstrip("b'").rstrip("'")
	def run(self):
		temp = re.findall("[^\x00-\x1F\x7F-\xFF]{4,}", self.blob)
		return False