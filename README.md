Requirements
------------

To host debuild.me you will need following tools
 * mongodb
 * node-less 

This can be installed with following command

 sudo apt-get install mongodb node-less

The following python packages are required for working of debuild.me
 * [monomoy](https://github.com/paultag/monomoy)
 * [chatham](https://github.com/paultag/chatham/)
 * [python-fishhook](https://github.com/paultag/python-fishhook)
 * flake8
 * flask
 * humanize
 * pymongo
 
Install these packages using virtualenv package and work in the same
virtual environment.

Building and Running
--------------------
Once above tools are installed run the following command

 make
 python runserver.py
 
This brings up the standalone instance of debuild.me which can be
accessed by hitting the url http://localhost:5000



