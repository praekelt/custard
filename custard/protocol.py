from twisted.internet.defer import Deferred

from txgsm.protocol import TxGSMProtocol


class CustardProtocol(TxGSMProtocol):

    def __init__(self):
        TxGSMProtocol.__init__(self)
        self.ready = Deferred()

    def connectionMade(self):
        self.log('Connected to the modem.')
        d = self.configure_modem()
        d.addCallback(self.on_modem_configured)
        return d

    def configure_modem(self):
        d = Deferred()
        d.addCallback(self.next('ATE0'))  # disable echo
        d.addCallback(self.next('AT+CMEE=1'))  # more useful error
        d.callback([])
        return d

    def on_modem_configured(self, response):
        self.log('modem is now ready: %r' % (response,))
        self.ready.callback(self)

    def disconnect(self):
        self.log('Disconnecting...')
        self.transport.loseConnection()
