#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main(int argc, char* argv[], char* envp[])
{
	if (argc < 2) {
		std::cerr << "Name of the CSV file is missing." << std::endl;
		return -1;
	}

	std::string filename = argv[1];
	std::fstream f(filename);
	std::string line;

	while (getline(f, line)) {
		std::string token;
		std::stringstream ss(line);
		std::vector<std::string> tokens;

		while(getline(ss, token, ',')) {
			tokens.push_back(token);
		}
		for (std::vector<std::string>::const_iterator ci = tokens.begin();
		     ci != tokens.end();
			 ++ci) {
			std::cout << *ci << ", ";
		}
		std::cout << std::endl;
	}

	f.close();
	return 0;
}

