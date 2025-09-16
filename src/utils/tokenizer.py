import tiktoken

class Tokenizer:
    """
    A simple wrapper around the tiktoken library for consistent token counting.
    """

    def __init__(self, model_name: str = "cl100k_base"):
        """
        Initializes the tokenizer with a specific encoding model.
        
        Args:
            model_name (str): The name of the model to use for tokenization,
                              e.g., 'cl100k_base' (for GPT-3.5/4) or 'p50k_base'.
        """
        try:
            self.encoding = tiktoken.get_encoding(model_name)
        except Exception as e:
            print(f"Warning: Could not get encoding for '{model_name}'. Falling back to 'cl100k_base'. Error: {e}")
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """
        Counts the number of tokens in a given string.
        
        Args:
            text (str): The input string.
            
        Returns:
            int: The number of tokens.
        """
        if not isinstance(text, str):
            return 0
        return len(self.encoding.encode(text))