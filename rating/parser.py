# Manage PPT Files

from bs4 import BeautifulSoup, NavigableString
import urllib, string
import urllib2
import cookielib
import mechanize
import time
import random, os, re
import fnmatch, os, sys, zipfile
import Image # PIL
import hashlib
import codecs

from rating.models import PptJpg
from rating.models import *
from rating.utility import parseInt, prettyString

class HtmlParser:
	PARSE_VERSION = 1 # Way for force updating db on algorithm changes
	
	def __init__(self, ppt, path, debug=False):
		self.ppt = ppt
		self.path = path # Where is the html folder?
		self.debug = debug # print debug statements?
		
		# Strip trailing slash
		if self.path[-1:] == '/' or self.path[-1:] == '\\':
			self.path = self.path[:-1]
		
		if not os.path.exists(self.path):
			raise Exception('Path %s does not exist.' % (self.path))
		
		# Find uploaded files.
		for p in PptUploadedFile.objects.filter(ppt_id=ppt.id):
			
			if p.jpg_export_status == '2' and (debug or p.jpg_parse_version < self.PARSE_VERSION):
				if os.path.exists(self.path+'/jpg'):
					self.parseJPG(ppt, self.path+'/jpg/')
					p.jpg_parse_version = self.PARSE_VERSION
					p.save()

			if p.html_export_status == '2' and (debug or p.html_parse_version < self.PARSE_VERSION):
				if os.path.exists(self.path+'/html_files'):
					self.parseHTML(ppt, self.path+'/html_files/')
					p.html_parse_version = self.PARSE_VERSION
					p.save()
				




	####################
	## Utility functions
	####################
	
	# Open a file and return a proper BeautifulSoup object.
	def _open(self, filename):
		# Try to fix encoding issue.  PPT appears to use meta tag saying that it uses CP1252
		fh = codecs.open(filename,'r', 'windows-1252')
		html = fh.read()
		#html = html.encode('utf-8') # database default encoding.
		# use html5lib instead of default to avoid problems with img tags not being self-closing.
		return BeautifulSoup(html, 'html5lib', from_encoding="windows-1252") 

	# Used to track logs for the process.
	# Note that on Windows, the console can onlu read ASCII characters, so strip out unicode.
	def _log(self, s, tuple, error=False):
		s = s.encode('ascii', 'ignore') % tuple
		if self._debug:
			print s


	def _parseSrc(self, img):
		
		if 'src' in img.attrs:
			return img.attrs['src']
		
		self.log('Error: img without src for %s', (img), True)
		return '' 
	
	def _getHash(self, path):
		f = open(path, 'rb')
		block_size=2**14
		md5 = hashlib.md5()
		while True:
			data = f.read(block_size)
			if not data:
				break
			md5.update(data)
		f.close()
		return md5.hexdigest()
	
	def _getMD5(self, text):
		block_size=2**14
		md5 = hashlib.md5()
		text = re.sub(r'\W+','', text) # remove all non alphanum characters to reduce unicode 
		md5.update(text)
		return md5.hexdigest()
	
	
	# source http://stackoverflow.com/questions/379906/python-parse-string-to-float-or-int
	#_parseStr = lambda x: x.isalpha() and x or x.isdigit() and \
	#	int(x) or x.isalnum() and x or \
	#	len(set(string.punctuation).intersection(x)) == 1 and \
	#	x.count('.') == 1 and float(x) or x
	
	# safe way of parsing integer values that may have string elements mixed in (such as % )
	
	
	# Recursively parse out the position from the beautifulsoup element passed.
	# Uses algorithm of return min left, min top, max width, max height
	# Note that once we get a position, the results will be returned.
	# This is a result of some divs not having a position, but relying upon contained spans
	# 	whose left/top/right/bottom must be combined. 
	#	However, other divs have position, and their contained spans are positioned relatively
	#	and % refers to the div, not the entire page.
	#
	# Currently, this is flawed.  Need to write in the opposite direction following:
	# Find child node
	# Goto parent until root doing
	# 	If position, then save
	#	If already had position, and both are absolutely positioned, then
	#		change child position to be the % of the parent position.
	def _parsePosition(self, bs, pos=None):
		
		# See if the top-left corner or bottom-right corner are outside existing pos
		def set(o1, o2, width, left):
			
			# Make sure we have 2 valid sets of positions.
			if o1[width] is None or o1[left] is None:
				return o2[width], o2[left]
			elif o2[width] is None or o2[left] is None:
				return o1[width], o1[left]
			
			# Set left
			if o1[left] < o2[left]:
				new_left = o1[left]
			else:
				new_left = o2[left]

			# Now that we have left, we can set width.
			if o1[width]+o1[left] > o2[width]+o2[left]:
				new_width = o1[width]+o1[left]-new_left
			else:
				new_width = o2[width]+o2[left]-new_left

			return new_width, new_left

		new_pos = {'width': None, 'left': None, 'top': None, 'height': None } 
		
		# Find the position of this element
		if 'style' in bs.attrs:
			for a in bs.attrs['style'].split(';'):
				a = a.split(':')
				a[0] = a[0].lower().strip()
				if a[0] in ['left', 'top', 'width', 'height']: new_pos[a[0]] = parseInt(a[1])

		if pos == None:
			# Set initial values to the dom object and continue.
			pos = new_pos
		else:
			pos['width'], pos['left'] = set(pos, new_pos, 'width','left')
			pos['height'], pos['top'] = set(pos, new_pos, 'height','top')

		
		# If we don't have a position, recursively search.
		# This is slightly complicated because we may have the following:
		## Div -> div.style -> span.style
		#  We want the divs, but not the span style, because it's relative to the div, and not the page.
		# But, we still need to have this work
		# Div -> [span.style, span.style]
		# And this,
		# Div -> [ div-> [span.style, span.style], div.style, div.style ]
		# So, the compromise is to stop recursing once we get a position, but to always iterate through
		# the current level completely.
		if pos['width'] == None or pos['left'] == None or pos['top'] == None or pos['height'] == None:
			# Search direct child nodes.
			for node in bs.children:
				if not isinstance(node, NavigableString):
					self._parsePosition(node, pos)
		
		for p in pos:
			# ensure that position is never less than 0, or greater than 100
			if pos[p] is None: continue
			if pos[p] < 0: pos[p] = 0
			if pos[p] > 100: pos[p] = 100
		
		# make sure we don't run off of the side of the screen.
		if pos['width']+pos['left'] > 100:
			pos['width'] = 100 - pos['left']

		if pos['height']+pos['top'] > 100:
			pos['height'] = 100 - pos['top']

		return pos
	
	
	####################
	## Parsing functions
	####################
	
	# Parse out the jpg files for the given presentation
	def parseJPG(self, ppt, path):
		files = os.listdir(path)
		
		# Delete all old JPG records in the db.
		[jpg.delete() for jpg in PptJpg.objects.filter(ppt_id=ppt.id)]

		for i in files:
			if not i[-4:] == '.JPG': continue
			
			jpg = PptJpg()
			jpg.ppt_id = ppt.id
			jpg.filename = i
			self._parseImage(path, i, jpg)
			jpg.save()
			self._log('Parsed PptJpg for %s, %s', (ppt.id, jpg.filename))
	
	
	# Update the passed model with the image properties.
	def _parseImage(self, path, filename, model):
		try:
			model.filename = filename
			imagepath = path+filename
			
			model.size = os.path.getsize(imagepath)
			model.md5 = self._getHash(imagepath)
			
			image = Image.open(imagepath)
			model.width = image.size[0]
			model.height = image.size[1]
			
		except IOError as detail:
			# Invalid image format, e.g., wmz or some other strange thing
			if detail.args[0] != 'cannot identify image file':
				self._log('_parseImage Error %s', (detail), True)
	
	
	def parseHTML(self, ppt, path):
		# Find Html Files 
		files = os.listdir(path)
		
		outline = None
		pages = []
		images = []
		
		for filename in files:
			fl = filename.lower()
			if fnmatch.fnmatch(fl, 'outline.htm'):
				outline = filename
			if fnmatch.fnmatch(fl, 'slide????.htm'):
				pages.append(filename)
			elif fnmatch.fnmatch(fl, 'slide????_image*'):
				images.append(filename)
			elif fnmatch.fnmatch(fl, 'master*_background*'):
				images.append(filename)
			elif fnmatch.fnmatch(fl, 'master*_image*'):
				images.append(filename)
		
		# Delete all old html records in the db.
		PptHtmlImage.objects.filter(ppt_id=ppt.id).delete()
		for p in PptHtmlPage.objects.filter(ppt_id=ppt.id):
			if not p.id == None:
				id = p.id
				[p.delete() for p in p.ppthtmlpagepoint_set.all()]
				[p.delete() for p in p.ppthtmlpagesrc_set.all()]
				[p.delete() for p in p.ppthtmlpagetext_set.all()]
				p.delete()


		### Find Html Image File Properties
		for filename in images:
			
			img = PptHtmlImage()
			img.template = (filename[0:6] == 'master') # is this a background image?
			img.ppt_id = ppt.id
			img.filename = filename
			self._parseImage(path, filename, img)

			img.save()
			self._log('Parsed PptHtmlImage for %s, %s', (ppt.id, img.filename))
		

		### begin parsing textual properties
		for filename in pages:
			bs = self._open(path+filename)
			html = bs.prettify()

			pptHtmlPage = PptHtmlPage()
			pptHtmlPage.ppt_id = ppt.id
			pptHtmlPage.filename = filename 
			pptHtmlPage.pagetype = 'S'  # slide type
			pptHtmlPage.md5 = self._getMD5(html)
			pptHtmlPage.html = html
			pptHtmlPage.title = '' # Set by outline parser code
			pptHtmlPage.order = None # Set by outline parser code. 
			pptHtmlPage.save()
			self._log('Parsed PptHtmlPage for %s, %s', (ppt.id, pptHtmlPage.filename))
		
			
			# Add a link for every image found on the page.
			images = bs.find_all('img')
			for img in images:
				
				src = self._parseSrc(img)
				if src is None:
					continue
				
				pos = self._parsePosition(img)

				# Find matching actual image entry and then add to page.
				pptHtmlImage = PptHtmlImage.objects.get(ppt_id=ppt.id, filename=src)
				pptHtmlPageSrc = PptHtmlPageSrc()
				pptHtmlPageSrc.pos_left = pos['left']
				pptHtmlPageSrc.pos_top = pos['top']
				pptHtmlPageSrc.pos_height = pos['height']
				pptHtmlPageSrc.pos_width= pos['width']
				pptHtmlPageSrc.ppthtmlpage_id = pptHtmlPage.id 
				pptHtmlPageSrc.ppthtmlimage_id = pptHtmlImage.id
				pptHtmlPageSrc.save()
				self._log('Parsed pptHtmlPageSrc for %s, %s', (pptHtmlPage.id, src ))
			
			
			def text_filter(tag):
				if not tag.name == 'div': return False

				if tag.has_key('class'):  # Listing every possibility getting too hard to do.
					if 'O' in tag['class']: return True # Bullet point
					if 'CT' in tag['class']: return True # Title 
					if 'CB' in tag['class']: return True # Sub-title 
					if 'T' in tag['class']: return True # Sub-title side bold? 
					if 'B' in tag['class']: return True # Sub-title side bold? 
					if 'B1' in tag['class']: return True # Sub-point bold.
				return False
			
			# Add each text snip
			divs = bs.find_all(text_filter)
			for d in divs:
				text = d.get_text()
				text = text.replace('\r','').replace('\n','').strip().encode('utf-8')
				
				if len(text) > 0:
					pptHtmlPageText = PptHtmlPageText()
					pptHtmlPageText.ppthtmlpage_id = pptHtmlPage.id
					pptHtmlPageText.md5 = self._getMD5(text)
					pptHtmlPageText.text = text
					pos = self._parsePosition(d)
					pptHtmlPageText.pos_top = pos['top']
					pptHtmlPageText.pos_left = pos['left']
					pptHtmlPageText.pos_height = pos['height']
					pptHtmlPageText.pos_width= pos['width']
					
					pptHtmlPageText.save()
					self._log('Created PptHtmlPageText for %s, %s', (pptHtmlPage.id, text))
			
			self._log('Finished parsing file %s', ('',))
		


		### parse outline ###
		if not outline is None:
			bs = self._open(path+outline)

			# Cache of slide ids to relate the titles to the bullets (which are in different parts of the html)
			slides = {}

			# Restrict search to just the table.
			for table in bs.find_all(id='OtlObj'):

				# Find the titles of each slide.
				for link in table.find_all('div', 'PTxt'):

					# Title of slide.
					title = prettyString(link.text)
					order = parseInt(link.get('id'))

					# find the filename from the single a link.
					for a in link.find_all('a')[0:1]:
						
						# Parse out slide0001.htm from the javascript code in href.
						filename = a.get('href') 
						regfilename = re.search("(slide\d{4}.htm)", filename)
						if regfilename is None:
							continue
						else:
							filename = regfilename.group()

						# Find the matching htmlpage & update its title & order
						pptHtmlPages = PptHtmlPage.objects.filter(ppt_id=ppt.id, filename=filename)
						if len(pptHtmlPages) > 0:
							pptHtmlPages[0].order = order
							pptHtmlPages[0].title = title
							pptHtmlPages[0].setjpg() # now that we have an order, we can find the right jpg file.
							pptHtmlPages[0].save()
							slides[order] = pptHtmlPages[0]
							self._log("Updated pptHtmlPage data from outline = %s, %s", (title, order))
						else:
							self._log("ERROR: Unable to find pptHtmlPage %s, %s", (ppt.id, filename), True)

				for bullet in table.find_all('div', 'CTxt'):

					order = parseInt(bullet.get('id')) # use to find slide by its order no.
					i = -1 # track order of bullets

					for li in bullet.find_all('li'):

						text = prettyString(li.text)
						i = i + 1

						# find matching slide
						if order not in slides:
							self._log("ERROR: Unable to find slide for bullet %s, %s", (order, text), True)
							continue
						else:
							slide = slides[order]

						pptHtmlPagePoint = PptHtmlPagePoint()
						pptHtmlPagePoint.ppthtmlpage_id = slide.id
						pptHtmlPagePoint.text = text
						pptHtmlPagePoint.order = i
						pptHtmlPagePoint.save()
						self._log("Created PptHtmlPagePoint %s, %s, %s", (pptHtmlPagePoint.id, text, order))


		self._log("Finished parsing html export %s",("",)) 




