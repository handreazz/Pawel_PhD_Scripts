#include <iostream>
using namespace std;

void SomeFunc2();

int main()
{
  unsigned short * p1;
  SomeFunc2();
  cout << *p1 << endl;
  return 0;
}

void SomeFunc2()
{
	unsigned short * p1;
	p1 = new unsigned short;     
	*p1=15;
	cout << p1 << endl;
	cout << *p1 << endl; 
	//delete p1; // p1 is leaked unless it gets deleted
}
