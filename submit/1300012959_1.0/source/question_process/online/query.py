#!/usr/bin/python
# -*- coding:utf-8 -*-

import sgmllib
import sys, time, urllib2
from sys import argv

tagstack = []
links = []
names = []
valid = 0

cur_name = ""

recording_psg = 0
cur_psg = ""
cur_psgs = []

def init():
    global links
    global names
    global valid
    global tagstack
    global cur_psgs
    global recording_psg
    valid = 0
    links = []
    names = []
    tagstack = []
    cur_psgs = []
    recording_psg = 0

class getLinks(sgmllib.SGMLParser):
    def handle_starttag(self, tag, method, attrs):
        if tag == "a":
            global cur_name
            cur_name = ""
            self.start_a(attrs)
        elif tag == "h3":
            self.start_h3(attrs)
        elif tag == "div":
            self.start_div(attrs)
#        print "#\t%s" % tag
        tagstack.append(tag)

    def handle_endtag(self, tag, method):
#        print "##\t"+tag
        if tag == "a":
            self.end_a()
        elif tag == "h3":
            self.end_h3()
        elif tag == "div":
            self.end_div()
        tagstack.pop()

    def end_a(self):
        global valid
        if valid == 1:
#            print "$ name: %s" % cur_name
            names.append(cur_name)

    def start_div(self, attrs):
        global recording_psg
        global cur_psg
        for i in range(len(attrs)):
            if attrs[i][0] == "class" \
                    and (attrs[i][1] == "c-abstract" or attrs[i][1] == "op_zhidaokv_answers"):
                recording_psg = 1
                cur_psg = ""

    def end_div(self):
        global recording_psg
        global cur_psg
        global cur_psgs
        if recording_psg == 1:
            recording_psg = 0
            cur_psgs.append(cur_psg)
            cur_psg = ""

    def handle_data(self, data):
        if len(tagstack) > 1 and tagstack[-1] == "a" and tagstack[-2] == "h3":
            global cur_name
            cur_name += data
        elif recording_psg == 1:
            global cur_psg
            cur_psg += data

    def start_h3(self, attrs):
        global valid
        global recording_psg
        global cur_psg
        global cur_psgs
        valid = 1
        if recording_psg == 1:
            recording_psg = 0
            cur_psgs.append(cur_psg)
            cur_psg = ""

    def end_h3(self):
        global valid
        valid = 0

    def start_a(self, attrs):
#        for attr in attrs:
#            print "**%s" % (str(attr)),
#        print ""
        if valid == 1 and len(tagstack) > 0 and tagstack[-1] == "h3":
            for (k, v) in attrs:
                if k == "href":
#                    print "find url: %s" % v
                    links.append(v)

    def unknown_starttag(self, tag, attrs): pass
    def unknown_endtag(self, tag): pass

def search_baidu(start_num, end_num):
    base_url = "http://www.baidu.com/s?wd="

    f = open("../questions/provided/q_facts.txt", "r")
    lines = [line.rstrip() for line in f.readlines()]
    f.close()


    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    f = open("psgs_"+str(start_num) + "_" + str(end_num) + ".txt", "w")
    cur = start_num
    for _line in lines[start_num:end_num]:
        cur += 1
        print "\r#\t%d" % cur,
        sys.stdout.flush()
        init()
        line = _line.replace(" ", "%20")
        if line != "":
            print base_url+line
            while True:
                try:
                    req = urllib2.Request(
                        url = base_url + line,
                        headers = headers
                        )
                    response = urllib2.urlopen(req)
                    break
                except urllib2.HTTPError as e:
                    print "HTPPERror = " + str(e.code)
                    time.sleep(10)
            html = response.read()
            getLinks().feed(html)
        f.write("<question id=%d>\n" % cur)
        for i in range(5):
            f.write("<doc>\n")
            f.write("%s\n%s\n" % (                          \
                    names[i] if i < len(names) else "",     \
                    links[i] if i < len(links) else ""))
            f.write(cur_psgs[i] if i < len(cur_psgs) else "")
            f.write("\n</doc>\n")
        f.write("</question>\n")
    f.close()

def main(start_num, end_num):
    search_baidu(start_num, end_num)

if __name__ == "__main__":
    if len(argv) < 3:
        print "specify start and end number!"
    else:
        print "processing %s...%s" % (argv[1], argv[2])
        main(int(argv[1]), int(argv[2]))
