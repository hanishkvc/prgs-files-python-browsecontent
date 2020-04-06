#!/usr/bin/env python3
# v20200406IST0918, HanishKVC


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys


class UdemyKUI(Gtk.Application):
	APPNAME = "UdemyKUI"
	DEFAULT_WIDTH = 640
	DEFAULT_HEIGHT = 480
	wMain = None

	def __init__(self):
		Gtk.Application.__init__(self, application_id="hanishkvc.edu.udemykui")


	def do_activate(self):
		wMain = Gtk.Window(application=self)
		wMain.set_title(self.APPNAME)
		wMain.set_default_size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
		wMain.set_position(Gtk.WindowPosition.CENTER)
		wMain.show_all()
		self.wMain = wMain


if __name__ == '__main__':
	app = UdemyKUI()
	app.run(sys.argv)
