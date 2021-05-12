#include "Vertex.h"

Vertex::Vertex(void)
{
	label = "";
	frequency = 0;
	outdegree = 0;
	weight = 1;
	psketch = NULL;
}

Vertex::~Vertex(void)
{
	psketch = NULL;
}
