# path: src/retrieval/context_retriever.py

from typing import List, Dict, Any

# Import all available data source classes
from ..data_sources.tasks import TaskContextSource
from ..data_sources.graphiti import GraphitiContextSource
from ..data_sources.documents import DocumentContextSource
from ..data_sources.semantic_search import SemanticSearchSource

class ContextRetriever:
    """
    Manages and queries multiple data sources to gather a broad set of context.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config.get("data_sources", {})
        self.sources = {}
        self._initialize_sources()

    def _initialize_sources(self):
        """
        Initializes instances of all configured and enabled data sources.
        """
        # Mapping of source keys in config to their respective classes
        source_class_map = {
            "tasks": TaskContextSource,
            "graphiti": GraphitiContextSource,
            "documents": DocumentContextSource,
            "semantic_search": SemanticSearchSource # For future use
        }

        for key, source_config in self.config.items():
            if source_config.get("enabled", False):
                if key in source_class_map:
                    try:
                        self.sources[key] = source_class_map[key](source_config)
                    except ValueError:
                        pass
                else:
                    pass

    def retrieve(self, query: str, allowed_sources: List[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves context from all specified and allowed data sources.
        
        Args:
            query (str): The user's query.
            allowed_sources (List[str]): A list of source keys that are
                                         permitted for the current query.
                                         If None, all initialized sources are used.
                                         
        Returns:
            List[Dict[str, Any]]: An aggregated list of context chunks from all queried sources.
        """
        all_chunks = []
        
        sources_to_query = self.sources
        if allowed_sources is not None:
            sources_to_query = {key: self.sources[key] for key in allowed_sources if key in self.sources}

        for source_name, source_instance in sources_to_query.items():
            try:
                chunks = source_instance.retrieve(query)
                all_chunks.extend(chunks)
            except Exception:
                pass

        return all_chunks