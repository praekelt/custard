from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
import parsley


class CommandLineApp(object):
    ussd_resp = None
    def __init__(self, protocol, options):
        self.protocol = protocol
        self.protocol.verbose = options['verbose']
        self.load_script(options)
        
    def load_script(self, options):
        with open(options['script'], 'r') as fp:
            self.script = fp.read()

    def on_modem_ready(self, configure_response):
        log.msg('Modem is ready!', configure_response)
        self.run_script_test()

    def convert_to_ussd(self, code):
        message = "at+cusd=1,%s,15" % (code,)
        return message

    def run_script_test(self):
        for line in self.script.split('\n'):
            if line:
                self.decryptLine(line)

    def ColorIt(self, output, color):  
            attr = []
            if color == "red":
                attr.append('31') 
            elif color == "green":
                attr.append('32')
            attr.append('1')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), output)
    
    def handle_response(self, message):
        print "Popped"
        cleanResponse = message.lstrip("+CUSD: ")
        cleanResponse = cleanResponse.replace(self.delimiter,"\n")
        ussd_response = cleanResponse[3:-5]
        self.ussd_resp = ussd_response

    @inlineCallbacks
    def dial(self, code):
        code = self.convert_to_ussd(code)
        self.response =  yield self.protocol.send_command(code, expect='+CUSD')
        self.response.addCallback(self.handle_response)
        print "response set"

    def expect(self, code):
#        if self.ussd_resp == None:
#            print "postponing"
#            reactor.callLater(2, self.expect(code))
        if code == self.ussd_resp:
            output = self.ColorIt("PASSED","green")
            print output
        else:
            output = self.ColorIt("FAILED","red")
            print output
            print "Expected: %s\nReceived:%s" % (code,self.ussd_resp)

    def send(self, code):
        self.dial(code)

    def setResponse(self, resp):
        print "Response set to ", resp
        self.ussd_resp = resp

    def end(self):
        yield self.protocol.disconnect()

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
