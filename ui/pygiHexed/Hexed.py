#!/usr/bin/python3

from gi.repository import Gtk, Gdk, Pango
from math import ceil

class FFTextWidget(Gtk.TextView):
    '''
    A base widget to derive from reducing LoC
    '''
    def __init__(self):
        '''
        Nothing much here... move along.
        '''
        super().__init__()
        self.set_font()
        self.set_editable(False)
        self.set_hexpand(False)

    def get_char_size_px(self, descr):
        '''
        Little routine to get the size of a single character fairly accurately
        '''
        label = Gtk.Label()
        label.set_text('A')
        pango_layout = label.get_layout()
        pango_layout.set_font_description(descr)
        return pango_layout.get_pixel_size()

    def set_font(self, font='DejaVu Sans Mono', size=12):
        '''
        Set a monospaced font for the widget along with
        setting some extra class attributes
        '''
        self.font = font
        self.font_size = size
        descr = Pango.font_description_from_string(self.font + ' ' + str(self.font_size))
        self.override_font(descr)
        xlen_text, ylen_text = self.get_char_size_px(descr)
        self.font_width = xlen_text
        self.font_height = ylen_text
        self.width_chars = 0
        self.height_chars = 0

    def set_width_in_chars(self):
        '''
        Adjust widget width.
        We have to insert newlines, because Gtk.CHAR wrap
        doesn't work for lots of characters.  I think that's a bug.
        There should probably be a "Gtk.EVERYCHARIMEANIT" or something.
        '''
        self.set_size_request(self.font_width*(self.width_chars+2), self.font_height*self.height_chars)

class OffsetWidget(FFTextWidget):
    '''
    A widget to show the offsets
    '''
    def __init__(self, width_chars=8):
        '''
        Nothing much here... move along.
        '''
        super().__init__()
        self.width_chars = width_chars
        self.rebase_to = 0

    def set_blob(self, blob):
        '''
        Just find the length, divide by your hex blob width,
        and do your thing man.
        '''
        self.length = len(blob)
        self.str_buf = ''
        i=self.rebase_to
        while i < self.length+self.rebase_to:
            self.str_buf += '\n ' + hex(i).lstrip('0x').zfill(8)
            i+=16
        self.str_buf = self.str_buf.lstrip('\n')
        self.height_chars = ceil(self.length/16)
        self.textbuffer = self.get_buffer()
        self.textbuffer.set_text(self.str_buf)
        self.set_width_in_chars()

    def rebase(self, rebase_to=0):
        self.rebase_to = rebase_to
        self.set_blob(self.get_parent().get_parent().get_parent().blob)
        self.show_all()

class HexViewWidget(FFTextWidget):
    '''
    A widget to represent the hex view
    '''
    def __init__(self, width_chars=49):
        '''
        Nothing much here... move along.
        calculating width from pango leaves you half a character short btw...
        '''
        super().__init__()
        self.width_chars = width_chars
        self.set_wrap_mode(Gtk.WrapMode.CHAR)

    def set_blob(self, blob):
        '''
        convert to hex text values
        '''
        self.str_buf = ''
        i=0
        for byte in blob:
            if i==0:
                self.str_buf += ' '
            elif (i % 16) == 0:
                self.str_buf += '\n '
            elif (i % 8) == 0:
                self.str_buf += '  '
            else:
                self.str_buf += ' '
            self.str_buf += hex(byte).lstrip('0x').zfill(2)
            i+=1

        self.height_chars = ceil(len(blob)/32)
        self.textbuffer = self.get_buffer()
        self.textbuffer.set_text(self.str_buf)
        self.set_width_in_chars()

    def toggle_edit_mode(self, widget):
        '''
        Turn on keypress listeners.  We won't be using conventional editing,
        because we want to maintain screen formatting and only allow specific
        characters.
        '''
        pass

    def highlighting(self, arg):
        pass
    
class TextViewWidget(FFTextWidget):
    '''
    A widget to represent most characters in ASCII
    '''
    def __init__(self, width_chars=16):
        '''
        Nothing much here... move along.
        '''
        super().__init__()
        self.width_chars = width_chars

    def set_blob(self, blob):
        '''
        <32 becomes . (no line breaks)
        '''
        self.str_buf = ''
        for byte in blob:
            if byte < 32:
                self.str_buf += '.'
            elif byte >= 127 and byte <= 159:
                self.str_buf += '.'
            else:
                self.str_buf += chr(byte)
        self.str_buf = ' ' + '\n '.join([self.str_buf[i:i+16] for i in range(0, len(self.str_buf), 16)])

        self.height_chars = ceil(len(self.str_buf)/16)
        self.textbuffer = self.get_buffer()
        self.textbuffer.set_text(self.str_buf)
        self.set_width_in_chars()

class HexedSeparator(Gtk.Separator):
    '''
    If I have to set params more than once, it needs to be a function
    or a class.
    '''
    def __init__(self):
        super().__init__()
        self.set_margin_left(5)
        self.set_margin_right(5)

class HexedWidget(Gtk.ScrolledWindow):
    '''
    Editing not yet implemented, so the name is a little deceptive.
    I plan on implementing that, but it's just part of a larger project,
    where I don't really need editing yet.

    #TODO flesh in editing, synchronization across widgets for colorizing
    analyzed and unanalyzed blob areas, add menu to the standalone example,
    anything else?
    '''
    def __init__(self):
        super().__init__()

        #Should probably move the scolled widget in to the Hexedit widget.
        self.main_box = Gtk.HBox()
        self.add(self.main_box)

        self.offset_view_widget = OffsetWidget()
        self.hex_view_widget = HexViewWidget()
        self.text_view_widget = TextViewWidget()
        '''
        Seems silly to do this, but I had to iterate over them more than once.
        Sure I will again as I add features.
        '''
        self.views = [ self.offset_view_widget, self.hex_view_widget, self.text_view_widget ]
        #add iterator for separators?
        i=0
        for view in self.views:
            self.main_box.pack_start(view, False, False, 0)
            if i < 2:
                self.main_box.pack_start(HexedSeparator(), False, False, 0)
            i+=1
        self.main_box.pack_start(Gtk.TextView(), True, True, 0)
        self.set_size_request(self.offset_view_widget.font_width*(10+18+51)+22+15, 500)

    def set_blob(self, blob):
        '''
        Set the binary blob for all the panes.
        '''
        self.blob = blob
        for view in self.views:
            view.set_blob(self.blob)

    def rebase(self, rebase_to=0):
        self.offset_view_widget.rebase(rebase_to)

class HexeditWindow(Gtk.Window):
    '''
    Simplistic demo of using the hexedit widget
    '''
    def __init__(self):
        super().__init__()
        self.set_title("Hexedit Widget Demo")
        #Just generating an example blob
        blob = bytearray()
        #I know, I don't use for loops even when I should...
        j=0
        while j < 5:
            i=0
            while i <= 255:
                blob.append(i)
                i+=1
            j+=1

        main_vbox = Gtk.VBox(homogeneous=False, spacing=0)
        self.add(main_vbox)

        '''
        This is where we use the widget:
        Just instantiate it, add it, and set the hex blob.
        That's it.

        If you want to rebase to a starting memory address,
        just call the instance.rebase method with an int.
        '''
        self.hexed_widget = HexedWidget()
        main_vbox.add(self.hexed_widget)


        self.hexed_widget.set_blob(bytes(blob))

        self.show_all()
        self.hexed_widget.rebase(16)
        self.connect('destroy', lambda w: Gtk.main_quit())

if __name__ == "__main__":
    main_win = HexeditWindow()
    Gtk.main()
