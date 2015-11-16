#include <stdio.h>

struct bond {
	int a;
	int b;
	int c;
};
typedef struct bond bond;

void main() {
	bond BIncH[2];
	bond First = {.a=1, .b=2, .c=3};
	bond Sec = {.a=5, .b=6, .c=7};
	
	BIncH[0]=First;
	BIncH[1]=Sec;
	
	
	
	printf("%d\n", First.c);
	printf("%d\n", BIncH[0].c);
	
	printf("%d\n", sizeof(BIncH));
	printf("%d\n", sizeof(BIncH[0]));
	printf("%d\n", sizeof(BIncH[1]));
}


