import os
import csv
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class ResultsReporter:
    """Class for generating reports and visualizations from experiments."""

    def __init__(self, results_dir="results"):
        """Initialize the reporter with a results directory."""
        self.results_dir = results_dir

        # Create results directory if it doesn't exist
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def save_results_to_csv(self, results, prefix=""):
        """Save experimental results to CSV files."""
        try:
            # Create subdirectory if prefix is provided
            if prefix:
                subdir = os.path.join(self.results_dir, prefix)
                os.makedirs(subdir, exist_ok=True)
                print(f"Saving results to directory: {subdir}")
            else:
                subdir = self.results_dir
                os.makedirs(subdir, exist_ok=True)

            # Save summary results
            with open(os.path.join(subdir, 'summary.csv'), 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Size', 'Edge Probability', 'Avg Time (s)', 'Avg Flow'])
                for result in results:
                    writer.writerow([result['size'], result['prob'], result['avg_time'], result['avg_flow']])

            # Save detailed results for each graph size
            for result in results:
                size = result['size']
                prob = result['prob']
                with open(os.path.join(subdir, f'size_{size}.csv'), 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Trial', 'Time (s)', 'Flow'])
                    for i, (t, flow) in enumerate(zip(result['times'], result['flows'])):
                        writer.writerow([i+1, t, flow])
        except Exception as e:
            print(f"Error saving results to CSV: {e}")

    def create_time_complexity_figure(self, sizes, times, prefix=""):
        """Create a figure comparing execution times with theoretical complexity."""
        if not sizes or not times:
            return

        try:
            # Create subdirectory if prefix is provided
            if prefix:
                subdir = os.path.join(self.results_dir, prefix)
                os.makedirs(subdir, exist_ok=True)
                print(f"Saving time complexity figure to directory: {subdir}")
            else:
                subdir = self.results_dir
                os.makedirs(subdir, exist_ok=True)

            plt.figure(figsize=(10, 6))

            # Plot actual execution times
            plt.plot(sizes, times, 'o-', label='Actual Execution Time')

            # Plot theoretical O(V^3) complexity
            theoretical = [times[0] * (s / sizes[0])**3 for s in sizes]
            plt.plot(sizes, theoretical, '--', label='Theoretical O(V^3)')

            # Get probability value from prefix for title
            prob_title = f" (Edge Probability: {prefix.split('_')[1]})" if prefix else ""

            plt.xlabel('Number of Vertices (V)')
            plt.ylabel('Execution Time (seconds)')
            plt.title(f'Ford-Fulkerson Algorithm: Execution Time vs Graph Size{prob_title}')
            plt.legend()
            plt.grid(True)

            output_file = os.path.join(subdir, 'time_complexity.png')
            plt.savefig(output_file)
            plt.close()
        except Exception as e:
            print(f"Error creating time complexity figure: {e}")
            plt.close()

    def create_max_flow_figure(self, sizes, flows, prefix=""):
        """Create a figure showing how max flow varies with graph size."""
        if not sizes or not flows:
            return

        try:
            # Create subdirectory if prefix is provided
            if prefix:
                subdir = os.path.join(self.results_dir, prefix)
                os.makedirs(subdir, exist_ok=True)
                print(f"Saving max flow figure to directory: {subdir}")
            else:
                subdir = self.results_dir
                os.makedirs(subdir, exist_ok=True)

            plt.figure(figsize=(10, 6))

            plt.plot(sizes, flows, 'o-')

            # Get probability value from prefix for title
            prob_title = f" (Edge Probability: {prefix.split('_')[1]})" if prefix else ""

            plt.xlabel('Number of Vertices (V)')
            plt.ylabel('Average Maximum Flow')
            plt.title(f'Ford-Fulkerson Algorithm: Maximum Flow vs Graph Size{prob_title}')
            plt.grid(True)

            output_file = os.path.join(subdir, 'max_flow.png')
            plt.savefig(output_file)
            plt.close()
        except Exception as e:
            print(f"Error creating max flow figure: {e}")
            plt.close()

    def create_comparison_table(self, results):
        """Create a detailed comparison table of execution times and max flows for all graph sizes and edge probabilities."""
        try:
            comparison_file = os.path.join(self.results_dir, 'comparison_table.csv')
            print(f"Creating comparison table at {comparison_file}")

            # Ensure the results directory exists
            os.makedirs(self.results_dir, exist_ok=True)

            with open(comparison_file, 'w', newline='') as f:
                writer = csv.writer(f)

                # Write header row
                writer.writerow(['Graph Size', 'Edge Probability', 'Trial', 'Execution Time (s)', 'Max Flow'])

                # Group results by edge probability and size for easier reporting
                grouped_results = defaultdict(list)

                for result in results:
                    key = (result['size'], result['prob'])
                    grouped_results[key].append(result)

                # Write data for each combination of size and probability
                for (size, prob), result_list in sorted(grouped_results.items()):
                    for result in result_list:
                        for i, (time, flow) in enumerate(zip(result['times'], result['flows'])):
                            writer.writerow([size, prob, i+1, f"{time:.6f}", f"{flow:.2f}"])

                        # Add a row with averages
                        writer.writerow([
                            size,
                            prob,
                            'Average',
                            f"{result['avg_time']:.6f}",
                            f"{result['avg_flow']:.2f}"
                        ])

                    # Add empty row for better readability
                    writer.writerow([])

                # Add a summary section
                writer.writerow(['Summary - Average Values'])
                writer.writerow(['Graph Size', 'Edge Probability', '', 'Avg Execution Time (s)', 'Avg Max Flow'])

                for (size, prob), result_list in sorted(grouped_results.items()):
                    for result in result_list:
                        writer.writerow([
                            size,
                            prob,
                            '',
                            f"{result['avg_time']:.6f}",
                            f"{result['avg_flow']:.2f}"
                        ])

            print(f"Comparison table successfully created at {comparison_file}")
        except Exception as e:
            print(f"Error creating comparison table: {e}")

    def visualize_graph(self, graph, size, max_flow, prefix=""):
        """Create a visualization of a flow network graph."""
        try:
            # Create subdirectory if prefix is provided
            if prefix:
                subdir = os.path.join(self.results_dir, prefix)
                os.makedirs(subdir, exist_ok=True)
                print(f"Saving visualization to directory: {subdir}")
            else:
                subdir = self.results_dir
                os.makedirs(subdir, exist_ok=True)

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

            # Get probability value from prefix for title
            prob_info = f", Edge Probability: {prefix.split('_')[1]}" if prefix else ""

            plt.title(f"Flow Network - Size: {size}{prob_info}, Max Flow: {max_flow}", fontsize=16)
            plt.axis('off')  # Turn off the axis

            # Add legend
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lime', markersize=15, label='Source Node'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='salmon', markersize=15, label='Sink Node'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=15, label='Regular Node')
            ]
            plt.legend(handles=legend_elements, loc='upper right')

            plt.tight_layout()

            # Save the figure with full path
            output_file = os.path.join(subdir, f"graph_size_{size}.png")
            print(f"Saving graph visualization to: {output_file}")
            plt.savefig(output_file, dpi=300)
            plt.close()

        except Exception as e:
            print(f"Error visualizing graph: {e}")
            # Close the figure in case of error to avoid memory leaks
            plt.close()

    def print_summary(self, results):
        """Print a summary of the experimental results."""
        print("\nFord-Fulkerson Experiment Results:")
        print("----------------------------------")
        print("Theoretical time complexity: O(E * max_flow)")
        print("For dense graphs (E ~ V²) and max_flow ~ V: O(V³)")
        print("\nResults Summary:")

        # Group results by edge probability
        grouped_results = defaultdict(list)

        for result in results:
            prob = result['prob']
            grouped_results[prob].append(result)

        for prob, prob_results in sorted(grouped_results.items()):
            print(f"\nEdge Probability: {prob}")
            print("-" * (18 + len(str(prob))))

            for result in sorted(prob_results, key=lambda x: x['size']):
                print(f"  Size {result['size']}: " +
                      f"Avg Time {result['avg_time']:.6f}s, " +
                      f"Avg Flow {result['avg_flow']:.2f}")

        print("\nDetailed results saved to CSV files in the results directory.")

    def create_combined_time_complexity_figure(self, all_results):
        """Create a combined figure showing time complexity for all edge probabilities.

        Parameters:
        all_results (dict): Dictionary with edge probabilities as keys and result data as values
        """
        try:
            plt.figure(figsize=(12, 8))

            # Define a color map for different edge probabilities
            colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

            # Plot actual execution times for each edge probability
            for i, (prob, data) in enumerate(sorted(all_results.items())):
                sizes = data['sizes']
                times = data['times']

                if not sizes or not times:
                    continue

                color_index = i % len(colors)
                plt.plot(sizes, times, 'o-', color=colors[color_index],
                         label=f'Edge Probability: {prob}')

                # Plot theoretical O(V^3) complexity for the first probability only
                if i == 0 and times and sizes:
                    theoretical = [times[0] * (s / sizes[0])**3 for s in sizes]
                    plt.plot(sizes, theoretical, '--', color='black', label='Theoretical O(V^3)')

            plt.xlabel('Number of Vertices (V)')
            plt.ylabel('Execution Time (seconds)')
            plt.title('Ford-Fulkerson Algorithm: Execution Time vs Graph Size (All Edge Probabilities)')
            plt.legend()
            plt.grid(True)

            # Ensure the results directory exists
            os.makedirs(self.results_dir, exist_ok=True)

            output_file = os.path.join(self.results_dir, 'combined_time_complexity.png')
            print(f"Saving combined time complexity figure to: {output_file}")
            plt.savefig(output_file, dpi=300)
            plt.close()

        except Exception as e:
            print(f"Error creating combined time complexity figure: {e}")
            plt.close()

    def create_combined_max_flow_figure(self, all_results):
        """Create a combined figure showing maximum flow for all edge probabilities.

        Parameters:
        all_results (dict): Dictionary with edge probabilities as keys and result data as values
        """
        try:
            plt.figure(figsize=(12, 8))

            # Define a color map for different edge probabilities
            colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

            # Plot max flows for each edge probability
            for i, (prob, data) in enumerate(sorted(all_results.items())):
                sizes = data['sizes']
                flows = data['flows']

                if not sizes or not flows:
                    continue

                color_index = i % len(colors)
                plt.plot(sizes, flows, 'o-', color=colors[color_index],
                         label=f'Edge Probability: {prob}')

            plt.xlabel('Number of Vertices (V)')
            plt.ylabel('Average Maximum Flow')
            plt.title('Ford-Fulkerson Algorithm: Maximum Flow vs Graph Size (All Edge Probabilities)')
            plt.legend()
            plt.grid(True)

            # Ensure the results directory exists
            os.makedirs(self.results_dir, exist_ok=True)

            output_file = os.path.join(self.results_dir, 'combined_max_flow.png')
            print(f"Saving combined max flow figure to: {output_file}")
            plt.savefig(output_file, dpi=300)
            plt.close()

        except Exception as e:
            print(f"Error creating combined max flow figure: {e}")
            plt.close()