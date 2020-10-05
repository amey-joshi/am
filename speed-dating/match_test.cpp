#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "Matches.hpp"

int main(int argc, char* argv[], char* [])
{
	bool find(int m, int n, const std::vector<Match> &matched);

	if (argc < 2) {
		std::cerr << "Name of the matching file is missing." << std::endl;
		return -1;
	}

	std::string filename = argv[1];
	std::fstream f(filename);
	std::string line;
	std::vector<Match> matches;

	while (getline(f, line)) {
		std::stringstream ss(line);
		std::string s;
		getline(ss, s, ',');
		int ms = std::stoi(s);
		getline(ss, s, ',');
		int ns = std::stoi(s);
		matches.push_back(Match(ms, ns));
	}

	std::cout << "Read " << matches.size() << " matches." << std::endl;

	std::cout << "Search {1, 24} " << find(1, 24, matches) << std::endl;
	std::cout << "Search {24, 1} " << find(24, 1, matches) << std::endl;
	std::cout << "Search {8, 1} " << find(8, 1, matches) << std::endl;
	return 0;
}
	
bool find(int m, int n, const std::vector<Match> &matched)
{
	bool found = false;

	for (int i = 0; i < matched.size(); ++i) {
		if (matched[i].same(m, n)) {
			found = true;
			break;
		}
	}

	return found;
}

