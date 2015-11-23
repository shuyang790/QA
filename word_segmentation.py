#!/usr/bin/python

import jieba
import jieba.posseg as pseg
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

jieba.enable_parallel(4)

def segmentation(filename, output_filename):
    f = open(filename, "r")
    content = f.read()
    f.close()

    words = pseg.cut(content)
    out = open(output_filename, "w")
    for word, flag in words:
        if (word != " " and word != "\t" and word != '\r\n') \
            and word != "\n":
            out.write("%s/%s " % (word, flag))
        elif (word == "\r\n" or word == "\n"):
            out.write("\n")
    out.close()

def main():
    segmentation("questions/q_facts.txt", "questions/q_facts_segged.txt")
    segmentation("questions/q_yesno.txt", "questions/q_yesno_segged.txt")

if __name__ == "__main__":
    main()
