#! /usr/bin/env python

"""This module imports XML and converts it to a plist-compatible format.

The primary method here is xml_to_dict. It iterates over the XML tree and looks 
for these terms as tags, attributes, and as children elements of the parent. It
compares these terms to the correct dictionary for the element and replaces the
FML word with the accepted .itpl word.

Forms and sections have a strict-ish syntax expectation. They primarily
use attributes to describe preferences and child elements to describe
content. Form and section titles are a little different and can be either-or.

As an example: 
<iEHR>Dr. Mario's Form</iehr>

This COULD also be written as follows:

<iEHR name="Dr. Mario's Form"></iEHR>

However, preferences such as 'archived' and 'available to clipboard' will only
be looked for as attributes. Example:

<iEHR archived='0'>Dr. Mario's Form</iEHR>

Sections (boxes) receive similar treatment -- names will be looked for in
either location, but data that acts as a preference is preferred to live
as an attribute.

Elements are less picky. A good example is a list element. in FML it looks like this:

<menu req='1'>Menu Title Here
	<list edit='1'>Foo##Bar##Baz##Eggs##Spam</list>
	<sublist>One##Two##Three##Four</sublist>
</menu>

This script will 'flatten' the above into the correct .plist format, and will
apply the attributes of the children to the parent, just like the .itpl file.
it will turn "edit='1'" into "<key>dynamic_list</key><integer>1</integer>" and
add it to the parent element.

Currently, it is not as recursive as it maybe could be, so only one layer of
nesting children is supported. also, it doesn't really care whether the
values are attributes or child elements, so if one *really* wanted to
one could create a list like this:

<menu list="Foo##Bar##Baz##Eggs##Spam">Menu Title Here
	<req>1</req>
</menu>

So it's not a strict syntax, and the use of attributes over elements is really
sort of up to the Form Former. However, I do strongly recommend a style wherein
'content' is in elements and 'preferences' are attributes.

Many values have defaults and do not need to be explicitly entered, but can be
easily overridden if they are present in the FML file. Order_num is determined
when the file is translated from FML to a dict for plistlib, so just by
building the FML correctly will the order of elements and sections be
determined."""
import xml.etree.ElementTree as ET
import plistlib as PLIB
import os as OS
import baseparts as BP
import formeditor as FE
import reorderform as ROF		##eventually move this out
from boxdict import _boxtypes
from fmltodict import _xmltranslate, _elemdict, _xmltextlocation
from pprint import pprint as pp

##these, along with the defaults in pyfml.py, should be in a separate file in a dict
FMLFOLDER = 'fml'
FMLFILE = 'test.fml'
IMGFOLDER = 'images'

##return this on element creation fail
_BADELEMENT = _elemdict['label'](field_label="**An error occurred here. REMOVE this element and correct.**")

def read_xml(xmlpath):
	"""Loads XML from stated path."""
	tree = ET.parse(xmlpath)
	return tree.getroot()
	
def new_shell_from_xml(xmlobj):
	"""Returns a form populated with translated FML values."""
	newShell = BP.make_new_form_shell()
	for k, v in xmlobj.attrib.iteritems():
		newShell[k] = v
	maybetitle = tidy_up(xmlobj.text)
	if len(maybetitle) > 0:
		newShell['template_name'] = maybetitle
	return newShell

def new_section_from_xml(xmlsection):
	"""Returns a section populated with translated FML values."""
	newSectionOuter = BP.make_new_section_outer()
	if xmlsection.tag in _boxtypes:		#catch hardcoded sections
		newSectionOuter['mp_box_type'] = _boxtypes[xmlsection.tag]
		del newSectionOuter['iform_section']	#not needed with hardcoded sections
		return newSectionOuter
	else:
		pass
	newSectionInner = BP.make_new_section_inner()
	for k, v in xmlsection.attrib.iteritems():
		if k is not 'order_num':
			newSectionInner[k] = v
	maybetitle = tidy_up(xmlsection.text)
	if len(maybetitle) > 0:
		newSectionInner['section_name'] = maybetitle
	newSectionOuter['iform_section'] = newSectionInner
	return newSectionOuter

def new_elem_from_xml(xmlelement):
	"""Returns an element populated with translated FML values."""
	try:
		elemType = xmlelement.tag
		translator = _xmltranslate[elemType]	##gets right function for next line
		newElem = _elemdict[elemType]()			##new blank element of elemType
	except KeyError:
		##log to Terminal and add 'error' label element
		##should probably catch all errors and report after form forming is complete
		print """There's no <%s> element in FML. Available elements are: \n%s
		""" % (elemType,''.join(['\n\t%s' % x for x in _elemdict.keys()]))
		return _BADELEMENT
	elemTextKey = _xmltextlocation[elemType]	##gets key of 'open text'
	##next line gets value of 'open text', or sets to '' if None.
	##this allows for void elements such as <label /> or simply
	##elements with no field_label. also, python ternary <3 <3
	##read as -- elem TextVal = xmlelem.text == None ? '' : xmlelem.text
	elemTextVal = xmlelement.text if xmlelement.text is not None else ''
	elemAttrib = xmlelement.attrib.items()		##attributes as list of tuples
	elemData = [(elemTextKey, elemTextVal)]
	for k, v in elemAttrib:
		elemData += [(k, v)]
	nestedData = []
	for item in xmlelement:				##add nested xml to 'parent' element
		## <3
		nestedData += [(item.tag, item.text if item.text is not None else '')]
		nestedAttrib = item.attrib.items()
		for k, v in nestedAttrib:
			nestedData += [(k, v)]
	for k, v in elemData + nestedData:
		if k in translator:				##turns fml keys to .plist keys
			k = translator[k]
		v = tidy_up(v)					##cleans up strings
		newElem[k] = v
	if 'imageObjData' in newElem:
		##encodes images if present
		##apparently this works for future builds but not current?? O_o
		newElem['imageObjData'] = img_path_to_base64(newElem['imageObjData'])
	return newElem
	
def img_path_to_base64(imageobjdatapath):
	"""Turns a relative path into a base64 encoded image.
	
	Should be called after the FML element is translated into a dict."""
	pathinfolder = OS.path.join(IMGFOLDER, imageobjdatapath)
	try:
		with open(pathinfolder, "rb") as f:
		#try:
			dataToTranslate = f.read()
	except IOError:
		print "Bad path: " % pathinfolder
		return None
	else:
		return PLIB.Data(dataToTranslate)

def xml_to_dict(xmlform):
	"""Pass this an FML file; returns a dict for plistlib to convert to .itpl.
	The order_num of elements is determined on translation, so it need not be
	present in the FML file."""
	newForm = new_shell_from_xml(xmlform)
	for section in xmlform:
		newSection = new_section_from_xml(section)
		for element in section:
			newElem = new_elem_from_xml(element)
			FE.add_elem_to_section(newElem, newSection)
		FE.add_section_to_form(newSection, newForm)
	return newForm

def tidy_up(somexml):
	"""Ensures strings are unicode, removes newlines and tabs from strings, 
	and replaces the ## delimiter as newlines from lists/sublists.
	If passed something besides basestring or int, returns it as-is."""
	if not isinstance (somexml, (basestring, int)):
		return somexml
	try:
		return int(somexml)
	except:
		newstr = somexml.strip().replace('##', '\r') ##type \r?!!?!? - jean-luc picard, time's arrow pt 1
		return u'%s' % newstr


###help methods for quick testing, not probably much use for anything else

def test(filepath=FMLFILE):
	"""Quickly tests fmltest.xml to see that it loads as both valid XML and turns into a plist-friendly dict.
	Both the XML and the dict are returned as (XML, dict) tuple.
	If need be, an optional filepath can be passed."""
	newpath = OS.path.join(FMLFOLDER, filepath)
	xmlF = read_xml(newpath)
	newF = xml_to_dict(xmlF)
	return newF
	
def quicktest():
	"""Even shorter test! Just pretty-prints the dict version of the FML file. Returns nothing."""
	pp(test())