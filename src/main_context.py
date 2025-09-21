# This file makes the src directory a Python package.
import os
from typing import List, Dict, Any

from .utils.config_loader import load_config, load_user_roles
from .retrieval.context_retriever import ContextRetriever
from .optimization.ranking import Ranker
from .optimization.deduplication import Deduplicator
from .optimization.token_budget import TokenBudgetManager
from .personalization.role_handler import RoleHandler

class ContextEngineer:
    """
    The main orchestrator for the context engineering pipeline.
    It integrates all components to retrieve, personalize, and optimize context.
    """

    def __init__(self, config_path: str, roles_path: str):
        """
        Initializes the ContextEngineer with configurations.
        Args:
            config_path (str): Path to the main context_config.yaml.
            roles_path (str): Path to the user_roles.yaml.
        """
        # Load configurations


        self.config = load_config(config_path)
        self.roles_config = load_user_roles(roles_path)

        # Initialize core components
        self.retriever = ContextRetriever(self.config)
        self.role_handler = RoleHandler(self.roles_config)
        
        # Initialize optimization components
        self.ranker = Ranker(method=self.config['optimization']['ranking']['method'])
        self.deduplicator = Deduplicator(threshold=self.config['optimization']['deduplication']['similarity_threshold'])
        self.budget_manager = TokenBudgetManager(
            max_tokens=self.config['defaults']['max_context_tokens'],
            tokenizer_model=self.config['defaults']['tokenizer_model']
        )

    def build_context(self, query: str, user_role: str) -> str:
        """
        Executes the full context engineering pipeline.
        
        Args:
            query (str): The user's query.
            user_role (str): The role of the user making the query.
            
        Returns:
            str: The final, optimized context string.
        """
        # 1. Personalization: Get permissions for the user's role
        try:
            permissions = self.role_handler.get_permissions(user_role)
            allowed_sources = permissions.get('allowed_sources', [])
            filter_tags = permissions.get('filter_by_tags', [])
        except ValueError as e:
            return "Error: Invalid user role specified."

        # 2. Retrieval: Fetch raw context from allowed sources
        raw_context_chunks = self.retriever.retrieve(query, allowed_sources)

        # 3. Personalization: Filter retrieved context based on tags
        filtered_context = self.role_handler.filter_context_by_role(raw_context_chunks, user_role)

        # 4. Optimization: Rank the filtered context
        ranked_context = self.ranker.rank(query, filtered_context)

        # 5. Optimization: Deduplicate the ranked context
        deduplicated_context = self.deduplicator.deduplicate(ranked_context)
        
        # 6. Optimization: Manage token budget
        final_context_string = self.budget_manager.construct_context(deduplicated_context)
        return final_context_string

if __name__ == '__main__':
    # Example of direct usage
    # Note: Assumes running from the root directory `contextcore/`
    CONFIG_PATH = 'config/context_config.yaml'
    ROLES_PATH = 'config/user_roles.yaml'

    if not (os.path.exists(CONFIG_PATH) and os.path.exists(ROLES_PATH)):
        print("Error: Configuration files not found. Make sure you are running this from the `contextcore` root directory.")
    else:
        engineer = ContextEngineer(config_path=CONFIG_PATH, roles_path=ROLES_PATH)
        
        test_query = "What is the status of the 'QuantumLeap' project and are there any related architecture documents?"
        
        # Test with Engineer role
        eng_context = engineer.build_context(query=test_query, user_role='engineer')
        print("\n=== FINAL CONTEXT FOR ENGINEER ===\n")
        print(eng_context)
        
        # Test with Product Manager role
        pm_context = engineer.build_context(query=test_query, user_role='product_manager')
        print("\n=== FINAL CONTEXT FOR PRODUCT MANAGER ===\n")
        print(pm_context)
