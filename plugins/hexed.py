from ODA.documentation.pluginprototype import PlugInTemplate
from ODA.ui.pygiHexed.Hexed import HexedWidget

class PlugIn(PlugInTemplate):
	def __init__(self, app):
		super().__init__(app)
		self.box = 'hexedit_tab_box'

	def run(self):
		pass