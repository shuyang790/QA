#include <cstdio>
#include <iostream>
#include <cmath>
#include <map>
#include <cstring>
#include <cstdlib>
#include <algorithm>

using namespace std;

const char* file = "wiki_seg_0";

const int maxn = 20000012;
const int M = 20000012;

const int maxlen = ~0U >> 1;

const int numart = 1000012;

struct record
{
	int v,w;
	record *next;
}*e,*P, *point[M];



FILE *infile, *outfile, *quesfile, *recfile;
char str[maxn];
int article = 0, totchar = 0, totword = 0,len;
int Start[M],End[M];
string word;
string word_set[M];
double word_val[M];
char *Arr;


int num[numart],timesum[numart];
double sum[numart];
int val, questot(0);


char filename[256];
map<string, int> word_num;


void Add_word(int u,int v)
{
	//cerr << u << ' ' << v << endl;
	if (point[u] != NULL && v == point[u] -> v)
	{
		++ (point[u] -> w);
	}
	else
	{
		P -> v = v;
		P -> w = 1;
		P -> next = point[u];
		point[u] = P ++;
	}
}

int check()
{
	if (str[0] == '<')
	{
		if (strstr(str,"doc") != NULL)
		{
			if (str[1] == '/')
				return 2;
			return 1;
		}
	}
	return 0;
}

bool getword()
{
	word = "";
	for(;len < strlen(str); ++ len)
	{
		if (str[len] ==	'\t')
		{
			++ len;
			return true;
		}
		word = word + str[len];
	}
	if (word != "")
		return true;
	return false;
}
bool getword_ques()
{
	int tmp = -1;
	bool flag = false;
	word = "";

	for(;len < strlen(str); ++ len)
	{
		if (str[len] == ' ')
		{
			++ len;
			break;
		}
		word = word + str[len];
	}
	if (word != "")
	{
		if (tmp == -1)
		{
			int o = word.find('/');
			if (word[o + 1] == 'n')
			{
				tmp = 1;
				if (o + 2 < word.length())
					if (word[o + 2] != 'd')
						tmp = 2;
			}
		}
		val = tmp;
	}
	return word != "\n";
}
bool cmp(int x, int y)
{
	if (sum[x] > sum[y])
		return true;
	return false;
}
int main()
{
	if ((Arr = (char*)malloc(maxlen)) == NULL)
	{
		cerr << "malloc error" << endl;
		return 0;
	}
	else
	{
		cerr << "malloc successful" << endl;
	}

	if ((e = (record*)malloc(maxlen)) == NULL)
	{
		cerr << "malloc error" << endl;
		return 0;
	}
	else
	{
		P = e;
		cerr << "malloc successful" << endl;
	}
	memset(point, NULL, sizeof(point));


	for(int t = 0;t < 10; ++ t)
	{

		sprintf(filename, "%s%d", file, t);

		infile = fopen(filename,"r");
		while (fgets(str, maxn, infile) != NULL)
		{

			
			int flag = check();
			if (flag == 1)
				Start[++article] = totchar;
			if (flag == 2)
				End[article] = totchar - 1;
			if (flag == 0)
			{

				for(int i = 0;i < strlen(str);++i)
					Arr[totchar++] = str[i];
				len = 0;
				while (getword())
				{

					//cerr << word << endl;
					//cerr << word << ' ' << word_num[word] << endl;
					if (word_num[word] == 0)
					{
						word_num[word] = ++totword;
						word_set[totword] = word;
					}
					//cerr << word << endl;
					//cerr << word << ' ' << word_num[word] << endl;
					Add_word(word_num[word],article);
				}
			}
			//cerr <<  100.0 * totchar / (1.56* 1024 * 1024 * 1024) << endl; 
		}
		cerr << "file" << t << "done" << endl;
	}
	/*outfile = fopen("wiki.out","w");
	fputs(Arr, outfile);

	recfile = fopen("article.out","w");
	fprintf(recfile, "%d\n", article);
	for(int i = 1;i <= article; ++ i)
	{
		fprintf(recfile, "%d %d %d\n", i, Start[i], End[i]);
	}
	fclose(recfile);
	recfile = fopen("word.out","w");
	fprintf(recfile, "%d\n", totword);
	for(int i = 1;i <= totword; ++ i)
	{
		fprintf(recfile, "%d %s\n", i, word_set[i].c_str());
	}
	fclose(recfile);
	recfile = fopen("recfile.out","w");
	for(int i = 1;i <= totword; ++ i)
	{
		for(record *it = point[i];it != NULL;it = it -> next)
			fprintf(recfile, "%d %d %d\n", i, it -> v, it -> w);
	}
	fclose(recfile);
	cerr << "record complete" << endl;*/

	for(int i = 1;i <= totword; ++ i)
	{
		int tmp = 0;
		for(record *it = point[i];it != NULL;it = it -> next)
			++tmp;
		word_val[i] = log(article / (1 + tmp));
	}

	quesfile = fopen("q_facts_sample_segged_kwd.txt","r");
	outfile = fopen("ans_sample.out", "w");
	recfile = fopen("test.out","w");
	while (fgets(str, maxn, quesfile) != NULL)
	{
		++questot;
		len = 0;
		cerr << questot << endl;
		memset(sum,0,sizeof(sum));
		memset(timesum,0,sizeof(timesum));
		int timetot = 0;
		while (getword_ques())
		{
			//cerr << word << ' ' << val << endl;
			//cerr << word << endl;
			//cerr << word << ' ' << word_num[word] << endl;
			
			if (word_num[word] == 0)
				continue;
			int tmpk = word_num[word];
			fprintf(recfile, "%s %d %.2lf %d\n",word.c_str(),tmpk,word_val[tmpk],val);
			if (val == 2) ++timetot;
			if (val > 0)
			for(record* j = point[tmpk];j !=  NULL; j = j -> next)
			{
				if (val == 1) sum[j -> v] += j -> w * word_val[tmpk];
				if (val == 2) 
				{
					sum[j -> v] += j -> w * word_val[tmpk] * 10;
					timesum[j -> v] ++;
				}
			}
			//cerr << word << endl;
			//cerr << word << ' ' << word_num[word] << endl;

		}
		int tmpn = 0;
		for(int i = 1;i <= article; ++ i)
		if (timesum[i] == timetot)
			num[++tmpn] = i;
		sort(num + 1, num + tmpn + 1, cmp);
		fprintf(outfile, "%d\n",questot);
		for(int i = 1;i <= min(5,tmpn); ++ i)
		{
			fprintf(outfile, "<Start>\n");
			for(int j = Start[num[i]];j <= End[num[i]]; ++ j)
				fprintf(outfile, "%c", Arr[j]);
			fprintf(outfile, "<End>\n");
		}
	}
	fclose(quesfile);
	fclose(outfile);
	fclose(recfile);
}