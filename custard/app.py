from twisted.python import log
from twisted.internet.defer import inlineCallbacks, succeed
import parsley, time, re


class CommandLineApp(object):
    delimiter = '\r\n'
    ussd_resp = None

    def __init__(self, protocol, options):
        self.protocol = protocol
        self.protocol.verbose = options['verbose']
        self.load_script(options)

    def load_script(self, options):
        self.script = ""
        with open(options['script'], 'r') as fp:
            while True:
                c = fp.read(1)
                if not c:
                    break
                elif c == '"':
                    quote = self.load_script_helper(fp)
                    self.script+=quote
                    continue
                self.script += c 

    def load_script_helper(self, fp):
        """reads whats inside the quotation marks and replaces \n characters with spaces"""
        quote = ""
        while True:
            c = fp.read(1)
            if not c:
                break
            if c == '"':
                break
            elif c == '\n':
                c = ' ';
            quote += c
        return quote


    def on_modem_ready(self, configure_response):
        log.msg('Modem is ready!', configure_response)
        return self.run_script_test()

    def convert_to_ussd(self, code):
        message = "AT+CUSD=1,%s,15" % (code,)
        return message

    @inlineCallbacks
    def run_script_test(self):
        start = time.time()
        for line in self.script.split('\n'):
            if line:
                response = yield self.decryptLine(line)
        end = time.time()
        duration = end - start
        print "Duration: %.2fs" % duration

    def ColorIt(self, output, color):
            attr = []
            if color == "red":
                attr.append('31')
            elif color == "green":
                attr.append('32')
            attr.append('1')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), output)

    def handle_response(self, message):
        rsp = " ".join(message['response'])
        cleanResponse = rsp.lstrip('OK+CUSD: ')
        ussd_response = cleanResponse[3:-5]
        self.ussd_resp = ussd_response
        return succeed(ussd_response)

    def trace_mismatch(self, resp, expt):   #traces the mismatch and highlights the differences
        output = ""
        length = min(len(resp),len(expt))
        breakingpoint = length
        for i in range (0,length):
            if resp[i] != expt[i]:
                breakingpoint = i
                break
        if len(expt) < len(resp):
            s = " (Expected string too short)"
            s = self.ColorIt(s, "red")
            output = expt + s
        else:
            newlen = 0  - (len(expt)- breakingpoint)
            str2 = expt[newlen:]
            str2 = self.ColorIt(str2,"red")
            str1 = expt[:newlen]
            output = str1 + str2

        print "Expected: %s\nReceived: %s" % (output,resp)

    def dial(self, code):
        code = self.convert_to_ussd(code)
        d = self.protocol.send_command(code, expect='+CUSD')
        d.addCallback(self.handle_response)
        return d

    def expect(self, code):
        code = code.strip()
        self.ussd_resp = self.ussd_resp.strip()
        if  self.match(self.ussd_resp, code):
            output = self.ColorIt("PASSED","green")
            print output
        else:
            output = self.ColorIt("FAILED","red")
            print output
            self.trace_mismatch(self.ussd_resp, code)
            self.ussd_resp = None
    
    def match(self, resp, expt):
            resp_list = resp.split(" ")
            expt_list = expt.split(" ")
            length = min(len(resp_list),len(expt_list))
            if len(resp_list) != len(expt_list):
                return False
            for i in range (0,length):
                word_resp = resp_list[i]
                word_expt = expt_list[i]
                if word_expt != word_resp:
                    match  = None
                    pattern = word_expt+"?;$"
                    try:
                        match = re.match(pattern,word_resp)
                    except:
                        print "%s does not match %s. Failed to compile %s as a regex." % (word_expt, word_resp, word_expt)
                    if match == None:
                        return False
            return True

    def send(self, code):
        return self.dial(code)

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

        return x(line).instruction()

    def expression(self, instr, num):
        instr = instr.lower()
        if instr == "dial":
            return self.dial(num)
        elif instr == "expect":
            return self.expect(num)
        elif instr == "send":
            return self.send(num)
        elif instr == "end":
            return self.end()
        else:
            print "Unknown instruction: ", instr