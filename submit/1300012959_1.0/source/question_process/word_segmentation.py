#!/usr/bin/python

import jieba
import jieba.posseg as pseg
import sys

import sys, os

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

reload(sys)
sys.setdefaultencoding("utf-8")

jieba.enable_parallel(4)

def segmentation_jieba(filename, output_filename):
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

def segmentation(filename, output_filename):

    print "segmenting '%s' to '%s'" % (filename, output_filename)

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    MODELDIR = "./ltp_data/"

    # segment
    segmentor = Segmentor()
    segmentor.load(os.path.join(MODELDIR, "cws.model"))

    # postag
    postagger = Postagger()
    postagger.load(os.path.join(MODELDIR, "pos.model"))
    
    # Named Entity Recognize
    recognizer = NamedEntityRecognizer()
    recognizer.load(os.path.join(MODELDIR, "ner.model"))
    
    # Parse and get SVO
    parser = Parser()
    parser.load(os.path.join(MODELDIR, "parser.model"))
    
    f = open(output_filename, "w")
    fner = open(output_filename.split(".")[0]+"_ner.txt", "w")

    for _line in lines:
        line = _line[:-1]
        if line[-1] in "\n\r":
            line = line[:-1]
        
        words = segmentor.segment(line)
        postags = postagger.postag(words)
#        netags = recognizer.recognize(words, postags)
#        arcs = parser.parse(words, postags)

        for i in range(len(words)):
            f.write( "%s/%s\t" % (words[i], postags[i]))
#            if netags[i]!='O':
#                fner.write("%s/%s\t" % (words[i], netags[i]))
        f.write("\n")
#        fner.write("\n")

    f.close()
#    fner.close()

   
def main():
    segmentation("questions/provided/q_facts.txt", "questions/q_facts_segged.txt")
    segmentation("questions/provided/q_yesno.txt", "questions/q_yesno_segged.txt")

if __name__ == "__main__":
    main()
