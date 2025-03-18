import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import config
import networkx as nx

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0] * vertices for _ in range(vertices)]

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def bfs(self, s, t, parent):
        # Mark all the vertices as not visited
        visited = [False] * self.V

        # Create a queue for BFS
        queue = []

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS Loop
        while queue:

            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True

        # We didn't reach sink in BFS starting
        # from source, so return false
        return False

    # Returns the maximum flow from s to t in the given graph
    def ford_fulkerson(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1]*(self.V)

        max_flow = 0 # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.bfs(source, sink, parent) :

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min (path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

    def plotGraph(self):
        G = nx.DiGraph()

        # Build the directed graph
        print("Edges being added:")
        for u in range(self.V):
            for v in range(self.V):
                if self.graph[u][v] > 0:
                    print(f"Edge from {u} to {v} with weight {self.graph[u][v]}")
                    G.add_edge(u, v, weight=self.graph[u][v])

        # Position nodes (equally spaced on a circle for clarity)
        pos = nx.circular_layout(G)

        plt.figure(figsize=(8, 6))

        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos,
            node_color='lightblue',
            node_size=1500
        )

        # Draw edges with arrowheads
        nx.draw_networkx_edges(
            G, pos,
            arrows=True,                # Enable arrowheads
            arrowstyle='->',            # Arrow style
            arrowsize=20,              # Arrow size
            edge_color='gray',          # Edge color
            node_size=1500,            # Must match the node_size above
            min_source_margin=15,       # Offset to start arrow away from node center
            min_target_margin=15        # Offset to end arrow before the node center
        )

        # Draw node labels (node IDs)
        nx.draw_networkx_labels(
            G, pos,
            font_color='black'
        )

        # Draw edge labels (the capacities/distances)
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Graph Visualization with Directed Arrows")
        plt.axis('off')  # Hide the axis for a cleaner look
        plt.show()


def generate_random_graph(size, max_capacity=20):
    graph = Graph(size)
    for i in tqdm(range(size), desc=f"Creating a graph for size {size}", unit="node"):
        for j in range(size):
            if i != j and np.random.rand() < 0.3:  # %30 ihtimalle bağlantı ekle
                graph.add_edge(i, j, np.random.randint(1, max_capacity))
    return graph


def experiment():
    lst = [x * config.MULTIPLIE_GRAPH_SIZE for x in config.GRAPH_SIZES]
    times = []

    for size in lst:
        graph = generate_random_graph(size)
        for row in graph.graph:
            print(row)
        source, sink = 0, size - 1
        start_time = time.time()
        max_flow = graph.ford_fulkerson(source, sink)
        end_time = time.time()
        print(f"For size: {size}")
        print(f"max_flow: {max_flow}")
        graph.plotGraph()
        times.append(end_time - start_time)

    plt.figure(figsize=(8, 5))
    plt.plot( [x * config.MULTIPLIE_GRAPH_SIZE for x in config.GRAPH_SIZES], times, marker='o', linestyle='-', color='b')
    plt.xlabel('Graph Size (Number of Nodes)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Ford-Fulkerson Execution Time Analysis')
    plt.grid(True)
    plt.show()

experiment()
