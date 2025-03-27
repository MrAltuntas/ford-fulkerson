import time
from collections import deque
import networkx as nx

class FordFulkerson:
    """Implementation of the Ford-Fulkerson algorithm for maximum flow."""

    def __init__(self, graph):
        """Initialize with a NetworkX directed graph."""
        self.graph = graph
        self.num_vertices = len(graph.nodes)

    def bfs(self, residual_graph, source, sink):
        """Find an augmenting path using breadth-first search."""
        # Initialize parent dictionary for path tracking
        parent = {source: None}
        queue = deque([source])

        # Standard BFS loop
        while queue:
            u = queue.popleft()

            # If we reached the sink, we found a path
            if u == sink:
                # Reconstruct the path
                path = []
                while u is not None:
                    path.append(u)
                    u = parent.get(u)
                return path[::-1]  # Reverse to start from source

            # Check all neighbors of u
            for v in residual_graph.neighbors(u):
                # If neighbor hasn't been visited and has capacity
                if v not in parent and residual_graph[u][v]['capacity'] > 0:
                    queue.append(v)
                    parent[v] = u

        # No path found
        return None

    def find_max_flow(self, source, sink):
        """Find the maximum flow from source to sink."""
        start_time = time.time()

        # Create a residual graph (deep copy)
        residual_graph = nx.DiGraph()

        # Add all nodes from original graph
        residual_graph.add_nodes_from(self.graph.nodes())

        # Add all edges from original graph with their capacities
        for u, v, data in self.graph.edges(data=True):
            residual_graph.add_edge(u, v, capacity=data['capacity'])
            # Add reverse edge with 0 capacity (for residual flow)
            if not residual_graph.has_edge(v, u):
                residual_graph.add_edge(v, u, capacity=0)

        # Initialize max flow
        max_flow = 0

        # Augment the flow while there is a path from source to sink
        path = self.bfs(residual_graph, source, sink)
        while path:
            # Find the minimum capacity in the path
            path_flow = float("Inf")

            # Find minimum capacity in the path
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                path_flow = min(path_flow, residual_graph[u][v]['capacity'])

            # Add path flow to overall flow
            max_flow += path_flow

            # Update residual capacities
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                # Decrease capacity in forward direction
                residual_graph[u][v]['capacity'] -= path_flow
                # Increase capacity in reverse direction
                residual_graph[v][u]['capacity'] += path_flow

            # Find next path
            path = self.bfs(residual_graph, source, sink)

        execution_time = time.time() - start_time

        return max_flow, execution_time