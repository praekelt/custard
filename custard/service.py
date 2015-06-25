# -*- test-case-name: txgsm.tests.test_service -*-
import sys
from pprint import pprint
from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import Service
from twisted.application.service import IServiceMaker
from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
from twisted.internet import reactor, stdio
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import clientFromString
from twisted.internet.serialport import SerialPort
from twisted.python import log

from txgsm.protocol import TxGSMProtocol
from txgsm.utils import USSDConsole


class Play(usage.Options):

    optParameters = [
        ["script", "s", None, "The script to load."],
    ]


class Options(usage.Options):

    subCommands = [
        ['play', None, Play, "Play a script"],
    ]

    optFlags = [
        ["verbose", "v", "Log AT commands"],
    ]

    optParameters = [
        ["endpoint", "e", None, "The endpoint to connect to."],
    ]


class CustardProtocol(TxGSMProtocol):

    def connectionMade(self):
        self.log('Connected to the modem.')
        d = self.configure_modem()
        d.addCallback(self.modem_ready)

    def configure_modem(self):
        d = Deferred()
        d.addCallback(self.next('ATE0'))  # disable echo
        d.addCallback(self.next('AT+CMEE=1'))  # more useful error
        d.callback([])
        return d

    def modem_ready(self, response):
        self.log('modem is now ready: %r' % (response,))
        self.disconnect()

    def disconnect(self):
        self.log('Disconnecting...')
        self.transport.loseConnection()


class CustardClientFactory(ClientFactory):

    protocol = CustardProtocol

    def __init__(self, service):
        self.service = service

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        return p

    def stopFactory(self):
        log.msg('Stopping the factory.')
        self.service.stopService()

    def clientConnectionLost(self, connector, reason):
        log.msg('Client connection lost.')
        self.service.stopService()

    def clientConnectionFailed(self, connector, reason):
        log.msg('Client connection failed.')
        self.service.stopService()


class CustardService(Service):

    protocol = CustardProtocol

    def __init__(self, endpoint, command, options):
        log.msg('Running %s with: %s' % (command, options))
        self.endpoint = endpoint
        self.command = command
        self.options = options
        self.protocol.verbose = True
        self.connection = None

    def startService(self):
        endpoint = clientFromString(reactor, self.endpoint)
        endpoint.connect(CustardClientFactory(self))
        
    def stopService(self):
        log.msg('Stopping the service.')



class CustardServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "custard"
    description = "Utilities for talking to a GSM modem over Telnet"
    options = Options

    def makeService(self, options):
        endpoint = options['endpoint']

        if not options.subCommand:
            sys.exit(str(options))

        return CustardService(
            endpoint, options.subCommand, options.subOptions)
