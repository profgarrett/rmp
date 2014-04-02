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

* Configure localsettings.py file for database setup.  Use the example template provided as a starting point.

* Configure Apache.  Following is a sample configuration to attach to http.conf

Alias /robots.txt "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/shared_static/robots.txt"
Alias /favicon.ico "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/shared_static/favicon.ico"

AliasMatch ^/([^/]*\.css) "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/shared_static/styles/$1"

Alias /media/ "E:/rmp2/ppts/"
Alias /static/ "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/shared_static/"

<Directory "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/shared_static">
Order deny,allow
Allow from all
</Directory>

<Directory "e:/rmp2/ppts/">
Order deny,allow
Allow from all
</Directory>

WSGIScriptAlias / "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/rmp/wsgi.py"
WSGIPythonPath "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/"

<Directory "C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/rmp/">
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>



Other Notes
===========


Credits
===========
Thanks to HTML5 Boilerplate project.  I used modified versions of their files (loaded in shared_static).