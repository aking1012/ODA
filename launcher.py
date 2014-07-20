from ODA.ui.pygiInterface import ODAPygi
from ODA.core.core import Core
import signal

class Application(object):
	'''
	Need to add set_status and log methods in here.
	GUI:
	set_status updates the status_bar
	log updates the python console

	CLI:
	both print

	BATCH:
	both write to the log file

    the file-id plugin
    the pyelftools plugin working for
      noting elf sections
      strings
    Parse the source of libmagic to get a list of all register-able file-types + 1 (raw binary/not found).
    Get these pieces to auto-run on a given blob that fits the profile.
	'''

	def __init__(self, mode):
		self.mode = mode
	def run(self):
		if self.mode == 'GUI':
			app.ui.run()
		elif self.mode == 'CLI':
			pass
		else:
			pass

signal.signal(signal.SIGINT, signal.SIG_DFL)

global app

#A blanket to throw all the parts inside
app = Application('GUI')
app.ui = ODAPygi(app)
app.core = Core(app)

app.run()
