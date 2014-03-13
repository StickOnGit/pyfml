"""With any luck at all, moves plist to xml."""
import plistlib as PLIB
import xml.etree.ElementTree as ET
from boxdict import _boxtypes

_formattrib = ['archived', 'available_to_clipboard']
_sectionattrib = ['pull_preference']
_elemattrib = ['is_required', 'hide_from_clipboard', 'placeholder_text', 
				'dynamic_list', 'sub_view_dynamic', 'multiple_selection', 'sub_view_type',
				'min_value', 'max_value', 'default_value', 'slider_precision']
_elemchildren = ['checked_narrative', 'unchecked_narrative', 'popup_values', 'sub_view_list',
					'imageObjData']
_elemtagdict = {1: 'textfield',
				2: 'textbox',
				3: 'popup',
				4: None,
				5: 'checkbox',
				6: None,
				7: 'label',
				8: 'slider',
				9: 'drawing',
				10: 'menu',
				11: 'seg',
				12: 'block'}

_imgpouch = {}
				
_htmldict = {"<":"[", ">":"]"}

_elemattrib = {'is_required': 'req',
				'hide_from_clipboard': 'noclip', 
				'dynamic_list': 'edit'}
				
_elemchildren = {'checked_narrative':'block', 
					'unchecked_narrative':'no', 
					'popup_values':'list', 
					'sub_view_list': 'sublist',
					'imageObjData':'img'}
					
_badvalues = [None, 0, '0']

_prefabboxes = {}
for k, v in _boxtypes.iteritems():
	"""Reverses the order of key-value pairs in the boxtypes
	and place them in _prefabboxes. Should be in {itpl:xml} order after
	doing this."""
	_prefabboxes[v] = k
				
def picky_dict(plistsection, sorter):
	"""I don't remember why this is here."""
	returnDict = {}
	for data in sorter:
		maybedata = plistsection.get(data, None)
		if maybedata is not None:
			maybedata = sorter.get(maybedata)
			returnDict[data] = maybedata
	if returnDict:
		return returnDict

def xml_shell_from_plist(dict):
	"""Creates the tree and root for an XML document.
	The root is the actual form tags <iEHR>, etc. The tree
	is a parent object to the form that is needed to save the file."""
	newRoot = ET.Element('iEHR')
	newShell = ET.ElementTree(newRoot)
	newdata = {}
	for attr in _formattrib:
		maybedata = dict.get(attr, None)
		if maybedata is not None:
			newdata[attr] = maybedata
		#newdata[attr] = dict.get(attr, 'default_xmlshell_attr')
	newRoot.text = dict.get('template_name', 'Default Form Name')
	##turn_into_fml(newdata)
	newShell.attrib = newdata
	return newShell
	
def xml_section_from_plist(formshell, sectiondict):
	"""Creates new section for XML form from loaded itpl data."""
	newdata = {}
	newSection = ET.SubElement(formshell.getroot(), 'box')
	maybeprefab = sectiondict.get('mp_box_type', None)
	if maybeprefab is not None:
		try:
			maybeprefab = int(maybeprefab)
		except:
			raise TypeError("Couldn't change %s box_type to int." % maybeprefab)
		newSection.tag = _prefabboxes.get(maybeprefab, '**ERROR**')
		newSection.text = None
		newSection.attrib = {}
	else:
		for attr in _sectionattrib:
			maybedata = sectiondict.get(attr, None)
			if maybedata is not None:
				newdata[attr] = maybedata
		newSection.text = sectiondict.get('iform_section', {}).get('section_name', 'Default Section Name')
		##turn_into_fml(newdata)
		newSection.attrib = newdata
	return newSection
	
def xml_elem_from_plist(parentsection, elemdict):
	"""Creates new subelements for sections based on itpl data."""
	newattrs = {}
	newchildren = {}
	elemTagKey = elemdict.get('iform_field_type_id', 'default_fieldtype_id')
	elementkind = _elemtagdict.get(int(elemTagKey), 'error')
	newElem = ET.SubElement(parentsection, elementkind)
	newElem.text = elemdict.get('field_label', 'Default Element Name')
	for attr in _elemattrib:
		fmlattr = _elemattrib.get(attr, attr)
		maybeattr = elemdict.get(attr, None)
		if maybeattr not in _badvalues:
			newattrs[fmlattr] = maybeattr
	for child in _elemchildren:
		fmlchild = _elemchildren.get(child, child)
		maybechild = elemdict.get(child, None)
		if maybechild not in _badvalues:
			newchildren[fmlchild] = maybechild
	newElem.attrib = newattrs
	if newchildren:
		#print newchildren
		for k, v in newchildren.iteritems():
			if k is not None and v not in _badvalues:
				newChild = ET.SubElement(newElem, k)
				newChild.text = v
	return newElem
	
def idtag(xmlsection, formplist):
	"""Looks for an mp_uuid, and if it finds one, creates the id element to
	append to that element/section/form."""
	maybeid = formplist.get('mp_uuid', None)
	if maybeid is not None:
		newmpid = ET.Element(tag='id', attrib={'mp_uuid': maybeid})
		#print "success!! mpuuid made!!"
		return newmpid
	else:
		#print "Didn't find an id in %s." % xmlsection.text
		pass
		
		

def plist_to_xml(plistform):
	"""Turns the itpl file into xml."""
	newForm = xml_shell_from_plist(plistform)
	for plistsection in plistform.get('iformSectionTiesArray', []):
		newSection = xml_section_from_plist(newForm, plistsection)
		for plistelement in plistsection.get('iform_section', {}).get('iformFieldsArray', []):
			#print "about to work with: ", plistelement.get('field_label', 'Nameless Thing')
			newElem = xml_elem_from_plist(newSection, plistelement)
			elemID = plistelement.get('mp_uuid', None)
			if elemID is not None:
				newElem.append(idtag(newElem, plistelement))
		sectionid = plistsection.get('iform_section', None)
		if sectionid is not None:
			newSection.append(idtag(newSection, sectionid))
	formRoot = newForm.getroot()
	formRoot.append(idtag(formRoot, plistform))
	return newForm
	
def dict_val_to_str(somedict):
	"""Converts ints to strings, since apparently xml.eteee.ElementTree
	dislikes smoke and integers.
	Only needed when saving an FML/XML file -- NOT for plist/itpl."""
	for k, v in somedict.iteritems():
		if isinstance(v, (int, PLIB.Data)):
			somedict[k] = str(v)
	else: pass

def plist_val_to_str(plist):
	"""Before saving, use this to convert form attributes
	from ints to strs."""
	dict_val_to_str(plist)
	for section in plist.get('iformSectionTiesArray', []):
		dict_val_to_str(section)
		for elem in section.get('iform_section', {}).get('iformFieldsArray', []):
			dict_val_to_str(elem)
			
def tag_to_square(formpart, translator):
	"""Changes all instances of html characters that seem to befuddle
	ElementTree's ability to parse the plist data.
	
	RUN THIS BEFORE PLIST_VAL_TO_STR. It uses type-checking to
	ensure it is changing values that 'should' be changed. While
	it probably doesn't break anything to do it the other
	way around, let's not tempt fate."""
	for name, content in formpart.items():
		if isinstance(content, basestring):
			newString = content
			for htmlval, newchar in translator.items():
				#print "looking for %s, changing to %s".format(htmlval, newchar)
				newString = newString.replace(htmlval, newchar)
			if newString != content:
				formpart[name] = newString
		else: pass
			
def plist_escape_html(plist):
	"""Changes string HTML to a different token.
	ElementTree chokes on HTML in plist strings, so it's important
	to do this when going from itpl to FML."""
	sections = plist.get('iformSectionTiesArray', [])
	for section in sections:
		tag_to_square(section, _htmldict)
		for element in section.get('iform_section', {}).get('iformFieldsArray', []):
			tag_to_square(element, _htmldict)
			
def pull_imgs(plistform):
	#found_imgs = 0
	#imgkey = 'mpimg'
	for section in plistform.get('iformSectionTiesArray', []):
		for element in section.get('iform_section', {}).get('iformFieldsArray', []):
			maybedrawing = element.get('iform_field_type_id')
			if maybedrawing == 9:		##extra step? will other things use this field?
				maybedata = element.get('imageObjData')
				if maybedata is not None:
					#found_imgs += 1
					#keyname = imgkey + str(found_imgs)
					keyname = id(maybedata)
					_imgpouch[keyname] = maybedata
					##now delete/overwrite old image in plist with the imgkey name here and replace
					##it on saving it. somehow. etree hates plistlib.Data() objects so i dunno.
					##in FML file... img="some_string" + the id? to ensure it gets seen?
					

	
def test(file='itpl/LW Chiro SOAP.itpl'):
	myP = PLIB.readPlist(file)
	myF = plist_to_xml(myP).getroot()
	return myF