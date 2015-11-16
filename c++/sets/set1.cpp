/*Example of creating class and set of class instances and printing
 * elements of that set out.
 * 
 * 
 */


#include "set"
#include "iostream"
#include <algorithm>
#include <iterator>
using namespace std;



class Student
{
public:
	int num;
	string name;
};

//This is the compare function needed to place new class objects in a set
// (because set always sorts elements and does not allow duplicates.
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
	
	//first way of printing elements
	cout << "First way: \n";
	std::ostream_iterator< double > output(cout, " " );
    std::copy( myset.begin(), myset.end(), output );
	cout <<endl;
	
	//second way (notice you need to dereference the iterator)
	cout << "Second way: \n";
	set<int>::iterator i;
	for( i = myset.begin(); i != myset.end(); i++ )
	{
		cout << *i <<" ";
	}
	cout <<endl;
	//third way (like second, just different syntax)
	cout << "Third way: \n";
	for (set<int>::iterator i = myset.begin(); i != myset.end(); i++) 
	{
		cout <<*i <<" ";
	}
	cout <<endl;	


	//Create set container of Student class objects
	set< Student, Comp > myStudent;
	//Instantiate two Student objects
	Student a1;
	Student a2;
	a1.num = 10;
	a1.name = "Anwar";
	a2.num = 5;
	a2.name = "Ziale";
	cout << a1.num<< "\n";
	//Pass objects to set
	myStudent.insert(a1);
	myStudent.insert(a2);
	myStudent.insert(a1);
	//set::size
	cout << "The number of students " << myStudent.size() << endl;
	
	//~ // First way... doesn't work...
	//~ cout << "First way: \n";
	//~ std::ostream_iterator<double> output2(cout, " " );
    //~ std::copy( myStudent.begin(), myStudent.end(), output2 );
	//~ cout <<endl;
	
	// Second way
	set <Student, Comp>::iterator it;
	for( it = myStudent.begin(); it != myStudent.end(); it++ ) 
	{
		cout << it->num << "\t" << it->name << endl;
	};
	
	return 0;
}
