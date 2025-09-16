#path: src/optimization/deduplication.py

from typing import List, Dict, Any

class Deduplicator:
    """
    Removes duplicate or highly similar context chunks.
    """

    def __init__(self, threshold: float = 0.9):
        """
        Initializes the Deduplicator.
        
        Args:
            threshold (float): The Jaccard similarity threshold above which
                               content is considered a duplicate.
        """
        self.threshold = threshold

    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calculates the Jaccard similarity between two texts.
        """
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        
        if not set1 and not set2:
            return 1.0 # Both empty
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

    def deduplicate(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters a list of chunks, removing near-duplicates.
        It keeps the first occurrence of a piece of content.
        
        Args:
            chunks (List[Dict[str, Any]]): A list of context chunks,
                                          ideally already ranked by relevance.
                                          
        Returns:
            List[Dict[str, Any]]: A list of unique context chunks.
        """
        unique_chunks = []
        seen_contents = []

        for chunk in chunks:
            content = chunk.get("content", "")
            is_duplicate = False
            for seen_content in seen_contents:
                if self._jaccard_similarity(content, seen_content) > self.threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_chunks.append(chunk)
                seen_contents.append(content)
        
        return unique_chunks
