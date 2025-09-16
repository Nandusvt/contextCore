# path: src/optimization/token_budget.py

from typing import List, Dict, Any
from ..utils.tokenizer import Tokenizer

class TokenBudgetManager:
    """
    Manages the token budget for the final context, ensuring it doesn't
    exceed the LLM's context window limit.
    """

    def __init__(self, max_tokens: int, tokenizer_model: str):
        """
        Initializes the TokenBudgetManager.
        
        Args:
            max_tokens (int): The maximum number of tokens allowed in the context.
            tokenizer_model (str): The model name for the tiktoken tokenizer.
        """
        self.max_tokens = max_tokens
        self.tokenizer = Tokenizer(tokenizer_model)

    def construct_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Constructs the final context string from chunks, respecting the token limit.
        It iterates through ranked and deduplicated chunks, adding them until the
        budget is nearly full.
        
        Args:
            chunks (List[Dict[str, Any]]): A list of chunks, sorted by importance.
            
        Returns:
            str: A single string containing the formatted context.
        """
        final_context = []
        current_tokens = 0

        for chunk in chunks:
            # Format the chunk content with its source for clarity
            content_str = f"Source: {chunk.get('source', 'unknown')}\nContent: {chunk.get('content', '')}\n---\n"
            
            chunk_token_count = self.tokenizer.count_tokens(content_str)
            
            if current_tokens + chunk_token_count <= self.max_tokens:
                final_context.append(content_str)
                current_tokens += chunk_token_count
            else:
                # Stop adding chunks if the next one would exceed the budget
                print(f"Token budget reached. Stopping context construction. Total tokens: {current_tokens}")
                break
        
        return "".join(final_context)
