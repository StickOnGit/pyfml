#! /usr/bin/env python

"""Makes the most basic version of the three major parts of forms: elements, sections, and the
form.

Values that are not part of the dicts these functions return are not required to successfully
create a form. Functions in other modules may add extra key-value pairs, but typically just
to create 'nice' default values for various elements."""

def make_new_element(field_label="_default", 
					hide_from_clipboard=0, 
					iform_field_type_id=0, 
					is_required=0, 
					order_num=0, 
					string_format_type=0):
	"""Returns a basic element. 
	If calling this by itself, be SURE to pass a nonzero iform_field_type_id. 
	It defaults to 0, but iEHR finds that to be useless."""
	
	return {"field_label":field_label, 
			"hide_from_clipboard":hide_from_clipboard, 
			"iform_field_type_id":iform_field_type_id, 
			"is_required":is_required,"order_num":order_num, 
			"string_format_type":string_format_type}
			
def make_new_section_inner(iformFieldsArray=None, pull_preference=0, section_name="_default"):
	"""Returns the innermost part of a section. Typically don't call this by itself."""
	if iformFieldsArray is None:
		iformFieldsArray = []
	
	return {"iformFieldsArray":iformFieldsArray,
			"pull_preference":pull_preference, 
			"section_name":section_name}
			
def make_new_section_outer(iform_section=None, order_num=0):
	"""Returns the outer part of a section. Typically not called by itself."""
	if iform_section is None:
		iform_section = {}
	
	return {"iform_section":iform_section, "order_num":order_num}
	
def make_new_section(iform_section=None, order_num=0, 
					iformFieldsArray=None, pull_preference=1, section_name="_default"):
	"""Returns a whole iEHR form section.
	Note that this function defaults pull_preference to 1."""
	
	newInner = make_new_section_inner(iformFieldsArray=iformFieldsArray,
										pull_preference=pull_preference, 
										section_name=section_name)
	newOuter = make_new_section_outer(iform_section=iform_section, order_num=order_num)
	newOuter['iform_section'] = newInner
	return newOuter
	
def make_new_form_shell(archived=0, available_to_clipboard=0, 
				iformSectionTiesArray=None, template_name="_default"):
	"""Returns a form 'shell'. Has no sections or elements."""
	
	if iformSectionTiesArray is None:
		iformSectionTiesArray = []
	
	return {"archived":archived, "available_to_clipboard":available_to_clipboard,
	"iformSectionTiesArray":iformSectionTiesArray, "template_name":template_name}