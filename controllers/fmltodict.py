"""Dictionaries to 'translate' FML terms into the correct names for the DB.
Keys are 'fml' terms, values are .itpl terms.
A good example is _xmlcheckbox: 'on' is the fml term, 'checked_narrative'
is the .itpl term. this script will see the fml term and replace it with
the .itpl term."""

import elems as _els

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

_xmlid = {
	"id": "mp_uuid"
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
	"date": _xmltextfield,
	"id": _xmlid
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
	"date": _els.make_datefield,
	"id": "id"
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