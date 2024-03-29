#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <ctime>
#include <vector>
#include <set>
#include <map>
#include <algorithm>

#include "misc.h"
#include "RandomGenerator.h"
#include "Vertex.h"

#define NATURALBASE	2.71828
#define	GOODQUERY	5
#define GOODSUBGRAPHQUERY	5

using namespace std;

typedef pair<string, Vertex*> VertexPair;
typedef pair<int, float> ErrorPair;

// Global data structure
map<string, Vertex*> vertexmap;
vector<CMSketch* > sketchvec;

int memory = 0;
double ratio_sum = (double)0.0;
double ratio_width = (double)0.0;
int	   width0 = 0;

string streamfile = "";
string queryfile = "";
string samplefile = "";
string workloadfile = "";
string answerfile = "";

fstream resultfile;

template <class T>
void ConvertFromString(T&, const string &);

// sort papers by year
struct SortByRatio
{
	bool operator()(const Vertex* start, const Vertex* end)
	{
		float startratio = (float)(start->frequency)/start->outdegree;
		float endratio = (float)(end->frequency)/end->outdegree;
		if (startratio > endratio)
			return true;
		return false;
	}
};

struct SortByWLRatio
{
	bool operator()(const Vertex* start, const Vertex* end)
	{
		float startratio = (float)(start->frequency)/start->weight;
		float endratio = (float)(end->frequency)/end->weight;
		if (startratio > endratio)
			return true;
		return false;
	}
};

struct SortByError
{
	bool operator()(const ErrorPair& start, const ErrorPair& end)
	{
		float startratio = start.second;
		float endratio = end.second;
		if (startratio > endratio)
			return true;
		return false;
	}
};

struct SortByType
{
	bool operator()(const ErrorPair& start, const ErrorPair& end)
	{
		if (start.first < end.first)
			return true;
		else if (start.first == end.first)
		{
			if (start.second > end.second)
				return true;
		}

		return false;
	}
};

void test_random()
{
	srand((unsigned int)time(NULL));
	RandomGenerator rg;
	rg.RGInit(rand(),2);

	for (int i = 0; i < 20; i++)
	{
		// long answer = rg.random_int();
		// cout << answer << endl;

		// double answer = rg.RGNormal();
		// cout << answer << endl;

		// double answer = rg.RGStabledbn(0.5);
		// cout << answer << endl;

		// double answer = rg.RGCauchy();
		// cout << answer << endl;

		// double answer = rg.RGAltstab(0.5);
		// cout << answer << endl;

		// double answer = rg.RGStable(0);
		// cout << answer << endl;

		double answer = rg.RGZipf(1.25, 100);
		cout << answer << endl;
	}
}

void test_median()
{
	int array[] = {0,100,90,80,70,60,50,40,30,20,10};
	int ans = medselect(5, 10, array);

	cout << ans << endl;
}

void test_hash()
{
	string s1 = "Charu	Peixiang";
	size_t s1_len = s1.size();
	unsigned int* words = new unsigned int[s1_len];

	for (size_t i = 0; i < s1_len; i++)
	{
		words[i] = (int)s1[i];
		cout << words[i] << '\t';
	}
	cout << endl;

	unsigned int value = hashword(words, s1_len, 0);

	cout << value << endl;

	if (words)
	{
		delete []words;
		words = NULL;
	}
}

unsigned int hashstring(const string& s1)
{
	size_t s1_len = s1.size();
	unsigned int* words = new unsigned int[s1_len];

	for (size_t i = 0; i < s1_len; i++)
		words[i] = (int)s1[i];

	unsigned int value = hashword(words, s1_len, 0);

	if (words)
	{
		delete []words;
		words = NULL;
	}
	return value;
}

void baseloading(string filename)
{
	fstream infile;
	infile.open(filename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the data file." << endl;
		exit(1);
	}

	CMSketch* pBaseSketch = sketchvec[0];

	string line;
	int edgecount = 0;

	cout << "Beginning parsing the data file" << endl;

	while (getline(infile,line))
	{
		edgecount++;

		if (edgecount % 500000 == 0)
			cout << "Now processing the " << edgecount << "th edge. " << endl;

		unsigned int value = hashstring(line);
		pBaseSketch->Update(value, 1);
	}

	infile.close();
}

void basequery(string filename)
{
	fstream infile;
	infile.open(filename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the query file." << endl;
		exit(1);
	}

	CMSketch* pBaseSketch = sketchvec[0];

	string line;
	int edgecount = 0;
	float relative_error = 0.0;

	cout << "Beginning processing the query file" << endl;

	int goodquery = 0;

	while (getline(infile,line))
	{
		edgecount++;

		if (edgecount % 1000 == 0)
			cout << "Now processing the " << edgecount << "th query. " << endl;

		string source = "";
		size_t pos = line.find_last_of('\t');
		source = line.substr(0, pos);

		string strfreq = line.substr(pos+1, line.size()-1);
		int frequency = 0;
		ConvertFromString(frequency, strfreq);

		unsigned int value = hashstring(source);
		int estvalue = pBaseSketch->PointEst(value);

		float one_error = (float)(estvalue-frequency)/frequency;

		relative_error += one_error;

		if (one_error <= GOODQUERY)
			goodquery++;
	}

	relative_error/= edgecount;

	cout << "Global Sketch relative error = " << relative_error << endl;
	cout << "Global Sketch good queries = " << goodquery << " Out of " << edgecount << endl;

	resultfile << "Global Sketch:" << endl;
	resultfile << "Global Sketch relative error = " << relative_error << endl;
	resultfile << "Global Sketch good queries = " << goodquery << " Out of " << edgecount << endl;
	resultfile << endl;

	infile.close();
}

void basegraphquery(string filename)
{
	fstream infile;
	infile.open(filename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the query file." << endl;
		exit(1);
	}

	CMSketch* pBaseSketch = sketchvec[0];
	float relative_error = 0.0;
	int goodquery = 0;

	vector<vector<string> > queryvec;

	string line;
	cout << "Beginning processing the query file" << endl;

	string strpivot = "";

	while (getline(infile,line))
	{
		string source = "";
		size_t pos = line.find_first_of('\t');
		source = line.substr(0, pos);

		if (source != strpivot)
		{
			vector<string> newquery;
			newquery.push_back(line);
			queryvec.push_back(newquery);
			strpivot = source;
		}
		else
		{
			vector<string>& oldquery = queryvec[queryvec.size()-1];
			oldquery.push_back(line);
		}
	}

	infile.close();

	for (size_t i = 0; i < queryvec.size(); i++)
	{
		vector<string>& subgraphquery = queryvec[i];
		int aggestvalue = 0;
		int aggtruevalue = 0;
		for (size_t j = 0; j < subgraphquery.size(); j++)
		{
			string line = subgraphquery[j];

			string source = "";
			size_t pos = line.find_last_of('\t');
			source = line.substr(0, pos);

			string strfreq = line.substr(pos+1, line.size()-1);
			int frequency = 0;
			ConvertFromString(frequency, strfreq);

			unsigned int value = hashstring(source);
			int estvalue = pBaseSketch->PointEst(value);

			aggtruevalue += frequency;
			aggestvalue += estvalue;
		}

		float one_error = (float)(aggestvalue-aggtruevalue)/aggtruevalue;
		relative_error += one_error;
		if (one_error <= GOODSUBGRAPHQUERY)
			goodquery++;
	}

	relative_error/= queryvec.size();

	resultfile << "Global Sketch:" << endl;
	resultfile << "Global Sketch relative error = " << relative_error << endl;
	resultfile << "Global Sketch good queries = " << goodquery << " Out of " << queryvec.size() << endl;
	resultfile << endl;


	cout << "Global Sketch relative error = " << relative_error << endl;
	cout << "Global Sketch good queries = " << goodquery << " Out of " << queryvec.size() << endl;
}

void partition(vector<Vertex*>& vertexvec, size_t begin, size_t end, int width)
{
	cout << "Begin = " << begin << " End = " << end << " Width = " << width << endl;

	if (begin > end)
		return;

	int sumfreq = 0;
	int sumdegree = 0;
	float sumnumerate = 0;
	int sumdenom = 0;

	for (size_t i = begin; i <= end; i++)
	{
		sumfreq += vertexvec[i]->frequency;				// stands for f_i
		sumdegree += vertexvec[i]->outdegree;			// stands for k_i
		sumnumerate += (float)vertexvec[i]->outdegree * vertexvec[i]->outdegree / vertexvec[i]->frequency;
		sumdenom +=  vertexvec[i]->outdegree;
	}

	// Early termination : Type 2 
	
	if (sumdegree <= ratio_sum*width)
	{
		int new_width = sumdegree / ratio_sum;
		if (new_width == 0)
			new_width = 1;

		CMSketch* pOrigSketch = sketchvec[0];
		CMSketch* pSketch = new CMSketch(*pOrigSketch, new_width, 2);

		// The second kind of sketch which satisfy the above criterion 
		pSketch->SetType(2);
		
		for (size_t i = begin; i <= end; i++)
			vertexvec[i]->psketch = pSketch;

		sketchvec.push_back(pSketch);

		memory -= new_width * 2;
		
		cout << "My sum is small" << endl;
		return;
	}

	// Early termination : Type 1 

	if (width <= width0)
	{
		CMSketch* pOrigSketch = sketchvec[0];
		int depth = pOrigSketch->Depth();
		CMSketch* pSketch = new CMSketch(*pOrigSketch, width / ratio_width, 1);

		// The first kind of sketch which satisfy the above criterion 
		pSketch->SetType(1);

		for (size_t i = begin; i <= end; i++)
			vertexvec[i]->psketch = pSketch;

		sketchvec.push_back(pSketch);

		memory -= 1* width / ratio_width;

		cout << "My width is small" << endl;
		return;
	}

	float base =  (sumfreq * sumnumerate) / width / sumdenom;
	//	cout << "Base = " << base << endl;

	size_t minindex = 0;
	float  minvalue = 65536;

	int subsumfreq1 = 0;
	int subwidth1 = width/2;
	float subsumnumerate1 = 0;
	int subsumdenom1 = 0;

	int subsumfreq2 = sumfreq;
	int subwidth2 = width/2;
	float subsumnumerate2 = sumnumerate;
	int subsumdenom2 = sumdenom;

	for (size_t pos = begin; pos < end; pos++)
	{
		// The first tentative partition
		subsumfreq1 += vertexvec[pos]->frequency;
		subsumnumerate1 += (float)vertexvec[pos]->outdegree * vertexvec[pos]->outdegree / vertexvec[pos]->frequency;
		subsumdenom1 +=  vertexvec[pos]->outdegree;

		float subbase1 =  (subsumfreq1 * subsumnumerate1) / subwidth1 / subsumdenom1;

		subsumfreq2 -= vertexvec[pos]->frequency;
		subsumnumerate2 -= (float)vertexvec[pos]->outdegree * vertexvec[pos]->outdegree / vertexvec[pos]->frequency;
		subsumdenom2 -=  vertexvec[pos]->outdegree;

		float subbase2 =  (subsumfreq2 * subsumnumerate2) / subwidth2 / subsumdenom2;

		float errorgain = subbase1 + subbase2 - base;

		if (errorgain < minvalue)
		{
			minindex = pos;
			minvalue = errorgain;
		}
	}

	cout << "Min Index = " << minindex << " Min Value = " << minvalue << endl;

	partition(vertexvec, begin, minindex, subwidth1);
	partition(vertexvec, minindex+1, end, subwidth2);
}

void wlpartition(vector<Vertex*>& vertexvec, size_t begin, size_t end, int width)
{
	cout << "Begin = " << begin << " End = " << end << " Width = " << width << endl;

	if (begin > end)
		return;

	int sumfreq = 0;
	int sumweight = 0;
	int sumdegree = 0;
	int sumweightfreq = 0;
	float sumnumerate = 0;
	int sumdenom = 0;

	for (size_t i = begin; i <= end; i++)
	{
		sumfreq += vertexvec[i]->frequency;				// stands for f_i
		sumdegree += vertexvec[i]->outdegree;			// stands for k_i
		sumweight += vertexvec[i]->weight;				// stands for w_i
	
		sumnumerate += (float)vertexvec[i]->outdegree * vertexvec[i]->weight / vertexvec[i]->frequency;
		sumdenom +=  vertexvec[i]->weight;
	}

	// Early termination : Type 2 

	if (sumdegree <= ratio_sum*width)
	{
		CMSketch* pOrigSketch = sketchvec[0];

		int new_width = sumdegree / ratio_sum;
		if (new_width == 0)
			new_width = 1;

		CMSketch* pSketch = new CMSketch(*pOrigSketch, new_width, 2);
		
		// The second kind of sketch which satisfy the above criterion 
		pSketch->SetType(2);

		for (size_t i = begin; i <= end; i++)
			vertexvec[i]->psketch = pSketch;

		sketchvec.push_back(pSketch);

		memory -= new_width * 2;
		
		cout << "My sum is small" << endl;
		return;
	}

	// Early termination : Type 1 

	if (width <= width0)
	{
		CMSketch* pOrigSketch = sketchvec[0];
		int depth = pOrigSketch->Depth();

		// CMSketch* pSketch = new CMSketch(*pOrigSketch, width*RATIOWIDTH, depth/RATIOWIDTH);
		CMSketch* pSketch = new CMSketch(*pOrigSketch, width / ratio_width, 1);

		// The first kind of sketch which satisfy the above criterion 
		pSketch->SetType(1);

		for (size_t i = begin; i <= end; i++)
			vertexvec[i]->psketch = pSketch;

		sketchvec.push_back(pSketch);

		// memory -= width * depth;
		memory -= 1 * width / ratio_width;

		cout << "My width is small" << endl;
		return;
	}

	float base =  (sumfreq * sumnumerate) / width / sumdenom;
	//	cout << "Base = " << base << endl;

	size_t minindex = 0;
	float  minvalue = 65536;

	int subsumfreq1 = 0;
	int subwidth1 = width/2;
	float subsumnumerate1 = 0;
	int subsumdenom1 = 0;

	int subsumfreq2 = sumfreq;
	int subwidth2 = width/2;
	float subsumnumerate2 = sumnumerate;
	int subsumdenom2 = sumdenom;

	for (size_t pos = begin; pos < end; pos++)
	{
		// The first tentative partition
		subsumfreq1 += vertexvec[pos]->frequency;
		subsumnumerate1 += (float)vertexvec[pos]->weight * vertexvec[pos]->outdegree / vertexvec[pos]->frequency;
		subsumdenom1 +=  vertexvec[pos]->weight;

		float subbase1 =  (subsumfreq1 * subsumnumerate1) / subwidth1 / subsumdenom1;

		subsumfreq2 -= vertexvec[pos]->frequency;
		subsumnumerate2 -= (float)vertexvec[pos]->weight * vertexvec[pos]->outdegree / vertexvec[pos]->frequency;
		subsumdenom2 -=  vertexvec[pos]->weight;

		float subbase2 =  (subsumfreq2 * subsumnumerate2) / subwidth2 / subsumdenom2;

		float errorgain = subbase1 + subbase2 - base;

		if (errorgain < minvalue)
		{
			minindex = pos;
			minvalue = errorgain;
		}
	}

	cout << "Min Index = " << minindex << " Min Value = " << minvalue << endl;

	wlpartition(vertexvec, begin, minindex, subwidth1);
	wlpartition(vertexvec, minindex+1, end, subwidth2);
}

void sampling(string samplename, int width)
{
	vector<Vertex*> vertexvec;
	set<string> edgeset;

	fstream infile;
	infile.open(samplename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the sample file." << endl;
		exit(1);
	}

	string line;
	int edgecount = 0;

	cout << "Beginning parsing the sample file" << endl;

	while (getline(infile,line))
	{
		edgecount++;

		if (edgecount % 100000 == 0)
			cout << "Now processing the " << edgecount << "th edge. " << endl;

		string source = "";
		size_t pos = line.find_first_of('\t');
		source = line.substr(0, pos);

		if (edgeset.find(line) != edgeset.end())
		{
			// This edge has been detected before, increase the edge frequency

			map<string, Vertex*>::iterator ite = vertexmap.find(source);

			if (ite == vertexmap.end())
			{
				cout << "The source node can not be found. " << endl;
				exit(1);
			}

			Vertex* pvertex = ite->second;
			pvertex->frequency++;
		}
		else
		{
			// This edge appears for the first time

			edgeset.insert(line);

			map<string, Vertex*>::iterator ite = vertexmap.find(source);

			// The source vertex appears for the first time
			if (ite == vertexmap.end())
			{
				Vertex* pVertex = new Vertex;
				pVertex->label = source;
				pVertex->outdegree++;
				pVertex->frequency++;

				vertexvec.push_back(pVertex);

				VertexPair onepair(source, pVertex);
				vertexmap.insert(onepair);
			}
			else
			{
				// The source node has been detected before, but the edge is new
				Vertex* pVertex = ite->second;
				pVertex->outdegree++;
				pVertex->frequency++;
			}
		}
	}

	sort(vertexvec.begin(), vertexvec.end(), SortByRatio());

	partition(vertexvec, 0, vertexvec.size()-1, width);

	infile.close();
	edgeset.clear();
	vertexvec.clear();
}

void workloadsampling(string samplefile, string workloadfile, unsigned int width)
{
	map<string, unsigned int> authorweightmap;

	// Processing the workload file
	fstream wlfile;
	wlfile.open(workloadfile.c_str(), ios::in);
	if (!wlfile)
	{
		cout << "Error: Can't open the workload file." << endl;
		exit(1);
	}

	string line;
	int edgecount = 0;

	cout << "Beginning parsing the workload file" << endl;

	while (getline(wlfile,line))
	{
		edgecount++;

		string name = "";
		size_t pos = line.find_first_of('\t');
		name = line.substr(0, pos);
		
		string strweight =  line.substr(pos+1, line.size());
		unsigned int weight = 0;
		ConvertFromString(weight, strweight);
		
		pair<string, unsigned int> onepair;
		onepair.first = name;
		onepair.second = weight;
		authorweightmap.insert(onepair);
	}

	wlfile.close();

	// Processing the sample file
	vector<Vertex*> vertexvec;
	set<string> edgeset;

	fstream infile;
	infile.open(samplefile.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the sample file." << endl;
		exit(1);
	}

	line = "";
	edgecount = 0;

	cout << "Beginning parsing the sample file" << endl;

	while (getline(infile,line))
	{
		edgecount++;

		if (edgecount % 100000 == 0)
			cout << "Now processing the " << edgecount << "th edge. " << endl;

		string source = "";
		size_t pos = line.find_first_of('\t');
		source = line.substr(0, pos);

		if (edgeset.find(line) != edgeset.end())
		{
			// This edge has been detected before, increase the edge frequency

			map<string, Vertex*>::iterator ite = vertexmap.find(source);

			if (ite == vertexmap.end())
			{
				cout << "The source node can not be found. " << endl;
				exit(1);
			}

			Vertex* pvertex = ite->second;
			pvertex->frequency++;
		}
		else
		{
			// This edge appears for the first time

			edgeset.insert(line);

			map<string, Vertex*>::iterator ite = vertexmap.find(source);

			// The source vertex appears for the first time
			if (ite == vertexmap.end())
			{
				Vertex* pVertex = new Vertex;
				pVertex->label = source;
				pVertex->outdegree++;
				pVertex->frequency++;

				if (authorweightmap.find(source) ==  authorweightmap.end())
					pVertex->weight = 1;
				else
					// pVertex->weight = authorweightmap[source];
					pVertex->weight = authorweightmap[source]+1;

				vertexvec.push_back(pVertex);

				VertexPair onepair(source, pVertex);
				vertexmap.insert(onepair);
			}
			else
			{
				// The source node has been detected before, but the edge is new
				Vertex* pVertex = ite->second;
				pVertex->outdegree++;
				pVertex->frequency++;
			}
		}
	}

	infile.close();
	
	authorweightmap.clear();
	edgeset.clear();

	sort(vertexvec.begin(), vertexvec.end(), SortByWLRatio());

	wlpartition(vertexvec, 0, vertexvec.size()-1, width);

	vertexvec.clear();
}

void loading(string filename, int depth)
{
	fstream infile;
	infile.open(filename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the data file." << endl;
		exit(1);
	}

	// Create a sketch for vertices not in samples
	CMSketch* pOrigSketch = sketchvec[0];

	int new_width = memory/depth;

	CMSketch* pSketch = new CMSketch(*pOrigSketch, new_width, depth);

	// The last sketch for all data not in sample
	pSketch->SetType(3);

	sketchvec.push_back(pSketch);

	string line;
	int edgecount = 0;

	cout << "Beginning parsing the data file" << endl;

	unsigned int insample = 0;
	unsigned int innew = 0;

	while (getline(infile,line))
	{
		edgecount++;

		if (edgecount % 500000 == 0)
			cout << "Now processing the " << edgecount << "th edge. " << endl;

		string source = "";
		size_t pos = line.find_first_of('\t');
		source = line.substr(0, pos);

		map<string, Vertex*>::iterator ite = vertexmap.find(source);
		if (ite != vertexmap.end())
		{
			insample++;
			Vertex* pvertex = ite->second;
			if (pvertex->psketch)
			{
				unsigned int value = hashstring(line);
				pvertex->psketch->Update(value, 1);
			}
			else
			{
				cout << "There is a hole ! " << endl;
			}
		}
		else
		{
			innew++;
			// Vertex not in the samples, all put in the last sketch
			unsigned int value = hashstring(line);
			pSketch->Update(value, 1);
		}
	}

	cout << "Vertices in sample = " << insample << endl;
	cout << "Vertices in new sketch = " << innew << endl;

	infile.close();
}

void diagnose(vector<ErrorPair>& ErrorVec)
{
	sort(ErrorVec.begin(), ErrorVec.end(), SortByError());

	int oneerrornum = 0;
	float oneerror = 0.0;
	int twoerrornum = 0;
	float twoerror = 0.0;
	int threeerrornum = 0;
	float threeerror = 0.0;

	for(size_t i = 0; i < ErrorVec.size(); i++)
	{// cout << ErrorVec[i].second << " : " << ErrorVec[i].first << endl;
		if (ErrorVec[i].first == 1)
		{
			oneerrornum++;
			oneerror += ErrorVec[i].second;
		}
		else if (ErrorVec[i].first == 2)
		{
			twoerrornum++;
			twoerror += ErrorVec[i].second;
		}
		else if (ErrorVec[i].first == 3)
		{
			threeerrornum++;
			threeerror += ErrorVec[i].second;
		}
		else cout << "Error occurs " << endl;
	}

	cout << "Queries in Category 1 = " << oneerrornum << " Error From Category 1 = " << oneerror << endl;
	cout << "Queries in Category 2 = " << twoerrornum << " Error From Category 2 = " << twoerror << endl;
	cout << "Queries in Category 3 = " << threeerrornum << " Error From Category 3 = " << threeerror << endl;

	sort(ErrorVec.begin(), ErrorVec.end(), SortByType());

	fstream outfile;
	outfile.open("diagnose", ios::out);
	if (!outfile)
	{
		cout << "Error: Can't open the diagnose file." << endl;
		exit(1);
	}

	for (size_t i = 0; i < ErrorVec.size(); i++)
		outfile << i+1 << '\t' << ErrorVec[i].second << endl;
	outfile.close();

	// Output the threshold answer for the queries
	int type1good = 0;
	int type1all = 0;
	int type2good = 0;
	int type2all = 0;
	int type3good = 0;
	int type3all = 0;

	for (size_t i = 0; i < ErrorVec.size(); i++)
	{
		if (ErrorVec[i].first == 1)
		{
			type1all++;
			if (ErrorVec[i].second <= GOODQUERY)
				type1good++;
		}
		else if (ErrorVec[i].first == 2)
		{
			type2all++;
			if (ErrorVec[i].second <= GOODQUERY)
				type2good++;
		}
		else if (ErrorVec[i].first == 3)
		{
			type3all++;
			if (ErrorVec[i].second <= GOODQUERY)
				type3good++;
		}
	}

	cout << "For type 1 : Good = " << type1good << " Out of " << type1all << endl;
	cout << "For type 2 : Good = " << type2good << " Out of " << type2all << endl;
	cout << "For type 3 : Good = " << type3good << " Out of " << type3all << endl;
	cout << "For overall : Good = " << (type1good + type2good + type3good) << " Out of " << (type1all + type2all + type3all) << endl;

}

void query(string filename)
{

	fstream infile;
	infile.open(filename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the query file." << endl;
		exit(1);
	}

	string line;
	int edgecount = 0;
	float relative_error = 0.0;

	int goodcount = 0;

	vector<ErrorPair> ErrorVec;

	cout << "Beginning processing the query file" << endl;

	while (getline(infile,line))
	{
		edgecount++;

		if (edgecount % 1000 == 0)
			cout << "Now processing the " << edgecount << "th query. " << endl;

		string source = "";
		size_t pos = line.find_last_of('\t');
		source = line.substr(0, pos);

		string strfreq = line.substr(pos+1, line.size()-1);
		int frequency = 0;
		ConvertFromString(frequency, strfreq);

		pos = source.find_first_of('\t');
		string author = source.substr(0, pos);

		int estvalue = 0;

		int onetype = 0;

		map<string, Vertex*>::iterator mite = vertexmap.find(author);

		if(mite != vertexmap.end())
		{
			CMSketch* pSketch = mite->second->psketch;
			if (pSketch != NULL)
			{
				unsigned int value = hashstring(source);
				estvalue = pSketch->PointEst(value);
				onetype = pSketch->Type();
			}
			else
			{
				cout << "There is a hole detected in query " << endl;
			}
		}
		else
		{
			CMSketch* pSketch = sketchvec[sketchvec.size()-1];
			unsigned int value = hashstring(source);
			estvalue = pSketch->PointEst(value);
			onetype = pSketch->Type();
		}

		float oneerror = (float)(estvalue-frequency)/frequency;

		relative_error += oneerror;

		if (oneerror <= GOODQUERY)
			goodcount++;

		ErrorPair onepair;
		onepair.first = onetype;
		onepair.second = oneerror;

		ErrorVec.push_back(onepair);
	}

	relative_error/= edgecount;
	cout << "relative error = " << relative_error << endl;
	cout << "the number of good queries = " << goodcount << " out of " << edgecount << endl;

	resultfile << "relative error = " << relative_error << endl;
	resultfile << "the number of good queries = " << goodcount << " out of " << edgecount << endl;

	diagnose(ErrorVec);

	ErrorVec.clear();

	infile.close();
}

void graphquery(string filename)
{
	fstream infile;
	infile.open(filename.c_str(), ios::in);
	if (!infile)
	{
		cout << "Error: Can't open the query file." << endl;
		exit(1);
	}

	vector<vector<string> > queryvec;

	string line;
	cout << "Beginning processing the query file" << endl;

	string strpivot = "";

	while (getline(infile,line))
	{
		string source = "";
		size_t pos = line.find_first_of('\t');
		source = line.substr(0, pos);

		if (source != strpivot)
		{
			vector<string> newquery;
			newquery.push_back(line);
			queryvec.push_back(newquery);
			strpivot = source;
		}
		else
		{
			vector<string>& oldquery = queryvec[queryvec.size()-1];
			oldquery.push_back(line);
		}
	}

	infile.close();

	float relative_error = 0.0;
	int goodquery = 0;



	for (size_t i = 0; i < queryvec.size(); i++)
	{
		vector<string>& subgraphquery = queryvec[i];
		int aggestvalue = 0;
		int aggtruevalue = 0;
		for (size_t j = 0; j < subgraphquery.size(); j++)
		{
			string line = subgraphquery[j];

			string source = "";
			size_t pos = line.find_last_of('\t');
			source = line.substr(0, pos);

			string strfreq = line.substr(pos+1, line.size()-1);
			int frequency = 0;
			ConvertFromString(frequency, strfreq);

			pos = source.find_first_of('\t');
			string author = source.substr(0, pos);

			int estvalue = 0;

			map<string, Vertex*>::iterator mite = vertexmap.find(author);
			if(mite != vertexmap.end())
			{
				CMSketch* pSketch = mite->second->psketch;
				if (pSketch != NULL)
				{
					unsigned int value = hashstring(source);
					estvalue = pSketch->PointEst(value);
				}
				else
				{
					cout << "There is a hole detected in query " << endl;
				}
			}
			else
			{
				CMSketch* pSketch = sketchvec[sketchvec.size()-1];
				unsigned int value = hashstring(source);
				estvalue = pSketch->PointEst(value);
			}

			aggtruevalue += frequency;
			aggestvalue += estvalue;
		}

		float one_error = (float)(aggestvalue-aggtruevalue)/aggtruevalue;
		relative_error += one_error;
		if (one_error <= GOODSUBGRAPHQUERY)
			goodquery++;
	}

	relative_error/= queryvec.size();

	cout << "gSketch relative error = " << relative_error << endl;
	cout << "gSketch good quereis = " << goodquery << " Out of " << queryvec.size() << endl;

	resultfile << "gSketch relative error = " << relative_error << endl;
	resultfile << "gSketch good quereis = " << goodquery << " Out of " << queryvec.size() << endl;
}

void postprocessing()
{
	map<string, Vertex*>::iterator ite;

	for (ite = vertexmap.begin(); ite != vertexmap.end(); ite++)
	{
		if (ite->second)
		{
			(ite->second)->psketch = NULL;
			delete ite->second;
			ite->second = NULL;
		}
	}
	vertexmap.clear();

	vector<CMSketch* >::iterator vite;
	for (vite = sketchvec.begin(); vite != sketchvec.end(); vite++)
	{
		if (*vite)
		{
			delete *vite;
			*vite = NULL;
		}
	}
	sketchvec.clear();
}

int power2(int temp_width)
{
	int base = 1;
	while (base < temp_width)
		base <<= 1;

	return base;
}

/*
Sketch 0 0.00005 0.005 2 8 512 ./DBLP/author-stream ./DBLP/author-stream-sample ./DBLP/author-stream-query ./DBLP/answer
*/

void usage()
{
	cout << "Sketch 0{1} epsilon delta ratio_sum ratio_width width0 stream_file sample_file {workload_file} query_file answer_file" << endl;
	cout << "0: data sample only." << endl;
	cout << "1: both data sample and workload sample." << endl;
}

int main(int argc, char** argv)
{
	bool bsample = true;

	// Input processing

	if ((argc != 11) && (argc != 12))
	{
		usage();
		return -1;
	}

	double epsilon, errordelta;

	cout << "Option = " << argv[1] << endl;
	
	if (!strcmp(argv[1],"0"))
	{
		if (argc != 11)
		{
			usage();
			return -1;
		}

		string tempstr = argv[2];
		ConvertFromString(epsilon,tempstr);
		cout << "epsilon = " << epsilon << endl;
			
		tempstr = argv[3];
		ConvertFromString(errordelta,tempstr);
		cout << "errordelta = " << errordelta << endl;

		tempstr = argv[4];
		ConvertFromString(ratio_sum,tempstr);
		cout << "ratio_sum = " << ratio_sum << endl;

		tempstr = argv[5];
		ConvertFromString(ratio_width,tempstr);
		cout << "ratio_width = " << ratio_width << endl;

		tempstr = (string)argv[6];
		ConvertFromString(width0,tempstr);
		cout << "width0 = " << width0 << endl;
		
		streamfile = (string)argv[7];
		cout << "stream file = " << streamfile << endl;

		samplefile = (string)argv[8];
		cout << "sample file = " << samplefile << endl;

		queryfile = (string)argv[9];
		cout << "query file = " << queryfile << endl;

		answerfile = (string)argv[10];
		cout << "answer file = " << answerfile << endl;

	}
	else if (!strcmp(argv[1],"1"))
	{
		if (argc != 12)
		{
			usage();
			return -1;
		}

		bsample = false;

		string tempstr = argv[2];
		ConvertFromString(epsilon,tempstr);
		cout << "epsilon = " << epsilon << endl;

		tempstr = argv[3];
		ConvertFromString(errordelta,tempstr);
		cout << "errordelta = " << errordelta << endl;

		tempstr = argv[4];
		ConvertFromString(ratio_sum,tempstr);
		cout << "ratio_sum = " << ratio_sum << endl;

		tempstr = argv[5];
		ConvertFromString(ratio_width,tempstr);
		cout << "ratio_width = " << ratio_width << endl;

		tempstr = argv[6];
		ConvertFromString(width0,tempstr);
		cout << "width0 = " << width0 << endl;

		streamfile = (string)argv[7];
		cout << "stream file = " << streamfile << endl;

		samplefile = (string)argv[8];
		cout << "sample file = " << samplefile << endl;

		workloadfile = (string)argv[9];
		cout << "workload file = " << workloadfile << endl;

		queryfile = (string)argv[10];
		cout << "query file = " << queryfile << endl;

		answerfile = (string)argv[11];
		cout << "answer file = " << answerfile << endl;
	}
	else
	{
		usage();
		return -1;
	}

	// Preprocessing

	int temp_width = (int)floor(NATURALBASE/epsilon);
	int width = power2(temp_width);

	cout << "Epsilon = " << epsilon << " Width = " << width << endl;

	int temp_height = (int)floor(log(1/errordelta));
	int height = power2(temp_height);

	cout << "Delta = " << errordelta << " Height = " << height << endl;

	memory = width * height;
	cout << "Memory usage = " << width*height << " Bytes" << endl;

	resultfile.open(answerfile.c_str(), ios::out);
	if (!resultfile)
	{
		cout << "Error: Can't open the answer file." << endl;
		exit(1);
	}

	resultfile << "Parametric settings: " << endl;
	resultfile << "epsilon = " << epsilon << endl;
	resultfile << "delta = " << errordelta << endl;

	resultfile << "width = " << width << endl;
	resultfile << "height = " << height << endl;

	resultfile << "memory usage = " << memory << endl;
	resultfile << "width0 = " << width0 << endl;
	resultfile << "ratio_sum = " << ratio_sum << endl;
	resultfile << "ratio_width = " << ratio_width << endl;
	resultfile << endl;

	resultfile << "File information: " << endl;
	resultfile << "stream file = " << streamfile << endl;
	resultfile << "sample file = " << samplefile << endl;
	if(!bsample)
		resultfile << "workload sample file = " << workloadfile << endl;
	resultfile << "query file = " << queryfile << endl;
	resultfile << "answer file = " << answerfile << endl;
	resultfile << endl;

	//initialize Begin and End for the timer
	
	clock_t begin, end;             

	/**************** Baseline Algorithm *******************/

	srand((unsigned int)time(NULL));
	int seed = rand();

	CMSketch* psketch = new CMSketch(width, height, seed);
	sketchvec.push_back(psketch);

	baseloading(streamfile);
	
	begin = clock() * CLK_TCK;      //start the timer  
	
	// basequery(queryfile);
	basegraphquery(queryfile);

	end = clock() * CLK_TCK;        //stop the timer 

	cout << "time = " << (end-begin)/1000 << " milliseconds. " << endl;
	resultfile << "time = " << (end-begin)/1000 << " milliseconds. " << endl;

	/**************** Partition Algorithm *******************/

	begin = clock() * CLK_TCK;      //start the timer  

	if (bsample)
		// For sample data only
		sampling(samplefile, width);
	else
		// For both sample and workload
		workloadsampling(samplefile, workloadfile, width);

	end = clock() * CLK_TCK;        //stop the timer 

	resultfile << endl;
	resultfile << "Partitioned based Sketch: " << endl;

	cout << "sketch partition time = " << (end-begin)/1000 << " milliseconds. " << endl;
	resultfile << "sketch partition time = " << (end-begin)/1000 << " milliseconds. " << endl;

	cout << "The number of distinct vertices in the sample = " << vertexmap.size() << endl;
	resultfile << "memory consumption for partition = " << vertexmap.size() << endl;

	memory -= vertexmap.size();
	cout << "Memory Left = " << memory << endl;
	if (memory <= 0)
	{
		cout << "There is no space for the additional streams. Error " << endl;
		return -1;
	}

	// loading(streamfile, 1);
	loading(streamfile, height);

	cout << "The number of sketches = " << sketchvec.size() << endl;

	begin = clock() * CLK_TCK;      //start the timer  

	// query(queryfile);
	graphquery(queryfile);

	end = clock() * CLK_TCK;        //stop the timer 

	cout << "time = " << (end-begin)/1000 << " milliseconds. " << endl;
	
	resultfile << endl;
	resultfile << "time = " << (end-begin)/1000 << " milliseconds. " << endl;

	postprocessing();
	resultfile.close();

	system("pause");
	// Done!
	return 0;
}

template <class T>
void ConvertFromString(T& value, const string& s)
{
	stringstream ss(s);
	ss >> value;
}