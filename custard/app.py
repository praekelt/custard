from twisted.python import log
from twisted.internet.defer import inlineCallbacks


class CommandLineApp(object):

    def __init__(self, protocol, options):
        self.protocol = protocol
        self.protocol.verbose = options['verbose']

    @inlineCallbacks
    def on_modem_ready(self, configure_response):
        log.msg('Modem is ready!', configure_response)
        response = yield self.protocol.send_command(
            'AT+CUSD=1,*100#,15', expect='+CUSD')
        print 'got response!', response
        yield self.protocol.disconnect()
