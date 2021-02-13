#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define SIZE 0.70710678
#define F_A(x) (2*sqrt((x)*(x)+1))
#define F_B(x) sqrt(1/2+1/F_A(x))
#define F_C(x) ((x)/sqrt(2+F_A(x)))
#define F_D(x) ((x)/2*F_A(x) + log(F_B(x)+F_C(x)) - log(F_B(x)-F_C(x)))
#define F_E(b, h) ((h)*(h)*(h)*(F_D(b) + F_D(SIZE-(b))))
#define   F(x, y) (0.5 + F_E(x,y) + F_E(x,SIZE-y) + F_E(y,x) + F_E(y,SIZE-x))/3

double test(double x, double y)
{
	double total = 0;
	size_t i = 0x10000;
	while (--i) {
		double x_0 = (float)rand()/RAND_MAX*SIZE;
		double y_0 = (float)rand()/RAND_MAX*SIZE;
		total += sqrt((x-x_0)*(x-x_0)+(y-y_0)*(y-y_0));
	}
	return total / 0x10000;
}

int main()
{
	srand((unsigned)time(NULL));

        double x, y, x_0, y_0, sum;

	for (unsigned i = 0; i < 70; i++) {
		printf("%.7f", test((float)i/100, (float)0));
		for (unsigned j = 0; j < 69; ++j)
			printf(",%.7f", test((float)i/100, (float)j/100));
		printf("\n");
	}
	for (unsigned i = 0; i < 70; i++) {
		printf("%.7f", F((float)i/100, (float)0));
		for (unsigned j = 0; j < 69; ++j)
			printf(",%.7f", F((float)i/100, (float)j/100));
		printf("\n");
	}
	return 0;
}
