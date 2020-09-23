#include <iostream>
#include <utility>
#include <algorithm>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>

using namespace boost;
typedef adjacency_list<vecS, vecS, bidirectionalS> Graph;

int main(int, char* [], char* [])
{
	enum {A, B, C, D, E, N};
	const int n_vertices = N;

	void show_vertices(const Graph& g);
	void show_edges(const Graph& g);

	typedef std::pair<int, int> Edge;
	Edge edges[] = {Edge(A, B), Edge(A, D), Edge(C, A), Edge(D, C),
						 Edge(C, E), Edge(B, D), Edge(D, E)};
	const int n_edges = sizeof(edges)/sizeof(edges[0]);

	Graph g(n_vertices);
	for (int i = 0; i < n_edges; ++i) {
		add_edge(edges[i].first, edges[i].second, g);
	}

	std::cout << "Created the graph." << std::endl;
	show_vertices(g);
	show_edges(g);

	return 0;
}

void show_vertices(const Graph &g) 
{
	typedef graph_traits<Graph>::vertex_descriptor Vertex;
	typedef property_map<Graph, vertex_index_t>::type IndexMap;

	IndexMap index = get(vertex_index, g);
	std::cout << "Vertices: ";
	typedef graph_traits<Graph>::vertex_iterator vertex_iter;
	std::pair<vertex_iter, vertex_iter> vp;
	for (vp = vertices(g); vp.first != vp.second; ++vp.first) {
		Vertex v = *vp.first;
		std::cout << index[v] << " " ;
	}
	std::cout << std::endl;
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

