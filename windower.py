#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Windower - virtual desktop windows positioner v1.0.0 (16.05.2012) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in gedit text editor.
#
# Notes:
    # 
#= Imports =====================================================================
import os
import sys
import time
import subprocess

import conf_parser as cp


try:
	subprocess.check_output
except AttributeError:
	try:
		import commands
	except ImportError:
		sys.stderr.write("Heh, now you are fucked. Try different version of python.\n")
		sys.exit(1)
	
	def check_output(command, shell=True):
		return commands.getoutput(command)
	
	subprocess.check_output = check_output



#= Variables ===================================================================
CONF_NAME = "config.txt"



#= API =========================================================================
def checkWmctrl():
	"Check if wmctrl is installed."
	
	return os.system("type wmctrl > /dev/null 2>&1") == 0


def grepWindowName(wn, case_sensitive=False):
	"""Returns list of windows with given name in title.
	
	If case_sensitive == True, matching is case sensitive. Default False.
	"""
	cs = ""
	if not case_sensitive:
		wn = wn.lower()
		cs = "-i "
	
	out = []
	try:
		for l in subprocess.check_output("wmctrl -l | grep " + cs + " \"" + str(wn) + "\"", shell=True).strip().splitlines():
			out.append(l.split()[0])
	except subprocess.CalledProcessError, e:
		pass
	
	return out


def switchToDesktop(n):
	"Switch to desktop with given number."
	
	if n >= getDekstopCount():
		raise IndexError("You don't have enough desktops!")
	
	os.system("wmctrl -s " + str(n))


def getDekstopCount():
	"Returns number of used virtual desktops."
	
	return len(subprocess.check_output("wmctrl -d", shell=True).splitlines())


def getActualDesktop():
	"Returns number of currently used desktop."
	
	i = 0
	for l in subprocess.check_output("wmctrl -d", shell=True).splitlines():
		if "*" in l:
			return str(i)
		
		i += 1
	
	raise IndexError("WTF? There is no active desktop?")


def moveAppHere(app_hash):
	"Move application identified by hash (see grepWindowName()) to this desktop."
	
	os.system("wmctrl -iR " + str(app_hash))


def maximizeWindow(app_hash):
	os.system("wmctrl -i -r " + str(app_hash) + " -b add,maximized_vert,maximized_horz")


def fullscreenWindow(app_hash):
	os.system("wmctrl -i -r " + str(app_hash) + " -b add,fullscreen")


def moveToCoordinates(app_hash, x, y):
	"Move window to given x,y coordinates."
	
	os.system("wmctrl -i -r " + str(app_hash) + " -e 0," + str(x) + "," + str(y) + ",-1,-1")


def resizeWindow(app_hash, x_size, y_size):
	"Resize window to given size."
	
	os.system("wmctrl -i -r " + str(app_hash) + " -e 0,-1,-1" + str(x_size) + "," + str(y_size))



#= Main program ================================================================
if __name__ == "__main__":
	if not checkWmctrl():
		sys.stderr.write("This program is only wrapper over 'wmctrl'. You have to install 'wmctrl'!\n")
		sys.exit(1)

	conf = cp.parseConf(CONF_NAME, case_sensitive_val = True, case_sensitive_namespace = True)
	
	while len(conf.keys()) > 0:
		for app_title in conf.keys():
			win_id = []
			
			# grep window id
			if "case_sensitive" in conf[app_title] and conf[app_title]["case_sensitive"] == "true":
				win_id = grepWindowName(app_title, True)
			else:
				win_id = grepWindowName(app_title)
			
			if "launch" not in conf[app_title]:
				# wait until app start
				if "waiting" in conf[app_title] and conf[app_title]["waiting"] > time.time() and len(win_id) == 0:
					continue
			
				# if app title not found in list of running apps, try again or remove app from todo
				if len(win_id) == 0:
					if "wait" in conf[app_title]:
						if "waiting" in conf[app_title]:
							del conf[app_title]
							continue
					
						conf[app_title]["waiting"] = time.time() + int(conf[app_title]["wait"])
					
						print "waiting", conf[app_title]["wait"], "for", app_title
					else:
						sys.stderr.write("Window with title '" + app_title + "' not found! Skipping..\n")
						del conf[app_title]
				
					continue
			
			if "launch" in conf[app_title]:
				print "Launching '" + conf[app_title]["launch"] + "' .."
				os.system(conf[app_title]["launch"] + " > /dev/null 2>&1 &")
				del conf[app_title]["launch"]
				
				if "waiting" not in conf[app_title]:
					conf[app_title]["waiting"] = time.time() + 30
				
				continue
			
			for wid in win_id:
				if "desktop" in conf[app_title] and conf[app_title]["desktop"] != getActualDesktop():
					try:
						switchToDesktop(int(conf[app_title]["desktop"]))
						time.sleep(0.2)
						moveAppHere(wid)
						time.sleep(0.5)
					except IndexError, e:
						sys.stderr.write(str(e) + "\n")
					except ValueError, e:
						sys.stderr.write(str(e) + "\n")
				if "resize" in conf[app_title]:
					conf[app_title]["resize"] = conf[app_title]["resize"].lower()
					
					if "," in conf[app_title]["resize"]:
						width_x, width_y = conf[app_title]["resize"].split(",")
						
						try:
							resizeWindow(wid, int(width_x.strip()), int(width_y.strip()))
						except ValueError, e:
							sys.stderr.write("Can't resize window '" + app_title + "', bad size parameters!\n")
							sys.stderr.write(str(e) + "\n")
					elif conf[app_title]["resize"] == "maximize":
						maximizeWindow(wid)
					elif conf[app_title]["resize"] == "fullscreen":
						fullscreenWindow(wid)
					else:
						sys.stderr.write("Unsupported argument '" + conf[app_title]["resize"] + "'!\n")
					
					time.sleep(0.5)
				if "move" in conf[app_title]:
					if "," in conf[app_title]["move"]:
						x, y = conf[app_title]["move"].split(",")
						
						try:
							moveToCoordinates(wid, int(x.strip()), int(y.strip()))
							time.sleep(0.3)
						except ValueError, e:
							sys.stderr.write("Can't move window '" + app_title + "', to given parameters '" + conf[app_title]["move"] + "'!\n")
							sys.stderr.write(str(e) + "\n")
					else:
						sys.stderr.write("Unsupported argument '" + conf[app_title]["move"] + "'!\n")
				
				del conf[app_title]
			
			time.sleep(5)
