#!/usr/bin/python
# -*- coding:utf-8 -*-

import sgmllib
import sys, time, urllib2, requests

tagstack = []
cur_psg = ""
q_psgs = []

def init():
    global tagstack
    global cur_psg
    tagstack = []
    cur_psg = ""

class getPassages(sgmllib.SGMLParser):
    def handle_starttag(self, tag, method, attrs):
        if tag == "p":
            self.start_p(attrs)
        tagstack.append(tag)

    def handle_endtag(self, tag, method):
#        print "##\t"+tag
        if tag == "p":
            self.end_p()
        tagstack.pop()

    def handle_data(self, data):
        if len(tagstack) > 0 and tagstack[-1] == "p":
            global cur_psg
            cur_psg += data

    def start_p(self, attrs):
        pass

    def end_p(self):
        global cur_psg
        cur_psg += "\n"

    def unknown_starttag(self, tag, attrs): pass
    def unknown_endtag(self, tag): pass

def main(start_num, end_num):
    f = open("urls_" + str(start_num) + "_" + str(end_num) + ".txt", "r")
    lines = [line.rstrip() for line in f.readlines()]
    f.close()

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept':'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip',
        'Connection':'close',
        'Referer': "www.baidu.com" #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }

    f = open("psgs_" + str(start_num) + "_" + str(end_num) + ".txt", "w")
    idx = -1
    for i in range(start_num, end_num):
        cur_psgs = []
        for j in range(2):
            idx = (i - start_num) * 10 + j * 2 + 1
            init()
            print "#\t%s|%s" % (lines[idx-1], lines[idx])
            req = urllib2.Request(
                url = lines[idx],
                headers = headers
            )
            retry = 0
            while retry < 10:
                try:
                    response = urllib2.urlopen(req)
                except Exception as e:
                    retry += 1
                    time.sleep(1 + (0 if retry < 4 else retry - 4))
                else:
                    break
            html = response.read()
            getPassages().feed(html)

            f.write("<doc id=%d>\n" % i)
            f.write(cur_psg)
            f.write("</doc>\n")

#            cur_psgs.append(cur_psg)
#        q_psgs.append(cur_psgs)
        print "\r%d" % (i),
        sys.stdout.flush()
    f.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "get passages 0...8000"
        main(0, 8000)
    else:
        start_num = int(sys.argv[1])
        end_num = int(sys.argv[2])
        print "get passages %d...%d" % (start_num, end_num)
        main(start_num, end_num)
