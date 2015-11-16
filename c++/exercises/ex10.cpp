#include <iostream>
#include <vector>
#include <time.h>

using namespace std;

class MatrixBase
{
public:
  MatrixBase(int m, int n):
    _m(m), _n(n), vals(m*n)
  {}

  virtual ~MatrixBase(){}

  virtual double& operator()(int i, int j) = 0;

  virtual void fill() = 0;

  virtual void matvec(vector<double>& x,
                      vector<double>& b) = 0;

  vector<double> operator*(vector<double>& x)
  {
    vector<double> b(x.size());
    matvec(x, b);
    return b;
  }


  double m(){return _m;}
  double n(){return _n;}

protected:
  int _m, _n;
  std::vector<double> vals;
};

class MatrixRowMajor : public MatrixBase
{
public:
  MatrixRowMajor(int m, int n):
    MatrixBase(m, n)
  {}

  virtual double& operator()(int i, int j)
  {
    return vals[i*_n + j]; // row major
  }

  virtual void fill(){
    int cnt=0;
    for (int i=0; i<_m; ++i)
      for (int j=0; j<_n; ++j)
        vals[i*_n + j] = cnt++;
  }

  virtual void matvec(vector<double>& x, vector<double>& y)
  {
    for(int i=0; i < _m; ++i){
      for(int j=0; j < _n; ++j){
        y[i] += vals[i*_n + j] * x[j];
      }
    }
  }
};

class MatrixColMajor : public MatrixBase
{
public:
  MatrixColMajor(int m, int n):
    MatrixBase(m, n)
  {}

  virtual double& operator()(int i, int j)
  {
    return vals[i + _m*j]; // col major
  }

  virtual void fill(){
    int cnt=0;
    for (int j=0; j<_n; ++j)
      for (int i=0; i<_m; ++i)
        vals[i + _m*j] = cnt++;
  }

  virtual void matvec(vector<double>& x, vector<double>& y)
  {
    for(int j=0; j < _n; ++j){
      for(int i=0; i < _m; ++i){
        y[i] += vals[i + _m*j] * x[j];
      }
    }
  }

};

void fill(MatrixBase* m)
{
  int cnt=0;
  for (int i=0; i<m->m(); ++i)
    for (int j=0; j<m->n(); ++j)
      (*m)(i,j) = cnt++;
}

void matvec(MatrixBase& A, vector<double>& x, vector<double>& y){
  for(int i=0; i < A.m(); ++i){
    for(int j=0; j < A.n(); ++j){
      y[i] += A(i, j) * x[j];
    }
  }
}

double diffclock(clock_t clock1,clock_t clock2)
{
  double diffticks=clock1-clock2;
  double diffms=(diffticks*10)/CLOCKS_PER_SEC;
  return diffms;
}

double avg(vector<double> v)
{
  double sum = 0;
  for(int i=0; i<v.size(); ++i){
    sum += v[i];
  }
  return sum / v.size();
}

void fill_test()
{
  MatrixRowMajor R(10000, 10000);
  MatrixColMajor C(10000, 10000);

  clock_t begin, end;
  vector<double> times(5);

  for(int i=0; i<5; ++i){
    begin = clock();
    fill(&R);
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "fill(R) time: " << avg(times) << " ms\n";

  for(int i=0; i<5; ++i){
    begin = clock();
    fill(&C);
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "fill(C) time avg: " << avg(times) << " ms\n";

  for(int i=0; i<5; ++i){
    begin = clock();
    R.fill();
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "R.fill() time: " << avg(times) << " ms\n";

  for(int i=0; i<5; ++i){
    begin = clock();
    C.fill();
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "C.fill() time: " << avg(times) << " ms\n";
}

void matvec_test()
{
  MatrixRowMajor R(10000, 10000);
  MatrixColMajor C(10000, 10000);
  vector<double> x(10000), y(10000);

  R.fill();
  C.fill();
  for(int i; i<x.size(); ++i){
    x[i] = i;
  }


  clock_t begin, end;
  vector<double> times(5);

  for(int i=0; i<5; ++i){
    begin = clock();
    matvec(R, x, y);
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "matvec(R, x, y) time: " << avg(times) << " ms\n";

  for(int i=0; i<5; ++i){
    begin = clock();
    matvec(C, x, y);
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "matvec(C, x, y) time: " << avg(times) << " ms\n";

  for(int i=0; i<5; ++i){
    begin = clock();
    y = R*x;
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "y=R*x time: " << avg(times) << " ms\n";

  for(int i=0; i<5; ++i){
    begin = clock();
    y = C*x;
    end = clock();
    times[i] = diffclock(end, begin);
  }
  cout << "y=C*x time avg: " << avg(times) << " ms\n";
}

int main()
{
  fill_test();
  matvec_test();
  return 0;
}
