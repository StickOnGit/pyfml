#! /usr/bin/env python

"""Creates minimal iEHR elements with some default values(cough, magic numbers)."""

from baseparts import make_new_element as _mne

def make_textfield():
	elem = _mne(iform_field_type_id=1, field_label='Textfield')
	elem['max_value'] = 100
	return elem
	
def make_textbox():
	elem = _mne(iform_field_type_id=2, field_label='Textbox')
	return elem
	
def make_popup():
	elem = _mne(iform_field_type_id=3, field_label='Popup')
	return elem
	
def make_checkbox():
	elem = _mne(iform_field_type_id=5, field_label='Checkbox')
	return elem

def make_label(field_label='Label'):
	elem = _mne(iform_field_type_id=7, field_label=field_label)
	return elem

def make_slider():
	elem = _mne(iform_field_type_id=8, field_label='Slider')
	elem['default_value'] = 1
	elem['min_value'] = 0
	elem['max_value'] = 10
	elem['slider_precision'] = 0
	return elem

def make_draw_elem():
	elem = _mne(iform_field_type_id=9, field_label='Drawing Element')
	return elem

def make_list():
	elem = _mne(iform_field_type_id=10, field_label='List')
	elem['multiple_selection'] = 0
	elem['sub_view_type'] = 0
	elem['sub_view_dynamic'] = 0
	return elem
	
def make_seg_control():
	elem = _mne(iform_field_type_id=11, field_label='Segmented Control')
	return elem

def make_html_block():
	elem = _mne(iform_field_type_id=12, field_label='HTML Block')
	return elem
	
###	###	###	###	###	###	###	###	###
#	other textfield-based objects #
###	###	###	###	###	###	###	###	###

def make_phonefield():
	elem = _mne(iform_field_type_id=1, field_label='Phone Field')
	elem['string_format_type'] = 1
	elem['max_value'] = 20
	return elem

def make_ssnfield():
	elem = _mne(iform_field_type_id=1, field_label='SSN Field')
	elem['string_format_type'] = 2
	elem['max_value'] = 15
	return elem
	
def make_zipfield():
	elem = _mne(iform_field_type_id=1, field_label='Zipcode Field')
	elem['string_format_type'] = 3
	elem['max_value'] = 15
	return elem

def make_datefield():
	elem = _mne(iform_field_type_id=1, field_label='Date Field')
	elem['string_format_type'] = 4
	elem['max_value'] = 20
	return elem
