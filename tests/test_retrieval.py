import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.retrieval.context_retriever import ContextRetriever
from src.utils.config_loader import load_config

class TestContextRetriever(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load config once for all tests."""
        cls.config = load_config("config/context_config.yaml")

    def test_initialization(self):
        """Test that the retriever initializes sources correctly."""
        retriever = ContextRetriever(self.config)
        # Check if enabled sources from config are present
        self.assertIn("tasks", retriever.sources)
        self.assertIn("documents", retriever.sources)
        self.assertIn("graphiti", retriever.sources)

    def test_full_retrieval(self):
        """Test retrieving from all sources."""
        retriever = ContextRetriever(self.config)
        results = retriever.retrieve("QuantumLeap")
        self.assertGreater(len(results), 3) # Should get results from tasks, docs, and graph
        
        sources_found = {r['source'] for r in results}
        self.assertEqual(sources_found, {"tasks", "documents", "graphiti"})

    def test_selective_retrieval(self):
        """Test retrieving from a subset of allowed sources."""
        retriever = ContextRetriever(self.config)
        results = retriever.retrieve("QuantumLeap", allowed_sources=["documents", "tasks"])
        self.assertGreater(len(results), 0)
        
        sources_found = {r['source'] for r in results}
        self.assertEqual(sources_found, {"tasks", "documents"})


if __name__ == '__main__':
    unittest.main()
