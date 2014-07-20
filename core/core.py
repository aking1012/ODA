'''
So far, this contains:
DataStore, which will just hold all plugin data.
PluginManager, which will - you guessed it - manage plugins.
Core is just a wrapper, so I can instantiate Core() and slap it in to app.
'''

from collections import OrderedDict
import os
from ODA import plugins

class DataStore:
	'''
	Nothing to see here, move along...
	'''
	def __init__(self):
		self.filename = ''
		self.blob = ''
	def save(self):
		'''
		Save a pkl of self
		'''
		pass
	def load(self):
		'''
		Load a pkl of self
		'''
		pass


class PluginManager:
	def __init__(self, app):
		self.plugins = {}
		self.app = app
	def init_plugins(self):
		#I really should make a dynamic import "module", so next time I want
		#to do this I don't have to look for it or muck about with it again.
		from pkgutil import iter_modules
		for item in iter_modules(plugins.__path__):
			#I know there aren't any more folders under this one, so the recursion
			#isn't a problem.  A check would be fluff.
			PlugIn = __import__('ODA.plugins.' + item[1], globals(), locals(), ['PlugIn'], 0)
			self.plugins[item[1]] = PlugIn.PlugIn(self.app)
		#Sort plug-ins by runlevel - added bonus, I can force a depending plugin
		#to run first to test the dependency kick-off
		#tested - the sort works
		self.plugins = OrderedDict(sorted(self.plugins.items(), key=lambda t: t[1].runlevel))
	def set_blob(self, blob):
		for key, plugin in self.plugins.items():
			plugin.set_blob(blob)
	def run_plugin(self, plugin):
		'''
		I don't check for circular dependencies.  Don't be an idiot.
		'''
		for dependency in self.plugins[plugin].dependencies:
			if not dependency.has_run:
				try:
					self.run_plugin(dependency)
				except:
					#TODO catch keyerror and alert user that they're missing a plugin
					#this plugin is dependent upon and print a stacktrace
					pass
		self.plugins[plugin].run()
	def run_plugins(self):
		for key, plugin in self.plugins.items():
			if plugin.autorun:
				self.run_plugin(key)
				plugin.has_run = True
	def build_uis(self):
		for plugin in self.plugins.items():
			plugin.build_ui()
	def reset_has_run(self):
		for key, plugin in self.plugins.items():
			plugin.has_run = False

class Core:
	def __init__(self, app):
		self.datastore = DataStore()
		self.plugin_manager = PluginManager(app)
		self.plugin_manager.init_plugins()
	def load_file(self, uri):
		self.datastore.filename = uri
		with open(uri, 'rb') as reader:
			blob = reader.read()
			self.datastore.blob = blob
			self.plugin_manager.set_blob(blob)
		self.plugin_manager.run_plugins()
		self.plugin_manager.run_plugin('conditional_plugin_registry_parse')