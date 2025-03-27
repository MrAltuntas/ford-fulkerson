import random
import networkx as nx

class GraphGenerator:
    """Class for generating random flow networks using NetworkX."""

    def __init__(self, num_vertices, edge_probability, min_capacity, max_capacity):
        """Initialize the graph generator with configuration parameters."""
        self.num_vertices = num_vertices
        self.edge_probability = edge_probability
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity

    def generate_graph(self):
        """Generate a random flow network without double edges."""
        # Create a directed graph
        G = nx.DiGraph()

        # Add vertices
        G.add_nodes_from(range(self.num_vertices))

        # Source is the first vertex (0)
        source = 0
        # Sink is the last vertex (num_vertices - 1)
        sink = self.num_vertices - 1

        # Create a list of all possible edges that satisfy our constraints
        possible_edges = []

        for u in range(self.num_vertices):
            for v in range(self.num_vertices):
                # Skip self-loops
                if u == v:
                    continue

                # No incoming edges to source
                if v == source:
                    continue

                # No outgoing edges from sink
                if u == sink:
                    continue

                # Add this as a possible edge
                possible_edges.append((u, v))

        # Shuffle the possible edges to randomize selection
        random.shuffle(possible_edges)

        # Determine how many edges to add based on probability
        num_edges_to_add = int(len(possible_edges) * self.edge_probability)

        # Add edges with random capacities
        for u, v in possible_edges[:num_edges_to_add]:
            # Generate a random capacity
            capacity = random.randint(self.min_capacity, self.max_capacity)

            # Add the edge to the graph
            G.add_edge(u, v, capacity=capacity)

        return G