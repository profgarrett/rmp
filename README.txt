RateMyPowerPoint Project
README File
Nathan Garrett
http://profgarrett.com

test

Goal
====

RMP is a simply tool to manage my PowerPoint research project.

Installation
============

First, install the following 
 * Apache
 * Python (if on Windows)
 * freetype & Jpeg


Install notes from pkarl.  Note, update to most recent versions when you download files.

	http://pkarl.com/articles/freetype-jpeg-zlib-and-python-imaging-library-osx-/

	$ curl -O http://download.savannah.gnu.org/releases/freetype/freetype-2.1.10.tar.bz2
	$ tar --use-compress-program bzip2 -xvf freetype-2.1.10.tar.bz2
	$ cd freetype-2.1.10
	$ ./configure
	cd builds/unix; ./configure 
	...lots of files...
	$ make
	...several seconds of compilation...
	$ sudo make install
	Password: *YOUR OSX ROOT PASS*

	$ curl -O http://www.ijg.org/files/jpegsrc.v8b.tar.gz
	$ tar xvzf jpegsrc.v8b.tar.gz
	$ cd jpeg-8b
	$ ./configure
	$ make
	$ make install



Second, download RMP files to the folder where you want to run them from.

From the command line and in your rmp folder:
	sudo easy_install -U pip
	sudo easy_install -U virtualenv
	mkdir tmp
	cd /tmp
	virtualenv --distribute rmpenv
	source rmpenv/bin/activate
	cd ..
	pip install -r requirements.txt

Note that after you install PIL, be sure to look to the log to see that jpeg support is available.  If not, you'll have trouble generating entropy for jpg files.



Third, configure localsettings.py file for database setup.  Use the example template provided as a starting point.



Fourth, install NLTK corpus.

	Follow instructions on http://nltk.org/install.html

	Open a python prompt.
	import nltk
	nltk.download()

	Use the GUI to download all resources.

VirtualEnv
===========

Use `source tmp/rmpenv/bin/activate` to activate the virtual environment and `deactivate` to turn off.
To update requirements, use `pip freeze > requirements.txt`

Other Notes
===========

I use South to manage db updates.

To update to a new schema with some changes to models.py, 
	python manage.py schemamigration rating --auto
	python manage.py migrate rating

Run the following to fake a migration (get south files upto date w/o changing db)
	python manage.py migrate myapp 0001 --fake
