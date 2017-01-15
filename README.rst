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
===============

We always recommend installing python applications into a python virtualenv.

Download or checkout all of the code from this repository::

 git clone https://github.com/russellballestrini/happymon.git
 
Change present working directory to happymon::

 cd happymon

Upgrade pip and setuptools::

 sudo pip3 install --upgrade pip setuptools
 
Install::

 sudo python3 setup.py install
 sudo pip3 install -r requirements.txt

Verify::

 hm --help

List plugins
================

happymon is extendable via plugins. By default the following plugins are automatically installed.
::

 hm --list-plugins
 collectors: http
 handlers: http_code
 notifiers: smtp, stdout

As you can see, there are three types of plugins:

* collectors
* handlers
* notifiers

Collectors reach out and collect information from external sources. For example the *http* collector connects to web sites over HTTP/HTTPS. Collectors return what they find.

Handlers take the results from Collectors and handle making decisions. For example, the *http_code* handler can be used to match 404s.

Notifiers get triggered when something interesting happens. For example, the smtp notifier can send a developer an email when their web service is down.

 
Config
==============


Here is a real life example that I use to test the health of one of my services:

**hm-prd.conf**::

 #threshold: 3
 #frequency: 60
 #timeout: 20

 notifiers:

   email-admins:
     handler: smtp
     extra:
       to: me@example.com
       from: root@happymon.example.com

   emit-to-stdout:
     handler: stdout

 checks:

   linkpeek-api:
     collector: http
     handler: http_code
     frequency: 60
     timeout: 45
     threshold: 4
     notifiers:
       - email-admins
       - emit-to-stdout
     extra:
       uri: https://linkpeek.com/api/v1?uri=http%3A//google.com&apikey=9fhvyH9KP&token=dfad5650142e3e0ef0b9c4bc9ea9d8dd&size=336x336&ttl=90
       desired_codes:
         - 302

   linkpeek-web:
     collector: http
     handler: http_code
     extra:
       uri: https://linkpeek.com
     notifiers:
       - email-admins
       - emit-to-stdout


Example
===========

::

 hm --config hm-prd.conf 
 linkpeek-api https://linkpeek.com/api/v1?uri=http%3A//google.com&apikey=9fhvyH9KP&token=dfad5650142e3e0ef0b9c4bc9ea9d8dd&size=336x336&ttl=90 302 Found
 linkpeek-web https://linkpeek.com 200 OK

Service
==========

Install Service
---------------

Here is how you install the service on either upstart or systemd.

upstart::

 sudo cp pkg/happymon.upstart.conf /etc/init/happymon.conf

systemd::

 sudo cp pkg/happymon.systemd.service /lib/systemd/system/happymon.service
 sudo systemctl enable happymon.service


Test
-------------

::

 sudo service happymon status
 sudo service happymon start

