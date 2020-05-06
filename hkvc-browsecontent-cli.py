#!/usr/bin/env python3

import os
import sys

gPrev = None
def unique(s1):
	global gPrev
	s1 = s1.split('.')[0]
	tPrev = gPrev
	gPrev = s1
	if tPrev == gPrev:
		return False
	else:
		return True

def process_dir(sPath):
	fileItems = os.listdir(sPath)
	items = list(filter(unique, fileItems))
	while True:
		print("\n\n\nCur [{}]".format(sPath))
		for i in range(len(items)):
			print("{}: {}".format(i, items[i]))
		menuItem = input("Select item[0-..,(b)ack,quit]:")
		try:
			mi = int(menuItem)
		except ValueError:
			if (menuItem == "quit"):
				exit()
			elif (menuItem == "b"):
				process_dir(sPath[0:sPath.rindex('/')])
			else:
				continue
		theItem = os.path.join(sPath, items[mi])
		if os.path.isdir(theItem):
			process_dir(theItem)
		else:
			os.system("xdg-open '{}'".format(theItem))


process_dir(sys.argv[1])

