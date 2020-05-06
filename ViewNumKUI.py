#!/usr/bin/env python3
# v20200406IST0918, HanishKVC


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
import os


APPNAME = "ViewNumKUI"
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
		self.gridMain = Gtk.Grid()
		self.add(self.gridMain)
		self.lbMain = Gtk.ListBox()
		self.gridMain.attach(self.lbMain,1,1,9,9)
		self.update_lb()
		self.lbMain.connect("row-activated", self.on_lb_row_activated)
		self.btnUp = Gtk.Button(label="Up")
		self.gridMain.attach(self.btnUp,1,10,1,1)

	def on_lb_row_activated(self, listbox, listboxrow):
		i = listboxrow.get_index()
		numDirs = len(self.curDirList)
		numFiles = len(self.curFileList)
		if i >= numDirs:
			print("File: {}".format(self.curFileList[i-numDirs]))
		else:
			print("Dir: {}".format(self.curDirList[i]))

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
			lbl = Gtk.Label(label="dir:%s"%(cur))
			lbl.set_halign(Gtk.Align.START)
			self.lbMain.add(lbl)
		for cur in self.curFileList:
			lbl = Gtk.Label(label="file:%s"%(cur))
			lbl.set_halign(Gtk.Align.START)
			self.lbMain.add(lbl)


class ViewNumKUI(Gtk.Application):
	wMain = None

	def __init__(self, basePath="."):
		Gtk.Application.__init__(self, application_id="hanishkvc.edu.viewnumkui")
		self.basePath = basePath

	def do_activate(self):
		self.wMain = MainWin(self, self.basePath)
		self.wMain.show_all()


if __name__ == '__main__':
	app = ViewNumKUI(sys.argv[1])
	exitStatus = app.run(sys.argv[2:])
	sys.exit(exitStatus)

