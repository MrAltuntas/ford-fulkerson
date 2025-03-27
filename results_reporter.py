import os
import csv
import matplotlib.pyplot as plt
import networkx as nx

class ResultsReporter:
    """Class for generating reports and visualizations from experiments."""

    def __init__(self, results_dir="results"):
        """Initialize the reporter with a results directory."""
        self.results_dir = results_dir

        # Create results directory if it doesn't exist
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def save_results_to_csv(self, results):
        """Save experimental results to CSV files."""
        # Save summary results
        with open(f'{self.results_dir}/summary.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Size', 'Avg Time (s)', 'Avg Flow'])
            for result in results:
                writer.writerow([result['size'], result['avg_time'], result['avg_flow']])

        # Save detailed results for each graph size
        for result in results:
            size = result['size']
            with open(f'{self.results_dir}/size_{size}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Trial', 'Time (s)', 'Flow'])
                for i, (t, flow) in enumerate(zip(result['times'], result['flows'])):
                    writer.writerow([i+1, t, flow])

    def create_time_complexity_figure(self, sizes, times):
        """Create a figure comparing execution times with theoretical complexity."""
        if not sizes or not times:
            return

        plt.figure(figsize=(10, 6))

        # Plot actual execution times
        plt.plot(sizes, times, 'o-', label='Actual Execution Time')

        # Plot theoretical O(V^3) complexity
        theoretical = [times[0] * (s / sizes[0])**3 for s in sizes]
        plt.plot(sizes, theoretical, '--', label='Theoretical O(V^3)')

        plt.xlabel('Number of Vertices (V)')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Ford-Fulkerson Algorithm: Execution Time vs Graph Size')
        plt.legend()
        plt.grid(True)

        plt.savefig(f'{self.results_dir}/time_complexity.png')
        plt.close()

    def create_max_flow_figure(self, sizes, flows):
        """Create a figure showing how max flow varies with graph size."""
        if not sizes or not flows:
            return

        plt.figure(figsize=(10, 6))

        plt.plot(sizes, flows, 'o-')

        plt.xlabel('Number of Vertices (V)')
        plt.ylabel('Average Maximum Flow')
        plt.title('Ford-Fulkerson Algorithm: Maximum Flow vs Graph Size')
        plt.grid(True)

        plt.savefig(f'{self.results_dir}/max_flow.png')
        plt.close()

    def visualize_graph(self, graph, size, max_flow):
        """Create a visualization of a flow network graph."""
        plt.figure(figsize=(12, 10))

        # Create a position layout for nodes using spring layout (no extra dependencies)
        pos = nx.spring_layout(graph, seed=42)

        # Define node colors - source (green), sink (red), others (light blue)
        node_colors = []
        source = 0
        sink = size - 1

        for node in graph.nodes():
            if node == source:
                node_colors.append('lime')
            elif node == sink:
                node_colors.append('salmon')
            else:
                node_colors.append('lightblue')

        # Draw the nodes
        nx.draw_networkx_nodes(graph, pos,
                               node_color=node_colors,
                               node_size=700,
                               edgecolors='black',
                               linewidths=1.5)

        # Draw node labels
        node_labels = {}
        for node in graph.nodes():
            if node == source:
                node_labels[node] = f"{node} (Source)"
            elif node == sink:
                node_labels[node] = f"{node} (Sink)"
            else:
                node_labels[node] = f"{node}"

        nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=10, font_weight='bold')

        # Draw edges with arrows
        nx.draw_networkx_edges(graph, pos,
                               arrowstyle='-|>',
                               arrowsize=20,
                               width=1.5,
                               edge_color='gray',
                               connectionstyle='arc3,rad=0.1',
                               arrows=True)

        # Draw edge labels (capacities)
        edge_labels = {(u, v): f"Capacity: {d['capacity']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(graph, pos,
                                     edge_labels=edge_labels,
                                     font_size=8,
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        plt.title(f"Flow Network - Size: {size}, Max Flow: {max_flow}", fontsize=16)
        plt.axis('off')  # Turn off the axis

        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lime', markersize=15, label='Source Node'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='salmon', markersize=15, label='Sink Node'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=15, label='Regular Node')
        ]
        plt.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/graph_size_{size}.png', dpi=300)
        plt.close()

    def print_summary(self, results):
        """Print a summary of the experimental results."""
        print("\nFord-Fulkerson Experiment Results:")
        print("----------------------------------")
        print("Theoretical time complexity: O(E * max_flow)")
        print("For dense graphs (E ~ V²) and max_flow ~ V: O(V³)")
        print("\nResults Summary:")

        for result in results:
            print(f"  Size {result['size']}: " +
                  f"Avg Time {result['avg_time']:.6f}s, " +
                  f"Avg Flow {result['avg_flow']:.2f}")

        print("\nDetailed results saved to CSV files in the results directory.")