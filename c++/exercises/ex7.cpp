#include <iostream>
#include <vector>
#include <time.h>

using namespace std;

void resize_mat(vector< vector<double> >& A, int m, int n)
{
  A.resize(m);
  for(int i=0; i<A.size(); ++i){
    A[i].resize(n);
  }
}

void fill_mat(vector< vector<double> >& A)
{
  for(int i=0; i<A.size(); ++i){
    for(int j=0; j<A[i].size(); ++j){
      A[i][j] = i + j;
    }
  }
}

void mat_vec(vector< vector<double> >& A, vector<double>& x, vector<double>& y){
  for(int i=0; i < A.size(); ++i){
    for(int j=0; j < A[0].size(); ++j){
      y[i] += A[i][j] * x[j];
    }
  }
}

void mat_mat(vector< vector<double> >& A, vector< vector<double> >& B,
             vector< vector<double> >& C){
  for(int i=0; i < A.size(); ++i){
    for(int j=0; j < A[0].size(); ++j){
      for(int k=0; k < B[0].size(); ++k) {
        C[i][k] += A[i][j] * B[j][k];
      }
    }
  }
}


void mat_vec(double A[][100], double x[], double y[]){
  for(int i=0; i < 100; ++i){
    for(int j=0; j < 100; ++j){
      y[i] += A[i][j] * x[j];
    }
  }
}

void mat_mat(double A[][100], double B[][100], double C[][100]){
  for(int i=0; i < 100; ++i){
    for(int j=0; j < 100; ++j){
      for(int k=0; k < 100; ++k) {
        C[i][k] += A[i][j]*B[j][k];
      }
    }
  }
}

double diffclock(clock_t clock1,clock_t clock2)
{
  double diffticks=clock1-clock2;
  double diffms=(diffticks*10)/CLOCKS_PER_SEC;
  return diffms;
}

void vector_test()
{
  vector< vector<double> > A, B, C;
  resize_mat(A, 100, 100);
  resize_mat(B, 100, 100);
  resize_mat(C, 100, 100);
  fill_mat(A);
  fill_mat(B);

  vector<double> x(100), y(100);
  for(int i=0; i<100; ++i){
    x[i] = i;
  }

  clock_t begin, end;
  begin=clock();
  mat_vec(A, x, y);
  end=clock();
  cout << "Time elapsed vector mat_vec: " << diffclock(end, begin) << " ms"<< endl;

  begin=clock();
  mat_mat(A, B, C);
  end=clock();
  cout << "Time elapsed vector mat_mat: " << diffclock(end, begin) << " ms"<< endl;
}

void array_test()
{
  double A[100][100], B[100][100], C[100][100];
  double x[100], y[100];
  for(int i=0; i<100; ++i){
    for (int j=0; j<100; ++j){
      A[i][j] = B[i][j] = i + j;
      C[i][j] = 0;
    }
    x[i] = i;
    y[i] = 0;
  }

  clock_t begin, end;
  begin=clock();
  mat_vec(A, x, y);
  end=clock();
  cout << "Time elapsed array mat_vec: " << diffclock(end, begin) << " ms"<< endl;

  begin=clock();
  mat_mat(A, B, C);
  end=clock();
  cout << "Time elapsed array mat_mat: " << diffclock(end, begin) << " ms"<< endl;

}

int main(int argc, char** argv){
  vector_test();
  array_test();
  return 0;
}
