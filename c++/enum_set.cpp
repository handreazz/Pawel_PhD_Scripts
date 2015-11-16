#include <iostream>
#include <string>
#include <unordered_set>

enum wind_directions_t {NO_WIND=1, NORTH_WIND, SOUTH_WIND, EAST_WIND, WEST_WIND};

int main() {
	
	std::cout << "Please enter NORTH, SOUTH, EAST, WEST, or NONE for our wind direction" <<std::endl;
	

	std::string user_wind_dir;
	std::cin >> user_wind_dir;

	wind_directions_t wind_dir;

	if ( user_wind_dir == "NORTH" )
	{
			wind_dir = NORTH_WIND;
	}
	else if ( user_wind_dir == "SOUTH" )
	{
			wind_dir = SOUTH_WIND;
	}
	else if ( user_wind_dir == "EAST" )
	{
			wind_dir = EAST_WIND;
	}
	else if ( user_wind_dir == "WEST" )
	{
			wind_dir = WEST_WIND;
	}
	else if ( user_wind_dir == "NONE" )
	{
			wind_dir = NO_WIND;
	}
	else
	{
			std::cout << "That's not a valid direction!" << std::endl;
	}
	std::unordered_set<int> wind_values ( {1,2,3,4,5} ); 
	if (wind_values.count(wind_dir)>0)
			std::cout << "wind_dir variable value is: " << wind_dir << std::endl;
	else
			std::cout << "wind_dir variable is undefined." << std::endl;
	return 0;
}
