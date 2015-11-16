#include <stdio.h>
#include <boost/python.hpp>
#include <vector>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

//a function that takes a pointer to an array
void doSomething( int const n, double * a )
{
   for ( std::size_t i=0; i<n; ++i )
     a[i] += 1.;
}  

void add1 (std::vector<double>& vec)
{
    doSomething(vec.size(),vec.data());
}

//boost::python registration 
#include <boost/python.hpp>
BOOST_PYTHON_MODULE(vector2)
{
	using namespace boost::python;
    def("doSomething", doSomething);
    def("add1", &add1);
        
    class_<std::vector<double> >("VectorOfDouble")
        .def(vector_indexing_suite<std::vector<double> >());
}

