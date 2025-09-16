import os
import sys

# Add the project's src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_context import ContextEngineer

def run_role_based_demo():
    """
    Demonstrates how context changes based on the user's role for the same query.
    """
    print("--- Running Role-Based Demo ---")

    # Define paths to configuration files
    config_path = "config/context_config.yaml"
    roles_path = "config/user_roles.yaml"

    if not (os.path.exists(config_path) and os.path.exists(roles_path)):
        print(f"\nError: Could not find configuration files.")
        print("Please ensure you are running this script from the root of the 'contextcore' project directory.")
        return
        
    # Initialize the ContextEngineer
    context_engineer = ContextEngineer(config_path, roles_path)

    # Define a query that touches on both technical and product aspects
    query = "What is the status of the QuantumLeap project and its documentation?"

    # --- SCENARIO 1: The Engineer ---
    print("\n\n--- SCENARIO 1: Query as an 'engineer' ---")
    engineer_context = context_engineer.build_context(query, "engineer")
    print("\n=== CONTEXT FOR ENGINEER ===\n")
    print(engineer_context)
    print("\nAnalysis: The engineer gets technical details from tasks, graph connections about architecture, and document chunks about the microservices stack.")

    # --- SCENARIO 2: The Product Manager ---
    print("\n\n--- SCENARIO 2: Query as a 'product_manager' ---")
    pm_context = context_engineer.build_context(query, "product_manager")
    print("\n=== CONTEXT FOR PRODUCT MANAGER ===\n")
    print(pm_context)
    print("\nAnalysis: The PM gets task status but is filtered out from seeing the deep technical architecture documents because their role lacks the 'technical' or 'architecture' tags.")

    # --- SCENARIO 3: The Guest ---
    print("\n\n--- SCENARIO 3: Query as a 'guest' ---")
    guest_context = context_engineer.build_context(query, "guest")
    print("\n=== CONTEXT FOR GUEST ===\n")
    print(guest_context)
    print("\nAnalysis: The guest has no access to tasks or internal documents. They can only see documents explicitly tagged as 'public'. In this case, for this query, they get no relevant information.")


if __name__ == "__main__":
    run_role_based_demo()
