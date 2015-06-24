from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol
from protocol_bgm import TxGSMProtocol


class ProtocolClass(LineReceiver):
	delimiter = '\r\n'

	def receiveInput(self, message):
		dialMessage = raw_input(message)
		self.dial(dialMessage)

	def connectionMade(self):
		print "We are connected"
		self.receiveInput("Enter number to dial:")

	def lineReceived(self, data):
		print "Server said: ", data

	def dial(self, message):
		self.sendLine('at+cusd=1,%s,15' % (message))
		#self.sendLine(message)

class FactoryClass(protocol.ClientFactory):
	def buildProtocol(self, addr):
		f = TxGSMProtocol();
		return f

	def clientConnectionFailed(self, connector, reason):
		print "Connection lost"
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print "Connection lost"

reactor.connectTCP("localhost", 2002, FactoryClass())
reactor.run()
