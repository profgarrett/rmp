# Manage PPT Files

# Return an integer value out of a given value.
def parseInt(ss):
	safe = ''
	for s in ss:
		if s.isdigit() or s == '.' or s == '-':
			safe = safe + s
	
	return int(round(float(safe)))


