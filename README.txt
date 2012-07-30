RateMyPowerPoint Project


== Installation ==

Install
	Apache
	Python (if on Windows)
	freetype & Jpeg


Install instructions from http://pkarl.com/articles/freetype-jpeg-zlib-and-python-imaging-library-osx-/

Note, update to most recent versions when you download files.

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


Download RMP files to the folder where you want to run them from.

Command Line:

sudo easy_install -U pip
sudo easy_install -U virtualenv
mkdir tmp
cd /tmp
virtualenv --distribute rmpenv
source rmpenv/bin/activate
cd ..
pip install -r requirements.txt

Next, install PIL.

pip install PIL

Note that after you install PIL, be sure to look t the log to see that jpeg support is available.  If not, you'll have trouble generating entropy for jpg files.

Next, install MySQL
= Active virtual env =

source tmp/rmpenv/bin/activate

deactivate

= Update press = 

pip freeze > requirements.txt


Prereqs:
	pip install BeautifulSoup4        <--- (Be sure to use 4, not 3)
	pip install html5lib
	Mechanize
	PIL

Configure localsettings.py file for database setup.  Use the example template provided as a starting point.
