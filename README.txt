RateMyPowerPoint
README File
Nathan Garrett
http://profgarrett.com

Goal
====

RMP is a tool to manage my PowerPoint research project.

Installation
============

* Python
	Use a version >3 (if on Windows). Note that you shoould be sure that the other packages listed below work, particularly with the binaries.  As of Mar '14, 3.3 was the best supported version.

	You'll probably need to update the path (go to System Properies, Advanced, Environmental Variables) to add "c:\Python34;c:\Python34\Scripts".

* PIP
	On Windows, install pip by downloading the install python file from their website.

* Pip install the following files.

Download RMP files to the folder where you want to run them from.
	pip install ipython <-- optional, but has a prettier interface for command line
	pip install Django
	pip install Pillow  <-- note you need the binary on windows

Third, configure localsettings.py file for database setup.  Use the example template provided as a starting point.


Other Notes
===========


Credits
===========
Thanks to HTML5 Boilerplate project.  I used modified versions of their files (loaded in shared_static).