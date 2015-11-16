#include <string>
#include <iostream>
#include <cstdio>

int main()
{
  std::string Number ("102");
  for ( std::string::iterator it=Number.begin(); it != Number.end(); ++it ) 
    {
      printf("%c\n", *it );
      //
      // This next line won't compile because
      // *it returns a char, 
      // but string can't be constructed with a char      
      //
      //std::string temp( *it ); 

      //
      // One can construct a string given 2 iterators, however
      //
      std::string temp( it, it+1 );
      printf("temp.c_str() = %s\n", temp.c_str() );

      // One can construct a string with a char*, where it is
      // assumed the string continues until the \0 null character
      // is reached (which is *Number.end()), but this is not what
      // you want
      // std::string temp( &(*it) ); // get the pointer of the character currently being iterated

      //
      // and this is the normal way
      //
      std::cout << "*it = " << *it << "\n";

      //
      // here's the c-way
      // create a char * of length 2; last element is null-character
      //
      char ctemp[2] = { *it, '\0' };
      printf("ctemp = %s\n",ctemp);
    };
  return 0;
}
