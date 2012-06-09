RateMyPowerPoint Project


== Installation ==

Install Django
Install Apache
Install Erlang
Install RabbitMQ
	Change the install folder, delete the guest account, and add a new one.
	Be sure to set the new account as an administrator, and give access to /
	Setup the management console for easier access via http://localhost:55672/
	Be sure to enable access via firewall to 5672 if being accessed from a remote
	machine.

Install Celery
	Use PIP to install
	Setup daemon running by seeing 
		http://www.calazan.com/windows-tip-run-applications-in-the-background-using-task-scheduler/
		and running celeryd.bat in the rmp folder.

Install DJCelery

Configure localsettings.py file for database and celery setup.