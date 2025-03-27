import networkx as nx
from config import GRAPH_SIZES, EDGE_PROBABILITY, MIN_CAPACITY, MAX_CAPACITY, NUM_TRIALS
from graph_generator import GraphGenerator
from ford_fulkerson import FordFulkerson
from results_reporter import ResultsReporter

def run_experiments():
    """Run Ford-Fulkerson experiments on graphs of various sizes."""
    # Initialize results reporter
    reporter = ResultsReporter()

    # Lists to store results
    sizes = []
    times = []
    flows = []
    results = []

    # Run experiments for each graph size
    for size in GRAPH_SIZES:
        print(f"Running experiments for graph size {size}...")

        size_times = []
        size_flows = []
        trials_completed = 0

        # Run multiple trials for each size
        while trials_completed < NUM_TRIALS:
            print(f"  Trial {trials_completed + 1}/{NUM_TRIALS}")

            # Generate a random graph
            generator = GraphGenerator(size, EDGE_PROBABILITY, MIN_CAPACITY, MAX_CAPACITY)
            graph = generator.generate_graph()

            # Check if graph has a path from source to sink
            source = 0
            sink = size - 1

            if not nx.has_path(graph, source, sink):
                print(f"  No path from source to sink. Regenerating graph...")
                continue

            # Run Ford-Fulkerson
            ff = FordFulkerson(graph)
            max_flow, execution_time = ff.find_max_flow(source, sink)

            # Store results
            size_times.append(execution_time)
            size_flows.append(max_flow)
            trials_completed += 1

            print(f"  Max Flow: {max_flow}, Time: {execution_time:.6f}s")

            # Visualize the first successful graph of each size
            if trials_completed == 1:
                reporter.visualize_graph(graph, size, max_flow)

        # Skip if no valid trials
        if not size_times:
            continue

        # Calculate averages
        avg_time = sum(size_times) / len(size_times)
        avg_flow = sum(size_flows) / len(size_flows)

        sizes.append(size)
        times.append(avg_time)
        flows.append(avg_flow)

        results.append({
            'size': size,
            'avg_time': avg_time,
            'avg_flow': avg_flow,
            'times': size_times,
            'flows': size_flows
        })

        print(f"  Average Time: {avg_time:.6f}s, Average Max Flow: {avg_flow:.2f}")

    # Generate reports
    reporter.save_results_to_csv(results)
    reporter.create_time_complexity_figure(sizes, times)
    reporter.create_max_flow_figure(sizes, flows)
    reporter.print_summary(results)

def main():
    """Main function to run experiments and analyze results."""
    print("Starting Ford-Fulkerson experiments...")
    run_experiments()
    print("Experiments completed.")

if __name__ == "__main__":
    main()