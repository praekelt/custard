# -*- test-case-name: txgsm.tests.test_service -*-

from twisted.python import usage
from twisted.internet.protocol import ClientFactory
from twisted.python import log

from custard.protocol import CustardProtocol


class Play(usage.Options):

    optFlags = [
        ["verbose", "v", "Log AT commands"],
    ]

    optParameters = [
        ["script", "s", None, "The script to load."],
        ["endpoint", "e", None, "The endpoint to connect to."],
    ]


class Options(usage.Options):

    subCommands = [
        ['play', None, Play, "Play a script"],
    ]


class CustardClientFactory(ClientFactory):

    protocol = CustardProtocol

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        print 'returning protocol'
        return p

    def clientConnectionLost(self, connector, reason):
        log.msg('Client connection lost.')

    def clientConnectionFailed(self, connector, reason):
        log.msg('Client connection failed.')
