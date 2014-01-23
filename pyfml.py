"""The command line interface for pyFML.

Type pyfml.py my_file to read a file and convert it to .itpl."""

import sys
import os
import plistlib as PLIB
from controllers.fmlreader import xml_to_dict, read_xml
from controllers.reorderform import set_order_num, set_field_ids, set_narrative

FMLFOLDER = 'fml'
ITPLFOLDER = 'itpl'

def end():
	print
	sys.exit(0)
	
def load_fml(loadpath):
	"""Loads .fml file.
	Looks under *local* fml folder. Will create folder if not seen."""
	file = os.path.join(FMLFOLDER, loadpath)
	print "...loading from %s" % file
	try:	#load the FML file
		fmlfile = read_xml(file)
	except IOError:
		if os.path.exists(FMLFOLDER):	#does fml folder exist? if so, must not be fml file present
			print "\tDidn't see %s in your fml folder." % file
		else:	#if local fml folder doesn't exist, create it.
			os.mkdir(FMLFOLDER)
			print "\tCreated local fml folder.\n\tHUMAN: move fml file to folder, try again."
		end()
	else:
		print "\tLoaded %s." % file
		return fmlfile
		
def save_itpl(savefile):
	"""Saves .itpl file.
	Saves in *local* itpl folder. Will create folder if not seen.
	Inserts numeral before extension if saving a duplicate."""
	if not os.path.exists(ITPLFOLDER):
		os.mkdir(ITPLFOLDER)
	savename = savefile['template_name']
	finalname = '%s.itpl' % savename
	savepath = os.path.join(ITPLFOLDER, finalname)
	dups = 1
	while os.path.exists(savepath):
		finalname = '%s%d.itpl' % (savename, dups)
		savepath = os.path.join(ITPLFOLDER, finalname)
		dups += 1
	try:
		PLIB.writePlist(savefile, savepath)
	except IOError as err:
		print "\tCouldn't save %s. Apparently, %s" % (finalname, err.strerror)
		print "path was %s" % savepath
		end()
	else:
		print "\nSaved '%s' to '%s'." % (finalname, savepath)
		
def init():
	"""Creates fml and itpl folders in the local directory."""
	print "\tPreparing current directory..."
	foldersmade = 0
	alreadyexists = 0
	for folder in [FMLFOLDER, ITPLFOLDER]:
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
	if foldersmade == 0 and alreadyexists == 2:
		print "This directory appears to be ready already. Already!"
	elif foldersmade == 0 and alreadyexists == 0:
		print "Init failed to create any folders. Try again with sudo."
	elif foldersmade == 2:
		print "Directory is ready!"
	else:
		print """Well, it's hard to say, this directory MIGHT be ready.
		Check for folders named fml and itpl; if they're there, you can
		probably go ahead and start converting files."""
	end()
	
def convert_to_itpl(xmlform):
	"""Returns a plist which is the converted FML file.
	Sets the order_nums, iform_field_ids, and creates narrative_strings."""
	formdict = xml_to_dict(xmlform)
	set_order_num(formdict)
	set_field_ids(formdict)
	set_narrative(formdict)
	return formdict

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
		end()
	else:
		if flag == 'init':
			init()
		elif '.xml' in flag or '.fml' in flag:
			thefile = load_fml(flag)
			theform = convert_to_itpl(thefile)
			save_itpl(theform)
		else:
			oops(flag)