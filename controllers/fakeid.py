"""Valid mp_uuid generator."""

from random import choice

_ENCODER = "0123456789ABCDEF"
_DASHLIST = [8, 13, 18, 23]
_MPID = 'mp_uuid'
_INSECTION = 'iform_section'
_ELEMENTLIST = 'iformFieldsArray'

def give_id():
	"""Generates an mp_uuid.
	Please only bestow an id if the object DOES NOT HAVE ONE."""
	newid = u''
	for i in range(0, 36):
		if i in _DASHLIST:
			newid += '-'
		else:
			newid += choice(_ENCODER)
	return newid

def id_wrap(id_func):
	"""Wrapper for the uuid creating function.
	This keeps track of which ids were produced, on the
	very, very, very, very slim chance two are alike."""
	def inner():
		"""The actual workhorse!"""
		newid = id_func()
		while newid in all_ids:
			newid = id_func()
		all_ids.append(newid)
		return newid
	all_ids = []
	return inner

def fake_id(pyform):
	"""Assigns new mp_uuids to form, section, and elements.
	Checks to ensure mp_uuid is not present before assigning.
	
	On the extreeeeeme outside chance that it generates the same
	mp_uuid twice for one form, holds them in an array and makes sure
	all newly generated IDs are unique until the form is done."""
	if not pyform.get(_MPID, False):
		pyform[_MPID] = give_id()
	for section in pyform.get('iformSectionTiesArray', []):
		if not section.get(_MPID, False):
			section[_MPID] = give_id()
		else: pass
		for element in section.get(_INSECTION, {}).get(_ELEMENTLIST, []):
			if not element.get(_MPID, False):
				element[_MPID] = give_id()
			else: pass
	else: pass
	
give_id = id_wrap(give_id)		##wraps give_id