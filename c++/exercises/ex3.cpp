#include <iostream>

using namespace std;

void hello_world()
{
  cout << "Hello World!\n";
}

void goodbye_world()
{
  cout << "Goodbye cruel World!\n";
}

int main()
{
  int select;
  cout << "Please enter\n\t1: for hello\n\t2: for goodbye\n> ";
  cin >> select;
  if (select == 1){
    hello_world();
  } else if (select == 2){
    goodbye_world();
  } else {
    cout << "undefined!!!!\n";
  }
  return 0;
}
