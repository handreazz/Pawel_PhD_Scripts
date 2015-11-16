/* Printing set members to a string
*
*
*/

#include <iostream>
#include <sstream>
#include <set>
#include <string>



template <class S,class C>
void printSet( S out, C a )
{
   for ( typename C::const_iterator p=a.begin(), pend=a.end(); p!=pend; ++p )
     out << *p << " ";
}

//~ template <class C>
//~ std::string sprintSet( C a )
//~ {
   //~ std::stringstream cout;
   //~ PrintSet( cout, a );
   //~ return cout.str();
//~ }



template <class C>
std::string sprintSet( C a )
{
   std::stringstream mystream;
   for ( typename C::const_iterator p=a.begin(), pend=a.end(); p!=pend; ++p )
     mystream << *p << " ";
   return mystream.str();
}

int main() {
	std::set<int> mySet = {1,4,7,6};
	std::string mystream=sprintSet(mySet);
	std::cout <<mystream <<std::endl;
	
	printSet( std::cout, mySet );
	//~ std::string mystring = strout.str();
	//~ char const * c_str = mystring.c_str();

	//double d;
	//strout >> d;
	return 0;
}

 
