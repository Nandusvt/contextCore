import os
import sys
import time

# Add the project's src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_context import ContextEngineer

def run_benchmark():
    """
    A simple benchmark to measure the performance of the context building process.
    """
    print("--- Running Performance Benchmark ---")

    config_path = "config/context_config.yaml"
    roles_path = "config/user_roles.yaml"

    if not (os.path.exists(config_path) and os.path.exists(roles_path)):
        print("\nError: Could not find configuration files.")
        print("Please ensure you are running this script from the root of the 'contextcore' project directory.")
        return

    # Initialize the ContextEngineer
    print("Initializing ContextEngineer...")
    start_init = time.perf_counter()
    context_engineer = ContextEngineer(config_path, roles_path)
    end_init = time.perf_counter()
    print(f"Initialization took: {end_init - start_init:.4f} seconds")

    queries_to_benchmark = [
        ("What is the status of the QuantumLeap project?", "engineer"),
        ("Tell me about the Phoenix project roadmap", "product_manager"),
        ("Find all public API documentation", "guest"),
        ("A very long and complex query about database schema optimizations and backend security protocols in the QuantumLeap project", "engineer")
    ]

    total_time = 0
    num_runs = 10  # Run multiple times to get a more stable average

    print(f"\nRunning {len(queries_to_benchmark)} queries, {num_runs} times each...")

    for query, role in queries_to_benchmark:
        start_time = time.perf_counter()
        for _ in range(num_runs):
            # We don't print the context here to keep the benchmark clean
            context_engineer.build_context(query, role)
        end_time = time.perf_counter()
        
        avg_time = (end_time - start_time) / num_runs
        total_time += (end_time - start_time)
        print(f"Query: '{query[:30]}...' ({role}) - Avg time: {avg_time:.4f} seconds")

    print("-" * 50)
    print(f"Total benchmark time for {len(queries_to_benchmark) * num_runs} builds: {total_time:.4f} seconds")
    print("Note: This is a simple benchmark on mock data. Performance will vary with real data sources and more complex logic.")


if __name__ == "__main__":
    run_benchmark()