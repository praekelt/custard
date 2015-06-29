from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.python import log

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
        self.ready.callback(response)

    def disconnect(self):
        self.log('Disconnecting...')
        self.transport.loseConnection()


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
