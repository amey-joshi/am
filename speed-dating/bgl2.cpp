#include <iostream>
#include <utility>
#include <algorithm>
#include <vector>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>

using namespace boost;
typedef adjacency_list<vecS, vecS, bidirectionalS> Graph;

struct Participant {
	int id;
	int self;
	int seek1;
	int seek2;
	int seek3;

	Participant() {id = self = seek1 = seek2 = seek3 = 0;}
	Participant(int i, int sl, int sk1, int sk2, int sk3) : id(i), 
		self(sl), seek1(sk1), seek2(sk2), seek3(sk3) {}
};

typedef std::pair<int, int> Edge;

int main(int, char* [], char* [])
{
	Graph build_graph();
	Graph g = build_graph();

	return 0;
}

Graph build_graph()
{
	std::vector<Participant> get_vertices();
	std::vector<Participant> vertices = get_vertices();
	void show_edges(const Graph& g);

	std::vector<Edge> get_edges(const std::vector<Participant>& vertices);
	std::vector<Edge> edges = get_edges(vertices);

	std::cout << "Got " << vertices.size() << " vertices" << std::endl;
	std::cout << "Got " << edges.size() << " edges" << std::endl;

	Graph g(vertices.size());
	for (int i = 0; i < edges.size(); ++i) {
		add_edge(edges[i].first, edges[i].second, g);
	}

	std::cout << "Created the graph." << std::endl;
	show_edges(g);

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

std::vector<Participant> get_vertices()
{
	std::vector<Participant> vertices;

	vertices.push_back(Participant(1, 1, 3, -1, -1));
	vertices.push_back(Participant(2, 2, 3, -1, -1));	
	vertices.push_back(Participant(3, 2, 1, -1, -1));	
	vertices.push_back(Participant(4, 3, 2, 3, 1));	
	vertices.push_back(Participant(5, 1, 2, -1, -1));	

	return vertices;
}

std::vector<Edge> get_edges(const std::vector<Participant>& vertices)
{
	std::vector<Edge> edges;

	edges.push_back(Edge(vertices[0].id, vertices[2].id));
	edges.push_back(Edge(vertices[1].id, vertices[3].id));
	edges.push_back(Edge(vertices[2].id, vertices[4].id));

	return edges;
}

