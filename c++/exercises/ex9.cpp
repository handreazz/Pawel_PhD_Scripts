#include <iostream>
#include <vector>

#define PI 3.1415926535897932384626433832795028841971693993751058209

using namespace std;

class Shape
{
public:
  virtual double area() = 0;
};

class Circle : public Shape
{
  double _radius;

public:
  Circle(double radius): _radius(radius)
  {}

  virtual double area()
  {
    return PI*_radius*_radius;
  }
};

class Square : public Shape
{
  double _side;

public:
  Square(double side): _side(side)
  {}

  virtual double area()
  {
    return _side*_side;
  }
};

class Trapezoid : public Shape
{
  double _height, _base, _top;

public:
  Trapezoid(double height, double base, double top):
    _height(height), _base(base), _top(top)
  {}

  virtual double area()
  {
    return 0.5*_height*(_base + _top);
  }
};

int main(int argc, char** argv){
  Circle c(0.5);
  Square s(1.0);
  Trapezoid t(0.5, 1.0, 2.0);
  vector<Shape*> vs(3);
  vs[0] = &c;
  vs[1] = &s;
  vs[2] = &t;
  double total_area = 0;
  for(int i; i<vs.size(); ++i){
    total_area += vs[i]->area();
  }
  cout << "Total area: " << total_area << endl;
}
