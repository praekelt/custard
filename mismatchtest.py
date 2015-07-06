def trace_mismatch(resp, expt):   #traces the mismatch and highlights the differences
    breakingpoint = find_and_highlight(resp,expt)
    resp_reverse = resp[::-1]
    expt_reverse = expt[::-1]
    endpoint = len(expt)-find_and_highlight(resp_reverse,expt_reverse)
    print "Start: %d finish%d" %(breakingpoint,endpoint)
    if len(expt) < len(resp):
        s = " (Expected string too short)"
        #s = self.ColorIt(s, "red")
        output = expt + s
    else:
        newlen = 0  - (len(expt)- breakingpoint)
        #str2 = expt[newlen:]
        #str2 = self.ColorIt(str2,"red")
        #str1 = expt[:newlen]
        #output = str1 + str2
        expt_part3 = expt[endpoint:]
        expt_part2 = expt[breakingpoint:endpoint]
        expt_part1 = expt[:breakingpoint]
        output = expt_part1+expt_part2+expt_part3
        print "Expect:%s" % expt_part2

    #print "Expected: %s\nReceived: %s" % (output,resp)

def find_and_highlight(resp, expt):
    output = ""
    length = min(len(resp),len(expt))
    breakingpoint = length
    for i in range (0,length):
        if resp[i] != expt[i]:
            breakingpoint = i
            break
    return breakingpoint

str1 = "1) Summary 2) Detailed 3) Promotional"
str2 = "1) Summary 2) Detailed (should not be here)3) Promotional"
trace_mismatch(str1, str2)