#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# NONAME v0.0.0 (dd.mm.yy) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in Geany text editor.
#
# Notes:
    # 
#= Imports =====================================================================



#= Variables ===================================================================



#= Functions & objects =========================================================
def parseConf(fn):
	f = open(fn)
	data = f.read().splitlines()
	f.close()
	
	data = map(lambda x: x.split("#")[0], data) # remove comments
	data = filter(lambda x: x.strip() != "", data) # remove blank lines
	
	out = {}
	namespace = ""
	for line in data:
		if line.startswith("\t") or line.startswith(" ") and namespace != "":
			if ":" in line:
				tmp = line.split(":")
				key = tmp[0]
				val = ":".join(tmp[1:])
			else:
				key = line
				val = "true"
				
			out[namespace][key.strip()] = val.strip()
		else:
			namespace = line.strip()
			out[namespace] = {}
	
	return out


#= Main program ================================================================









