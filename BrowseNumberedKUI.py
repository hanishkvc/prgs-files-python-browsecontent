#!/usr/bin/env python3
# v20200406IST0918, HanishKVC


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
import os


APPNAME = "BrowseNumberedKUI"
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
		# Add the listbox in a scrolled window
		self.swMain = Gtk.ScrolledWindow()
		self.swMain.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.swMain.set_min_content_height(DEFAULT_HEIGHT*0.9)
		self.swMain.set_max_content_height(DEFAULT_HEIGHT*0.9)
		self.lbMain = Gtk.ListBox()
		#self.swMain.add_with_viewport(self.lbMain)
		self.swMain.add(self.lbMain)
		self.gridMain.attach(self.swMain,1,1,9,9)
		self.update_lb()
		self.lbMain.connect("row-activated", self.on_lb_row_activated)
		# Add the buttons
		self.btnUp = Gtk.Button(label="Up")
		self.btnUp.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnUp,1,10,1,1)
		self.btnPrev = Gtk.Button(label="Prev")
		self.btnPrev.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnPrev,7,10,1,1)
		self.btnPlay = Gtk.Button(label="Play")
		self.btnPlay.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnPlay,8,10,1,1)
		self.btnNext = Gtk.Button(label="Next")
		self.btnNext.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnNext,9,10,1,1)

	def lb_select(self, theLB, mode="next"):
		rowSel = theLB.get_selected_row()
		rowPrev = None
		rowNext = None
		rowFirst = None
		bFound = False
		for row in theLB:
			if rowFirst == None:
				rowFirst = row
			if row == rowSel:
				bFound = True
			else:
				if bFound:
					rowNext = row
					break
			if not bFound:
				rowPrev = row
		if rowNext == None:
			rowNext = rowFirst
		if rowPrev == None:
			rowPrev = rowFirst
		if mode=="next":
			theLB.select_row(rowNext)
			theLB.set_focus_child(rowNext)
			rowNext.get_child().grab_focus()
		if mode=="prev":
			theLB.select_row(rowPrev)
			theLB.set_focus_child(rowPrev)
			rowPrev.get_child().grab_focus()

	def lb_play(self, theLB):
		rowSel = theLB.get_selected_row()
		sContent = rowSel.get_child().get_text()
		[sType, sPath] = sContent.split(':',1)
		print(sType, sPath)
		if sType == "dir":
			self.curPath = os.path.join(self.curPath, sPath)
			self.update_lb()
			self.show_all()

	def lb_up(self, theLB):
		newPath = self.curPath.rsplit('/',1)[0]
		if newPath != self.curPath:
			self.curPath = newPath
			self.update_lb()
			self.show_all()
		else:
			print("INFO:lb_up: Already reached top")

	def on_btn_clicked(self, button):
		if button == self.btnUp:
			print("INFO:btn_clicked: Up")
			self.lb_up(self.lbMain)
		elif button == self.btnPrev:
			print("INFO:btn_clicked: Prev")
			self.lb_select(self.lbMain, mode="prev")
		elif button == self.btnPlay:
			print("INFO:btn_clicked: Play")
			self.lb_play(self.lbMain)
		elif button == self.btnNext:
			print("INFO:btn_clicked: Next")
			self.lb_select(self.lbMain, mode="next")

	def on_lb_row_activated(self, listbox, listboxrow):
		i = listboxrow.get_index()
		numDirs = len(self.curDirList)
		numFiles = len(self.curFileList)
		if i >= numDirs:
			print("File: {}".format(self.curFileList[i-numDirs]))
		else:
			print("Dir: {}".format(self.curDirList[i]))

	def clear_lb(self):
		for i in self.lbMain:
			self.lbMain.remove(i)

	def update_lb(self, path=None, mode="all"):
		self.clear_lb()
		if path == None:
			path = self.curPath
		# Get list of current path contents
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
		# Remove unwanted files and sort
		newFileList = filter(lambda x: False if x.endswith('srt') else True, self.curFileList)
		self.curFileList = list(newFileList)
		self.curFileList.sort()
		# Add things to listbox
		for cur in self.curDirList:
			lbl = Gtk.Label(label="dir:%s"%(cur))
			lbl.set_halign(Gtk.Align.START)
			self.lbMain.add(lbl)
		for cur in self.curFileList:
			lbl = Gtk.Label(label="file:%s"%(cur))
			lbl.set_halign(Gtk.Align.START)
			self.lbMain.add(lbl)


class BrowseNumberedKUI(Gtk.Application):
	wMain = None

	def __init__(self, basePath="."):
		Gtk.Application.__init__(self, application_id="hanishkvc.browse.numbered.kui")
		self.basePath = basePath

	def do_activate(self):
		self.wMain = MainWin(self, self.basePath)
		self.wMain.show_all()


if __name__ == '__main__':
	app = BrowseNumberedKUI(sys.argv[1])
	exitStatus = app.run(sys.argv[2:])
	sys.exit(exitStatus)

