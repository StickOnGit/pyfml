"""Dicts for reorder.py to use for determining the correct HTML tags
for auto-generating a narrative.

Intended to be used with an element's iform_field_type_id as the key.

Since it uses mydict.get(the_key, default_if_no_key) to get the values, we don't need
to list every tag, just everything that shouldn't default to None or an empty string.
Hence the baby dicts with a single value. This just leaves room for expansion in the future."""

_outertags = {1: 'div', 
				2: 'div', 
				3: 'div', 
				5: 'div', 
				7: 'div', 
				8: 'div', 
				9: 'div', 
				11: 'div'}
				
_innertags = {2: 'p', 
				9: 'div', 
				10: 'ul'}
				
_presuftag = {10: 'li'}

_sublisttags = {10: 'span'}

_checkunchecktags = {5: 'div'}