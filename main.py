import networkx as nx
from config import GRAPH_SIZES, EDGE_PROBABILITY, MIN_CAPACITY, MAX_CAPACITY, NUM_TRIALS
from graph_generator import GraphGenerator
from ford_fulkerson import FordFulkerson
from results_reporter import ResultsReporter

def run_experiments():
    """Run Ford-Fulkerson experiments on graphs of various sizes and densities."""
    # Initialize results reporter
    reporter = ResultsReporter()

    # Dictionary to store all results by edge probability
    all_results = {}

    # Run experiments for each edge probability
    for prob in EDGE_PROBABILITY:
        print(f"\nRunning experiments for edge probability {prob}...")

        # Lists to store results for current probability
        sizes = []
        times = []
        flows = []
        results = []

        # Run experiments for each graph size with current probability
        for size in GRAPH_SIZES:
            print(f"  Running experiments for graph size {size}...")

            size_times = []
            size_flows = []
            trials_completed = 0

            # Run multiple trials for each size
            while trials_completed < NUM_TRIALS:
                print(f"    Trial {trials_completed + 1}/{NUM_TRIALS}")

                # Generate a random graph with current probability
                generator = GraphGenerator(size, prob, MIN_CAPACITY, MAX_CAPACITY)
                graph = generator.generate_graph()

                # Check if graph has a path from source to sink
                source = 0
                sink = size - 1

                if not nx.has_path(graph, source, sink):
                    print(f"    No path from source to sink. Regenerating graph...")
                    continue

                # Run Ford-Fulkerson
                ff = FordFulkerson(graph)
                max_flow, execution_time = ff.find_max_flow(source, sink)

                # Store results
                size_times.append(execution_time)
                size_flows.append(max_flow)
                trials_completed += 1

                print(f"    Max Flow: {max_flow}, Time: {execution_time:.6f}s")

                # Visualize the first successful graph of each size and probability
                if trials_completed == 1:
                    reporter.visualize_graph(graph, size, max_flow, f"prob_{prob}")

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
                'prob': prob,  # Store probability with results
                'avg_time': avg_time,
                'avg_flow': avg_flow,
                'times': size_times,
                'flows': size_flows
            })

            print(f"    Average Time: {avg_time:.6f}s, Average Max Flow: {avg_flow:.2f}")

        # Store results for current probability
        all_results[prob] = {
            'sizes': sizes,
            'times': times,
            'flows': flows,
            'results': results
        }

        # Generate reports for current probability
        reporter.save_results_to_csv(results, f"prob_{prob}")
        reporter.create_time_complexity_figure(sizes, times, f"prob_{prob}")
        reporter.create_max_flow_figure(sizes, flows, f"prob_{prob}")

    # Create combined charts for all edge probabilities
    reporter.create_combined_time_complexity_figure(all_results)
    reporter.create_combined_max_flow_figure(all_results)

    # Create comparison table with all results
    all_results_flat = []
    for prob_results in all_results.values():
        all_results_flat.extend(prob_results['results'])

    reporter.create_comparison_table(all_results_flat)
    reporter.print_summary(all_results_flat)

def main():
    """Main function to run experiments and analyze results."""
    print("Starting Ford-Fulkerson experiments...")
    run_experiments()
    print("Experiments completed.")

if __name__ == "__main__":
    main()