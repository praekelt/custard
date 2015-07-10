custard

pre-setup
=======
	make sure you have a working connection to the Truteq Servers

install
=======

::
    $ pip install https://github.com/pmarti/python-messaging/tarball/master#egg=python-messaging-dev
    $ pip install -e .
    
scripts
=======

	All scripts files must have a ".cstd" extension.
	Accepted instructions: DIAL, SEND, EXPECT, END

API
===========

	DIAL "string to dial"					- dials number
	EXPECT "string expected to come back"	- testing utility, checks the given string against the received string
	SEND "response string after expect"		- dials number as a response
	END 									- ends test

running custard
==============
	custard play -e TCP:servername:portnumber -s script_to_be_tested.cstd