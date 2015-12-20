#!/usr/bin/python

import random

f_online = open("./online/zhidao_answer.txt", "r")
online_content = f_online.readlines()
f_online.close()

f_close = open("./answer_fact_zwt.txt", "r")
close_content = f_close.readlines()
f_close.close()

f = open("open.txt", "w")

i = 0
j = 0
for k in range(8000):
    num_o = int(online_content[i].split("\t")[0])
    num_c = int(close_content[j].split("\t")[0])
    if num_o < num_c:
        f.write(online_content[i])
        i += 1
    elif num_o == num_c:
        f.write(online_content[i])
        i += 1
        j += 1
    else:
        f.write(close_content[j])
        j += 1
        if num_o == num_c:
            i += 1

f.close()
