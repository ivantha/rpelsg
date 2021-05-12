#pragma once

#define min(x,y)	((x) < (y) ? (x) : (y))
#define max(x,y)	((x) > (y) ? (x) : (y))

class CMSketch
{
private:
	int type;
	long long count;				// The total count of all entries
	int depth;						
	int width;
	int ** counts;					// The sketch matrix
	unsigned int *hasha, *hashb;	

	CMSketch(void);

public:
	CMSketch(int, int, int);
	CMSketch(const CMSketch&);
	CMSketch(const CMSketch&, int, int);
	~CMSketch(void);

	int Size();

	int Depth() const;
	int Width() const;

	inline int Type() const
	{
		return type;
	}

	inline void SetType(int newtype)
	{
		type = newtype;
	}

	void Update(unsigned int, int); 
	int PointEst(unsigned int);
	int PointMed(unsigned int);
	int InnerProd(const CMSketch&);
	int Residue(unsigned int*);

	bool operator==(const CMSketch& ) const;

};
