
import dbus.mainloop.glib

from gi.repository import Gtk

from doflicky.ui import OpPage, CompletionPage
from .driver_list_box import DriverListBox
from .toolbar import Toolbar


APP_NAME = "DoFlicky"
APP_SUBTITLE = "Solus Driver Management"
APP_ICON_NAME = "jockey"


class DoFlickyWindow(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self)

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.set_title(APP_NAME)
        self.set_size_request(400, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.set_icon_name(APP_ICON_NAME)

        hbar = Gtk.HeaderBar()
        hbar.set_title(APP_NAME)
        hbar.set_subtitle(APP_SUBTITLE)
        hbar.set_show_close_button(True)
        self.set_titlebar(hbar)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        mlayout = Gtk.VBox(0)
        self.stack.add_named(mlayout, "main")
        self.add(self.stack)
        self.layout = mlayout

        layout = Gtk.HBox(0)
        layout.set_border_width(20)
        mlayout.pack_start(layout, True, True, 0)

        app_icon_img = Gtk.Image.new_from_icon_name(APP_ICON_NAME,
                                                    Gtk.IconSize.INVALID)
        app_icon_img.set_pixel_size(64)
        layout.pack_start(app_icon_img, False, False, 0)

        text = """
In some cases you may gain improved performance or
features from the manufacturer's proprietary drivers.
Note that the Solus Project developers cannot audit this
closed source code."""

        lab = Gtk.Label(text)
        lab.set_margin_start(20)
        layout.pack_start(lab, True, True, 5)

        # Allow installing 32-bit drivers..
        lb = "Also install 32-bit driver (Required for Steam & Wine)"
        self.check_vga_emul32 = Gtk.CheckButton.new_with_label(lb)
        self.check_vga_emul32.set_halign(Gtk.Align.START)
        mlayout.pack_start(self.check_vga_emul32, False, False, 0)
        self.check_vga_emul32.set_no_show_all(True)
        self.check_vga_emul32.set_property("margin-top", 3)
        self.check_vga_emul32.set_property("margin-bottom", 3)
        self.check_vga_emul32.set_property("margin-start", 12)

        toolbar = Toolbar()
        self.toolbar = toolbar
        mlayout.pack_end(toolbar, False, False, 0)

        listbox = DriverListBox()
        listbox.connect("driver-selected", self._on_driver_selected)

        self.listbox = listbox
        scl = Gtk.ScrolledWindow(None, None)
        scl.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scl.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scl.add(listbox)

        mlayout.pack_end(scl, True, True, 0)

        # update page..
        page = OpPage()
        self.op_page = page
        self.op_page.connect('complete', self._finished_handler)
        self.op_page.connect('cancelled', self._cancelled_handler)
        self.stack.add_named(page, "operations")
        self.show_all()

        self.cpage = CompletionPage()
        self.stack.add_named(self.cpage, "complete")

    def refresh(self):
        raise "Not Implemented"

    def _finished_handler(self, *args, **kwargs):
        """ TODO: remove me"""
        pass

    def _cancelled_handler(self, *args, **kwargs):
        """ TODO: remove me"""
        pass

    def _on_driver_selected(self, _, pkg):
        if not pkg:
            self.toolbar.btn_remove.set_sensitive(False)
            self.toolbar.btn_install.set_sensitive(False)
            self.check_vga_emul32.hide()
            return

        if pkg.has_32bit:
            self.check_vga_emul32.show()
        else:
            self.check_vga_emul32.hide()

        self.toolbar.btn_remove.set_sensitive(pkg.installed)
        self.toolbar.btn_install.set_sensitive(not pkg.installed)
