from twisted.python import log


class CommandLineApp(object):

    def __init__(self, protocol, options):
        self.protocol = protocol
        self.protocol.verbose = options['verbose']
        self.protocol.ready.addCallback(self.modem_ready)

    def modem_ready(self, protocol):
        log.msg('Modem is ready!')
        protocol.disconnect()
