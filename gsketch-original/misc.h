#ifndef MISC_H
#define MISC_H

#include <cmath>
#include <cstdlib>
#include <cstdio>

#define PI 3.141592653589793
#define MOD 2147483647
#define HL 31

#define SWAP(a,b) temp=(a);(a)=(b);(b)=temp;
// defined for the purposes of the median finding procedures below

/* 
Routine from Numerical Recipes
find the k'th element out of n that are in arr (assumed indexed from 1 to n)
*/
#define MEDIAN \
	\
	int i, ir, j, mid, l;\
	\
	l=1; \
	ir=n; \
	for (;;) { \
	if (ir <= l+1) { \
	if (ir == l+1 && arr[ir] < arr[l]) { \
	SWAP(arr[l],arr[ir]) \
	} \
	return arr[k]; \
	} \
	else \
	  { \
	  mid=(l+ir) >> 1; \
	  SWAP(arr[mid],arr[l+1]) \
	  if (arr[l] > arr[ir]) { \
	  SWAP(arr[l],arr[ir]) \
	  } \
	  if (arr[l+1] > arr[ir]) { \
	  SWAP(arr[l+1],arr[ir]) \
	  } \
	  if (arr[l] > arr[l+1]) { \
	  SWAP(arr[l],arr[l+1]) \
	  } \
	  i=l+1; \
	  j=ir; \
	  a=arr[l+1]; \
	  for (;;) { \
	  do i++; while (arr[i] < a);\
	  do j--; while (arr[j] > a);\
	  if (j < i) break;\
	  SWAP(arr[i],arr[j])\
	  }\
	  arr[l+1]=arr[j];\
	  arr[j]=a;\
	  if (j >= k) ir=j-1;\
	  if (j <= k) l=i;\
	  }\
	}\


#define rot(x,k) (((x)<<(k)) | ((x)>>(32-(k))))

/*
-------------------------------------------------------------------------------
mix -- mix 3 32-bit values reversibly.

This is reversible, so any information in (a,b,c) before mix() is
still in (a,b,c) after mix().

If four pairs of (a,b,c) inputs are run through mix(), or through
mix() in reverse, there are at least 32 bits of the output that
are sometimes the same for one pair and different for another pair.
This was tested for:
* pairs that differed by one bit, by two bits, in any combination
of top bits of (a,b,c), or in any combination of bottom bits of
(a,b,c).
* "differ" is defined as +, -, ^, or ~^.  For + and -, I transformed
the output delta to a Gray code (a^(a>>1)) so a string of 1's (as
is commonly produced by subtraction) look like a single 1-bit
difference.
* the base values were pseudorandom, all zero but one bit set, or 
all zero plus a counter that starts at zero.

Some k values for my "a-=c; a^=rot(c,k); c+=b;" arrangement that
satisfy this are
4  6  8 16 19  4
9 15  3 18 27 15
14  9  3  7 17  3
Well, "9 15 3 18 27 15" didn't quite get 32 bits diffing
for "differ" defined as + with a one-bit base and a two-bit delta.  I
used http://burtleburtle.net/bob/hash/avalanche.html to choose 
the operations, constants, and arrangements of the variables.

This does not achieve avalanche.  There are input bits of (a,b,c)
that fail to affect some output bits of (a,b,c), especially of a.  The
most thoroughly mixed value is c, but it doesn't really even achieve
avalanche in c.

This allows some parallelism.  Read-after-writes are good at doubling
the number of bits affected, so the goal of mixing pulls in the opposite
direction as the goal of parallelism.  I did what I could.  Rotates
seem to cost as much as shifts on every machine I could lay my hands
on, and rotates are much kinder to the top and bottom bits, so I used
rotates.
-------------------------------------------------------------------------------
*/
#define mix(a,b,c) \
{ \
	a -= c;  a ^= rot(c, 4);  c += b; \
	b -= a;  b ^= rot(a, 6);  a += c; \
	c -= b;  c ^= rot(b, 8);  b += a; \
	a -= c;  a ^= rot(c,16);  c += b; \
	b -= a;  b ^= rot(a,19);  a += c; \
	c -= b;  c ^= rot(b, 4);  b += a; \
}

/*
-------------------------------------------------------------------------------
final -- final mixing of 3 32-bit values (a,b,c) into c

Pairs of (a,b,c) values differing in only a few bits will usually
produce values of c that look totally different.  This was tested for
* pairs that differed by one bit, by two bits, in any combination
of top bits of (a,b,c), or in any combination of bottom bits of
(a,b,c).
* "differ" is defined as +, -, ^, or ~^.  For + and -, I transformed
the output delta to a Gray code (a^(a>>1)) so a string of 1's (as
is commonly produced by subtraction) look like a single 1-bit
difference.
* the base values were pseudorandom, all zero but one bit set, or 
all zero plus a counter that starts at zero.

These constants passed:
14 11 25 16 4 14 24
12 14 25 16 4 14 24
and these came close:
4  8 15 26 3 22 24
10  8 15 26 3 22 24
11  8 15 26 3 22 24
-------------------------------------------------------------------------------
*/
#define final(a,b,c) \
{ \
	c ^= b; c -= rot(b,14); \
	a ^= c; a -= rot(c,11); \
	b ^= a; b -= rot(a,25); \
	c ^= b; c -= rot(b,16); \
	a ^= c; a -= rot(c,4);  \
	b ^= a; b -= rot(a,14); \
	c ^= b; c -= rot(b,24); \
}

long hash31(long long, long long, long long);
long fourwise(long long, long long, long long, long long, long long);
int medselect(int, int, int*);
long long llmedselect(int, int, long long *);
double dmedselect(int, int, double *);
long lmedselect(int, int, long*);

unsigned int hashword(const unsigned int*, size_t, int);

#endif