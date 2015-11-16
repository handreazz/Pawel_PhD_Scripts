#include <string>
#include <iostream>
#include <boost/python.hpp>
#include <vector>

#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
//~ #include <boost/python/module.hpp>
//~ #include <boost/python/def.hpp>
//~ #include <boost/python/implicit.hpp>


using namespace boost::python;

//receive python list, reverse it using boost::python objects and pass list back to python 
list reverse_list (list mylist)
{
	mylist.reverse();
	return mylist;
} 

// print first element of std::vector
void firstelement (std::vector<double> vec)
{
	std::cout << vec[0] << '\n';
}

struct X // a container element
{
    std::string s;
    X():s("default") {}
    X(std::string s):s(s) {}
    std::string repr() const { return s; }
    void reset() { s = "reset"; }
    void foo() { s = "foo"; }
    bool operator==(X const& x) const { return s == x.s; }
    bool operator!=(X const& x) const { return s != x.s; }
};

// a function for X
std::string x_value(X const& x)
{
    return "gotya " + x.s;
}

//a function that takes a pointer
void doSomething( int const n, double * a )
{
   for ( std::size_t i=0; i<n; ++i )
     a[i] += 1.;
}  

//a function that passes the vector pointer to another function and returns a new vector
std::vector<double> pointer (std::vector<double> vec)
{
	doSomething(vec.size(),vec.data());
	return vec;
}


 
#include <boost/python.hpp>
BOOST_PYTHON_MODULE(vector)
{
	using namespace boost::python;
	def("reverse_list",reverse_list);
    def("firstelement", &firstelement);
    def("x_value", x_value);
    def("doSomething", doSomething);
    def("pointer", &pointer);
    
    class_<X>("X")
        .def(init<>())
        .def(init<X>())
        .def(init<std::string>())
        .def("__repr__", &X::repr)
        .def("reset", &X::reset)
        .def("foo", &X::foo);

    implicitly_convertible<std::string, X>();
    
    class_<std::vector<X> >("XVec")
        .def(vector_indexing_suite<std::vector<X> >());
        
    class_<std::vector<double> >("VectorOfDouble")
        .def(vector_indexing_suite<std::vector<double> >());

}

