#!/usr/bin/python
# -*- coding:utf-8 -*-

from sklearn import *
import string
import os

stop_words = []

num_category = 6

words2num = {}

wh_words = [
    "什么",
    "谁",
    "哪",
    "何时",
    "第几",
    "多少",
    "几",
    "为什么"
]

category_names = [
    "Q_person",
    "Q_time",
    "Q_place",
    "Q_number",
    "Q_organization",
    "Q_other"
]

category_name2index = {
    "Q_person": 0,
    "Q_time": 1,
    "Q_place": 2,
    "Q_number": 3,
    "Q_organization": 4,
    "Q_other": 5
}

clf_rules_wh_words = {
    "谁": "Q_person",
    "哪一年": "Q_time",
    "哪年": "Q_time",
    "哪个月": "Q_time",
    "哪一天": "Q_time",
    "哪里": "Q_place",
    "哪儿": "Q_place",
    "多少": "Q_number",
    "第几": "Q_number",
    "多少倍": "Q_number",
}

clf_rules_cent_words = {
    "作者": "Q_person",
    "诗人": "Q_person",
    "作家": "Q_person",
    "校长": "Q_person",
    "名字": "Q_person",
    "国家": "Q_place",
    "省份": "Q_place",
    "地区": "Q_place",
    "城市": "Q_place",
    "地点": "Q_place",
    "海拔": "Q_number",
    "年龄": "Q_number",
    "大学": "Q_organization",
    "少数民族": "Q_other",
    "语言": "Q_other"
}

clf_rules_cent_word_pos = {
    "nh": "Q_person",
    "ns": "Q_place",
    "nl": "Q_place",
    "ni": "Q_organization",
    "m": "Q_number",
    "nt": "Q_time",
    "nz": "Q_other",
}

def build_w2n_mapping():
    ''' build a mapping from 'word' to 'number'
    return mapping dict to global variable words2num
    '''
    f = open("questions/q_all.txt", "r")
    content_lines = f.readlines()
    f.close()

    global words2num
    words2num = {"": 0}
    cnt_words = 1
    for content in content_lines:
        for word in content.split("\t"):
            if words2num.get(word) == None:
                words2num[word] = cnt_words
                cnt_words += 1

    print "total %d words" % cnt_words

def read_stop_words():
    global stop_words
    tf = open("stop_words.txt", "r")
    lines = tf.readlines()
    tf.close()
    stop_words = [line[:-1] for line in lines]
    stop_words.append("是")

def read_Qs(filename):
    ''' read questions from a file
    return [[], [], ...] as lines of words
    '''
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    res = [line.split("\t")[:-1] for line in lines]
    return res

def find_wh_word_pos(line):
    ''' find w/h words in line,
    return (pos, wh-word)
    '''
    for wh in wh_words:
        for word_pos in range(len(line)):
            word = line[word_pos]
            if word.startswith(wh):
                return (word_pos, word.split("/")[0])
    return (-1, "")

def gen_cent_word(line):
    ''' generate central word
    in a question sentence
    '''
    l = len(line)
    pos = find_wh_word_pos(line)[0]
    if pos != -1:
        for i in range(pos, l):
            attr = line[i].split("/")[1]
            if len(attr)>0 and attr[0]=='n':
                return line[i]
    if "是/v" in line:
        pos = 0
        while (line[pos]!="是/v"):
            pos += 1
        for i in range(pos, -1, -1):
            attr = line[i].split("/")[1]
            if attr[0]=='n':
                return line[i]
    return ""

def gen_keywords(line):
    ''' generate keywords for a question
    return a list of keywords
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
        if len(attr)>0 and attr[0]=='n' and line[i]!=cent_word:
            nouns.append(line[i])
    ret += nouns

    # verbs
    verbs = []
    for i in range(l):
        word = line[i].split("/")[0]
        attr = line[i].split("/")[1]
        if len(attr) > 0 and attr[0]=='v' and not (line[i] in stop_words):
            verbs.append(line[i])
    ret += verbs

    # other words
    for i in range(l):
        word = line[i].split("/")[0]
        if not line[i] in ret:
            ret.append(line[i])

    return ret

def gen_q_features(line):
    ''' generate feature vectors of a question
    return a list of numeric values
    '''
    global words2num

    # wh-word
    wh_pos = find_wh_word_pos(line)[0]
    ret = [words2num[line[wh_pos]] if wh_pos > -1 else 0]

    # central word
    ret.append(words2num[gen_cent_word(line)])

    # # other words
    # words = [w for w in line]
    # num_words = len(words2num)
    # for i in range(num_words):
    #     if words2num.items()[i][0] in words:
    #         ret.append(1)
    #     else:
    #         ret.append(0)

    return ret

def init():
    read_stop_words()
    build_w2n_mapping()

def train_clf():
    f = open("questions/q_classified_label.txt")
    lines = f.readlines()
    f.close()
    num_trainset = len(lines)
    lbls = [[] for i in range(num_category)]
    for line in lines:
        for i in range(num_category):
            lbls[i].append(1 if category_name2index[line.rstrip()] == i else 0)
    print "trainging set of size %d" % num_trainset

    tQs = read_Qs("questions/q_classified_train.txt")
    fs = [gen_q_features(Q) for Q in tQs[:num_trainset]]

    clfs = [svm.SVC() for i in range(num_category)]
    for i in range(num_category):
        clfs[i].fit(fs, lbls[i])

    return clfs

def process(clfs, filename):

    # keyword generation
    Qs = read_Qs(filename)
    f = open(filename.split(".")[0] + "_kwd.txt", "w")
    for Q in Qs:
        keywords = gen_keywords(Q)
        for word in keywords:
            f.write(word + " ")
        f.write('\n')
    f.close()

    print "question keywords generated for '%s' in '%s'" \
        % (filename, filename.split(".")[0] + "_kwd.txt")

    # Question Classification by Rules
    flag = [-1 for i in range(len(Qs))]
    for idx in range(len(Qs)):
        for (wh_word, c) in clf_rules_wh_words.items():
            if find_wh_word_pos(Qs[idx])[1].startswith(wh_word):
                flag[idx] = category_name2index[c]
                break
        if flag[idx] != -1:
            continue
        for (cword, c) in clf_rules_cent_words.items():
            if gen_cent_word(Qs[idx]).split("/")[0] == cword:
                flag[idx] = category_name2index[c]
                break

    # Question Classification by Central Word POS
    for idx in range(len(Qs)):
        if flag[idx] != -1 \
                or find_wh_word_pos(Qs[idx])!= -1\
                or not "是/v" in Qs[idx]:
            continue
        pos = gen_cent_word(Qs[idx]).split("/")[1]
        for (p, c) in clf_rules_cent_word_pos.items():
            if pos.startswith(p):
                flag[idx] = category_name2index[c]
                break

    for idx in range(len(Qs)):
        if flag[idx] != -1:
            q_st = string.join(Qs[idx])
            l_st = category_names[flag[idx]]
            os.system('echo "' + q_st + '" >> questions/q_classified_train.txt')
            os.system('echo "' + l_st + '" >> questions/q_classified_label.txt')

    # Question Classification by SVM
    features = [gen_q_features(Q) for Q in Qs]
    res = [clf.predict(features).tolist() for clf in clfs]
    num = len(res[0])
    for i in range(num):
        if flag[i] != -1:
            continue
        j = 0
        while j < num_category - 1:
            if res[j][i] == 1:
                break
            j += 1
        flag[i] = j

    # Question Classification result printing
    f = open(filename.split(".")[0] + "_clf.txt", "w")
    for i in range(num):
        f.write(category_names[flag[i]]+"\n")
    f.close()

    print "question classified for '%s' in '%s'" \
        % (filename, filename.split(".")[0] + "_clf.txt")

def main():
    init()
    clfs = train_clf()

#    process(clfs, "questions/debug_question.txt")
#    process(clfs, "questions/q_facts_segged.txt")
    process(clfs, "questions/q_yesno_segged.txt")

if __name__ == "__main__":
    main()
