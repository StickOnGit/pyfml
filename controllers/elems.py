#! /usr/bin/env python

"""Creates minimal iEHR elements with some default values(cough, magic numbers)."""

from baseparts import make_new_element as _mne

def make_textfield(field_label=''):
	elem = _mne(iform_field_type_id=1, field_label=field_label)
	elem['max_value'] = 100
	return elem
	
def make_textbox(field_label=''):
	elem = _mne(iform_field_type_id=2, field_label=field_label)
	return elem
	
def make_popup(field_label=''):
	elem = _mne(iform_field_type_id=3, field_label=field_label)
	return elem
	
def make_checkbox(field_label=''):
	elem = _mne(iform_field_type_id=5, field_label=field_label)
	return elem

def make_label(field_label=''):
	elem = _mne(iform_field_type_id=7, field_label=field_label)
	return elem

def make_slider(field_label=''):
	elem = _mne(iform_field_type_id=8, field_label=field_label)
	elem['default_value'] = 1
	elem['min_value'] = 0
	elem['max_value'] = 10
	elem['slider_precision'] = 0
	return elem

def make_draw_elem(field_label=''):
	elem = _mne(iform_field_type_id=9, field_label=field_label)
	return elem

def make_list(field_label=''):
	elem = _mne(iform_field_type_id=10, field_label=field_label)
	elem['multiple_selection'] = 0
	elem['sub_view_type'] = 0
	elem['sub_view_dynamic'] = 0
	return elem
	
def make_seg_control(field_label=''):
	elem = _mne(iform_field_type_id=11, field_label=field_label)
	return elem

def make_html_block(field_label='HTML Block'):
	elem = _mne(iform_field_type_id=12, field_label=field_label)
	return elem
	
###	###	###	###	###	###	###	###	###
#	other textfield-based objects #
###	###	###	###	###	###	###	###	###

def make_phonefield(field_label=''):
	elem = _mne(iform_field_type_id=1, field_label=field_label)
	elem['string_format_type'] = 1
	elem['max_value'] = 20
	return elem

def make_ssnfield(field_label=''):
	elem = _mne(iform_field_type_id=1, field_label=field_label)
	elem['string_format_type'] = 2
	elem['max_value'] = 15
	return elem
	
def make_zipfield(field_label=''):
	elem = _mne(iform_field_type_id=1, field_label=field_label)
	elem['string_format_type'] = 3
	elem['max_value'] = 15
	return elem

def make_datefield(field_label=''):
	elem = _mne(iform_field_type_id=1, field_label=field_label)
	elem['string_format_type'] = 4
	elem['max_value'] = 20
	return elem
