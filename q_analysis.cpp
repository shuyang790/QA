/*************************************************************************
    > File Name: word_segmentation.cpp
    > Author:
    > Created Time: 一 12/14 21:51:19 2015
 ************************************************************************/

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <string>
#include <vector>
#include <iostream>
#include <unistd.h>
#include <pthread.h>

#include "segment_dll.h"
#include "postag_dll.h"
#include "ner_dll.h"
#include "parser_dll.h"


using namespace std;

#define STR_LEN 65536

void * segment(char *src_filename, char *segment_filename,
				char *ner_filename, char *parser_filename,
				int startno, int endno){

        void * segmentor = segmentor_create_segmentor("./ltp_data/cws.model");
        void * postagger = postagger_create_postagger("./ltp_data/pos.model");
		void * recognizer = ner_create_recognizer("./ltp_data/ner.model");
		void * parser = parser_create_parser("./ltp_data/parser.model");

		char *str = new char[STR_LEN];

		FILE *fin, *fseg, *fner, *fparser;

		fin = fopen(src_filename, "r");

		if (startno) {
			fseg = fopen(segment_filename, "a"),
			fner = fopen(ner_filename, "a"),
			fparser = fopen(parser_filename, "a");
		}
		else {
			fseg = fopen(segment_filename, "w"),
			fner = fopen(ner_filename, "w"),
			fparser = fopen(parser_filename, "w");
		}

		vector <string> questions;

        while (fgets(str, STR_LEN, fin) != NULL) {
			string tmp = string(str);
			while (tmp.size() > 0 &&
					(tmp[tmp.size()-1] == '\n' || tmp[tmp.size()-1] == '\r'))
				tmp.erase(tmp.size()-1);
			questions.push_back(tmp);
		}

		fclose(fin);

		for (int i=startno; i<questions.size() && i<endno; i++) {
			vector <string> words, postags;
			vector <string> netags;
			vector <int> heads;
			vector <string> deprels;
			int len;

			if (!questions[i].size())
				goto nxt;

			len = segmentor_segment(segmentor, questions[i], words);
			postagger_postag(postagger, words, postags);
			ner_recognize(recognizer, words, postags, netags);
			parser_parse(parser, words, postags, heads, deprels);

			for (int j=0; j<len; j++) {
				fprintf(fseg, "%s/%s\t", words[j].c_str(), postags[j].c_str());
				if (netags[j]!=string("O"))
					fprintf(fner, "%s/%s\t", words[j].c_str(), netags[j].c_str());
				/* TODO: parser info print */
			}

nxt:
			fprintf(stderr, "\r#\t%d", i);
			fprintf(fseg, "\n");
			fprintf(fner, "\n");
			fprintf(fparser, "\n");
		}

		fclose(fseg);
		fclose(fner);
		fclose(fparser);

		delete []str;

		parser_release_parser(parser);
		ner_release_recognizer(recognizer);
        postagger_release_postagger(postagger);
        segmentor_release_segmentor(segmentor);
        return 0;
}

int main(int argc, char *argv[]) {
		segment("./questions/provided/q_facts.txt",
				"./questions/q_facts_segged.txt",
				"./questions/q_facts_segged_ner.txt",
				"./questions/q_facts_segged_psr.txt",
				000, 9000);
        return 0;
}
