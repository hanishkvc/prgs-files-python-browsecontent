#!/usr/bin/env python3
# v20200406IST0918, HanishKVC


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys


APPNAME = "UdemyKUI"
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


class MainWin(Gtk.ApplicationWindow):

	def __init__(self, app):
		Gtk.Window.__init__(self, title=APPNAME, application=app)
		self.set_default_size(DEFAULT_WIDTH, DEFAULT_HEIGHT)
		self.set_position(Gtk.WindowPosition.CENTER)


class UdemyKUI(Gtk.Application):
	wMain = None

	def __init__(self):
		Gtk.Application.__init__(self, application_id="hanishkvc.edu.udemykui")

	def do_activate(self):
		self.wMain = MainWin(self)
		self.wMain.show_all()


if __name__ == '__main__':
	app = UdemyKUI()
	exitStatus = app.run(sys.argv)
	sys.exit(exitStatus)

