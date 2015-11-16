/*Example of creating class and set of class instances and printing
 * elements of that set out.
 * 
 * Has a simplified template that works. To compare to Tim's sophisticated version.
 * 
 */


#include "set"
#include "iostream"
#include <algorithm>
#include <iterator>
using namespace std;


// Tim's template
//~ template <class C>
//~ void printSet( std::ostream & os, C const & a )
//~ {
  //~ for ( typename C::const_iterator p=a.begin(), pend=a.end(); p!=pend; ++p )
    //~ os << *p << " ";
//~ }

// My template
template <class C>
void printSet(C a )
{
  for ( typename C::const_iterator p=a.begin(), pend=a.end(); p!=pend; ++p )
    cout << *p << " ";
}



class Student
{
public:
	int num;
	string name;
};

class Comp
{
public:
	bool operator()(Student s1, Student s2)
	{
		return (s1.num) < (s2.num);
	}
};


int main(int argc, char* argv[])
{ 
	//create set of intergers
	set<int> myset;
	myset.insert(5);
	myset.insert(6);
	
	
	// Fourth way
	cout << "Fourth way: \n";
	//printSet( cout, myset );
	printSet( myset );
	cout << "\n";

	return 0;
}
