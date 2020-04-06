#!/usr/bin/env python3
# v20200406IST0918, HanishKVC


from gi.repository import Gtk
import sys


class UdemyKUI(Gtk.Application):
	APPNAME = "UdemyKUI"

	def __init__(self):
		Gtk.Application.__init__(self, application_id="hanishkvc.edu.udemykui")


	def do_activate(self):
		wMain = Gtk.Window(application=self)
		wMain.set_title(APPNAME)
		wMain.show_all()

if __name__ == '__main__':
	app = UdemyKUI()
	app.run(sys.argv)
