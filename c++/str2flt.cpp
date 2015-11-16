#include <iostream>
#include <string>
#include <sstream>


std::string name;
int num;

int main() {
    name="Pawel5";
    std::istringstream(name.substr(5,1)) >>num;
    std::cout <<num <<'\n';
    std::cout <<name.substr(5,1)<< '\n';
    return(0);
} 
