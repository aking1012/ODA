#/usr/bin/env python3
from ODA.documentation.pluginprototype import PlugInTemplate
import magic
from gi.repository import Gtk
#pip3 didn't work.  needed to git clone https://github.com/ahupp/python-magic

class FileIDGUI(Gtk.VBox):
    def __init__(self):
        super().__init__()
    def build(self):
        pass

class PlugIn(PlugInTemplate):
    def __init__(self, app):
        super().__init__(app)
        self.autorun = True
        self.box = 'fileid_tab_box'
        self.info = {}

    def run(self):
        val = magic.from_buffer(self.blob)
        self.info['type'] = (str(val).lstrip("b'").rstrip("'"), str(0))
        
