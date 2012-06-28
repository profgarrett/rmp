# Manage PPT Files

# Return an integer value out of a given value.
def parseInt(ss):
	safe = ''
	for s in ss:
		if s.isdigit() or s == '.' or s == '-':
			safe = safe + s
	
	return int(round(float(safe)))


# Remove all newlines and odd characters from a string
def prettyString(s):
	
	# remove linebreaks
	s = s.replace('\r','').replace('\n','')
	
	# tabs
	s = s.replace('\t',' ')

	# remove double spaces
	i = len(s)
	s = s.replace('  ', ' ')
	
	while len(s) < i:
		i = len(s)
		s = s.replace('  ', ' ')

	# trim
	return s.strip()