#! /usr/bin/env python

"""This module imports XML and converts it to a plist-compatible format.

The primary method here is xml_to_form. It iterates over the XML tree and looks 
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
import elems as _els
import formeditor as FE
import reorderform as ROF
from pprint import pprint as pp

FMLFOLDER = 'fml'
FMLFILE = 'test.fml'

###
# dictionaries to 'translate' FML terms into the correct names for the DB.
# keys are 'fml' terms, values are .itpl terms.
# a good example is _xmlcheckbox: 'on' is the fml term, 'checked_narrative'
# is the .itpl term. this script will see the fml term and replace it with
# the .itpl term.

_xmltextfield = {
	"req": "is_required",
	"remind": "placeholder_text",
	"chars": "max_value",
	"noclip": "hide_from_clipboard"
}

_xmltextbox = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard"
}

_xmlpopup = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard",
	"list": "popup_values",
	"edit": "dynamic_list"
}

_xmlcheckbox = {
	"req": "is_required",
	"remind": "placeholder_text",
	"on": "checked_narrative",
	"off": "unchecked_narrative",
	"noclip": "hide_from_clipboard"
}

_xmllabel = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard"
}

_xmlslider = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard",
	"min": "min_value",
	"max": "max_value",
	"start": "default_value",
	"tick": "slider_precision"
}

#needs improvement
_xmldrawing = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard",
	"img": "imageObjData"
}

_xmlmenu = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard",
	"list": "popup_values",
	"sublist": "sub_view_list",
	"edit": "dynamic_list",
	"subedit": "sub_view_dynamic",
	"multi": "multiple_selection",
	"subtype": "sub_view_type"
}

_xmlseg = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard"
}

_xmlblock = {
	"req": "is_required",
	"remind": "placeholder_text",
	"noclip": "hide_from_clipboard"
}

###
# these three dicts are dicts of dicts. they are used to reference the correct
# dict when attempting to translate FML terms to .itpl terms.
# The keys are the 'fml' terms, the values are the corresponding dicts.
# These dicts need to be updated at the same time to keep everything working;
# if the FML term for some data changes, it'll need to be updated in all of these.
# if I level up I might figure out a better way to map all the things.

_xmltranslate = {
	"textfield": _xmltextfield,
	"textbox": _xmltextbox,
	"popup": _xmlpopup,
	"checkbox": _xmlcheckbox,
	"label": _xmllabel,
	"slider": _xmlslider,
	"drawing": _xmldrawing,
	"menu": _xmlmenu,
	"seg": _xmlseg,
	"block": _xmlblock,
	"phone": _xmltextfield,
	"ssn": _xmltextfield,
	"zip": _xmltextfield,
	"date": _xmltextfield
}
_elemdict = {
	"textfield": _els.make_textfield,
	"textbox": _els.make_textbox,
	"popup": _els.make_popup,
	"checkbox": _els.make_checkbox,
	"label": _els.make_label,
	"slider": _els.make_slider,
	"drawing": _els.make_draw_elem,
	"menu": _els.make_list,
	"seg": _els.make_seg_control,
	"block": _els.make_html_block,
	"phone": _els.make_phonefield,
	"ssn": _els.make_ssnfield,
	"zip": _els.make_zipfield,
	"date": _els.make_datefield	
}
_xmltextlocation = {
	"textfield": "field_label",
	"textbox": "field_label",
	"popup": "field_label",
	"checkbox": "field_label",
	"label": "field_label",
	"slider": "field_label",
	"drawing": "field_label",
	"menu": "field_label",
	"seg": "field_label",
	"block": "checked_narrative",
	"phone": "field_label",
	"ssn": "field_label",
	"zip": "field_label",
	"date": "field_label"
}

# static sections need a dict too. the key is the box name,
# the value is the mp_box_type.
_boxtypes = {
	"allergies": 12,
	"attach": 14,
	"careslip": 19,
	"edurec": 16,
	"erx": 8,
	"immune": 13,
	"medrec": 6,
	"orders": 11,
	"prevcare": 15,
	"problem": 10,
	"refer": 17,
	"sig": 21,
	"smoke": 2,
	"vitals": 9
}

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
	if xmlsection.tag in _boxtypes:
		newSectionOuter['mp_box_type'] = _boxtypes[xmlsection.tag]
		del newSectionOuter['iform_section']
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
		##raise KeyError("There's no <%s> element in FML.\nAvailable elements are: %s." % (elemType,''.join([_elemdict.keys(), '\n'])))
		print ("There's no <%s> element in FML.\nAvailable elements are: \n%s\n" % (elemType,''.join(['\n\t%s' % x for x in _elemdict.keys()])))
		return _els.make_label(field_label="An error occurred.")
	elemTextKey = _xmltextlocation[elemType]	##gets k of 'open text'
	elemTextVal = xmlelement.text				##gets v of 'open text'
	elemAttrib = xmlelement.attrib.items()		##attributes as list of tuples
	elemData = [(elemTextKey, elemTextVal)]
	for k, v in elemAttrib:
		elemData += [(k, v)]
	nestedData = []
	for item in xmlelement:		##add nested xml to 'parent' element
		nestedData += [(item.tag, item.text)]
		nestedAttrib = item.attrib.items()
		for k, v in nestedAttrib:
			nestedData += [(k, v)]
	for k, v in elemData + nestedData:
		if k in translator:				##turns fml keys to .plist keys
			k = translator[k]
		v = tidy_up(v)					##cleans up strings
		newElem[k] = v
	if 'imageObjData' in newElem:
		try:
			newElem['imageObjData'] = img_path_to_base64(newElem['imageObjData'])
			newElem['attached_file_id'] = -1
		except IOError:
			sectName = newSection['iform_section']['section_name']
			print "No image or bad path for drawing element in %s." % (sectName)
			newElem['imageObjData'] = None
	return newElem
	
def img_path_to_base64(imageobjdatapath):
	"""Turns a relative path into a base64 encoded image.
	
	Should be called after the FML element is translated into a dict."""
	with open(imageobjdatapath, "rb") as f:
		dataToTranslate = f.read()
		#return repr(dataToTranslate.encode("base64")).encode('base64')
		return PLIB.Data(dataToTranslate)

def xml_to_form(xmlform):
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
	ROF.fix_all_orders(newForm)
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
	#print newpath
	#print OS.path.exists(newpath)
	xmlF = read_xml(newpath)
	newF = xml_to_form(xmlF)
	return (xmlF, newF)
	
def quicktest():
	"""Even shorter test! Just pretty-prints the dict version of the FML file. Returns nothing."""
	pp(test()[1])