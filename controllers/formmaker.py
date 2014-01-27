#! /usr/bin/env python

"""Creates a basic form."""
import baseparts as BP
import formeditor as FE
import reorderform as ROF

def make_new_form():
	"""Returns a dict of nested lists and dicts. Follows .itpl format."""
	newForm = BP.make_new_form_shell(template_name="New Template")
	newSection = BP.make_new_section(section_name="New Section")

	newForm['iformSectionTiesArray'].append(newSection)
	return newForm