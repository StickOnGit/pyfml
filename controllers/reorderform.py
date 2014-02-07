#! /usr/bin/env python
"""Gets an FML-based dict ready to be saved as a plist.
Automatically assigns order_num, field_id, narrative_strings,
and HTML tags for correct display on the narrative.
"""

from narrativedicts import _outertags, _innertags, _presuftag, _sublisttags, _checkunchecktags


def new_set_order(pyform):
	sectioncount = 0
	for section in pyform.get('iformSectionTiesArray', []):
		sectioncount += 1
		section['order_num'] = sectioncount
		elementcount = 0
		for element in section.get('iform_section', {}).get('iformFieldsArray', []):
			elementcount += 1
			element['order_num']  = elementcount

def new_set_ids(pyform):			
	fieldID = -1
	for section in pyform.get('iformSectionTiesArray', []):
		for element in section.get('iform_section', {}).get('iformFieldsArray', []):
			element['iform_field_id'] = fieldID
			fieldID -= 1
			
def new_set_nar(pyform):
	"""Creates narrative string.
	
	This function is more verbose than the previous one but is
	better at handling an absence of sections/inner sections/elements."""
	for section in pyform.get('iformSectionTiesArray', []):
		autoString = u''
		for element in section.get('iform_section',{}).get('iformFieldsArray', []):
			fieldID = element.get('iform_field_id', False)
			fieldLabel = element.get('field_label', '')
			if fieldID is not False:
				autoString = "%s{{%d.%s}}" % (autoString, fieldID, fieldLabel)
			else: pass
			auto_tag(element)
			if autoString:
				section['iform_section']['narrative_string'] = autoString
			else: pass
	else: pass
				
def label_to_narrative(string):
	"""Tries to ensure a string is ready to become a list_header string.
	Removes whitespace from front and back (if any) and looks for the
	last character. If that character is NOT an alphanumeric character,
	it's deleted. It stops when it finds an alphanumeric character, and
	adds a colon.
	
	TLDR?
	
	Changes ' How Did This Happen?!' to 'How Did This Happen:'"""
	try:
		string = string.strip()		##zap leading/trailing whitespace
	except AttributeError:
		return string
	newString = string
	while newString and not newString[-1].isalnum():	##remove non-alphanum
		newString = newString[:-1]						##chars from end
	if not newString:			##if somehow the whole string was deleted
		return string			##return old string (minus whitespace)
	else:
		return "%s: " % newString
	
def auto_tag(element):
	"""Uses reference dicts (imported) to assign basic HTML tags to
	the sections of elements which would appear on the narrative."""
	newdata = {}
	elemID = element.get('iform_field_type_id', None)
	headnarrative = ''
	footnarrative = ''
	listheadtext = label_to_narrative(element.get('field_label', ''))
	if listheadtext:
		headnarrative = "<b>%s</b>" % listheadtext
	outsidetag = _outertags.get(elemID, None)
	if outsidetag is not None:
		headnarrative = "<%s>%s" % (outsidetag, headnarrative)
		footnarrative = "</%s>" % outsidetag
	insidetag = _innertags.get(elemID, None)
	if insidetag is not None:
		headnarrative = "%s<%s>" % (headnarrative, insidetag)
		footnarrative = "</%s>%s" % (insidetag, footnarrative)
	if outsidetag is not None or insidetag is not None:
		if headnarrative:
			newdata['list_header'] = headnarrative
		if footnarrative:
			newdata['list_footer'] = footnarrative
	checkunchecktag = _checkunchecktags.get(elemID, None)
	if checkunchecktag is not None:
		currentchecked = element.get('checked_narrative', '')
		currentunchecked = element.get('unchecked_narrative', '')
		newdata['checked_narrative'] = "<%s>%s</%s>" % (checkunchecktag, currentchecked, checkunchecktag)
		newdata['unchecked_narrative'] = "<%s>%s</%s>" % (checkunchecktag, currentunchecked, checkunchecktag)
	listtag = _presuftag.get(elemID, None)
	if listtag is not None:
		newdata['list_prefix'] = "<%s>" % listtag
		newdata['list_suffix'] = "</%s>" % listtag
	sublisttag = _sublisttags.get(elemID, None)
	if sublisttag is not None:
		newdata['sublist_prefix'] = "<%s>" % sublisttag
		newdata['sublist_suffix'] = "</%s>" % sublisttag
	if newdata:
		for k, v in newdata.iteritems():
			element[k] = unicode(v)
	else: pass

def setup_form(pyform):
	"""The one function to bind them all.
	Calls the current implementation functions which set order_num,
	field_ids, and data pertaining to the narrative."""
	new_set_order(pyform)
	new_set_ids(pyform)
	new_set_nar(pyform)