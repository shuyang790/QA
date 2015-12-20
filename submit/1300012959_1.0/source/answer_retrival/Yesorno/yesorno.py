# -*- coding: utf-8 -*-
import math

# 'a', 'b', 'c', 'd', 'e', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'nd', 'nh', 'ni',
# 'nl', 'ns', 'nt', 'nz', 'nz', 'o', 'p', 'q', 'r', 'u', 'v', 'wp', 'ws', 'x'

synonym = {}
sum_cat = {}


def load_in_synonym():
    with open('synonym.txt', 'rb') as fin:
        while True:
            terms = fin.readline().strip().split(' ')
            if len(terms) == 1 and terms[0] == '':
                break
            # print terms
            # print terms[1]
            cat = terms[0]
            for i in range(len(cat)):
                s = cat[0: i]
                if sum_cat.get(s) is None:
                    sum_cat[s] = 1
                else:
                    sum_cat[s] += 1
            for i in range(1, len(terms)):
                if synonym.get(terms[i]) is None:
                    synonym[terms[i]] = [terms[0]]
                else:
                    synonym[terms[i]].append(terms[0])


def calc(sa, sb):
    a = 0.45
    b = 0.65
    c = 0.8
    d = 0.96
    e = 0.5
    f = 0.1
    g = 20
    if sa[0] != sb[0]:
        return f
    if sa[1] != sb[1]:
        n = sum_cat[sa[0: 1]]
        k = abs(ord(sa[1]) - ord(sb[1]))
        return a * math.cos(n * math.pi * math.pi / 180 / 180) * (n - k + 1) / n
    if sa[2] != sb[2] or sa[3] != sb[3]:
        n = sum_cat[sa[0: 2]]
        k = abs(int(sa[2: 4]) - int(sb[2: 4]))
        return b * math.cos(n * math.pi * math.pi / 180 / 180) * (n - k + 1) / n
    if sa[4] != sb[4]:
        n = sum_cat[sa[0: 4]]
        k = abs(ord(sa[4]) - ord(sb[4]))
        return c * math.cos(n * math.pi * math.pi / 180 / 180) * (n - k + 1) / n
    if sa[5] != sb[5] or sa[6] != sb[6]:
        n = sum_cat[sa[0: 5]]
        k = abs(int(sa[5: 7]) - int(sb[5: 7]))
        return d * math.cos(n * math.pi * math.pi / 180 / 180) * (n - k + g) / (n + g)
    if sa[7] == '#':
        return e
    return 1.0
    # Sim(A,B) = a*cos(n*pi/180)*[(n-k+1)/n]


def get_similar(termA, termB):
    if termB.find('/') == -1 or termA.find('/') == -1:
        return 0.0
    grA = termA[termA.find('/'):]
    grB = termB[termB.find('/'):]
    termA = termA[0: termA.find('/')]
    if termA == '曹雪芹' or termA == '河北省':
        return 0.0
    termB = termB[0: termB.find('/')]
    # print termA
    if termA == termB:
        return 1.0
    ga = synonym.get(termA)
    gb = synonym.get(termB)
    if (ga is None) or (gb is None):
        if grA == grB:
            return 0.2
        return 0.0
    ret = 0.0
    for i in range(len(ga)):
        for j in range(len(gb)):
            ret = max(ret, calc(ga[i], gb[j]))
    return ret


coef = [10.0, 8.7, 3.4, 2.3, 1.2]


def calc_sentence_similar(question, sentence):
    ret = 0.0
    ct = 0
    for term in question:
        maxv = 0.0
        for term_seq in sentence:
            maxv = max(maxv, get_similar(term, term_seq))
        if ct > 4:
            ret += maxv
        else:
            ret += coef[ct] * maxv
        ct += 1
    return ret


def entity(s):
    if s.find('/') == -1:
        return False
    s = s[s.find('/') + 1:]
    if len(s) < 2:
        return False
    if s[0] == 'n' and (s[1] in ['l', 'h', 's', 'i', 't', 'z']):
        return True
    return False


load_in_synonym()
count = 0
with open('yesorno_out.txt', 'wb') as fout:
    with open('yesorno_question.txt', 'rb') as fq:
        with open('yesorno_content.txt', 'rb') as fin:
                # for t in q_terms:
                #     print t[0: t.index('/')]
            cc = fin.readline()
            quit_flag = 0
            while True:
                cc = fq.readline()
                count += 1
                # if count > 5:
                #     break
                # if count > right:
                #     break
                # if count < left:
                #     while True:
                #         line = fin.readline().strip()
                #         if line == str(count + 1):
                #             break
                #     continue
                q_terms = cc.strip().split(' ')
                q = []
                for i in range(len(q_terms)):
                    if entity(q_terms[i]):
                        q.append(q_terms[i])
                        print q_terms[i],
                print ''
                ans = ''
                maxv = 0.0
                print 'Doing', count
                while True:
                    line = fin.readline()
                    if line == '':
                        quit_flag = 1
                        break
                    if line.strip() == str(count + 1):
                        break
                    line_words = line.strip().split('\t')
                    for term in line_words:
                        for j in range(len(q)):
                            if q[j] != '':
                                if get_similar(q[j], term) > 0.97:
                                    q[j] = ''

                flag = 0
                print q
                for word in q:
                    if word != '':
                        flag = 1
                        break
                if flag == 1:
                    print >> fout, 'No'
                else:
                    print >> fout, 'Yes'

                if quit_flag:
                    break


