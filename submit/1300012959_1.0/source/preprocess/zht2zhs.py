#!/usr/bin/python 

import os

for i in range(10):
    os.system("opencc -i wiki_0" + str(i) + " -o wiki_chs_0" + str(i) + " -c /usr/local/share/opencc/tw2s.json")
    
