#include <iostream>
float somefunc(float fvar)
{
fvar=99.9;
return fvar;
}

int main()
{
  float fl=3.14;
  fl=somefunc(fl);
  std::cout << fl << std::endl;
  return 0;
}


