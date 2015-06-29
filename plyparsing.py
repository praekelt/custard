import parsley

class custardTestInterface(object):
	pingC = None
	script = None
	ussd_resp = None
	
	def __init__(self, pc):
		self.pingC = pc
		filename = raw_input("Enter file name (make sure its in the same directory:\n")
		f = open(filename, 'r')
		self.script = f.readlines()
		self.runTest()

	def attachScript(self, fileString):
		self.script = fileString	

	def dial(self, code):
		self.pingC.dialNumber(code)

	def expect(self, code):
		if code == self.ussd_resp:
			print "PASSED"
		else:
			print "FAILED\n"
			print "Expected: %s\nReceived:%s" % (code,self.ussd_resp)

	def send(self, code):
		self.pingC.dialNumber(code)

	def setResponse(self, resp):
		print "Response set to ", resp
		self.ussd_resp = resp

	def end(self):
		self.pingC.shutdown()

	def decryptLine(self, line):
		x = parsley.makeGrammar(
			""" 
			digit = anything:c ?(c in '0123456789*#') 
			word = anything:c ?(c != ' ')
			ws = ' '* 
			instruction = <word+>:pika ws <anything*>:dee-> expression(pika,dee)
			""", 
			{"expression":self.expression}
		)

		x(line).instruction()

	def expression(self, instr, num):
		instr = instr.lower()
		if instr == "dial":
			self.dial(num)
		elif instr == "expect":
			self.expect(num)
		elif instr == "send":
			self.send(num)
		elif instr == "end":
			self.end()
		else:
			print "Unknown instruction: ", instr

	def runTest(self):
		lines = self.script
		for line in lines:
			self.decryptLine(line)