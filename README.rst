happymon
########

Monitoring systems have jumped the shark.  

We need a better way.  Current solutions have a million dependencies, confusing installation instructions, terrible agent configurations (yes ssh, smnp, NRPE, those are all agents). Existing solutions have very poor user interfaces and design, too much thinking involved to make the smallest of changes.

I just want to know what broke.

happymon is _not_:

 * "The Industry Standard In IT Infrastructure Monitoring"
 * "Unified IT monitoring and analytics powering the Intelligent Data Center"

Don't worry, be happy, mon!

Install
########

We always recommend installing python applications into a python virtualenv.

Download or checkout all of the code from this repository::

 git clone https://github.com/russellballestrini/happymon.git
 
Change present working directory to happymon::

 cd happymon
 
Install::

 python setup.py develop # or you may pass `install`

Verify:

 hm --help
 
 
