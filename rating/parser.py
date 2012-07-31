# coding=UTF-8


# Manage PPT Files

from bs4 import BeautifulSoup, NavigableString
import hashlib
import codecs
import Image
import fnmatch
import re
import math


from rating.models import PptJpg
from rating.models import *
from rating.utility import parseInt, prettyString


class HtmlParser:
    PARSE_VERSION = 2  # Way for force updating db on algorithm changes

    def __init__(self, ppt, debug=False):

        # remove the trailing file name from the path.
        path = ppt.get_absolute_filepath()
        path = os.path.dirname(path)

        # Strip trailing slash (if any)
        if path[-1:] == '/' or path[-1:] == '\\':
            path = path[:-1]
       
        if not os.path.exists(path):
            raise Exception('Path %s does not exist.' % (path))
        
        self.ppt = ppt
        self.path = path  # Where is the folder?
        self.debug = debug  # print debug statements?
        
        # JPG
        try:
            if ppt.jpg_export_status == '2' and (debug or ppt.jpg_parse_version is None or ppt.jpg_parse_version < self.PARSE_VERSION):
                if os.path.exists(self.path + '/jpg'):
                    self.parseJPG(ppt, self.path + '/jpg/')
                    ppt.jpg_parse_version = self.PARSE_VERSION
                else:
                    ppt.jpg_parse_version = -1
                
                ppt.save()

        except Exception as err:
            ppt.jpg_parse_version = -1
            raise

        # HTML
        try:
            if ppt.html_export_status == '2' and (debug or ppt.html_parse_version is None or ppt.html_parse_version < self.PARSE_VERSION):
                if os.path.exists(self.path + '/html_files'):
                    self.parseHTML(ppt, self.path + '/html_files/')
                    ppt.html_parse_version = self.PARSE_VERSION
                else:
                    ppt.html_parse_version = -1
                
                ppt.save()

        except Exception as err:
            ppt.html_parse_version = -1
            raise





    ####################
    ## Utility functions
    ####################
    
    # Open a file and return a proper BeautifulSoup object.
    def _open(self, filename):
        if self.debug: self._log('Opening file %s', (filename,))
        # Try to fix encoding issue.  PPT appears to use meta tag saying that it uses CP1252
        fh = codecs.open(filename, 'r', 'windows-1252', errors='ignore')

        html = fh.read()
        #html = html.encode('utf-8') # database default encoding.
        # use html5lib to avoid problems with img tags not being self-closing.
        return BeautifulSoup(html, 'html5lib', from_encoding="windows-1252")

    # Used to track logs for the process.
    # On Windows, the console can onlu read ASCII characters, so strip out unicode.
    def _log(self, s, tup, error=False):
        
        #encode arguments and formatting string
        args = []
        ascii = self._ascii(s)  # unicode(s, 'UTF-8').encode('ascii', 'ignore')
        for i in range(len(tup)):
            if hasattr(tup[i], 'encode'):
                # String
                args.append(self._ascii(tup[i]))
            else:
                # integer / long
                args.append(tup[i])
        
        if self.debug:
            print ascii % tuple(args)
    
    # Return a safe ascii string for printing to the console.
    def _ascii(self, arg):
        
        if isinstance(arg, unicode):
            return arg.encode('ascii', 'ignore')
        else:
            return arg.decode('ascii', 'ignore')
    
    def _parseSrc(self, img):
        
        if 'src' in img.attrs:
            return img.attrs['src']
        
        self.log('Error: img without src for %s', (img), True)
        return ''
    
    def _getHash(self, path):
        f = open(path, 'rb')
        block_size = 2 ** 14
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        f.close()
        return md5.hexdigest()
    
    def _getMD5(self, text):
        md5 = hashlib.md5()
        text = re.sub(r'\W+', '', text)  # no non-alphanum (eg unicode)
        md5.update(text)
        return md5.hexdigest()

    # Calculate image entropy.  Many thanks to example code from
    #  http://brainacle.com/calculating-image-entropy-with-python-how-and-why.html
    def _image_entropy(self, img):
        histogram = img.histogram()
        histogram_length = sum(histogram)

        samples_probability = [float(h) / histogram_length for h in histogram]

        return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])
        
    # Update the passed model with the image properties.
    def _parseImage(self, path, filename, model):
        try:
            model.filename = filename
            imagepath = path + filename
            
            model.size = os.path.getsize(imagepath)
            model.md5 = self._getHash(imagepath)
            
            image = Image.open(imagepath)
            model.entropy = self._image_entropy(image)
            model.width = image.size[0]
            model.height = image.size[1]
            
        except IOError as detail:
            # Invalid image format, e.g., wmz or some other strange thing
            if detail.args[0] != 'cannot identify image file':
                self._log('_parseImage Error %s', (detail), True)

    # Recurively searches for instances of text inside of the html page.
    #
    # Creates the string entries.
    #
    # @bs_stack The current item being examinaged.
    # @parent_pos The left, hight, width, and top attributes for the parent.  None if not set.
    def _parseText(self, pptHtmlPage, bs, w=None, l=None, t=None, h=None):

        if w == None or h == None or l == None or t == None:
            # Set to 100% of screen for initial container.
            w = h = 100
            t = l = 0

        elif not bs.name[0] == 'v':
            # Find if there's a size for this object as long as it's not a v object (custom IE stuff)
            new_pos = self._parsePosition(bs)

            # Reduce size of this object based upon the size of the containing object.
            if not new_pos == None:
                
                # Left & top are:
                #   1. Scaled to the percentage of the container's width/height
                #   2. Added to the existing left/top from the container.
                l = l + int(round(new_pos['left'] * w / 100, 0))
                t = t + int(round(new_pos['top'] * h / 100, 0))

                # Width & Height are set to the % of the container width & height
                w = int(round(w * new_pos['width'] / 100, 0))
                h = int(round(h * new_pos['height'] / 100, 0))

                # Don't allow objects to extend beyond sides of screen
                if w + l > 100:
                    w = w - (l + w - 100)
                if t + h > 100:
                    h = h - (t + h - 100)

        # Is this a string or does it contain strings?
        for node in bs.children:
            if isinstance(node, NavigableString):
                # Create a new text node.

                # strip out unwanted line break characters, html bullet points, and leading/trailing spaces.
                text = node.replace('\r', '').replace('\n', '').replace('&#13;', '').replace(u'•', '').replace(u'\xe2', u'').strip()
                
                # filter out html comments, xml [blacked] items, and where there's no text.
                if  not ( text[0:4] == '<!--' and text[-3:] == '-->') and \
                    not ( len(text) < 1) and \
                    not ( text[0] == '[' and text[-1] == ']' ):

                    # See if an existing text with these same dimensions exists.  If so, add this text
                    # to that text instead of creating a new object.  This happens when several spans
                    # are inside of an object with set dimensions.
                    pptHtmlPageTexts = PptHtmlPageText.objects.filter(ppthtmlpage_id=pptHtmlPage.id,
                            pos_top=t, pos_left=l, pos_height=h, pos_width=w)

                    if len(pptHtmlPageTexts) > 0:
                        pptHtmlPageText = pptHtmlPageTexts[0]
                        text = pptHtmlPageText.text + " " + text
                        text = text.replace('  ', ' ')
                    else:
                        pptHtmlPageText = PptHtmlPageText()
                        pptHtmlPageText.ppthtmlpage_id = pptHtmlPage.id
                        pptHtmlPageText.pos_top = t
                        pptHtmlPageText.pos_left = l
                        pptHtmlPageText.pos_height = h
                        pptHtmlPageText.pos_width = w

                    pptHtmlPageText.md5 = self._getMD5(text)
                    pptHtmlPageText.text = text
                    
                    pptHtmlPageText.save()
                    self._log('Created PptHtmlPageText %s for %s, %s, [l %s, top %s, wid %s, h %s]', \
                        (pptHtmlPageText.id, pptHtmlPage.id, text, pptHtmlPageText.pos_left, pptHtmlPageText.pos_top, \
                        pptHtmlPageText.pos_width, pptHtmlPageText.pos_height))
            else:
                # Recurse on textual nodes only.
                if not node.name[0:3] == 'src':  # or node.name[0:3] == 'div' or node.name[0:4] == 'span':
                    self._parseText(pptHtmlPage, node, w, l, t, h)
    
    # Return the position of this element in isolation OR None.
    def _parsePosition(self, bs):
        pos = {'width': None, 'left': None, 'top': None, 'height': None}
        
        # Find the position of this element
        if 'style' in bs.attrs:
            for a in bs.attrs['style'].split(';'):
                a = a.split(':')
                a[0] = a[0].lower().strip()
                if a[0] in ['left', 'top', 'width', 'height']:
                    pos[a[0]] = parseInt(a[1])

        if pos['width'] == None or pos['height'] == None or pos['left'] == None or pos['top'] == None:
            return None
        else:
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
            elif fnmatch.fnmatch(fl, 'slide????_background*'):
                images.append(filename)
            elif fnmatch.fnmatch(fl, 'master*_background*'):
                images.append(filename)
            elif fnmatch.fnmatch(fl, 'master*_image*'):
                images.append(filename)
        
        # Delete all old html records in the db.
        #   Do not use references from the htmlimage to related objects, as sometimes id=None
        #   if an error is thrown during parsing (leaving it incomplete)
        PptHtmlImage.objects.filter(ppt_id=ppt.id).delete()
        htmlpages = PptHtmlPage.objects.filter(ppt_id=ppt.id)
        for p in htmlpages:
            PptHtmlPageSrc.objects.filter(ppthtmlpage_id=p.id).delete()
            PptHtmlPagePoint.objects.filter(ppthtmlpage_id=p.id).delete()
            PptHtmlPageText.objects.filter(ppthtmlpage_id=p.id).delete()

        PptHtmlImage.objects.filter(ppt_id=ppt.id).delete()
        htmlpages.delete()

        ### Find Html Image File Properties
        for filename in images:
            
            img = PptHtmlImage()
            img.filename = filename
            img.template = (filename[0:6] == 'master' or 'background.' in filename)  # is this a background image?
            img.vector = img.filename_is_vector()
            img.ppt_id = ppt.id
            self._parseImage(path, filename, img)

            img.save()
            self._log('Parsed PptHtmlImage for %s, %s', (ppt.id, img.filename))
        
        ### begin parsing textual properties
        for filename in pages:
            bs = self._open(path + filename)
            html = bs.prettify()

            pptHtmlPage = PptHtmlPage()
            pptHtmlPage.ppt_id = ppt.id
            pptHtmlPage.filename = filename
            pptHtmlPage.pagetype = 'S'  # slide type
            pptHtmlPage.md5 = self._getMD5(html)
            pptHtmlPage.html = html
            pptHtmlPage.title = ''  # Set by outline parser code
            pptHtmlPage.order = None  # Set by outline parser code.
            pptHtmlPage.save()
            self._log('Parsed PptHtmlPage for %s, %s', (ppt.id, pptHtmlPage.filename))
            
            # Add a link for every image found on the page.
            images = bs.find_all('img')
            for img in images:
                
                src = self._parseSrc(img)
                if src is None or src.strip() == "":
                    continue
                
                pos = self._parsePosition(img)

                # Find matching actual image entry and then add to page.
                pptHtmlImages = PptHtmlImage.objects.filter(ppt_id=ppt.id, filename=src)
                if len(pptHtmlImages) == 1:
                    pptHtmlPageSrc = PptHtmlPageSrc()
                    pptHtmlPageSrc.pos_left = pos['left']
                    pptHtmlPageSrc.pos_top = pos['top']
                    pptHtmlPageSrc.pos_height = pos['height']
                    pptHtmlPageSrc.pos_width = pos['width']
                    pptHtmlPageSrc.ppthtmlpage_id = pptHtmlPage.id
                    pptHtmlPageSrc.ppthtmlimage_id = pptHtmlImages[0].id
                    pptHtmlPageSrc.save()
                    self._log('Parsed pptHtmlPageSrc for %s, %s', (pptHtmlPage.id, src))
                else:
                    self._log('Error finding pptHtmlPageSrc for %s, %s', (pptHtmlPage.id, src), True)

            # Add each text snip
            for slideObj in bs.find_all(id='SlideObj'):
                self._parseText(pptHtmlPage, slideObj)
            
            self._log('Finished parsing file %s', ('',))
        
        ### parse outline ###
        if not outline is None:
            bs = self._open(path + outline)

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
                            pptHtmlPages[0].setjpg()  # now that we have an order, we can find the right jpg file.
                            pptHtmlPages[0].save()
                            slides[order] = pptHtmlPages[0]
                            self._log("Updated pptHtmlPage data from outline = %s, %s", (title, order))
                        else:
                            self._log("ERROR: Unable to find pptHtmlPage %s, %s", (ppt.id, filename), True)

                for bullet in table.find_all('div', 'CTxt'):

                    order = parseInt(bullet.get('id'))  # use to find slide by its order no.
                    i = -1  # track order of bullets

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