import sys

from twisted.internet.task import react
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString
from twisted.internet.defer import inlineCallbacks
from twisted.python import usage, log

from custard.service import Options, CustardClientFactory
from custard.app import CommandLineApp


@inlineCallbacks
def play(options):
    endpoint = clientFromString(reactor, options['endpoint'])
    protocol = yield endpoint.connect(CustardClientFactory())
    protocol.verbose = options['verbose']
    yield protocol.ready
    CommandLineApp(protocol, options)


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
