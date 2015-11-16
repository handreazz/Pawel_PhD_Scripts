#include <iostream>
#include <vector>

using namespace std;

void fill(vector<double>& v)
{
  v.resize(10);
  for(int i=0; i<10; i++){
    v[i] = i;
  }
}

int main(int argc, char** argv){
  vector<double> v;
  fill(v);

  for(int i=0; i<v.size(); ++i){
    cout << "arg " << i << ": " << v[i] << endl;
  }
  return 0;
}
