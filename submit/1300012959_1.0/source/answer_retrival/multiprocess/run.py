import os
for i in range(4):
    os.system("./python extract.py %d %d &" % (i * 10 + 1, i * 10 + 10))
