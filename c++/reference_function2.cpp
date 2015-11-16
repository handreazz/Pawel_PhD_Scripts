#include <iostream>
#include <array>

/*
 * three ways to pass an array to a function without knowing beforehand
 * how big the array is 
 */


/*myfunc1 is most general because it doesn't depend on the container-type
 *  at all. Pointers are "scary" when used to manage memory, but they are
 *  OK to use as dummy arguments to simple functions that don't perform 
 * any memory management. 
 */
int & myfunc1( int * a ) { return a[4]; }

/*myfunc2 will also work for any container type (even raw pointers) in 
 * so far as the body of the function doesn't use the variable in a 
 * container-specific-way. 
 */
template<class T>
int & myfunc2( T & a ) { return a[4]; }

/* myfunc3 will ONLY work for std::array of int's. Usually not a good idea 
 * to write it in this way because now the only way to use myfunc3 is if
 *  you first get your data into a std::array. If your data is in a std::vector
 *  then you are SOL. 
*/
template <int N>
int & myfunc3( std::array<int,N> & a ) { return a[4]; }




int main() { 
	std::array<int,5> myarray={{6, 7, 8, 9, 10}};
	
	std::cout << myfunc1( myarray.data() ) <<std::endl;

	std::cout << myfunc2( myarray ) <<std::endl;

	std::cout << myfunc3( myarray ) <<std::endl;

	return 0;
}
