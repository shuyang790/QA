CC=g++
FLAGS=-I../ltp-3.3.0/include/ltp
FLAGS+=-I../ltp-3.3.0/thirdparty/boost/include/boost 
FLAGS+=-L../ltp-3.3.0/lib/
FLAGS+=-lsegmentor -lboost_regex
FLAGS+=-lpostagger
FLAGS+=-lparser
FLAGS+=-lner
FLAGS+=-lpthread


q_analysis: q_analysis.cpp
	$(CC) -O2 -o q_analysis q_analysis.cpp $(FLAGS)

clean:
	rm q_analysis
