#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/max_cardinality_matching.hpp>
#include "Participant.hpp"
#include "Matches.hpp"

using namespace boost;
typedef adjacency_list<vecS, vecS, bidirectionalS> Graph;
typedef std::pair<int, int> Edge;

std::vector<Edge> get_edges(const std::vector<Participant>& ps,
						    std::vector<Match>& matches);
void show_edges(const Graph& g);
void previous_matches(const std::string &filename,
					  std::vector<Match> &matches);
bool find(int m, int n, const std::vector<Match> &matches);

const bool VERBOSE = true;

int main(int argc, char* argv[], char* envp[])
{
	if (argc < 3) {
		std::cerr << "Names of the CSV files are missing." << std::endl;
		std::cerr 
			<< "Run this program as: bgl <choice-file> <previous-matching>" 
			<< std::endl;
		return -1;
	}

	auto start = std::chrono::high_resolution_clock::now();
	std::vector<Match> matches;
	previous_matches(argv[2], matches);
	std::string filename = argv[1];
	std::fstream f(filename);
	std::string line;
	int fields[5]; // To store values of the fields of a Participant object.

	std::vector<Participant> ps;

	bool first_line = true;
	while (getline(f, line)) {
		if (first_line) {
			first_line = false;
			continue;
		}

		std::string token;
		std::stringstream ss(line);
		std::vector<std::string> tokens;

		while(getline(ss, token, ',')) {
			tokens.push_back(token);
		}
		int j = 0;
		for (std::vector<std::string>::const_iterator ci = tokens.begin();
		     ci != tokens.end();
			 ++ci) {
			fields[j++] = std::atoi(ci->c_str());
		}
		ps.push_back(Participant(fields[0], fields[1], fields[2],
                                 fields[3], fields[4]));
	}

	f.close();

	if (VERBOSE)
		std::cout << "Read " << ps.size() << " ps." << std::endl;

	Graph g(ps.size());
	std::vector<Edge> edges = get_edges(ps, matches);

	for (int i = 0; i < edges.size(); ++i) {
		add_edge(edges[i].first, edges[i].second, g);
	}

	if (VERBOSE) {
		std::cout << "Created the graph." << std::endl;
		show_edges(g);
	}

	std::vector<graph_traits<Graph>::vertex_descriptor> mate(ps.size());
	edmonds_maximum_cardinality_matching(g, &mate[0]);

	if (VERBOSE) {
		std::cout << "Found matching of size " << matching_size(g, &mate[0])
		  << std::endl;
		std::cout << "The matching is: " << std::endl;
	}

	graph_traits<Graph>::vertex_iterator vi, vi_end;
	for(tie(vi, vi_end) = vertices(g); vi != vi_end; ++vi) {
		if (mate[*vi] != graph_traits<Graph>::null_vertex() &&
			*vi < mate[*vi]) {
			std::cout << *vi << "," << mate[*vi] << std::endl;
		}
	}	
	std::cout << std::endl;

	auto end = std::chrono::high_resolution_clock::now();
	double diff = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() * 1e-9;

	std::cout << "Time taken: " << std::fixed << diff << std::setprecision(9) 
			  << " s for " << ps.size() << " participants." << std::endl;
	return 0;
}

void show_edges(const Graph& g)
{
	std::cout << "Edges: ";
	typedef property_map<Graph, vertex_index_t>::type IndexMap;
	IndexMap index = get(vertex_index, g);
	graph_traits<Graph>::edge_iterator ei, ei_end;

	for (boost::tie(ei, ei_end) = edges(g); ei != ei_end; ++ei) {
		std::cout << "(" << index[source(*ei, g)] 
				  << "," << index[target(*ei, g)] << ") ";
	}
	std::cout << std::endl;
}

std::vector<Edge> get_edges(const std::vector<Participant>& ps,
                            std::vector<Match>& matches) 
{
	std::vector<Edge> edges;

	int n_ps = ps.size();
	for (int i = 0; i < n_ps; ++i) {
		for (int j = i + 1; j < n_ps; ++j) {
			if (ps[i].can_pair(ps[j]) && ps[j].can_pair(ps[i])) {
				if (!find(ps[j].id, ps[i].id, matches))
					edges.push_back(Edge(ps[i].id, ps[j].id));
			}
		}
	}

	return edges;
}


void previous_matches(const std::string &filename,
					  std::vector<Match> &matches)
{
	std::fstream f(filename);
	std::string line;

	while (getline(f, line)) {
		std::stringstream ss(line);
		std::string s;
		getline(ss, s, ',');
		int ms = std::stoi(s);
		getline(ss, s, ',');
		int ns = std::stoi(s);

		matches.push_back(Match(ms, ns));
	}

	if (VERBOSE)
		std::cout << "Read " << matches.size() << " matches." << std::endl;
}


bool find(int m, int n, const std::vector<Match> &matches)
{
	bool found = false;

	for (int i = 0; i < matches.size(); ++i) {
		if (matches[i].same(m, n)) {
			found = true;
			break;
		}
	}

	return found;
}

