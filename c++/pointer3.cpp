#include <iostream>

using namespace std;

// FUNCTION PROTOTYPES

// passing to a function by value
int add( int a, int b);
// passing to a function by reference using pointers
void addone( int * a, int * b);
// passing to a function by reference using reference
void swap( int &a, int &b);

int main()

{
// define integers a and b
int a = 1;
int b = 4;

// add() function call return value will be printed out
  cout << "add() function\n";
  cout << add(a,b) << endl;
  cout << "a = " << a << "\tb = " << b << endl;
// addone() function call
  cout << "addone() function\n";
  addone(&a,&b);
// after addone() function call value a=2 and b=5 
  cout << "a = " << a << "\tb = " << b << endl;
// swap() function call
  cout << "swap() function\n";
  swap(a,b);
// after swap() function call value a=5 and b=2
  cout << "a = " << a << "\tb = " << b << endl;

return 0;
}
// add() fuction header
int add( int a, int b) 
{
// add() function definition
// this function returns sum of two integers
  return a + b;
}

// addone() fuction header
void addone( int * c, int * d)
{
// addone() function definition
// this function adds 1 to each value
  ++*c;
  ++*d;
  cout << d <<endl;
}

// swap() function header
void swap( int &a, int &b)
{
// swap() function definition
// this function swaps values
int tmp;

  //~ tmp = a;
  //~ a = b;
  b++;
  
}
