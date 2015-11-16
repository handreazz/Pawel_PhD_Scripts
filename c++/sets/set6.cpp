#include <iostream>
#include <vector>
#include <set>
#include <string>

template <class T>
void printSet( T set )
{
   for ( typename T::const_iterator p=set.begin(), pend=set.end(); p!=pend; ++p )
     std::cout << *p << " ";
}


int main() {
	
	std::vector<int> myVec={1,2,4};
	std::cout << myVec.size() <<std::endl;	
	std::set<int> mySet(myVec.begin(), myVec.end());
	printSet(mySet);
	
	std::vector<std::string> myVec2={"hello","bye","again"};
	
	return 0;
}
