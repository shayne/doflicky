import pisi.api

from gi.repository import GObject
from pisi.db.installdb import InstallDB

from doflicky import detection


installdb = InstallDB()


class PackageService(object):
    @classmethod
    def get_hardware_packages(cls):
        return [Pkg.from_pkg_name(pkg)
                for pkg in detection.detect_hardware_packages()]


class Pkg(GObject.GObject):

    @classmethod
    def from_pkg_name(cls, pkg_name):
        meta, _ = pisi.api.info(pkg_name)
        return cls(pkg_name, meta)

    def __init__(self, pkg_name, pisi_meta):
        GObject.GObject.__init__(self)
        self.pkg_name = pkg_name
        self.pisi_meta = pisi_meta

    @property
    def summary(self):
        return self.pisi_meta.package.summary

    @property
    def version(self):
        return self.pisi_meta.package.version

    @property
    def icon_name(self):
        if self.pisi_meta.package.partOf != "xorg.driver":
            return "drive-removable-media"
        return "video-display"

    @property
    def installed(self):
        return installdb.has_package(self.pkg_name)

    @property
    def has_32bit(self):
        return self.pisi_meta.package.partOf == "xorg.driver"
