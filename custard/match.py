import re
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


match("Airtime is Prom;" , "Airtime is Prom;")