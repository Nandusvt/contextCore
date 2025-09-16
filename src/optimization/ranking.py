#path: src/optimization/ranking.py

from typing import List, Dict, Any

class Ranker:
    """
    Ranks a list of context chunks based on their relevance to a query.
    """

    def __init__(self, method: str = "keyword_match"):
        """
        Initializes the Ranker.
        
        Args:
            method (str): The ranking method to use.
                          'keyword_match' is a simple default.
                          Future methods could include 'embedding_similarity'.
        """
        self.method = method

    def _rank_by_keyword_match(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks chunks based on the number of query keywords they contain.
        
        Args:
            query (str): The user's query.
            chunks (List[Dict[str, Any]]): The list of context chunks.
            
        Returns:
            List[Dict[str, Any]]: Chunks sorted by relevance score, descending.
        """
        query_terms = set(query.lower().split())
        if not query_terms:
            return chunks

        scored_chunks = []
        for chunk in chunks:
            content = chunk.get("content", "").lower()
            match_count = sum(1 for term in query_terms if term in content)
            
            # Add score to each chunk's metadata for transparency
            if 'metadata' not in chunk:
                chunk['metadata'] = {}
            chunk['metadata']['relevance_score'] = match_count
            scored_chunks.append(chunk)

        # Sort chunks by score in descending order
        return sorted(scored_chunks, key=lambda x: x['metadata']['relevance_score'], reverse=True)

    def rank(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Applies the configured ranking method to the chunks.
        
        Args:
            query (str): The user's query.
            chunks (List[Dict[str, Any]]): The list of context chunks.
            
        Returns:
            List[Dict[str, Any]]: The sorted list of context chunks.
        """
        if self.method == "keyword_match":
            return self._rank_by_keyword_match(query, chunks)
        else:
            print(f"Warning: Unknown ranking method '{self.method}'. Returning original order.")
            return chunks
