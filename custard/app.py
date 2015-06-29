from twisted.python import log
from twisted.internet.defer import inlineCallbacks


class CommandLineApp(object):

    def __init__(self, protocol, options):
        self.protocol = protocol
        self.protocol.verbose = options['verbose']
        with open(options['script'], 'r') as fp:
            self.script = fp.read()

    @inlineCallbacks
    def on_modem_ready(self, configure_response):
        log.msg('Modem is ready!', configure_response)
        for line in self.script.split('\n'):
            if line:
                response = yield self.protocol.send_command(
                    line, expect='+CUSD')
        print 'got response!', response
        yield self.protocol.disconnect()
