mixpanel_proxy
==============

A service which accepts Mixpanel stats via TCP and delivers them to Mixpanel Mixpanel asynchronously. No job queue necessary.


Install
-------

    $ git clone git://github.com/powdahound/mixpanel_proxy.git
    $ cd mixpanel_proxy
    $ python setup.py install


Run
---

Testing:

    $ twistd -n mixpanel_proxy --verbose

Daemon:

    $ twistd --pidfile=mixpanel_proxy.pid --logfile=mixpanel_proxy.log mixpanel_proxy


Use
---

Connect to mixpanel_proxy on localhost:8067 and send the full JSON blob followed by a newline. The interface and port can be changed using the `--interface` option.

Command line:

    $ telnet localhost 8067
    Trying localhost...
    Connected to localhost.
    Escape character is '^]'.
    {"event":"test","properties":{"ip":"10","token":"abc123"}}
    OK

PHP:

Python:

Ruby:


Connections are closed automatically after 10 minutes of inactivity so make sure you can handle reconnection if necessary.
