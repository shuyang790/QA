/*************************************************************************
    > File Name: word_segmentation.cpp
    > Author:
    > Created Time: 一 12/14 21:51:19 2015
 ************************************************************************/

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <iostream>
#include <unistd.h>
#include <pthread.h>

#include "segment_dll.h"
#include "postag_dll.h"


#define NUM_THREAD 4

using namespace std;

pthread_t threads[NUM_THREAD];

const char _srcname [] = "./extracted_chs/wiki_chs_00";
const char _dstname [] = "./extracted_chs_seg_ltp/wiki_seg_00";

const int start_num = 6;  /* START NUMBER of WIKI BLOCK */
const int end_num = 10;   /* END NUMBER of WIKI BLOCK */

#define STR_LEN 65536


void segment_file(void * segmentor, void * postagger,
                char * srcname, char * dstname) {

		char *str = new char[STR_LEN];

        FILE *fin = fopen(srcname, "r");
		vector < vector<string> > passages;
        vector <string> psg;
        char ch;
		fgets(str, STR_LEN, fin);
        while (fgets(str, STR_LEN, fin) != NULL) {
			string tmp = string(str);
			while (tmp.size() > 0 &&
					(tmp[tmp.size()-1] == '\n' || tmp[tmp.size()-1] == '\r'))
				tmp.erase(tmp.size()-1);
			if (!strncmp(str, "</doc>", 6)){
				passages.push_back(psg);
				psg.clear();
				fgets(str, STR_LEN, fin);
			}
			else
				psg.push_back(tmp);
		}
        fclose(fin);
        fprintf(stderr, "\tfile '%s' read.\n", srcname);

        FILE *fout = fopen(dstname, "w");

		for (int k=0; k<passages.size(); k++){
			fprintf(fout, "<doc>\n");
			for (int l = 0; l < passages[k].size(); l++){

				vector <string> words, postags;
				int len = segmentor_segment(segmentor, passages[k][l], words);
				postagger_postag(postagger, words, postags);

				for (int i=0; i<len; i++)
                    fprintf(fout, "%s/%s\t", words[i].c_str(), postags[i].c_str());
				fprintf(fout, "\n");
			}
			fprintf(fout, "</doc>\n");
		}
        fclose(fout);
        fprintf(stderr, "file '%s' segmented to '%s'\n", srcname, dstname);

		delete []str;
}


void * segment(void *arg){
        int num = *(int*)arg;

        void * segmentor = segmentor_create_segmentor("../ltp_data/cws.model");
        void * postagger = postagger_create_postagger("../ltp_data/pos.model");

        for (int i=num + start_num; i<end_num; i+=NUM_THREAD){
                char * srcname = new char[strlen(_srcname)+1];
                char * dstname = new char[strlen(_dstname)+1];
                strcpy(srcname, _srcname);
                strcpy(dstname, _dstname);
                srcname[strlen(srcname)-1] = i + '0';
                dstname[strlen(dstname)-1] = i + '0';
                segment_file(segmentor, postagger, srcname, dstname);
				delete []srcname;
				delete []dstname;
        }

        postagger_release_postagger(postagger);
        segmentor_release_segmentor(segmentor);
        return 0;
}

int main(int argc, char *argv[]) {

        for (int i=0, *t; i<NUM_THREAD; i++){
                t = new int;
                *t = i;
                pthread_create(threads+i, NULL, segment, t);
        }
        for (int i=0; i<NUM_THREAD; i++)
                pthread_join(threads[i], NULL);

        return 0;
}
