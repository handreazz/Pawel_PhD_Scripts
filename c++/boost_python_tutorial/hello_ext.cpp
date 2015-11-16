#include <string>
#include <iostream>
#include <boost/python.hpp>
using namespace boost::python;
//std::string greet()
const char* greet()
{
	   return "hello, world";
}

int addition (int a, int b)
{
	int r;
	r=a+b;
	return r;
}

object print_str2 (boost::python::str name)
{
	std::string tmp = boost::python::extract<std::string>(name);
	std::cout << tmp << std::endl;

	boost::python::str NAME = name.upper();
	object msg = "%s is bigger than %s" % make_tuple(NAME,name);
	str x=str(msg);
	//str x=str(1);
	return msg;
}
 
int print_str1 (std::string mystring)
{
	std::cout << mystring <<"\n";
	return 0;
} 
 
 
#include <boost/python.hpp>
BOOST_PYTHON_MODULE(hello_ext)
{
	    using namespace boost::python;
	        def("greet", greet);
	        def("add", addition);
			def("print_str1", &print_str1);
			def("print_str2", print_str2);
}
