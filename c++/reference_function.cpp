#include <iostream>
#include <array>

int myfunc1 (std::array<int,5> a) {
	return a[3];
}

int & myfunc2 (std::array<int,5> & a) {
	return a[3];
}

int main() { 
	std::array<int,5> myarray={{6, 7, 8, 9, 10}};

	std::cout << "Change to variable does not affect array element:" << std::endl;
	int var1=myfunc1(myarray);
	var1++;
	std::cout << "Variable: " << var1 << std::endl;
	std::cout << "Array element: " << myarray[3] << "\n\n";

	std::cout << "But with reference operator, change to variable also changes array"<< std::endl;
	int & var2=myfunc2(myarray);
	var2++;	
	std::cout << "Variable: " << var2 << std::endl;
	std::cout << "Array element: " << myarray[3] <<"\n\n";
	
	std::cout << "But this doesn't change the array because var3 allocates a new memory \
address containing the value that myfunc2(myarray) references to"<< std::endl;
	int var3=myfunc2(myarray);
	var3++;	
	std::cout << "Variable: " << var3 << std::endl;
	std::cout << "Array element: " << myarray[3] <<std::endl;

	std::cout << "But here I don't increment var4, I actually increment the element in\
the array that myfunc2(myarray) is referencing to."<< std::endl;
	int var4=++myfunc2(myarray);
	std::cout << "Variable: " << var4 << std::endl;
	std::cout << "Array element: " << myarray[3] <<std::endl;
	

	return 0;
}
