#include "MSketch.h"
#include "RandomGenerator.h"

double eps;	           //	1+epsilon = approximation factor
double delta;          //	probability of failure

CMSketch::CMSketch(void)
{
}

CMSketch::~CMSketch(void)
{
	if (counts)
	{
		if (counts[0])
		{
			delete []counts[0];
			counts[0] = NULL;
		}
		delete []counts;
		counts = NULL;
	}

	if (hasha)
	{
		delete []hasha;
		hasha = NULL;
	}

	if (hashb)
	{
		delete []hashb;
		hashb = NULL;
	}
}

CMSketch::CMSketch(int iwidth, int idepth, int seed)
{
	type = -1;

	// initialize the generator to pick the hash functions

	RandomGenerator rg;
	rg.RGInit(-abs(seed), 2);

	depth=idepth;
	width=iwidth;
	count=0;
	counts = new int*[depth];
	counts[0] = new int[depth*width];
	hasha = new unsigned int[depth];
	hashb = new unsigned int[depth];
	if (counts && counts[0] && hasha && hashb)
	{
		for (int j = 0; j < depth; j++)
		{
			// pick the hash functions
			hasha[j] = rg.random_int() & MOD;
			hashb[j] = rg.random_int() & MOD;

			counts[j]=(int *) counts[0]+(j*width);

			for(int i = 0; i < width; i++)
				counts[j][i] = 0;
		}
	}
	else  
	{
		// cout << "Construction Error " << endl;
		exit(-1);
	}
}

CMSketch::CMSketch(const CMSketch& rhs)
{
	type = -1;

	depth = rhs.depth;
	width = rhs.width;
	count = 0;
	counts = new int*[depth];
	counts[0] = new int[depth*width];
	hasha = new unsigned int[depth];
	hashb = new unsigned int[depth];
	if (counts && counts[0] && hasha && hashb)
	{
		for (int j = 0; j < depth; j++)
		{
			// pick the hash functions
			hasha[j] = rhs.hasha[j];
			hashb[j] = rhs.hashb[j];

			counts[j]=(int *) counts[0]+(j*width);

			for(int i = 0; i < width; i++)
				counts[j][i] = 0;
		}
	}
	else  
	{
		// cout << "Copy Construction Error " << endl;
		exit(-1);
	}
}

CMSketch::CMSketch(const CMSketch& rhs, int new_width, int new_depth)
{
	type = -1;

	depth = new_depth;
	width = new_width;
	count = 0;
	counts = new int*[depth];
	counts[0] = new int[depth*width];
	hasha = new unsigned int[depth];
	hashb = new unsigned int[depth];
	if (counts && counts[0] && hasha && hashb)
	{
		for (int j = 0; j < depth; j++)
		{
			// pick the hash functions
			hasha[j] = rhs.hasha[j];
			hashb[j] = rhs.hashb[j];

			counts[j]=(int *) counts[0]+(j*width);

			for(int i = 0; i < width; i++)
				counts[j][i] = 0;
		}
	}
	else  
	{
		// cout << "Copy Construction Error " << endl;
		exit(-1);
	}

}

// return the size of the sketch in bytes

int CMSketch::Size()
{ 
	int counts, hashes, admin;
	admin=sizeof(CMSketch);
	counts=width*depth*sizeof(int);
	hashes=depth*2*sizeof(unsigned int);
	return(admin + hashes + counts);
}

int CMSketch::Depth() const
{
	return depth;
}

int CMSketch::Width() const
{
	return width; 
}


// this can be done more efficiently if the width is a power of two

void CMSketch::Update(unsigned int item, int diff)
{
	int j;

	count+=diff;
	for (j=0;j<depth;j++)
		counts[j][hash31(hasha[j],hashb[j],item) % width]+=diff;
}

// return an estimate of the count of an item by taking the minimum
// this can be done more efficiently if the width is a power of two

int CMSketch::PointEst(unsigned int query)
{
	int j, ans;

	ans=counts[0][hash31(hasha[0],hashb[0],query) % width];
	for (j=1;j<depth;j++)
		ans=min(ans,counts[j][hash31(hasha[j],hashb[j],query)%width]);
	return (ans);
}

// return an estimate of the count by taking the median estimate
// useful when counts can become negative
// depth needs to be larger for this to work well

int CMSketch::PointMed(unsigned int query)
{
	int j, *ans, result=0;

	ans = new int[1+depth];

	for (j=0;j<depth;j++)
		ans[j+1]=counts[j][hash31(hasha[j],hashb[j],query)%width];

	if (depth==1)
		result=ans[1];
	else
		if (depth==2)
		{
			//result=(ans[1]+ans[2])/2;
			if (abs(ans[1]) < abs(ans[2]))
				result=ans[1]; 
			else 
				result=ans[2];
			// special tweak for small depth sketches
		}
		else
			result=(medselect(1+depth/2,depth,ans));
	if (ans)
	{
		delete []ans;
		ans = NULL;
	}

	return result;
	// need to adjust for routine starting at 1
}

// test whether two sketches are comparable (have same parameters)

bool CMSketch::operator==(const CMSketch& rhs) const 
{
	int i;
	if (width!=rhs.width) 
		return false;
	if (depth!=rhs.depth) 
		return false;
	for (i=0;i<depth;i++)
	{
		if (hasha[i]!=rhs.hasha[i]) 
			return false;
		if (hashb[i]!=rhs.hashb[i]) 
			return false;
	}
	return true;
}

// Estimate the inner product of two vectors by comparing their sketches

int CMSketch::InnerProd(const CMSketch& rhs)
{ 
	int i,j, tmp, result;

	result=0;
	if (*this == rhs)
	{
		for (i=0;i<width;i++)
			result+=counts[0][i]*rhs.counts[0][i];
		for (j=1;j<depth;j++)
		{
			tmp=0;
			for (i=0;i<width;i++)
				tmp+=counts[j][i]*rhs.counts[j][i];
			result=min(tmp,result);
		}

	}

	return result;
}

// CM_Residue computes the sum of everything left after the points 
// from Q have been removed
// Q is a list of points, where Q[0] gives the length of the list

int CMSketch::Residue(unsigned int* Q)
{
	char* bitmap;
	int i,j;
	int estimate=0, nextest;

	bitmap = new char[width];

	for (j=0;j<depth;j++)
	{
		nextest=0;
		for (i=0;i<width;i++)
			bitmap[i]=0;
		for (i=1;i<(int)(Q[0]);i++)
			bitmap[hash31(hasha[j],hashb[j],Q[i]) % width]=1;
		for (i=0;i<width;i++)
			if (bitmap[i]==0) 
				nextest+=counts[j][i];
		estimate=max(estimate,nextest);
	}

	if (bitmap)
	{
		delete []bitmap;
		bitmap = NULL;
	}

	return(estimate);
}

