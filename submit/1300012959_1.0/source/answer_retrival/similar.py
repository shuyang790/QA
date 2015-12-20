# -*- coding: utf-8 -*-
import math


synonym_dict = {}


def init():
    with open('vectors.txt', 'r') as fin:
        s = fin.readline().strip().split(' ')
        n = int(s[0])
        k = int(s[1])
        for i in range(n):
            a = fin.readline().strip().split(' ')
            vect = []
            for j in range(1, len(a)):
                vect.append(float(a[j]))
            ret = 0
            for x in vect:
                ret += x*x
            length = math.sqrt(ret)
            for i in range(len(vect)):
                vect[i] /= length
            # print ret
            a[0] = a[0][: a[0].find('/')]
            synonym_dict[a[0]] = vect


def get_similar(termA, termB):
    if termB.find('/') == -1 or termA.find('/') == -1:
        return 0.0
    grA = termA[termA.find('/'):]
    grB = termB[termB.find('/'):]
    termA = termA[0: termA.find('/')]
    termB = termB[0: termB.find('/')]
    if termA == termB:
        return 1.0
    ga = synonym_dict.get(termA)
    gb = synonym_dict.get(termB)
    if (ga is None) or (gb is None):
        if grA == grB:
            return 0.2
        return 0.0
    ret = 0.0
    print ga
    print gb
    for i in range(150):
        ret += ga[i] * gb[i]
    return ret


init()
print 'Finished'
for i in range(100000):
    print get_similar('公民/x', '人民/x')