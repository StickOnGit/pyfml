"""I really don't remember why this is a thing. I just don't want to undo it"""
def find_section_in_form(section, form):
	searcharea = form['iformSectionTiesArray']
	for i in range(0, len(searcharea)):
		if searcharea[i]['iform_section']['section_name'] == section:
			return i