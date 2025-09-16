import unittest
import os

# To make this runnable, we need to add the project's src directory to the path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_sources.tasks import TaskContextSource
from src.data_sources.documents import DocumentContextSource

class TestDataSources(unittest.TestCase):

    def setUp(self):
        """Set up mock configs for testing."""
        self.tasks_config = {
            "path": "data/mock/mock_tasks.json",
            "enabled": True
        }
        self.docs_config = {
            "path": "data/mock/mock_documents.json",
            "enabled": True
        }

    def test_task_retrieval(self):
        """Test that the Task source retrieves relevant tasks."""
        source = TaskContextSource(self.tasks_config)
        results = source.retrieve("QuantumLeap backend")
        self.assertTrue(len(results) >= 2)
        # Check if a known task title is in the content of one of the results
        self.assertTrue(any("Implement authentication service" in r['content'] for r in results))

    def test_document_retrieval(self):
        """Test that the Document source retrieves relevant doc chunks."""
        source = DocumentContextSource(self.docs_config)
        results = source.retrieve("microservices architecture")
        self.assertEqual(len(results), 1)
        self.assertIn("QuantumLeap Architecture", results[0]['content'])

    def test_no_results(self):
        """Test that sources return empty lists for irrelevant queries."""
        task_source = TaskContextSource(self.tasks_config)
        task_results = task_source.retrieve("nonexistentqueryxyz")
        self.assertEqual(len(task_results), 0)

        doc_source = DocumentContextSource(self.docs_config)
        doc_results = doc_source.retrieve("nonexistentqueryxyz")
        self.assertEqual(len(doc_results), 0)

if __name__ == '__main__':
    unittest.main()
