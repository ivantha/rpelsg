#include <cmath>
#include <cstdio>
#include <cstdlib>
#include "misc.h"

long hash31(long long a, long long b, long long x)
{

	long long result;
	long lresult;  

	// return a hash of x using a and b mod (2^31 - 1)
	// may need to do another mod afterwards, or drop high bits
	// depending on d, number of bad guys
	// 2^31 - 1 = 2147483647

	//  result = ((long long) a)*((long long) x)+((long long) b);
	result=(a * x) + b;
	result = ((result >> HL) + result) & MOD;
	lresult=(long) result; 

	return(lresult);
}

long fourwise(long long a, long long b, long long c, long long d, long long x)
{
	long long result;
	long lresult;

	// returns values that are 4-wise independent by repeated calls
	// to the pairwise independent routine. 

	result = hash31(hash31(hash31(x,a,b),x,c),x,d);
	lresult = (long) result;
	return lresult;
}

int medselect(int k, int n, int arr[]) 
{
	int a, temp;

	MEDIAN
}

long long llmedselect(int k, int n, long long arr[]) 
{
	long long a, temp;

	MEDIAN
}

double dmedselect(int k, int n, double arr[]) 
{
	double a, temp;

	MEDIAN
}

long lmedselect(int k, int n, long arr[]) 
{
	long a, temp;

	MEDIAN
}

/*
--------------------------------------------------------------------
This works on all machines.  To be useful, it requires
-- that the key be an array of int's, and
-- that the length be the number of int's in the key
--------------------------------------------------------------------
*/
unsigned int hashword(const unsigned int*	  k,                   /* the key, an array of int values */
					  size_t			      length,              /* the length of the key, in size_t */
					  int					  initval)			   /* the previous hash, or an arbitrary value */
{
	unsigned int a,b,c;

	/* Set up the internal state */
	a = b = c = 0xdeadbeef + (((unsigned int)length)<<2) + initval;

	/*------------------------------------------------- handle most of the key */
	while (length > 3)
	{
		a += k[0];
		b += k[1];
		c += k[2];
		mix(a,b,c);
		length -= 3;
		k += 3;
	}

	/*------------------------------------------- handle the last 3 uint32_t's */
	switch(length)                     /* all the case statements fall through */
	{ 
	case 3 : c+=k[2];
	case 2 : b+=k[1];
	case 1 : a+=k[0];
		final(a,b,c);
	case 0:     /* case 0: nothing left to add */
		break;
	}
	/*------------------------------------------------------ report the result */
	return c;
}

