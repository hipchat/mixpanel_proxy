import sys
from mixpanel_proxy.service import MixpanelProxyService
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements


class Options(usage.Options):
    optFlags = [
        ["verbose", "v", "Verbose logging"]]

    optParameters = [
        ["interface", None, "localhost:8067",
            "Interface to accept requests on."]]

    longdesc = 'This is a service for sending Mixpanel stats asynchronously. \
        Please see http://github.com/powdahound/mixpanel_proxy for details.'


class MixpanelProxyServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "mixpanel_proxy"
    description = "A service for sending Mixpanel stats asynchronously."
    options = Options

    def makeService(self, options):
        for opt, val in dict(options).items():
            if val is None:
                print "ERROR: Please provide --%s.\n" % opt
                print options
                sys.exit(1)

        return MixpanelProxyService(options['interface'],
                                    bool(options['verbose']))


serviceMaker = MixpanelProxyServiceMaker()
