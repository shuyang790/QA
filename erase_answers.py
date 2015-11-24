#!/usr/bin/python

filename = "data_stage1/sample_questions.txt"
filename = "questions/qa_facts.txt"

f = open(filename, "r")
lines = f.readlines()
f.close()
f = open(filename, "w")
for line in lines:
	newline = line.split("\t")[0].split(" ")[0]
#	print (newline + "#")
	if newline[-1]!='\n':
		newline = newline + '\n'
	f.write(newline)
f.close()
