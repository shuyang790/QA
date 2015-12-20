#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller



MODELDIR="../ltp_data/"

def main():

    f = open("psgs.txt", "r")
    lines = [line.rstrip() for line in f.readlines()]
    f.close()

    segmentor = Segmentor()
    segmentor.load(os.path.join(MODELDIR, "cws.model"))

    postagger = Postagger()
    postagger.load(os.path.join(MODELDIR, "pos.model"))

    f = open("psgs_segged.txt", "w")
    fans = open("zhidao_answer.txt", "w")
    i = 0
    qid = 0
    flag = 0

    while i < len(lines):
        line = lines[i]
        if (i % 1000 == 0):
            print "\r#\t%d" % i,
            sys.stdout.flush()
        if line.startswith("<question"):
            qid = int(line.split(" ")[1].split("=")[1].split(">")[0])
            flag = 0
            f.write(line + "\n")
        elif line.startswith("</doc") or line.startswith("</question"):
            f.write(line + "\n")
        elif line.startswith("<doc"):
            f.write(line + "\n" + lines[i+1] + "\n")
            i += 2
        else:
            L = len(line)
            s = 0
            for s in range(L):
                if line[s:].startswith("最佳答案:"):
                    break
            s += 14
            if s < L and flag == 0:
                t = s + 1
                while t < L and line[t:].startswith("更多") == False:
                    t += 1
                if s < t and t-s < 100 and t-s > 1:
                    fans.write("%d\t%s\n" % (qid, line[s:t].rstrip(".。 ?？，,")))
                    flag = 1
#            words = segmentor.segment(line)
#            postags = postagger.postag(words)
#            for j in range(len(words)):
#                f.write("%s/%s\t" % (words[j], postags[j]))
#            f.write("\n")
        i += 1
    f.close()
    fans.close()

if __name__ == "__main__":
    main()
