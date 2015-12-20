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


load_in_synonym()

# for i in range(1000000):
#     print get_similar('初中生/x', '学生/x')
# quit()
count = 0
left = 1
right = 30
with open('sample_out.txt', 'wb') as fout:
    with open('sample_question.txt', 'rb') as fq:
        with open('sample_content.txt', 'rb') as fin:
                # for t in q_terms:
                #     print t[0: t.index('/')]

            while True:
                cc = fq.readline()
                count += 1
                print count
                if count > right or count < left:
                    while True:
                        line = fin.readline()
                        if line == str(count + 1):
                            break
                    continue
                q_terms = cc.strip().split('\t')
                cc = fin.readline()
                if cc == '':
                    break
                ans = ''
                maxv = 0.0
                while True:
                    # if count == 3:
                    #     print count
                    line = fin.readline()
                    if line == '':
                        break
                    line = line.strip()
                    if line == str(count + 1):
                        break
                    sentences = [line]  # .split('。')
                    for sentence in sentences:
                        v = calc_sentence_similar(q_terms, sentence.split('\t'))
                        # print v, sentence
                        if v > maxv:
                            maxv = v
                            ans = str(v) + '\t' + sentence

                # ans_list.sort(key=lambda func: -func[0])

                print >> fout, '<Start>'
                print >> fout, ans
                print >> fout, '<End>'
