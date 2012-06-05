import sqlalchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, DateTime, String, ForeignKey, Table, Text, Sequence, MetaData, Unicode
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql://rmp:n29bdbd!!320@3rdrow.woodbury.edu/ppt')
engine.execute('select 1').scalar() ## test connection
Session = sessionmaker(bind=engine)
session = Session()

## Declare Tables

Base = declarative_base()
metadata = MetaData()


## Multi-relationships

#presentation_author = Table('presentation_author', Base.metadata, 
#	Column('presentation_id', Integer, ForeignKey('presentation.id')),
#	Column('author_id', Integer, ForeignKey('author.id'))
#)

presentation_tag = Table('presentation_tag', Base.metadata, 
	Column('presentation_id', Integer, ForeignKey('presentation.id')),
	Column('tag_id', Integer, ForeignKey('tag.id'))
)

unit_tag = Table('unit_tag', Base.metadata, 
	Column('unit_id', Integer, ForeignKey('unit.id')),
	Column('tag_id', Integer, ForeignKey('tag.id'))
)



## Tables


# Organization owning class, conference
class Organization(Base):
	__tablename__ = 'organization'
	#__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	title = Column(String(240))
	description = Column(Text())
	
	units = relationship('Unit', backref='organization')
	
	def __repr__(self):
		return "<Organization ('%s','%s')>" % (self.id, self.title)


# Class, Conference Year
class Unit(Base):
	__tablename__ = 'unit'
	#__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	title = Column(String(240))
	type = Column(String(240)) # Conference, Class, Website
	description = Column(Text())
	url = Column(String(255))
	
	year = Column(String(4))
	month = Column(String(2))
	day = Column(String(2))
	
	tags = relationship('Tag', secondary='unit_tag', backref = 'units')
	
	presentations = relationship('Presentation', backref='unit')
	organization_id = Column(Integer, ForeignKey('organization.id'))
	
	def __repr__(self):
		return "<Unit ('%s','%s')>" % (self.id, self.title)



class Author(Base):
	__tablename__ = 'author'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(240))
	url = Column(String(240))
	peopleid = Column(String(240))
	
	def __repr__(self):
		return "<Author ('%s','%s')>" % (self.id, self.name)


# Tag is a definitional attribute used to sort/organize. For example, tracking disciplines.
class Tag(Base):
	__tablename__ = 'tag'
	#__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	tag = Column(String(240), unique=True)
	
	def __repr__(self):
		return "<Tag ('%s')>" % (self.tag)



# Individual Files
class Presentation(Base):
	__tablename__ = 'presentation'
	__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	filename = Column(String(240))
	url = Column(String(240))
	filetype = Column(String(3))
	htmlfolder = Column(String(255))
	imagefolder = Column(String(255))
	rnd = Column(Integer)
	
	unit_id = Column(Integer, ForeignKey('unit.id'))
	
	tags = relationship('Tag', secondary=presentation_tag, backref = 'presentations')
	
	def __repr__(self):
		return "<PPT ('%s','%s')>" % (self.id, self.filename)



##################################################
# Pearson tables
##################################################


discipline_course = Table('discipline_course', Base.metadata, 
	Column('discipline_id', Integer, ForeignKey('discipline.id')),
	Column('course_id', Integer, ForeignKey('course.id'))
)

course_book = Table('course_book', Base.metadata,
	Column('course_id', Integer, ForeignKey('course.id')),
	Column('book_id', Integer, ForeignKey('book.id'))
)



## Tables

# Discipline table is used as titles in Pearson's websites.
class Discipline(Base):
	__tablename__ = 'discipline'
	__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	url = Column(String(240), nullable=False, unique=True)
	title = Column(String(240))
	
	courses = relationship('Course', secondary=discipline_course, backref = 'disciplines')
	
	def __repr__(self):
		return "<Discipline ('%s','%s', '%s')>" % (self.id, self.url, self.title)


# Course is a title in Pearson's website.
class Course(Base):
	__tablename__ = 'course'
	__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	url = Column(String(240), nullable=False, unique=True)
	title = Column(String(240))
	
	books = relationship('Book', secondary=course_book, backref = 'courses')
	
	def __repr__(self):
		return "<Course ('%s','%s', '%s')>" % (self.id, self.url, self.title)


# Book is a single page with linked resources
# note that one book may have several units, depending on how many 
# bookfile objects were downloaded.
class Book(Base):
	__tablename__ = 'book'
	__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	url = Column(String(240), nullable=False, unique=True)
	title = Column(String(240))
	status = Column(Integer)
	
	unit_id= Column(Integer, ForeignKey('unit.id'))
	unit = relationship('Unit', backref='books')
	
	
	def __repr__(self):
		return "<Book ('%s','%s', '%s')>" % (self.id, self.url, self.title)

# A zip or ppt file downloaded from Pearson.
# Note that there is not a 1-to-1 relationship between a bookfile and a presentation.
# Instead, use the unit table to link the two entities.
# NOTE: these also include non ppt files, such as instructor's manuals.  See the status
# column for the download state
class BookFile(Base):
	__tablename__ = 'bookfile'
	
	id = Column(Integer, primary_key=True)
	supplementISBN10 = Column(String(240))
	supplementISBN13 = Column(String(240))
	leadAuthor = Column(String(240))
	SupplementTitle = Column(String(240))
	edition = Column(String(240))
	copyRightYear = Column(String(240))
	parentISBN10 = Column(String(240))
	parentISBN13 = Column(String(240))
	parentLeadAuthorLastName = Column(String(240))
	parentLeadAuthorFirstName = Column(String(240))
	parentTitle = Column(String(240))
	parentEdition = Column(String(240))
	parentCopyRightYear = Column(String(240))
	fileName = Column(String(240))
	linkText = Column(String(240))
	mediaID = Column(String(240))
	supplementSourceGroupCode = Column(String(240))
	fileFldr = Column(String(240))
	iwPreActions = Column(String(240))
	url = Column(String(240))
	status = Column(Integer) # 0, not downloaded, 1 = error, 2 = downloaded
	rnd = Column(Integer)
	
	book_id = Column(Integer, ForeignKey('book.id'))
	book = relationship('Book', backref='bookfiles')
	
	unit_id= Column(Integer, ForeignKey('unit.id'))
	unit = relationship('Unit', backref='bookfiles')
	
	def __repr__(self):
		return "<bookfile ('%s','%s', '%s')>" % (self.id, self.mediaID, self.fileName)




##################################################
# Moodle information 
##################################################


class MoodleFile(Base):
	__tablename__ = 'moodle'
	__table_args__ = {'extend_existing': True}
	
	id = Column(Integer, primary_key=True)
	words = Column(Integer)
	paras = Column(Integer)
	slides = Column(Integer)
	filename = Column(String(255))
	images = Column(Integer)
	filebytes = Column(Integer)
	imagepixels = Column(Integer)
	imagebytes = Column(Integer)
	slidesasjpg = Column(Integer)
	courseid = Column(Integer)
	course = Column(String(255))
	year = Column(String(4))
	term = Column(String(2))
	graduate = Column(Integer)
	discipline = Column(String(255))
	subdiscipline = Column(String(255))
	enrollment = Column(Integer)
	fac = Column(Integer)
	facid = Column(String(20))
	faccourses = Column(Integer)
	facslides = Column(Integer)
	facage = Column(Integer)
	facyatwu = Column(Integer)
	downloads = Column(Integer)
	
	presentation_id = Column(Integer, ForeignKey('presentation.id'))
	presentation = relationship('Presentation', backref='moodlefiles')
	
	def __repr__(self):
		return "<Moodle ('%s', '%s', '%s')" % (self.id, self.course, self.filename)




##################################################
# Rater Tables
##################################################

class Rater(Base):
	__tablename__ = 'rater'
	
	id = Column(Integer, primary_key=True)
	username = Column(String(200))
	password = Column(String(200))
	
	def __repr__(self):
		return "<Rater ('%s', '%s')" % (self.id, self.username)


class Rating(Base):
	__tablename__ = 'rating'
	
	id = Column(Integer, primary_key=True)
	ratedate = Column(DateTime) # datetime.date.today()
	empty = Column(Boolean)
	contentimage = Column(Integer)
	contenttext = Column(Integer)
	slidenovel = Column(Integer)
	slidestudy = Column(Integer)
	slidequality= Column(Integer)
	slideinteresting = Column(Integer)
	
	rater_id = Column(Integer, ForeignKey('rater.id'))
	rater = relationship('Rater', backref='ratings')
	
	presentation_id = Column(Integer, ForeignKey('presentation.id'))
	presentation = relationship('Presentation', backref='ratings')
	
	def __repr__(self):
		return "<Rating ('%s', '%s', '%s', '%s', '%s' )" % (self.id, self.ratedate, self.rater_id, self.presentation_id, self.slidequality)



##################################################
# Rater Tables
##################################################

class PresentationFile(Base):
	__tablename__ = 'presentationfile'
	
	id = Column(Integer, primary_key=True)
	md5 = Column(String(255))
	filename = Column(String(255))
	size = Column(Integer)
	
	presentation_id = Column(Integer, ForeignKey('presentation.id'))
	presentation = relationship('Presentation', backref='presentationfile')
	
	def __repr__(self):
		return "<PresentationFile ('%s', '%s', '%s' )" % (self.id, self.filename, self.presentation_id)


class PresentationJpg(Base):
	__tablename__ = 'presentationjpg'
	
	id = Column(Integer, primary_key=True)
	md5 = Column(String(255))
	filename = Column(String(255))
	size = Column(Integer)
	height = Column(Integer)
	width = Column(Integer)
	
	presentation_id = Column(Integer, ForeignKey('presentation.id'))
	presentation = relationship('Presentation', backref='presentationjpg')
	
	def __repr__(self):
		return "<PresentationJpg ('%s', '%s', '%s' )" % (self.id, self.filename, self.presentation_id)


class PresentationHtmlImage(Base):
	__tablename__ = 'presentationhtmlimage'
	
	id = Column(Integer, primary_key=True)
	md5 = Column(String(255))
	filename = Column(String(255))
	size = Column(Integer)
	height = Column(Integer)
	width = Column(Integer)
	
	pos_left = Column(Integer)
	pos_width = Column(Integer)
	pos_top = Column(Integer)
	pos_height = Column(Integer)
	
	presentation_id = Column(Integer, ForeignKey('presentation.id'))
	presentation = relationship('Presentation', backref='presentationhtmlimage')
	
	def __repr__(self):
		return "<PresentationImage ('%s', '%s', '%s' )" % (self.id, self.filename, self.presentation_id)


class PresentationHtmlPage(Base):
	__tablename__ = 'presentationhtmlpage'
	
	id = Column(Integer, primary_key=True)
	md5 = Column(String(255))
	filename = Column(String(255))
	
	presentation_id = Column(Integer, ForeignKey('presentation.id'))
	presentation = relationship('Presentation', backref='presentationhtmlpage')
	
	def __repr__(self):
		return "<PresentationHtmlPage ('%s', '%s', '%s' )" % (self.id, self.filename, self.presentation_id)


class PresentationHtmlPageText(Base):
	__tablename__ = 'presentationhtmlpagetext'
	
	id = Column(Integer, primary_key=True)
	md5 = Column(String(255))
	text = Column(Text())
	left = Column(Integer)
	top = Column(Integer)
	width = Column(Integer)
	height = Column(Integer)
	
	presentationhtmlpage_id = Column(Integer, ForeignKey('presentationhtmlpage.id'))
	presentationhtmlpage = relationship('PresentationHtmlPage', backref='text')
	
	def __repr__(self):
		return "<PresentationHtmlPageText ('%s', '%s', '%s' )" % (self.id, self.text, self.presentation_id)


class PresentationHtmlPageImage(Base):
	__tablename__ = 'presentationhtmlpageimage'
	
	id = Column(Integer, primary_key=True)
	
	pos_left = Column(Integer)
	pos_width = Column(Integer)
	pos_top = Column(Integer)
	pos_height = Column(Integer)
	
	presentationhtmlimage_id = Column(Integer, ForeignKey('presentationhtmlimage.id'))
	presentationhtmlimage = relationship('PresentationHtmlImage', backref='htmlpageimages')
	
	presentationhtmlpage_id = Column(Integer, ForeignKey('presentationhtmlpage.id'))
	presentationhtmlpage = relationship('PresentationHtmlPage', backref='htmlimages')
	
	def __repr__(self):
		return "<PresentationHtmlPageImage ('%s', '%s', '%s' )" % (self.id, self.presentationhtmlimage_id, self.presentationhtmlpage_id)




# Create All!
# Base.metadata.create_all(engine)


