#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# namespace conf parser v1.0.0 (16.05.2012) by Bystroushaak (bystrousak@kitakitsune.org)
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in gedit text editor.
#
# Notes:
    # 

def parseConf(fn, case_sensitive_key = False, case_sensitive_val = False, case_sensitive_namespace = False):
	"""
	Parse configuration in this format:
	
	#---
	namespace
		key: val # comment
	#---
	
	to:
	
	{"namespace" : {"key":"val"}}
	"""
	f = open(fn)
	data = f.read()
	data = data.splitlines()
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
				
			out[namespace][key.strip() if case_sensitive_key else key.strip().lower()] = val.strip()if case_sensitive_val else val.strip().lower() 
		else:
			namespace = line.strip() if case_sensitive_namespace else line.strip().lower() 
			out[namespace] = {}
	
	return out


#= Main program ================================================================
if __name__ == "__main__":
	pass
