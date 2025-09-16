import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_context import ContextEngineer

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize the ContextEngineer once for all integration tests."""
        cls.engineer = ContextEngineer(
            config_path="config/context_config.yaml",
            roles_path="config/user_roles.yaml"
        )

    def test_engineer_role_context_build(self):
        """
        Test the full pipeline for the 'engineer' role.
        An engineer should get technical context about QuantumLeap.
        """
        query = "What is the architecture of QuantumLeap?"
        final_context = self.engineer.build_context(query, user_role="engineer")

        self.assertIsInstance(final_context, str)
        self.assertGreater(len(final_context), 0)
        
        # Check for expected technical content
        self.assertIn("microservices architecture", final_context.lower())
        self.assertIn("QuantumLeap Architecture", final_context) # From graph and docs
        
        # Ensure no product-specific, non-technical info is present
        self.assertNotIn("Product Roadmap", final_context)

    def test_pm_role_context_build(self):
        """
        Test the full pipeline for the 'product_manager' role.
        A PM should not see deep technical architecture details.
        """
        query = "What's the plan for the Phoenix project?"
        final_context = self.engineer.build_context(query, user_role="product_manager")
        
        self.assertIsInstance(final_context, str)
        self.assertGreater(len(final_context), 0)
        
        # Check for product/planning content
        self.assertIn("Product Roadmap", final_context)
        self.assertIn("user dashboard", final_context.lower())
        
        # A PM shouldn't see the QuantumLeap architecture doc as it's not tagged 'product'
        self.assertNotIn("microservices architecture", final_context.lower())
        
    def test_invalid_role(self):
        """Test that the system handles an undefined role gracefully."""
        query = "any query"
        final_context = self.engineer.build_context(query, user_role="ceo")
        self.assertIn("Invalid user role", final_context)


if __name__ == '__main__':
    unittest.main()