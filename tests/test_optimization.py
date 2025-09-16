import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.optimization.ranking import Ranker
from src.optimization.deduplication import Deduplicator
from src.optimization.token_budget import TokenBudgetManager

class TestOptimization(unittest.TestCase):

    def setUp(self):
        """Set up sample data for testing."""
        self.sample_chunks = [
            {'source': 'docs', 'content': 'The quick brown fox jumps over the lazy dog.', 'metadata': {}},
            {'source': 'tasks', 'content': 'A lazy dog is no match for a quick fox.', 'metadata': {}},
            {'source': 'docs', 'content': 'This is a completely different sentence.', 'metadata': {}},
            {'source': 'graph', 'content': 'The fox is brown and very quick.', 'metadata': {}}
        ]

    def test_ranking(self):
        """Test the keyword-based ranker."""
        ranker = Ranker(method="keyword_match")
        query = "quick brown fox"
        ranked = ranker.rank(query, self.sample_chunks)
        
        self.assertEqual(len(ranked), 4)
        # The first result should have the highest score (most keyword matches)
        self.assertEqual(ranked[0]['content'], 'The quick brown fox jumps over the lazy dog.')
        self.assertEqual(ranked[0]['metadata']['relevance_score'], 3)
        self.assertEqual(ranked[3]['content'], 'This is a completely different sentence.')
        self.assertEqual(ranked[3]['metadata']['relevance_score'], 0)


    def test_deduplication(self):
        """Test the Jaccard similarity-based deduplicator."""
        deduplicator = Deduplicator(threshold=0.8)
        # The first two sentences are very similar
        deduplicated = deduplicator.deduplicate(self.sample_chunks)
        
        self.assertEqual(len(deduplicated), 3)
        # It should keep the first one and remove the second one
        contents = [c['content'] for c in deduplicated]
        self.assertIn('The quick brown fox jumps over the lazy dog.', contents)
        self.assertNotIn('A lazy dog is no match for a quick fox.', contents)

    def test_token_budget(self):
        """Test the token budget manager."""
        # Use a very small budget to test truncation
        budget_manager = TokenBudgetManager(max_tokens=15, tokenizer_model="cl100k_base")
        
        final_context = budget_manager.construct_context(self.sample_chunks)
        
        # Only the first chunk should fit, as it's around 15 tokens with formatting
        # (Content is ~10, plus formatting)
        self.assertIn("The quick brown fox", final_context)
        self.assertNotIn("completely different", final_context)
        
        final_token_count = budget_manager.tokenizer.count_tokens(final_context)
        self.assertLessEqual(final_token_count, 15)

if __name__ == '__main__':
    unittest.main()