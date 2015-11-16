#include <iostream>
void somefunc(float* fptr)
{
   *fptr=99.9;
}

int main()
{
  float fl=3.14;
  float* addr = &fl;
  somefunc(addr);
  std::cout << fl << std::endl;
  return 0;
}
