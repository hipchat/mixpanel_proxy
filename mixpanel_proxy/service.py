import json
from base64 import b64encode
from twisted.application.service import Service
from twisted.internet import defer, protocol, reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.python import log
from twisted.web.client import getPage, HTTPClientFactory


class MixpanelProxyProtocol(DatagramProtocol):

    def __init__(self, service):
        self.service = service

    def datagramReceived(self, data, (host, port)):
        if self.service.verbose:
            log.msg("VERBOSE: Received data %r" % data)

        # verify message as JSON
        try:
            data = json.loads(data)
        except Exception, e:
            log.msg('ERROR: Invalid JSON. data=%r' % data)
            return

        if 'event' not in data:
            log.msg('ERROR: Missing "event". data=%r' % data)
            return

        if 'properties' not in data:
            log.msg('ERROR: Missing "properties". data=%r' % data)
            return

        if 'token' not in data['properties']:
            log.msg('ERROR: Missing "token". data=%r' % data)
            return

        self.service.sendStat(data)


class MixpanelProxyService(Service):

    def __init__(self, port, verbose):
        self.port = int(port)
        self.verbose = bool(verbose)

        if not self.verbose:
            # we don't want to hear about each HTTP request we make
            HTTPClientFactory.noisy = False

    @defer.inlineCallbacks
    def sendStat(self, data):
        if self.verbose:
            log.msg("VERBOSE: Sending stat: %r" % data)
        b64data = b64encode(json.dumps(data))
        try:
            url = 'http://api.mixpanel.com/track/?data=%s' % b64data
            r = yield getPage(url)
            if self.verbose:
                log.msg("VERBOSE: Mixpanel response: %r" % r)
            if r == "1":
                log.msg("Stat sent: %r" % data)
            else:
                log.msg("Stat rejected: %r" % data)
        except Exception, e:
            log.msg("ERROR: Error connecting to Mixpanel: %s" % e)

    def startService(self):
        Service.startService(self)
        reactor.listenUDP(self.port, MixpanelProxyProtocol(self))
        log.msg('Listening (UDP) on port %s...' % self.port)

    def stopService(self):
        Service.stopService(self)
