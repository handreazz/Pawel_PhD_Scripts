#include <fstream>
#include <string>
#include <cerrno>
#include <iostream>
#include <boost/algorithm/string.hpp>
#include <vector>
#include <algorithm>
#include <iterator>


/* Read entire file into std::string. 
 * Than split by line into vector. 
 * Remove blank lines.
 */


std::string get_file_contents(const char *filename)
//~ std::string get_file_contents(std::string filename)
{
  std::ifstream in(filename, std::ios::in | std::ios::binary);
  if (in)
  {
    std::string contents;
    in.seekg(0, std::ios::end);
    contents.resize(in.tellg());
    in.seekg(0, std::ios::beg);
    in.read(&contents[0], contents.size());
    in.close();
    return(contents);
  }
  throw(errno);
}

int main()
{
	//~ std::string filename = "tmp_file.txt";
  
  // read file into a std::string
  char filename[]="tmp_file.txt";
  std::string file_contents = get_file_contents(filename);
	std::cout << file_contents;
  printf("\n");
  
  // split by new line into vector of lines. 
  // remove empty lines.
  std::vector<std::string> lines;
  boost::split(lines, file_contents, boost::is_any_of("\n"));
  lines.erase( std::remove(lines.begin(), lines.end(), ""), lines.end() );
 
  //print 
 	std::cout << "[\n";
	for (unsigned int i=0; i < lines.size(); ++i) {
    printf("%d %s\n", i, lines[i].c_str());
    //~ std::cout << i << lines[i] << "\n";  
  }
	std::cout << "]\n";

  
  
  
	return 0;
}
