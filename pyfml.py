#! /usr/bin/env python

"""The command line interface for pyFML.

Type pyfml.py my_file to read a file and convert it to .itpl."""

import sys
import os
import plistlib as PLIB
from controllers.fmlreader import xml_to_dict, read_xml
from controllers.reorderform import setup_form

_FMLFOLDER = 'fml'
_ITPLFOLDER = 'itpl'
_IMGFOLDER = 'images'
_ALLFOLDERS = [_FMLFOLDER, _ITPLFOLDER, _IMGFOLDER]

def end():
	print
	sys.exit(0)
	
def load_fml(loadpath):
	"""Loads .fml file.
	Looks under *local* fml folder. Will create folder if not seen."""
	file = os.path.join(_FMLFOLDER, loadpath)
	print "...loading from %s" % file
	try:	#load the FML file
		fmlfile = read_xml(file)
	except IOError:
		if os.path.exists(_FMLFOLDER):	#does fml folder exist? if so, must not be fml file present
			print "\tDidn't see %s in your fml folder." % file
		else:	#if local fml folder doesn't exist, create it.
			os.mkdir(_FMLFOLDER)
			print "\tCreated local fml folder.\n\tHUMAN: move fml file to folder, try again."
		end()
	else:
		print "\tLoaded %s." % file
		return fmlfile
		
def save_itpl(savefile):
	"""Saves .itpl file.
	Saves in *local* itpl folder. Will create folder if not seen.
	Inserts numeral before extension if saving a duplicate."""
	if not os.path.exists(_ITPLFOLDER):
		os.mkdir(_ITPLFOLDER)
	savename = savefile['template_name']
	finalname = '%s.itpl' % savename
	savepath = os.path.join(_ITPLFOLDER, finalname)
	dups = 1
	while os.path.exists(savepath):
		finalname = '%s%d.itpl' % (savename, dups)
		savepath = os.path.join(_ITPLFOLDER, finalname)
		dups += 1
	try:
		PLIB.writePlist(savefile, savepath)
	except (TypeError, IOError) as err:
		print "\tCouldn't save %s. Apparently, %s" % (finalname, err)
		print "\tCheck '%s' to see if there's a partial save file: \n\tthis may help you see which element or section pyFML choked on." % savepath
		end()
	else:
		print "\nSaved '%s' to '%s'." % (finalname, savepath)
		
def init():
	"""Creates fml and itpl folders in the local directory."""
	print "\tPreparing current directory..."
	foldersmade = 0
	alreadyexists = 0
	totalneededfolders = len(_ALLFOLDERS)
	for folder in _ALLFOLDERS:
		if not os.path.exists(folder):
			try:
				os.mkdir(folder)
			except:
				print "\tInit failed. Couldn't create %s." % folder
			else:
				print "\tCreated %s folder." % folder
				foldersmade += 1
		else:
			print "\t%s already exists here." % folder
			alreadyexists += 1
	if foldersmade == 0 and alreadyexists == totalneededfolders:
		print "This directory appears to be ready already. Already!"
	elif foldersmade == 0 and alreadyexists == 0:
		print "Init failed to create any folders. Try again with sudo."
	elif foldersmade == totalneededfolders:
		print "Directory is ready!"
	else:
		print """Well, it's hard to say, this directory MIGHT be ready.
		Check for folders named fml and itpl; if they're there, you can
		probably go ahead and start converting files."""
	end()
	
def convert_to_itpl(xmlform):
	"""Returns a plist which is the converted FML file.
	Sets the order_nums, iform_field_ids, and creates narrative_strings."""
	pyform = xml_to_dict(xmlform)
	setup_form(pyform)
	return pyform

def oops(userdata=None):
	if not userdata:
		print "\tpyFML didn't see a command."
	else:
		print "\tpyFML doesn't understand or work with %s. (...yet?)" % userdata
	print """Try:
	pyfml.py file_name		-- read an XML file; or
	pyfml.py init			-- prepare this directory for work."""
	end()
	

if __name__ == "__main__":
	print
	try:
		flag = sys.argv[1]
	except IndexError:
		oops()
	else:
		if flag == 'init':
			init()
		elif '.xml' in flag or '.fml' in flag:
			thefile = load_fml(flag)
			theform = convert_to_itpl(thefile)
			save_itpl(theform)
		else:
			oops(flag)