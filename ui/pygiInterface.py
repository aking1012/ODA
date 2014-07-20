from ODA.ui.gtkpyinterpreter.gtkpyinterpreter import GtkPyInterpreterWidget
from gi.repository import Gtk
import signal, os

'''
there's a statement here...
'''
wave   = '浪'
people = '人'

class GtkODAShellWidget(GtkPyInterpreterWidget):
    banner = 'ODA Interactive Python3 shell.\n' + \
             'The app can be accessed via the app local.'

    def __init__(self, interpreter_locals={}, history_fn=None, app=None):
        this_locals = {}
        this_locals['app'] = (app)
        this_locals.update(interpreter_locals)
        super().__init__(this_locals, history_fn)
        self.show_all()

class ODAPygi(object):
    '''
    The root of the application interface...
    I live at app.ui in the relevant namespaces
    '''
    def __init__(self, app):
        self.app = app
        self.ui_callbacks = UICallbacks(app)
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "interface.ui"))
        #Add the AnalysisNameStore to the dropdown
        self.builder.connect_signals(self.ui_callbacks)

    def run(self, *args):
        main_win = self.builder.get_object("main_win")
        main_win.connect("delete-event", self.ui_callbacks.preclose_hooks)
        main_win.set_title("Open Disassembler 0.01 pre-alpha")
        self.builder.get_object("console_box").pack_start(GtkODAShellWidget(app=self.app), True, True, 0)
        main_win.maximize()
        main_win.set_decorated(False)
        main_win.show()
        Gtk.main()

    def log(self, msg):
        self.builder.get_object("statusbar").set_status(msg)

class AnalysisNameStore(Gtk.ListStore):
    def __init__(self):
        super().__init__(int, str)
        self.append([1, "Entry Points"])
        self.append([2, "Binary Pattern"])
        self.append([3, "Text Pattern"])
        self.append([4, "Crossreferences To"])
        self.append([5, "Immediate Value"])
        self.append([6, "Void Operands"])
        self.append([7, "Marked Positions"])
        self.append([8, "Problems"])

class UICallbacks:
    '''
    Any callbacks you specify in the glade file should definitely live here...
    '''
    def __init__(self, app):
        self.app = app

    def on_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        row_id, name = model[tree_iter][:2]
        log("Selected: ID=%d, name=%s" % (row_id, name))

    def on_file_open(self, widget):
        def add_filters(dialog):
            '''
            TODO: add useful filters later...
            .so*
            .dll
            .exe
            etc etc etc

            filter_py = Gtk.FileFilter()
            filter_py.set_name("Python files")
            filter_py.add_mime_type("binary/x-python")
            dialog.add_filter(filter_py)
            '''

            filter_any = Gtk.FileFilter()
            filter_any.set_name("Any files")
            filter_any.add_pattern("*")
            dialog.add_filter(filter_any)
        dialog = Gtk.FileChooserDialog("Please choose a file", self.app.ui.builder.get_object("mainwin"),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.app.core.load_file(dialog.get_filename())
        dialog.destroy()

    def preclose_hooks(self, *args):
        self.on_quit()

    def on_quit(self, widget=False):
        Gtk.main_quit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.ui = ODAPygi(app)
    app.ui.run()