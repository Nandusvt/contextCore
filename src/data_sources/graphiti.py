# path: src/data_sources/graphiti.py

import json
from typing import List, Dict, Any
from .base import BaseContextSource

class GraphitiContextSource(BaseContextSource):
    """
    Retrieves context from a JSON file representing a simple knowledge graph.
    The graph connects different entities (tasks, documents, etc.).
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.source_id = "graphiti"
        self.graph_path = config.get("path")
        if not self.graph_path:
            raise ValueError("Path for graphiti data source is not specified in config.")
        self._load_data()

    def _load_data(self):
        """Loads graph data from the JSON file."""
        try:
            with open(self.graph_path, 'r', encoding='utf-8-sig') as f:
                self.data = json.load(f)
            # If data is a dict with 'graphiti' key, use that
            if isinstance(self.data, dict) and 'graphiti' in self.data:
                self.data = self.data['graphiti']
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError as e:
            self.data = []

    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieves graph connections where a node's name matches the query.
        """
        query_lower = query.lower()
        relevant_chunks = []

        for connection in self.data:
            source_name = connection.get("source", {}).get("name", "").lower()
            target_name = connection.get("target", {}).get("name", "").lower()

            if query_lower in source_name or query_lower in target_name or any(term in source_name or term in target_name for term in query.lower().split()):
                content = (
                    f"Knowledge Graph Connection: "
                    f"Entity '{connection.get('source', {}).get('name')}' ({connection.get('source', {}).get('type')}) "
                    f"is '{connection.get('relationship')}' "
                    f"Entity '{connection.get('target', {}).get('name')}' ({connection.get('target', {}).get('type')})."
                )
                metadata = {
                    "type": "graph_connection",
                    "relationship": connection.get("relationship"),
                    "tags": connection.get("tags", []),
                }
                formatted_chunk = self._format_chunk(
                    id=connection.get("id"),
                    content=content,
                    metadata=metadata
                )
                relevant_chunks.append(formatted_chunk)

        return relevant_chunks
