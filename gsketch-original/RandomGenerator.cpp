#include "RandomGenerator.h"

/*************************************************************************/
/*	Some pseudo-random number generators sourced from other places		 */
/*************************************************************************/

// There are *THREE* alternate implementations of Random Generators here.
// One taken from Numerical Recipes in C, the second from www.agner.org
// The third is an internal C random library, srand
// The variable usenric controls which one is used: pick one 
// and stick with it, switching between the two will give unpredictable
// results.  This is controlled by the ran_init procedure, call it with
// usenric == 1 to use the Numerical Recipes gens
// usenric == 2 to use the agner.org PRNGs or
// usenric == 3 to use the inbuilt C routines

#define IA 16807
#define IM 2147483647
#define AM (1.0/IM)
#define IQ 127773
#define IR 2836
#define NDIV (1+(IM-1)/NTAB)
#define EPS 1.2e-7
#define RNMX (1.0-EPS)

float ran1(RandomGenerator* prng) 
{
	// A Random Number Generator that picks a uniform [0,1] random number
	// From Numerical Recipes, page 280
	// Should be called with a NEGATIVE value of idum to initialize
	// subsequent calls should not alter idum

	int j;
	long k;
	float temp;

	if (prng->floatidum <= 0 || !prng->iy) 
	{
		if (-(prng->floatidum) < 1) 
			prng->floatidum=1;
		else 
			prng->floatidum = -(prng->floatidum);
		for (j=NTAB+7;j>=0;j--) 
		{
			k=(prng->floatidum)/IQ;
			prng->floatidum=IA*(prng->floatidum-k*IQ)-IR*k;
			if (prng->floatidum < 0) 
				prng->floatidum+=IM;
			if (j<NTAB) 
				prng->iv[j]=prng->floatidum;
		}
		prng->iy=prng->iv[0];
	}
	k = (prng->floatidum)/IQ;
	prng->floatidum=IA*(prng->floatidum-k*IQ)-IR*k;
	if (prng->floatidum<0) 
		prng->floatidum += IM;
	j = prng->iy/NDIV;
	prng->iy=prng->iv[j];
	prng->iv[j]=prng->floatidum;
	if ((temp=(float)AM*prng->iy) > RNMX) 
		return (float)RNMX;
	else return temp;
}

long ran2(RandomGenerator* prng) 
{
	// A Random Number Generator that picks a uniform random number
	// from the range of long integers.
	// From Numerical Recipes, page 280
	// Should be called with a NEGATIVE value of idum to initialize
	// subsequent calls should not alter idum
	// This is a hacked version of the above procedure, so proceed with
	// caution.

	int j;
	long k;

	if (prng->intidum <= 0 || !prng->iy) 
	{
		if (-(prng->intidum) < 1) 
			prng->intidum=1;
		else 
			prng->intidum = -(prng->intidum);
		for (j=NTAB+7;j>=0;j--) 
		{
			k=(prng->intidum)/IQ;
			prng->intidum=IA*(prng->intidum-k*IQ)-IR*k;
			if (prng->intidum < 0) 
				prng->intidum+=IM;
			if (j<NTAB) 
				prng->iv[j]=prng->intidum;
		}
		prng->iy=prng->iv[0];
	}
	k = (prng->intidum)/IQ;
	prng->intidum=IA*(prng->intidum-k*IQ)-IR*k;
	if (prng->intidum<0) 
		prng->intidum += IM;
	j = prng->iy/NDIV;
	prng->iy=prng->iv[j];
	prng->iv[j]=prng->intidum;
	return prng->iy;
}

/**********************************************************************/

// Following routines are from www.agner.org

/************************* RANROTB.C ******************** AgF 1999-03-03 *
*  Random Number generator 'RANROT' type B                               *
*                                                                        *
*  This is a lagged-Fibonacci type of random number generator with       *
*  rotation of bits.  The algorithm is:                                  *
*  X[n] = ((X[n-j] rotl r1) + (X[n-k] rotl r2)) modulo 2^b               *
*                                                                        *
*  The last k values of X are stored in a circular buffer named          *
*  randbuffer.                                                           *
*                                                                        *
*  This version works with any integer size: 16, 32, 64 bits etc.        *
*  The integers must be unsigned. The resolution depends on the integer  *
*  size.                                                                 *
*                                                                        *
*  Note that the function RanrotAInit must be called before the first    *
*  call to RanrotA or iRanrotA                                           *
*                                                                        *
*  The theory of the RANROT type of generators is described at           *
*  www.agner.org/random/ranrot.htm                                       *
*                                                                        *
*************************************************************************/

unsigned long rotl (unsigned long x, unsigned long r) 
{
	return (x << r) | (x >> (sizeof(x)*8-r));
}

/* define parameters (R1 and R2 must be smaller than the integer size): */
#define JJ  10
#define R1   5
#define R2   3

/* returns some random bits */
unsigned long ran3(RandomGenerator* prng) 
{
	unsigned long x;

	/* generate next random number */

	x = prng->randbuffer[prng->r_p1] = rotl(prng->randbuffer[prng->r_p2], R1) 
		+  rotl(prng->randbuffer[prng->r_p1], R2);
	/* rotate list pointers */
	if (--prng->r_p1 < 0) prng->r_p1 = KK - 1;
	if (--prng->r_p2 < 0) prng->r_p2 = KK - 1;
	/* conversion to float */
	return x;
}

/* returns a random number between 0 and 1 */
double ran4(RandomGenerator* prng) 
{
	/* conversion to floating point type */
	return (ran3(prng) * prng->scale);
}

double zeta(long n, double theta) 
{

	// the zeta function, used by the below zipf function
	// (this is not often called from outside this library)
	// ... but have made it public now to speed things up

	int i;
	double ans=0.0;

	for (i=1; i <= n; i++)
		ans += pow(1./(double)i, theta);
	return(ans);
}

/**********************************************************************/
/* These are wrapper procedures for the uniform random number gens    */
/**********************************************************************/

RandomGenerator::RandomGenerator(void)
{
}

RandomGenerator::~RandomGenerator(void)
{
}

long RandomGenerator::random_int() 
{
	// returns a pseudo-random long integer.  Initialize the generator
	// before use!

	long response=0;

	switch (usenric)
	{
	case 1 : response=(ran2(this)); break;
	case 2 : response=(ran3(this)); break;
	case 3 : response=(rand()); break;
	}
	return response;
}

float RandomGenerator::random_float() 
{
	// returns a pseudo-random float in the range [0.0,1.0].  
	// Initialize the generator before use!
	float result=0;

	switch (usenric)
	{
	case 1 : result=(ran1(this)); break;
	case 2 : result=(float)(ran4(this)); break;
	case 3 : result=(float)(rand()); break;
	}
	return result;
}

/* this function initializes the random number generator.      */
/* Must be called before the first call to RanrotA or iRanrotA */
void RandomGenerator::RanrotAInit (unsigned long seed) 
{
	int i;

	/* put semi-random numbers into the buffer */
	for (i=0; i<KK; i++) 
	{
		randbuffer[i] = seed;
		seed = rotl(seed,5) + 97;
	}

	/* initialize pointers to circular buffer */
	r_p1 = 0;  
	r_p2 = JJ;

	/* randomize */
	for (i = 0;  i < 300;  i++) 
		ran3(this);
	scale = ldexp((float)1, (int)((-8)*(sizeof(unsigned long))));
}

void RandomGenerator::RGInit(long seed, int nric) 
{
	// Initialize the random number generators.  nric determines
	// which algorithm to use, 1 for Numerical Recipes in C, 
	// 0 for the other one. 
	iy=0;
	usenric=nric; 
	floatidum=-1;
	intidum=-1;
	iset=0;

	// set a global variable to record which algorithm to use
	switch (nric)
	{ 
	case 2 : 
		RanrotAInit(seed);
		break;
	case 1 : 
		if (seed>0) 
		{ 
			// to initialize the NRiC PRNGs, call it with a negative value
			// so make sure it gets a negative value!
			floatidum = -(seed);  
			intidum = -(seed);
		} 
		else 
		{
			floatidum=seed; 
			intidum=seed;
		}
		break;
	case 3 : 
		srand(seed);
		break;
	}

	// call the routines to actually initialize them
	random_float();
	random_int();
}

void RandomGenerator::RGReseed(long seed)
{
	switch (usenric)
	{ 
	case 2 : 
		RanrotAInit(seed);
		break;
	case 1 : 
		if (seed>0) { 
			// to initialize the NRiC PRNGs, call it with a negative value
			// so make sure it gets a negative value!
			floatidum = -(seed);  
			intidum = -(seed);
		} 
		else 
		{
			floatidum=seed; 
			intidum=seed;
		}
		break;
	case 3 : 
		srand(seed);
		break;
	}
} 

/**********************************************************************/
/* Next, a load of routines that convert uniform random variables     */
/* from [0,1] to stable distributions, such as Gaussian, Levy or      */
/* general                                                            */
/**********************************************************************/

double RandomGenerator::RGNormal() 
{
	// Pick random values distributed N(0,1) using the Box-Muller transform
	// Taken from numerical recipes in C p289
	// picks two at a time, returns one per call (buffers the other)

	double fac,rsq,v1,v2;
	if (iset == 0) 
	{
		do 
		{
			v1 = 2.0*random_float()-1.0;
			v2 = 2.0*random_float()-1.0;
			rsq=v1*v1+v2*v2;
		} while (rsq >= 1.0 || rsq == 0.0);

		fac = sqrt((double) -2.0*log((double)rsq)/rsq);
		gset=v1*fac;
		iset=1;
		return v2*fac;
	}
	else 
	{
		iset = 0;
		return gset;
	}
}

double RandomGenerator::RGStabledbn(double alpha) 
{
	// From "stable distributions", John Nolan, manuscript, p24
	// we set beta = 0 by analogy with the normal and Cauchy case
	// identical to the above routine, but returns a double instead 
	// of a long double (you'll see this a lot...)

	double theta, W, holder, left, right;

	theta=PI*(random_float() - 0.5);
	W = -log(random_float()); // takes natural log

	//  printf("theta %Lf, W = %Lf \n", theta, W);

	// some notes on Nolan's notes:
	// if beta == 0 then c(alpha,beta)=1; theta_0 = 0
	// expression reduces to sin alpha.theta / (cos theta) ^1/alpha
	//  * (cos (theta - alpha theta)/W) ^(1-alpha)/alpha
	left = (sin(alpha*theta)/pow(cos(theta), 1.0/alpha));
	right= pow(cos(theta*(1.0 - alpha))/W, ((1.0-alpha)/alpha));
	holder=left*right;
	return(holder);
}

long double RandomGenerator::RGCauchy() 
{
	// return a value from the Kauchy distribution
	// using the formula in 'Stable Distributions', p23
	// this is distributed Cauchy(1,0)

	return(tan(PI*(random_float() - 0.5)));
}

double RandomGenerator::RGAltstab(double p) 
{
	double u,v,result;

	u=random_float();
	v=random_float();
	result=pow(u,p);
	// result=exp(p*log(u));
	if (v<0.5) 
		result=-result;
	return(result);
}

double RandomGenerator::RGStable(double alpha) 
{
	// wrapper for the stable distributions above:
	// call the appropriate routine based on the value of alpha given

	// initializing it with the seed in idum
	// randinit must be called before entering this procedure for
	// the first time since it uses the random generators


	if (alpha==2.0) 
		return(RGNormal());
	else if (alpha==1.0)
		return(RGCauchy());
	else if (alpha<0.01)
		return(RGAltstab(-50.0));
	else 
		return (RGStabledbn(alpha));
}

long double RandomGenerator::RGZipf(double theta, long n) 
{
	// this draws values from the zipf distribution
	// this is mainly useful for test generation purposes
	// n is range, theta is skewness parameter 
	// theta = 0 gives uniform dbn,
	// theta > 1 gives highly skewed dbn. 

	double alpha;
	double zetan;
	double eta;
	double u;
	double uz;
	long double val;

	// randinit must be called before entering this procedure for
	// the first time since it uses the random generators

	alpha = 1. / (1. - theta);
	zetan = zeta(n, theta);
	eta = (1. - pow(2./n, 1. - theta)) / (1. - zeta(2.,theta)/zetan);

	u = random_float();
	uz = u * zetan;
	if (uz < 1.) 
		val = 1;
	else if (uz < (1. + pow(0.5, theta))) 
		val = 2;
	else val = 1 + (long long)(n * pow(eta*u - eta + 1., alpha));

	return(val);
}

double RandomGenerator::Fastzipf(double theta, long n, double zetan) 
{
	// this draws values from the zipf distribution
	// this is mainly useful for test generation purposes
	// n is range, theta is skewness parameter 
	// theta = 0 gives uniform dbn,
	// theta > 1 gives highly skewed dbn. 
	
	double alpha;
	double eta;
	double u;
	double uz;
	long double val;

	// randinit must be called before entering this procedure for
	// the first time since it uses the random generators

	alpha = 1. / (1. - theta);
	eta = (1. - pow(2./n, 1. - theta)) / (1. - zeta(2.,theta)/zetan);

	u = random_float();
	uz = u * zetan;
	if (uz < 1.) 
		val = 1;
	else if (uz < (1. + pow(0.5, theta))) 
		val = 2;
	else 
		val = 1 + (long long)(n * pow(eta*u - eta + 1., alpha));

	return(val);
}

