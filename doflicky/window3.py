from threading import Thread

from gi.repository import GObject
from .service import PackageService
from .window2 import DoFlickyWindow


class DoFlickyAppController(object):

    def __init__(self):
        window = DoFlickyWindow()
        self._window = window

        window.listbox.connect("driver-selected", self._on_driver_selected)
        window.toolbar.connect("remove-clicked", self._on_remove_clicked)
        window.toolbar.connect("install-clicked", self._on_install_clicked)

        self.selection = None

    @property
    def window(self):
        return self._window

    def refresh(self):
        t = Thread(target=self._do_refresh)
        t.start()

    def _do_refresh(self):
        pkgs = PackageService.get_hardware_packages()
        GObject.idle_add(lambda: self.window.listbox.add_pkgs(pkgs))

    def _on_driver_selected(self, _, pkg):
        self.selection = pkg

    def _on_remove_clicked(self, _):
        print "remove", self.selection.pkg_name

    def _on_install_clicked(self, _):
        print "install", self.selection.pkg_name
