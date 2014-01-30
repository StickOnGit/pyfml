#! /usr/bin/env python
"""Gets an FML-based dict ready to be saved as a plist.
Automatically assigns order_num, field_id, narrative_strings,
and HTML tags for correct display on the narrative.
"""

from narrativedicts import _outertags, _innertags, _presuftag, _sublisttags, _checkunchecktags


def correct_order(somelist):
	"""Sets the order_num for a list of items, in the order it sees them. Begins at 1.
	Does not increment or add an order_num to a dict if it isn't already present."""
	currentcount = 1
	for item in range(len(somelist)):
		if 'order_num' in somelist[item]:
			somelist[item]['order_num'] = currentcount
			currentcount += 1
		else:
			pass

def set_order_num(pyform):
	"""Sets the order_num of each element and section for a form dict."""
	try:
		correct_order(pyform['iformSectionTiesArray'])
	except KeyError:
		raise KeyError("fix_all_orders did not find iformSectionTiesArray.")
	unfixed_sections = 0
	number_of_sections = len(pyform['iformSectionTiesArray'])
	if number_of_sections == 0:
		return "No sections to fix."
	for section in pyform['iformSectionTiesArray']:
		try:
			correct_order(section['iform_section']['iformFieldsArray'])
		except KeyError:
			unfixed_sections += 1
	if unfixed_sections == 0:
		return "Confirmed order of elements in {fixed} of {notfixed} sections".format(
			fixed=number_of_sections - unfixed_sections,
			notfixed=number_of_sections
		)
	elif unfixed_sections < number_of_sections:
		return "Found at least one section, but not every section had elements to reorder."
	elif unfixed_sections == number_of_sections:
		return "Did not fix any element order_num within sections."
		
def set_field_ids(pyform, fieldID=-1):
	"""Sets incremental negative iform_field_ids.
	Can take optional fieldID argument. Apparently field_id is always
	negative in the .plist so if the argument is positive, it will
	use the additive inverse instead. (yes, i googled that word)"""
	try:
		fieldID = int(fieldID)
		if fieldID > 0:
			fieldID *= -1
	except:	##why bother specifying TypeError and ValueError, who cares
		print "field_id should be a number, preferably negative."
		fieldID = -1
	for section in pyform['iformSectionTiesArray']:
		try:
			for element in section['iform_section']['iformFieldsArray']:
				element['iform_field_id'] = fieldID
				fieldID -= 1
		except KeyError:
			pass
			
def set_narrative(pyform):
	"""Automatically creates a basic narrative string."""
	for section in pyform['iformSectionTiesArray']:
		narrString = ''
		if 'iform_section' in section:
			for element in section['iform_section']['iformFieldsArray']:
				if 'iform_field_id' in element:
					insertStr = "{{%d.%s}}" % (element['iform_field_id'], element['field_label'])
					narrString += insertStr
				else:
					pass
				#auto_tag(element)
				auto_tag(element)
			if narrString:
				section['iform_section']['narrative_string'] = narrString
			else:
				pass

def label_to_narrative(string):
	"""Tries to ensure a string is ready to become a list_header string.
	Removes whitespace from front and back (if any) and looks for the
	last character. If that character is NOT an alphanumeric character,
	it's deleted. It stops when it finds an alphanumeric character, and
	adds a colon.
	
	TLDR?
	
	Changes ' How Did This Happen?!' to 'How Did This Happen:'"""
	string = string.strip()		##zap leading/trailing whitespace
	newString = string
	while newString and not newString[-1].isalnum():	##remove non-alphanumeric
		newString = newString[:-1]		##chars from end
	if not newString:			##oops, couldn't work with it;
		return string			##return old string minus whitespace
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
	for k, v in newdata.iteritems():
		element[k] = unicode(v)
