from gi.repository import Gtk, GObject


class Toolbar(Gtk.Toolbar):
    __gsignals__ = {
        'remove-clicked': (GObject.SIGNAL_RUN_FIRST, None, tuple()),
        'install-clicked': (GObject.SIGNAL_RUN_FIRST, None, tuple())
    }

    def __init__(self):
        Gtk.Toolbar.__init__(self)

        sep = Gtk.SeparatorToolItem()
        sep.set_expand(True)
        sep.set_draw(False)
        self.add(sep)

        btn = Gtk.ToolButton.new(None, "Remove")
        btn.connect('clicked', self._on_remove_clicked)
        self.btn_remove = btn
        btn.set_sensitive(False)
        btn.set_property("icon-name", "list-remove-symbolic")
        btn.set_is_important(True)
        self.add(btn)

        btn = Gtk.ToolButton.new(None, "Install")
        btn.connect('clicked', self._on_install_clicked)
        self.btn_install = btn
        btn.set_sensitive(False)
        btn.set_property("icon-name", "list-add-symbolic")
        btn.set_is_important(True)
        self.add(btn)

        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

    def _on_remove_clicked(self, *args, **kwargs):
        self.emit("remove-clicked")

    def _on_install_clicked(self, *args, **kwargs):
        self.emit("install-clicked")
