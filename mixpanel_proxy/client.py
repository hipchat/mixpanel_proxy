import json
from twisted.internet import defer, protocol, reactor
from twisted.protocols.basic import LineOnlyReceiver
from twisted.python import log


class MixpanelProxyClientProtocol(LineOnlyReceiver):

    def connectionMade(self):
        log.msg("Connection made to mixpanel_proxy: %r" % self.transport)

    def send(self, data):
        self.sendLine(json.dumps(data))

    def lineReceived(self, line):
        # TODO: Actually wait for response and return it to caller
        pass


class MixpanelProxyConnection:

    def __init__(self, host='localhost', port=8067):
        self.connection = None
        self.pending_deferreds = []
        self.pending_connection = False

        self.host = host
        self.port = int(port)

    def _connection(self):
        # return immediately if we're connected
        if self.connection:
            if self.connection._disconnected:
                self.connection = None
            else:
                d = defer.Deferred()
                d.callback(self.connection)
                return d

        # return a deferred if we're already waiting on a connection.
        # these deferreds are fired once the connection is established
        if self.pending_connection:
            d = defer.Deferred()
            self.pending_deferreds.append(d)
            return d

        def cb(conn):
            log.msg('Connected to mixpanel_proxy at %s:%s => %r'
                    % (self.host, self.port, conn))
            self.connection = conn
            # provide connection to waiting operations
            for d in self.pending_deferreds:
                d.callback(conn)
            self.pending_connection = False
            self.pending_deferreds = []
            return conn

        def eb(error):
            log.msg('ERROR: Unable to connect to mixpanel_proxy at %s:%s'
                    % (self.host, self.port))
            for d in self.pending_deferreds:
                d.errback(error)
            self.pending_connection = False
            self.pending_deferreds = []
            return None

        self.pending_connection = True
        cc = protocol.ClientCreator(reactor, MixpanelProxyClientProtocol)
        d = cc.connectTCP(self.host, self.port)
        d.addCallback(cb).addErrback(eb)
        return d

    def sendStat(self, data):

        def cb(protocol):
            if not protocol:
                return None

            protocol.send(data)
            return True

        # Connection failures should just return None
        def eb(error):
            log.msg('ERROR: mixpanel_proxy connection error: %s' % error)
            return None

        d = self._connection()
        d.addCallback(cb).addErrback(eb)
        return d

    def shutdown(self):
        if self.connection:
            log.msg('Closing mixpanel_proxy connection')
            self.connection.timeoutConnection()


@defer.inlineCallbacks
def test():
    print 'Testing MixpanelProxyConnection...'
    mp = MixpanelProxyConnection()

    data = {
        'event': 'test',
        'properties': {
            'distinct_id': 123456,
            'token': 'abc123',
        }
    }

    res = yield mp.sendStat(data)
    print "Result: %r" % res

    reactor.callLater(1, reactor.stop)


if __name__ == "__main__":
    test()
    reactor.run()
