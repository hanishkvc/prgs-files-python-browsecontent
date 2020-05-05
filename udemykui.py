#!/usr/bin/env python3
# v20200406IST0918, HanishKVC


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
import os


APPNAME = "UdemyKUI"
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


class MainWin(Gtk.ApplicationWindow):

	def __init__(self, app, basePath):
		Gtk.Window.__init__(self, title=APPNAME, application=app)
		self.set_default_size(DEFAULT_WIDTH, DEFAULT_HEIGHT)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.basePath = basePath
		self.curPath = basePath
		self.build_ui()

	def build_ui(self):
		self.lbMain = Gtk.ListBox()
		self.add(self.lbMain)
		self.update_lb()
		self.lbMain.connect("row-activated", self.on_lb_row_activated)

	def on_lb_row_activated(self, listbox, listboxrow):
		print("listbox: {};\n\t listboxrow: {}".format(listbox, listboxrow))

	def update_lb(self, path=None, mode="all"):
		if path == None:
			path = self.curPath
		dirContents = os.listdir(path)
		self.curDirList = []
		self.curFileList = []
		for cur in dirContents:
			curPath = os.path.join(path, cur)
			if os.path.isdir(curPath):
				self.curDirList.append(cur)
			elif os.path.isfile(curPath):
				self.curFileList.append(cur)
			else:
				continue
		for cur in self.curDirList:
			lbl = Gtk.Label("dir:%s"%(cur))
			self.lbMain.add(lbl)
		for cur in self.curFileList:
			lbl = Gtk.Label("file:%s"%(cur))
			self.lbMain.add(lbl)


class UdemyKUI(Gtk.Application):
	wMain = None

	def __init__(self, basePath="."):
		Gtk.Application.__init__(self, application_id="hanishkvc.edu.udemykui")
		self.basePath = basePath

	def do_activate(self):
		self.wMain = MainWin(self, self.basePath)
		self.wMain.show_all()


if __name__ == '__main__':
	app = UdemyKUI(sys.argv[1])
	exitStatus = app.run(sys.argv[2:])
	sys.exit(exitStatus)

