#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import argv
import synonym


def corres2(term, qtype):
    x = term.find('/')
    term += '   '
    if x == -1:
        return 0
    if qtype == 'Q_other':
        if term[x + 1] == 'n' and not(term[x + 2] in ['l', 'h', 's', 'i', 't']):
            return 1.0
        else:
            return 0.3
    if qtype == 'Q_number':
        if term[x + 1] == 'm' or (term[0] in "0123456789"):
            return 1.5
        elif term[x + 1] == 'n' and term[x + 2] == 't':
            return 0.8
        else:
            return 0.3

    if qtype == 'Q_person':
        if term[x + 1] == 'n' and term[x + 2] == 'h':
            return 1.5
        elif term[x + 1] == 'n':
            return 0.7
        else:
            return 0.3
    if qtype == 'Q_place':
        if term[x + 1] == 'n' and (term[x + 2] == 'l' or term[x + 2] == 's'):
            return True
        elif term[x + 1] == 'n':
            return 0.7
        else:
            return 0.3
    if qtype == 'Q_organization':
        if term[x + 1] == 'n' and term[x + 2] == 'i':
            return 1.5
        elif term[x + 1] == 'n':
            return 0.7
        else:
            return 0.3
    if qtype == 'Q_time':
        if term[x + 1] == 'n' and term[x + 2] == 't':
            return 1.5
        elif term[x + 1] == 'm':
            return 0.8
        else:
            return 0.3


def corres(term, qtype):
    x = term.find('/')
    term += '   '
    if x == -1:
        return 0
    if qtype == 'Q_other':
        if term[x + 1] == 'n' and not(term[x + 2] in ['l', 'h', 's', 'i', 't']):
            return True
        else:
            return False
    if qtype == 'Q_number':
        if term[x + 1] == 'm' or (term[0] in "0123456789"):
            return True
        else:
            return False
    if qtype == 'Q_person':
        if term[x + 1] == 'n' and term[x + 2] == 'h':
            return True
        else:
            return False
    if qtype == 'Q_place':
        if term[x + 1] == 'n' and (term[x + 2] == 'l' or term[x + 2] == 's'):
            return True
        else:
            return False
    if qtype == 'Q_organization':
        if term[x + 1] == 'n' and term[x + 2] == 'i':
            return True
        else:
            return False
    if qtype == 'Q_time':
        if term[x + 1] == 'n' and term[x + 2] == 't':
            return True
        else:
            return False
# -----------------------------------------------------------------


synonym.load_in_synonym()
dis = [10, 70, 60, 50, 40]
left = int(argv[1])
right = int(argv[2])
with open('sample_qtype.txt', 'r') as fqtype:
    with open('sample_out.txt' + str(left), 'r') as fin:
        with open('sample_question.txt', 'r') as fq:
            with open('final_answer.txt' + str(left), 'w') as fout:
                for skip in range(1, left):
                    fqtype.readline()
                    fq.readline()
                for cases in range(left, right + 1):
                    print 'Doing', cases
                    qtype = fqtype.readline().strip()
                    termsq = fq.readline().strip().split('\t')
                    val = [0 for index in range(10000)]
                    fin.readline()
                    s = fin.readline().strip().split('\t')
                    sim_array = [1]
                    for i in range(1, len(s)):
                        maxs = 0
                        cc = 0
                        for j in range(len(termsq)):
                            sim = synonym.get_similar(s[i], termsq[j])
                            if sim > maxs:
                                maxs = sim
                                cc = j
                        sim_array.append(maxs)
                        if maxs > 0.5:
                            for j in range(i - 4, i + 4):
                                if (j >= 0) and (j < len(s)):
                                    # print i, j
                                    if (cc > 5) or (cc < 1):
                                        val[j] += maxs * dis[abs(i - j)]
                                    else:
                                        val[j] += maxs * synonym.coef[cc - 1] * dis[abs(i - j)]
                    maxv = 0
                    ans = ''
                    for i in range(1, len(s)):
                        # print val[i], s[i],
                        if val[i] / sim_array[i] / sim_array[i] > maxv:
                            if corres(s[i], qtype):
                                maxv = val[i] / sim_array[i] / sim_array[i]
                                ans = s[i]
                    if ans == '':
                        for i in range(1, len(s)):
                            ret = corres2(s[i], qtype)
                            if val[i] * ret / sim_array[i] > maxv:
                                maxv = val[i] * ret / sim_array[i]
                                ans = s[i]
                    print >> fout, ans[: ans.find('/')]
                    fin.readline()
