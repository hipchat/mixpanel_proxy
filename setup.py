#!/usr/bin/env python

# Based off http://chrismiles.livejournal.com/23399.html

import sys

try:
    import twisted
except ImportError:
    raise SystemExit("twisted not found. Make sure you "
                     "have installed the Twisted core package.")

from distutils.core import setup


def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))


if __name__ == "__main__":
    setup(name='mixpanel_proy',
        version='1.0',
        description='Asynchronous sending of Mixpanel stats.',
        author='Garret Heaton',
        author_email='powdahound@gmail.com',
        url='http://github.com/powdahound/mixpanel_proxy',
        packages=[
            'mixpanel_proxy',
            'twisted.plugins'],
        package_data={
            'twisted': ['plugins/mixpanel_proxy_plugin.py']
        })

    refresh_plugin_cache()
