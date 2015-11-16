#include <iostream>
#include <vector>
#include <time.h>
#include <utility>

using namespace std;

typedef std::pair<int, int> Size;

class Matrix
{
  vector< vector<double> > _A;

 public:
  Matrix()
  {}

  Matrix(int m, int n)
  {
    resize(m, n);
  }

  double& operator()(int i, int j){
    return _A[i][j];
  }

  Size size()
  {
    return Size(_A.size(), _A[0].size());
  }

  void resize(int m, int n){
    _A.resize(m);
    for(int i=0; i<_A.size(); ++i){
      _A[i].resize(n);
    }
  }

  void fill()
  {
    for(int i=0; i<_A.size(); ++i){
      for(int j=0; j<_A[i].size(); ++j){
        _A[i][j] = i + j;
      }
    }
  }

  void mat_vec(vector<double>& x, vector<double>& y)
  {
    for(int i=0; i < _A.size(); ++i){
      for(int j=0; j < _A[0].size(); ++j){
        y[i] += _A[i][j] * x[j];
      }
    }
  }

  void mat_mat(Matrix& B, Matrix& C)
  {
    for(int i=0; i < _A.size(); ++i){
      for(int j=0; j < _A[0].size(); ++j){
        for(int k=0; k < B.size().second; ++k) {
          C(i, k) += _A[i][j] * B(j, k);
        }
      }
    }
  }
};

double diffclock(clock_t clock1,clock_t clock2)
{
  double diffticks=clock1-clock2;
  double diffms=(diffticks*10)/CLOCKS_PER_SEC;
  return diffms;
}

void class_test()
{
  Matrix A(100, 100), B(100, 100), C(100, 100);
  A.fill();
  B.fill();

  vector<double> x(100), y(100);
  for(int i=0; i<100; ++i){
    x[i] = i;
  }

  clock_t begin, end;
  begin=clock();
  A.mat_vec(x, y);
  end=clock();
  cout << "Time elapsed vector mat_vec: " << diffclock(end,begin) << " ms"<< endl;

  begin=clock();
  A.mat_mat(B, C);
  end=clock();
  cout << "Time elapsed vector mat_mat: " << diffclock(end,begin) << " ms"<< endl;
}

int main(int argc, char** argv){
  class_test();
  return 0;
}
