#!/usr/bin/python
# -*- coding:utf-8 -*-

tf = open("stop_words.txt", "r")
stop_words = []
lines = tf.readlines()
for line in lines:
    stop_words.append(line[:-1])
tf.close()

stop_words.append("是")

wh_words = ["什么", "谁", "哪", "何时", "第几", "多少", "几", "为什么"]

def read_Qs(filename):
    ''' read questions from a file
    return [[], [], ...] as lines of words
    '''
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    res = []
    for line in lines:
        res.append(line.split(" ")[:-1])
    return res

def find_wh_word_pos(line):
    ''' find w/h words in line,
    return (pos, wh-word)
    '''
    for wh in wh_words:
        for word_pos in range(len(line)):
            word = line[word_pos]
            flag = 1
            for i in range(len(wh)):
                if len(word) == i \
                or word[i]!=wh[i]:
                    flag = 0
                    break
            if flag:
                return (word_pos, wh)
    return (-1, "")

def gen_cent_word(line):
    ''' generate central word
    in a question sentence
    '''
    l = len(line)
    pos = 0
    if "是/v" in line:
        while (line[pos]!="是/v"):
            pos += 1
        for i in range(pos, -1, -1):
            attr = line[i].split("/")[1]
            if attr[0]=='n':
                return line[i]
    else:
        pos = find_wh_word_pos(line)[0]
        if pos == -1:
            return ""
        for i in range(pos, l):
            attr = line[i].split("/")[1]
            if attr[0]=='n':
                return line[i]
    return ""

def gen_keywords(line):
    '''generate keywords for a question
    '''
    l = len(line)

    # central word
    cent_word = gen_cent_word(line)
    ret = [cent_word]

    # nouns
    nouns = []
    for i in range(l):
        #print ("#%s#" % (line[i]))
        attr = line[i].split("/")[1]
        if attr[0]=='n' and line[i]!=cent_word:
            nouns.append(line[i])
    ret += nouns

    # verbs
    verbs = []
    for i in range(l):
        word = line[i].split("/")[0]
        attr = line[i].split("/")[1]
        if attr[0]=='v' and not (line[i] in stop_words):
            verbs.append(line[i])
    ret += verbs

    # other words
    for i in range(l):
        word = line[i].split("/")[0]
        if not (line[i] in ret) and not (word in stop_words):
            ret.append(line[i])

    return ret

def main():
    Qs = read_Qs("questions/q_facts_segged.txt")
    for Q in Qs:
        keywords = gen_keywords(Q)
        for word in keywords:
            print word,
        print

    # TODO: Question Classification

if __name__ == "__main__":
    main()
