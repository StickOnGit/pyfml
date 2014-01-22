#! /usr/bin/env python

"""Some simple functions that replace the need to constantly reference the correct index of a list nested in a dict nested in a dict of arrays and dicts.

I figure 'add_blah_to_derp' is easier to remember than 'myForm['iformDurdleArray'][27]['iform_section']['iFormHurp'] = newElem'.

The functions do pretty much what they say; whenever a (section/element) is added to a (form/section) it is appended to the end of the list of (sections/elements).

order_num is NOT updated by calling these functions. Use reorderform.py to auto-update the order of all the things."""

def add_section_to_form(newsection, form):
	"""Adds a section to the form.
	Requires two arguments - the new section, and the form.
	Automatically appends the new section to the end of the_form['iformSectionTiesArray']."""
	form['iformSectionTiesArray'].append(newsection)
	
def add_elem_to_section(newelem, section):
	"""Adds an element to a section.
	Requires two arguments - the new element, and the section. the_form['iformSectionTiesArray'][X] is the section index."""
	section['iform_section']['iformFieldsArray'].append(newelem)

