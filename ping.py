from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ClientEndpoint
from protocol_bgm import TxGSMProtocol


class PingProtocol(LineReceiver):
	delimiter = '\r\n'
	deffererds = []

	def connectionMade(self):
		self.setRawMode()
		pingConsole(self)

	def rawDataReceived(self, data):
		data = data.strip()
		if data.startswith('+CUSD'):
			d = self.deffererds.pop(0)
			d.callback(data)

	def dial(self, message):
		d = Deferred()
		self.deffererds.append(d)
		prefix = self.ColorIt("Dialing: ")
		display = message + "..."
		print prefix, display
		self.sendLine('at+cusd=1,%s,15' % (message))
		return d

	def ColorIt(self, output):  
			attr = []
			attr.append('31')
			attr.append('1')
			return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), output)

class PingFactory(protocol.ClientFactory):
	def startedConnecting(self, connector):
		print "Connected"

	def buildProtocol(self, addr):
		f = PingProtocol()
		return f

	def clientConnectionFailed(self, connector, reason):
		print "Connection lost"
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print "Connection lost"
		reactor.stop()


class pingConsole(LineReceiver):
	facto = None
	delimiter = '\r\n'

	def __init__(self, pf):
		self.facto = pf
		code = self.prompt("Enter number to dial\n")
		self.dialNumber(code)

	def prompt(self, message):
		user_input = raw_input(message)
		return user_input

	def dialNumber(self, number):
		d = self.facto.dial(number)
		d.addCallback(self.handleResponse)

	def showMessage(self, message):
		cleanResponse = message.lstrip("+CUSD: ")
		cleanResponse = cleanResponse.replace(self.delimiter,"\n")
		cleanResponse = cleanResponse[3:-5]
		msg = self.facto.ColorIt("Server said: ")
		user_response = self.prompt(msg+cleanResponse)
		return user_response

	def handleResponse(self, data):
		user_response = self.showMessage(data)
		if user_response == "exit":
			reactor.callLater(0, reactor.stop)
		else:
			self.dialNumber(user_response)

reactor.connectTCP("localhost", 2002, PingFactory())
reactor.run()