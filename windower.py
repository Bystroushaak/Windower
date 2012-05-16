#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# NONAME v0.0.0 (dd.mm.yy) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in Geany text editor.
#
# Notes:
    # Check na existenci instalace wmctrl
#= Imports =====================================================================
import os
import sys
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
		cs = "-i "
	
	out = []
	try:
		for l in subprocess.check_output("wmctrl -l | grep " + cs + " " + str(wn), shell=True).strip().splitlines():
			out.append(l.split()[0])
	except subprocess.CalledProcessError, e:
		pass
	
	return out


def moveToDesktop(n):
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
			return i
		
		i += 1
	
	raise IndexError("WTF? There is no active desktop?")


#= Main program ================================================================
if not checkWmctrl():
	sys.stderr.write("This program is only wrapper over 'wmctrl'. You have to install 'wmctrl'!\n")
	sys.exit(1)

print grepWindowName("firefox")
print getDekstopCount()
print getActualDesktop()