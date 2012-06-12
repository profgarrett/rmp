# Manage PPT Files

from bs4 import BeautifulSoup
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
from rating.utility import parseInt

class HtmlParser:
	
	def __init__(self, ppt, path, debug=False):
		self.ppt = ppt
		self.path = path # Where is the html folder?
		self.debug = debug # print debug statements?
		
		if self.path[-1:] == '/' or self.path[-1:] == '\\':
			self.path = self.path[:-1]
		
		if not os.path.exists(self.path):
			raise Exception('Path %s does not exist.' % (self.path))
		
		# Find Jpg Files 
		if os.path.exists(self.path+'/jpg'):
			self.parseJPG(ppt, self.path+'/jpg/')
		
		# Find html files
		if os.path.exists(self.path+'/html_files'):
			self.parseHTML(ppt, self.path+'/html_files/')
	
	
	####################
	## Utility functions
	####################
	
	def _parseSrc(self, img):
		
		if 'src' in img.attrs:
			return img.attrs['src']
		
		if self.debug: print 'Error: img without src for ', img 
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
	def _parsePosition(self, bs, pos=None):
		
		if pos == None:
			pos = {'width': None, 'left': None, 'top': None, 'height': None } 
		
		if 'style' in bs.attrs:
			attrs = bs.attrs['style'].split(';')
			
			for a in attrs:
				a = a.split(':')
				a[0] = a[0].lower().strip()
				for p in pos:
					if p in a[0]:
						i = parseInt(a[1])
						if a[0] in ['width', 'height'] and (pos[a[0]] is None or i > pos[a[0]]):
							pos[a[0]] = i
						if a[0] in ['left', 'top'] and (pos[a[0]] is None or i < pos[a[0]]):
							pos[a[0]] = i
		
		# recursively scan descendents that have a style.
		for bssub in bs.find_all(style=re.compile('left')):
			self._parsePosition(bssub, pos)
		
		return pos
	
	
	####################
	## Parsing functions
	####################
	
	# Parse out the jpg files for the given presentation
	def parseJPG(self, ppt, path):
		PARSE_VERSION = 1 # Way for force updating db on algorithm changes
		files = os.listdir(path)
		
		for i in files:
			if not i[-4:] == '.JPG': continue
			
			# Exists?
			jpg = PptJpg.objects.filter(ppt_id=ppt.id,filename=i)
			if jpg.count() > 0 and jpg[0].parseVersion == PARSE_VERSION:
				if self.debug: print 'Already processed PptJpg for ' + str(ppt.id) + ' - ' + jpg[0].filename
				continue
			
			# Create/filter
			if jpg.count() > 0:
				jpg = jpg[0]
			else:
				jpg = PptJpg()
			
			# Update
			jpg.ppt_id = ppt.id
			jpg.filename = i
			self._parseImage(path, i, jpg)
			jpg.parseVersion = PARSE_VERSION
			jpg.save()
			if self.debug: print 'Parsed PptJpg for ' + str(ppt.id) + ' - ' + jpg.filename
	
	
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
			if self.debug: print detail
			if detail.args[0] != 'cannot identify image file':
				print ('ERROR: ', detail)
	
	
	def parseHTML(self, ppt, path):
		PARSE_VERSION = 1 # Way for force updating db on algorithm changes
		# Find Html Files 
		files = os.listdir(path)
		
		pages = []
		images = []
		
		for filename in files:
			fl = filename.lower()
			if fnmatch.fnmatch(fl, 'slide????.htm'):
				pages.append(filename)
			elif fnmatch.fnmatch(fl, 'slide????_image*'):
				images.append(filename)
			elif fnmatch.fnmatch(fl, 'master*_background*'):
				images.append(filename)
			elif fnmatch.fnmatch(fl, 'master*_image*'):
				images.append(filename)
		
		### Find Html Image File Properties
		for filename in images:
			
			# Exists?
			img = PptHtmlImage.objects.filter(ppt_id=ppt.id,filename=filename)
			if img.count() > 0 and img[0].parseVersion == PARSE_VERSION:
				if self.debug: print 'Already processed PptHtmlImage for ' + str(ppt.id) + ' - ' + img[0].filename
				continue
			
			# New or exists?
			if img.count() > 0:
				img = img[0]
			else:
				img = PptHtmlImage()
			
			# Update
			img.ppt_id = ppt.id
			img.filename = filename
			self._parseImage(path, filename, img)
			img.parseVersion = PARSE_VERSION
			img.save()
			if self.debug: print 'Parsed PptHtmlImage for ' + str(ppt.id) + ' - ' + img.filename
		
		
		### begin parsing textual properties
		for filename in pages:
			#html = open(path+p, 'r').read()
			#html = html.decode('windows-1252')
			
			# Try to fix encoding issue.  PPT appears to use meta tag saying that it uses CP1252
			fh = codecs.open(path+filename,'r', 'windows-1252')
			html = fh.read()
			html = html.encode('utf-8') # DB default encoding.
			bs = BeautifulSoup(html)
			
			
			# Setup html page first.
			# Exists?
			pptHtmlPage = PptHtmlPage.objects.filter(ppt_id=ppt.id,filename=filename)
			if pptHtmlPage.count() > 0 and pptHtmlPage[0].parseVersion == PARSE_VERSION:
				pptHtmlPage = pptHtmlPage[0]
				if self.debug: print 'Already processed PptHtmlPage for ' + str(ppt.id) + ' - ' + pptHtmlPage.filename
			else:
				
				# Update / Create
				if pptHtmlPage.count() > 0:
					pptHtmlPage = pptHtmlPage[0]
				else:
					pptHtmlPage = PptHtmlPage()
				
				# Update information
				pptHtmlPage.ppt_id = ppt.id
				pptHtmlPage.filename = filename 
				pptHtmlPage.pagetype = 'S'  # slide type
				pptHtmlPage.md5 = self._getMD5(html)
				pptHtmlPage.parseVersion = PARSE_VERSION
				pptHtmlPage.html = html
				pptHtmlPage.save()
				if self.debug: print 'Parsed PptHtmlPage for ' + str(ppt.id) + ' - ' + pptHtmlPage.filename
			
			
			
			# Add a link for every image found on the page.
			images = bs.find_all('img')
			for img in images:
				
				src = self._parseSrc(img)
				if src is None:
					continue
				
				pos = self._parsePosition(img)
				
				# Find matching actual image entry and then add to page.
				pptHtmlImage = PptHtmlImage.objects.get(ppt_id=ppt.id, filename=src)
				pptHtmlPageSrc = PptHtmlPageSrc.objects.filter(
						ppthtmlpage_id=pptHtmlPage.id, ppthtmlimage_id=pptHtmlImage.id
				)
				if pptHtmlPageSrc.count() > 0 and pptHtmlPageSrc[0].parseVersion == PARSE_VERSION:
					if self.debug: print 'Already processed PptHtmlPageSrc for ' + str(ppt.id) + ' - ' + src 
					continue
				
				if pptHtmlPageSrc.count() > 0:
					pptHtmlPageSrc = pptHtmlPageSrc[0]
				else:
					pptHtmlPageSrc = PptHtmlPageSrc()
				
				pptHtmlPageSrc.pos_left = pos['left']
				pptHtmlPageSrc.pos_top = pos['top']
				pptHtmlPageSrc.pos_height = pos['height']
				pptHtmlPageSrc.pos_width= pos['width']
				pptHtmlPageSrc.parseVersion = PARSE_VERSION
				pptHtmlPageSrc.ppthtmlpage_id = pptHtmlPage.id 
				pptHtmlPageSrc.ppthtmlimage_id = pptHtmlImage.id
				pptHtmlPageSrc.save()
				if self.debug: print 'Parsed pptHtmlPageSrc for ' + str(pptHtmlPage.id) + ' - ' + src 
			
			
			
			# Add each text snip
			divs = bs.find_all('div', 'O')
			for d in divs:
				text = d.get_text()
				text = text.replace('\r','').replace('\n','').strip().encode('utf-8')
				
				if len(text) > 0:
					pos = self._parsePosition(d)
					md5 = self._getMD5(text)
					
					pptHtmlPageText = PptHtmlPageText.objects.filter(
							md5=md5, ppthtmlpage_id = pptHtmlPage.id, pos_left=pos['left'], pos_top=pos['top']
					)
					if pptHtmlPageText.count() > 0 and pptHtmlPageText[0].parseVersion == PARSE_VERSION:
						if self.debug: print 'Already processed PptHtmlPageText for ' + str(pptHtmlPage.id) + ' - ' + text 
						continue
					
					if pptHtmlPageText.count() > 0:
						pptHtmlPageText = pptHtmlPageText[0]
					else:
						pptHtmlPageText = PptHtmlPageText()
					
					pptHtmlPageText.ppthtmlpage_id = pptHtmlPage.id
					pptHtmlPageText.md5 = md5
					pptHtmlPageText.text = text
					pptHtmlPageText.pos_top = pos['top']
					pptHtmlPageText.pos_left = pos['left']
					pptHtmlPageText.pos_height = pos['height']
					pptHtmlPageText.pos_width= pos['width']
					pptHtmlPageText.parseVersion = PARSE_VERSION
					
					pptHtmlPageText.save()
					if self.debug: print 'Created PptHtmlPageText for ' + str(pptHtmlPage.id) + ' - ' + text
			
			
			if self.debug: print "Finished parsing file"
		
		if self.debug: print "Finished parsing file"




