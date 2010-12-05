import json
from base64 import b64encode
from twisted.application.service import Service
from twisted.internet import defer, protocol, reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.protocols.policies import TimeoutMixin
from twisted.python import log
from twisted.web.client import getPage


class MixpanelProxyProtocol(LineOnlyReceiver, TimeoutMixin):

    IDLE_TIMEOUT = 60 * 10

    def connectionMade(self):
        LineOnlyReceiver.connectionMade(self)
        self.setTimeout(self.IDLE_TIMEOUT)
        if self.factory.service.verbose:
            log.msg("VERBOSE: Connection made: %r" % self.transport)

    def connectionLost(self, reason):
        LineOnlyReceiver.connectionLost(self, reason)
        if self.factory.service.verbose:
            log.msg("VERBOSE: Connection lost: %r, reason=%s"
                    % (self.transport, reason))

    def lineReceived(self, line):
        self.resetTimeout()
        if self.factory.service.verbose:
            log.msg("VERBOSE: Received line %r" % line)

        # quit if requested - just to make telnet testing easier
        if line == 'quit':
            self.transport.loseConnection()
            return

        # verify message as JSON
        try:
            data = json.loads(line)
        except Exception, e:
            self.sendError('Invalid JSON: %r' % line)
            return

        if 'event' not in data:
            self.sendError('Missing "event" data.')
            return

        if 'properties' not in data:
            self.sendError('Missing "properties" data.')
            return

        if 'token' not in data['properties']:
            self.sendError('Missing "token" property.')
            return

        if 'distinct_id' not in data['properties'] and \
            'ip' not in data['properties']:
            self.sendError('You need a "distinct_id" or "ip" property.')
            return

        self.factory.service.sendStat(data)
        self.sendLine('OK')

    def sendError(self, message):
        message = "ERROR: %s" % message
        self.sendLine(message)
        log.msg(message)

    def timeoutConnection(self):
        log.msg("Connection timed out: %r" % self.transport)
        self.transport.loseConnection()


class MixpanelProxyProtocolFactory(Factory):

    protocol = MixpanelProxyProtocol

    def __init__(self, service):
        self.service = service


class MixpanelProxyService(Service):

    def __init__(self, interface, verbose):
        self.interface = interface
        self.verbose = bool(verbose)

        protocol.Factory.noisy = False

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
            if r == "0":
                log.msg("Stat rejected: %r" % data)
        except Exception, e:
            log.msg("ERROR: Error connecting to Mixpanel: %s" % e)
        log.msg("Stat sent: %r" % data)

    def startService(self):
        Service.startService(self)
        f = MixpanelProxyProtocolFactory(self)
        interface, port = self.interface.split(':')
        reactor.listenTCP(port=int(port), interface=interface, factory=f)
        log.msg('Listening on %s...' % self.interface)

    def stopService(self):
        Service.stopService(self)
