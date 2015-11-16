/* Different ways of 
 *  - creating sets, 
 *  - getting element number in list, 
 *  - printing set.
*/


#include <iostream>
#include <set>
#include <string>
#include <type_traits>   //c++11 thing


template <class C>
void printSet(C a )
{
  for ( typename C::const_iterator p=a.begin(), pend=a.end(); p!=pend; ++p )
    std::cout << *p << " ";
}



int main()
{
	// create set of ints
    int myints[]= {1,5,8};
    std::set<int> myIntSet(myints, myints+3);
    
    // or (only c++11)
    std::set<int> myIntSet2 = {1,5,7};
    
	// create set of strings (only c++11)
    std::set<std::string> myStrSet = {"apple", "orange", "peach"};
    
    // or
    std::string mystr[]= { "apple", "orange", "pear" };
    std::set<std::string> myStrSet2(mystr, mystr+3);
    
    // print number of elements in list
    std::cout << "List myints has this number of elements: ";
    std::cout << std::extent <decltype( myints )> ::value <<std::endl;
    
    // print set elements
    std::cout << "Elements in myIntSet: "; printSet(myIntSet); std::cout << std::endl;
    std::cout << "Elements in myIntSet2: "; printSet(myIntSet2); std::cout << std::endl;
    std::cout << "Elements in myStrSet: "; printSet(myStrSet); std::cout << std::endl;
    std::cout << "Elements in myStrSet2: "; printSet(myStrSet2); std::cout << std::endl;
    
    return 0;
}
//
 

