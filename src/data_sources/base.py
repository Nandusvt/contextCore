from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseContextSource(ABC):
    """
    Abstract base class for all context data sources.
    Defines the interface that all concrete data source implementations must follow.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the data source with its specific configuration.
        
        Args:
            config (Dict[str, Any]): A dictionary containing configuration
                                      details, such as file paths or API endpoints.
        """
        self.config = config
        self.source_id = "base" # Should be overridden by subclasses

    @abstractmethod
    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieves context relevant to the given query from the data source.
        
        Args:
            query (str): The user's query to search for.
            **kwargs: Additional keyword arguments for source-specific retrieval.
            
        Returns:
            List[Dict[str, Any]]: A list of context chunks. Each chunk is a 
                                  dictionary with at least 'source', 'id', 
                                  'content', and 'metadata'.
        """
        pass

    def _format_chunk(self, id: str, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        A helper method to ensure all returned chunks have a consistent format.
        
        Args:
            id (str): A unique identifier for the chunk within the source.
            content (str): The actual text content of the chunk.
            metadata (Dict[str, Any]): A dictionary of metadata about the chunk.
            
        Returns:
            Dict[str, Any]: A consistently formatted dictionary representing the context chunk.
        """
        return {
            "source": self.source_id,
            "id": f"{self.source_id}_{id}",
            "content": content,
            "metadata": metadata
        }
