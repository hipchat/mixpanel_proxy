mixpanel_proxy
==============

A service which accepts Mixpanel stats via UDP and delivers them to Mixpanel asynchronously. No job queue necessary.


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

Send a UDP datagram to the service (defaults to port 8067) containing the full JSON blob expected by the Mixpanel API. Code examples provided in the examples/ directory.

