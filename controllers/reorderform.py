#! /usr/bin/env python
"""Used to automate the process of assigning order_num to XML-created objects.

Since the goal of FML is to reduce time and keystrokes, it determines order_num
by simply reading the document tree and assigning order_num in the order of
elements found. It does likewise with sections.
"""
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
			if narrString:
				section['iform_section']['narrative_string'] = narrString
			else:
				pass
