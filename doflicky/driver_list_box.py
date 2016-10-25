from gi.repository import Gtk, GObject

from .service import Pkg


class DriverListBox(Gtk.ListBox):

    __gsignals__ = {
        "driver-selected": (GObject.SIGNAL_RUN_FIRST, None, (Pkg,))
    }

    def __init__(self):
        Gtk.ListBox.__init__(self)

        rs = Gtk.Label("<b>Searching for available drivers</b>")
        rs.show_all()
        rs.set_use_markup(True)

        self.set_placeholder(rs)

        self.connect("row-selected", self.on_row_selected)

    def add_pkgs(self, pkgs):
        for child in self.get_children():
            child.destroy()

        self.pkgs = pkgs
        for pkg in self.pkgs:
            self._add_row(pkg)

    def _add_row(self, pkg):
        icon_name = "video-display"
        icon_img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        icon_img.set_margin_start(12)

        row_box = Gtk.HBox(0)
        row_box.pack_start(icon_img, False, False, 0)

        suffix = " [installed]" if pkg.installed else ""

        lab_text = "<big>{}</big> - <small>{}{}</small>".format(
                pkg.summary, pkg.version, suffix)

        lab = Gtk.Label(lab_text)
        lab.set_margin_start(12)
        lab.set_use_markup(True)
        row_box.pack_start(lab, False, True, 0)

        row_box.show_all()
        self.add(row_box)

    def on_row_selected(self, _, row):
        pkg = None
        if row is not None:
            pkg = self.pkgs[row.get_index()]
        self.emit("driver-selected", pkg)
