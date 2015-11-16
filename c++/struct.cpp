#include <iostream>

struct Cx 
{
	int i;
	int *jj;
	float *kk;
	float* dd;
};



void f(Cx someCx) 
{
	someCx.i=5;
	*someCx.jj=6;
	someCx.dd[1]=10.6;
}

int main()
{
  Cx myCx;
  myCx.i=4;
  int j=2;
  myCx.jj = &j;
  float k=5.2;
  myCx.kk = &k;
  
  myCx.dd = (float*)malloc(3*sizeof(float));
  myCx.dd= {0.1,9.4,8.3};
  
  f(myCx);
  std::cout << myCx.i << std::endl;
  std::cout << "MyCx.jj: " << myCx.jj << "  j: " << j << std::endl;  
  std::cout << k << std::endl;
  return 0;
}
