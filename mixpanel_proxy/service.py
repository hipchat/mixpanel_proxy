import json
from twisted.application.service import Service
from twisted.internet import reactor
from twisted.python import log


class MixpanelProxyService(Service):

    def __init__(self, interface, verbose):
        self.interface = interface
        self.verbose = bool(verbose)

    def startService(self):
        Service.startService(self)

    def stopService(self):
        Service.stopService(self)
