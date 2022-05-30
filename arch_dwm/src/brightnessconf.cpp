#include <iostream>
#include <sstream>
#include <fstream>
#include <string>

using namespace std;

const string base = "/sys/class/backlight/amdgpu_bl0";
const double default_br = 80; // %

int main(int argc, char **argv){
	int cur_br, new_br, max_br, add;
	stringstream ss;
	fstream file;
	
	file.open(base + "/max_brightness", ios::in);
	file >> max_br;
	file.close();
	
	file.open(base + "/brightness", ios::in);
	file >> cur_br;
	file.close();
	
	if(argc < 2) new_br = max_br / 100. * default_br;
	else{
		ss << argv[1];
		ss >> add;
		new_br = cur_br + max_br / 100. * (double)add;
	}
	
	if(new_br > max_br) new_br = max_br;
	else if(new_br < 0) new_br = 0;
	
	file.open(base + "/brightness", ios::out | ios::trunc);
	file.seekp(ios::beg);
	file << new_br;
	file.close();
	
	return 0;
}
