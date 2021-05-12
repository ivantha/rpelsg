#pragma once

#include <string>

#include "MSketch.h"

using namespace std;

class Vertex
{
public:
	string label;
	unsigned int outdegree;
	unsigned int frequency;
	unsigned int weight;
	CMSketch* psketch;

	Vertex(void);
	~Vertex(void);
};
