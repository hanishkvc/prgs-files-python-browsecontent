#!/usr/bin/env python3
# A simple browser of file contents in a given directory and its subdirs
# v20200509IST1317, HanishKVC


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
from gi.repository import EvinceDocument, EvinceView
import sys
import os
import time
import subprocess



APPNAME = "BrowseContentKUI"
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
bResizeBothWays = True
bBasePathInTitle = True
bPlayInternal = True
bPlayGeneric = True



GDEBUGLEVEL = 10
def dprint(sMsg, dbgLvl=GDEBUGLEVEL):
	if dbgLvl < GDEBUGLEVEL:
		print(sMsg)



class MainWin(Gtk.ApplicationWindow):

	def __init__(self, app, basePath=".", width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
		sTitlePlus = ""
		if bBasePathInTitle:
			sTitlePlus = self.__get_title(basePath)
		sTitle = "%s:%s"%(APPNAME, sTitlePlus)
		Gtk.Window.__init__(self, title=sTitle, application=app)
		if width == None:
			width = self.get_screen().width()
		self.scrWidth = width
		if height == None:
			height = self.get_screen().height()
		self.scrHeight = height
		self.set_default_size(self.scrWidth, self.scrHeight)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.basePath = os.path.abspath(basePath)
		self.curPath = self.basePath
		self.load_config()
		self.prevClickTime = 0
		self.rowActTime = -1
		self.connect("check-resize", self.on_check_resize)
		self.build_ui()
		self.resize_setup()

	def __get_title(self, basePath):
		sTitle = ""
		sPath = basePath
		iParts = 0
		while (len(sTitle) < 64) and (len(sPath) > 0) and (iParts < 16):
			iParts += 1
			sCur = os.path.basename(sPath)
			sPath = os.path.dirname(sPath)
			# if path ends with path separator, then basename of "" needs skipping
			# if path has only path separator, then path remains same, need exiting
			if sCur == "":
				if sPath == os.path.sep:
					break
				else:
					continue
			sTitle = "%s/%s"%(sCur,sTitle)
		return sTitle

	def resize_setup(self):
		(minHeight, self.btnHeight) = self.btnUp.get_preferred_height()
		if minHeight > self.btnHeight:
			self.btnHeight = minHeight
		if self.btnHeight < 42:
			self.btnHeight = 42
		self.do_resize()

	def do_resize(self):
		#heightRatio = 1-(64/self.scrHeight)
		heightRatio = 1-((self.btnHeight+8)/self.scrHeight)
		swLBWidth = self.scrWidth*0.29
		swLBHeight = self.scrHeight*heightRatio
		swWVWidth = self.scrWidth*0.69
		swWVHeight = swLBHeight
		if not bResizeBothWays:
			self.swLB.set_min_content_width(swLBWidth)
			self.swLB.set_min_content_height(swLBHeight)
			self.swLB.set_max_content_height(swLBHeight)
			self.swWV.set_min_content_width(swWVWidth)
		self.swLB.set_size_request(swLBWidth, swLBHeight)
		self.swWV.set_size_request(swWVWidth, swWVHeight)

	def on_check_resize(self, container):
		(newWidth, newHeight) = self.get_size()
		#if (newWidth < self.scrWidth+10) and (newHeight < self.scrHeight+10):
		if (newWidth == self.scrWidth) and (newHeight == self.scrHeight):
			return
		print("INFO:AppWin:CheckResize:{}".format(self.get_size()))
		self.scrWidth = newWidth
		self.scrHeight = newHeight
		self.do_resize()

	def build_ui(self):
		self.gridMain = Gtk.Grid()
		self.add(self.gridMain)
		# Add the listbox in a scrolled window
		self.swLB = Gtk.ScrolledWindow()
		self.swLB.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.lbMain = Gtk.ListBox()
		#self.swLB.add_with_viewport(self.lbMain)
		self.swLB.add(self.lbMain)
		self.gridMain.attach(self.swLB,1,1,4,9)
		self.update_lb()
		self.lbMain.connect("row-activated", self.on_lb_row_activated)
		self.lbMain.connect("button-release-event", self.on_lb_button_release)
		# Added a separator
		self.vSep = Gtk.VSeparator()
		self.gridMain.attach(self.vSep,5,2,1,7)
		# Add a WebView
		self.wvMain = WebKit2.WebView()
		self.wvMain.load_html("<html> <head><title> Browser </title></head> <body> <center> Satyameva Jayate </center> </body> </html>")
		self.swWV = Gtk.ScrolledWindow()
		self.swWV.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		self.swWV.add(self.wvMain)
		self.gridMain.attach(self.swWV,6,1,9,9)
		# Add EvinceView
		self.evMain = EvinceView.View()
		EvinceDocument.init()
		self.evDoc = None
		# Add the buttons
		self.btnBase = Gtk.Button(label="Base")
		self.btnBase.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnBase,1,10,1,1)
		self.btnLast = Gtk.Button(label="Last")
		self.btnLast.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnLast,2,10,1,1)
		self.btnUp = Gtk.Button(label="Up")
		self.btnUp.connect("clicked", self.on_btn_clicked)
		self.gridMain.attach(self.btnUp,6,10,1,1)
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
		sCurRow = None
		if mode=="next":
			theLB.select_row(rowNext)
			theLB.set_focus_child(rowNext)
			rowNext.get_child().grab_focus()
			sCurRow = "Next:%s"%(rowNext.get_child().get_text())
		if mode=="prev":
			theLB.select_row(rowPrev)
			theLB.set_focus_child(rowPrev)
			rowPrev.get_child().grab_focus()
			sCurRow = "Prev:%s"%(rowPrev.get_child().get_text())
		if sCurRow != None:
			print(sCurRow)

	def lb_select_fromtext(self, theLB, selText):
		for row in theLB:
			curText = row.get_child().get_text()
			curText = curText.replace("dir:","",1)
			dprint("DBUG:lb_sel_fromtext:%s,%s"%(curText, selText))
			if curText == selText:
				theLB.select_row(row)
				theLB.set_focus_child(row)
				row.get_child().grab_focus()
				break

	def play_internal(self, theFile):
		theFile = "file:///%s"%(os.path.abspath(theFile))
		if self.wvMain.get_parent() != None:
			# Force stopping of any previously played media
			self.wvMain.load_html("<html> <head><title> Browser </title></head> <body> <center> Satyameva Jayate </center> </body> </html>")
			self.swWV.remove(self.wvMain)
		if self.evMain.get_parent() != None:
			self.swWV.remove(self.evMain)
		if theFile.lower().endswith(".pdf"):
			self.evDoc = EvinceDocument.Document.factory_get_document(theFile)
			self.evModel = EvinceView.DocumentModel()
			self.evModel.set_document(self.evDoc)
			self.evMain.set_model(self.evModel)
			self.swWV.add(self.evMain)
		else:
			self.swWV.add(self.wvMain)
			self.wvMain.load_uri(theFile)

	def play_external(self, theFile):
		if bPlayGeneric:
			sCmd = [ "xdg-open", theFile ]
			subprocess.call(sCmd)
		elif theFile.lower().endswith(".pdf"):
			sCmd = [ "evince", theFile ]
			subprocess.call(sCmd)
		else:
			print("ERRR:play_ext:Dont know how to play [%s]"%(theFile))

	def play_file(self, theFile=None):
		if theFile == None:
			theFile = self.lastFile
		if bPlayInternal:
			self.play_internal(theFile)
		else:
			self.play_external(theFile)

	def lb_play(self, theLB, thePath=None):
		if thePath == None:
			rowSel = theLB.get_selected_row()
			sContent = rowSel.get_child().get_text()
		else:
			sContent = thePath
		[sType, sPath] = sContent.split(':',1)
		print(sType, sPath)
		thePath = os.path.join(self.curPath, sPath)
		if sType == "dir":
			self.curPath = thePath
			self.update_lb()
		elif sType == "file":
			self.lastFile = thePath
			self.play_file(self.lastFile)
		self.show_all()

	def lb_up(self, theLB):
		[newPath, thePrevSel] = self.curPath.rsplit('/',1)
		if newPath != self.curPath:
			self.curPath = newPath
			self.update_lb()
			self.lb_select_fromtext(self.lbMain, thePrevSel)
			self.show_all()
			print("Up:%s"%(self.curPath))
		else:
			print("INFO:lb_up: Already reached top")

	def on_btn_clicked(self, button):
		if button == self.btnBase:
			dprint("INFO:btn_clicked: Base")
			self.lb_play(self.lbMain, "dir:%s"%(self.basePath))
		elif button == self.btnLast:
			dprint("INFO:btn_clicked: Last")
			thePath = os.path.dirname(self.lastFile)
			self.lb_play(self.lbMain, "dir:%s"%(thePath))
		elif button == self.btnUp:
			dprint("INFO:btn_clicked: Up")
			self.lb_up(self.lbMain)
		elif button == self.btnPrev:
			dprint("INFO:btn_clicked: Prev")
			self.lb_select(self.lbMain, mode="prev")
		elif button == self.btnPlay:
			dprint("INFO:btn_clicked: Play")
			self.lb_play(self.lbMain)
		elif button == self.btnNext:
			dprint("INFO:btn_clicked: Next")
			self.lb_select(self.lbMain, mode="next")

	def on_lb_row_activated(self, listbox, listboxrow):
		i = listboxrow.get_index()
		numDirs = len(self.curDirList)
		numFiles = len(self.curFileList)
		self.rowActTime = time.time()
		if i >= numDirs:
			print("File: {}".format(self.curFileList[i-numDirs]))
		else:
			print("Dir: {}".format(self.curDirList[i]))

	def on_lb_button_release(self, listbox, event):
		curTime = time.time()
		diffTime = curTime - self.prevClickTime
		if diffTime < 0.5:
			print("INFO:btn_rel: mouse button double clicked")
			if self.rowActTime > self.prevClickTime:
				self.lb_play(self.lbMain)
			else:
				print("WARN:btn_rel: Need to click on a valid row")
		self.prevClickTime = curTime
		return False

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
		self.lbMain.set_size_request(self.scrWidth*0.25,self.scrHeight*0.9)

	def config_file(self):
		return "%s/.browsecontent.cfg"%(self.basePath)

	def save_config(self):
		f = open(self.config_file(), mode="w+")
		theLastFile = self.lastFile.replace(self.basePath,"",1)
		if theLastFile.startswith("/"):
			theLastFile = theLastFile[1:]
		f.write("lastFile:%s"%(theLastFile))
		f.close()

	def load_config(self):
		try:
			f = open(self.config_file())
			l = f.readline()
			theLastFile = l.replace("lastFile:","",1)
			print("INFO:load_config:basePath:%s"%(self.basePath))
			self.lastFile = os.path.join(self.basePath, theLastFile)
			#self.curPath = os.path.dirname(self.lastFile) , should also work
			self.curPath = os.path.join(self.basePath, os.path.dirname(theLastFile))
			print("INFO:load_config:curPath:%s"%(self.curPath))
			f.close()
		except FileNotFoundError:
			print("WARN:load_config: No config file found at %s"%(self.basePath))



class BrowseContentKUI(Gtk.Application):
	wMain = None

	def __init__(self, basePath="."):
		Gtk.Application.__init__(self, application_id="hanishkvc.browse.content.kui")
		self.basePath = basePath

	def do_activate(self):
		#self.wMain = MainWin(self, self.basePath, None, None)
		self.wMain = MainWin(self, self.basePath)
		self.wMain.show_all()



if __name__ == '__main__':
	sPath = "."
	if len(sys.argv) > 1:
		sPath = sys.argv[1]
	app = BrowseContentKUI(sPath)
	exitStatus = app.run()
	app.wMain.save_config()
	sys.exit(exitStatus)

