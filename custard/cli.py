import sys

from twisted.internet.task import react
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString
from twisted.internet.defer import inlineCallbacks, Deferred, succeed
from twisted.python import usage, log

from custard.protocol import CustardClientFactory
from custard.app import CommandLineApp


@inlineCallbacks
def play(options):
    endpoint = clientFromString(reactor, options['endpoint'])
    protocol = yield endpoint.connect(CustardClientFactory())
    protocol.verbose = options['verbose']
    protocol.ready.addErrback(log.err)
    app = CommandLineApp(protocol, options)
    protocol.ready.addCallback(app.on_modem_ready)
    yield protocol.ready
    flag = app.reset_flag()
    if flag:
        app2 = CommandLineApp(protocol, options)
        protocol.ready.addCallback(app2.on_modem_ready)
        yield protocol.ready

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


def twisted_cli(_reactor, name, *args):
    log.startLogging(sys.stdout)
    try:
        options = Options()
        options.parseOptions(args)
    except (usage.UsageError,), errortext:
        print '%s: %s' % (name, errortext)
        print '%s: Try --help for usage details.' % (name,)
        sys.exit(1)

    return {
        'play': play,
    }[options.subCommand](options.subOptions)


def main():
    react(twisted_cli, sys.argv)
