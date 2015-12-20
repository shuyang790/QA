#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import extract


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


extract.load_in_synonym()
dis = [80, 70, 60, 50, 40]
with open('sample_qtype.txt', 'r') as fqtype:
    with open('sample_out.txt', 'r') as fin:
        with open('sample_question.txt', 'r') as fq:
            for cases in range(100):
                qtype = fqtype.readline().strip()
                termsq = fq.readline().strip().split('\t')
                val = [0 for index in range(1000)]
                fin.readline()
                s = fin.readline().strip().split('\t')
                for i in range(1, len(s)):
                    maxs = 0
                    cc = 0
                    for j in range(len(termsq)):
                        sim = extract.get_similar(s[i], termsq[j])
                        if sim > maxs:
                            maxs = sim
                            cc = j
                    if maxs > 0.5:
                        for j in range(i - 4, i + 4):
                            if (j >= 0) and (j < len(s)):
                                # print i, j
                                if cc > 5:
                                    val[j] += maxs * dis[abs(i - j)]
                                else:
                                    val[j] += maxs * extract.coef[cc - 1] * dis[abs(i - j)]
                maxv = 0
                ans = ''
                for i in range(1, len(s)):
                    # print val[i], s[i],
                    if val[i] > maxv:
                        if corres(s[i], qtype):
                            maxv = val[i]
                            ans = s[i]
                print ans
                for i in range(1):
                    fin.readline()
