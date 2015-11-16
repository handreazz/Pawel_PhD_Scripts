#include <iostream>
#include <iomanip>
#include <stdlib.h>

using namespace std;

int main(){
  cout << setprecision(8);
  for(int i=0; i<5; i++) {
    double rv = static_cast<double>(random()) / static_cast<double>(RAND_MAX);
    cout << rv << "     ";
  }
  cout << endl;
  return 0;
}
