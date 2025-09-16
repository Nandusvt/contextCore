import os
import sys

# Add the project's src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_context import ContextEngineer

def run_basic_demo():
    """
    Demonstrates the basic functionality of the ContextEngineer
    by building context for a single query and role.
    """
    print("--- Running Basic Usage Demo ---")

    # Define paths to configuration files
    # This assumes you are running the script from the root `contextcore` directory
    config_path = "config/context_config.yaml"
    roles_path = "config/user_roles.yaml"

    if not (os.path.exists(config_path) and os.path.exists(roles_path)):
        print(f"\nError: Could not find configuration files.")
        print("Please ensure you are running this script from the root of the 'contextcore' project directory.")
        return

    # 1. Initialize the ContextEngineer
    try:
        context_engineer = ContextEngineer(config_path, roles_path)
    except Exception as e:
        print(f"Failed to initialize ContextEngineer: {e}")
        return

    # 2. Define a query and user role
    query = "Tell me about the QuantumLeap project's database and architecture."
    user_role = "engineer" # An engineer should have access to this information

    # 3. Build the context
    final_context = context_engineer.build_context(query, user_role)

    # 4. Print the result
    print("\n" + "="*50)
    print("                FINAL CONTEXT                ")
    print("="*50)
    print(f"Query: '{query}'")
    print(f"User Role: '{user_role}'")
    print("-"*50)
    print(final_context)
    print("="*50)

if __name__ == "__main__":
    run_basic_demo()
