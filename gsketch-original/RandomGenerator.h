// Probabilistic Random Number Generators
#pragma once

#include "misc.h"

#define KK  17
#define NTAB 32

class RandomGenerator
{
public:
	int usenric;					 // which prng to use
	float scale;					 // 2^(- integer size) 
	long floatidum;
	long intidum;					 // needed to keep track of where we are in the nric random number generators
	long iy;
	long iv[NTAB];
	unsigned long randbuffer[KK];	 // history buffer 
	int r_p1, r_p2;					 // indexes into history buffer
	int iset;
	double gset;

private:

	void RanrotAInit(unsigned long seed);

public:
	RandomGenerator(void);
	~RandomGenerator(void);

	void RGInit(long, int);
	void RGReseed(long);

	long random_int();
	float random_float();

	double Fastzipf(double, long, double, RandomGenerator*);
	double Zeta(long, double);
	double RGNormal();
	double RGStabledbn(double);
	long double RGCauchy();
	double RGAltstab(double);
	double RGStable(double alpha);

	long double RGZipf(double theta, long n);
	double Fastzipf(double theta, long n, double zetan);

};
