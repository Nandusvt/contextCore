#path: src/data_sources/documents.py

import json
from typing import List, Dict, Any
from .base import BaseContextSource

class DocumentContextSource(BaseContextSource):
    """
    Retrieves context from a JSON file containing documents.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.source_id = "documents"
        self.docs_path = config.get("path")
        if not self.docs_path:
            raise ValueError("Path for documents data source is not specified in config.")
        self._load_data()

    def _load_data(self):
        """Loads document data from the JSON file."""
        try:
            with open(self.docs_path, 'r', encoding='utf-8-sig') as f:
                self.data = json.load(f)
            # If data is a dict with 'documents' key, use that
            if isinstance(self.data, dict) and 'documents' in self.data:
                self.data = self.data['documents']
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError as e:
            self.data = []

    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieves document chunks where content or title matches the query.
        """
        query_terms = set(query.lower().split())
        relevant_chunks = []

        for doc in self.data:
            doc_title = doc.get('title', '')
            for i, chunk_content in enumerate(doc.get('chunks', [])):
                content_to_search = f"{doc_title} {chunk_content}"
                content_terms = set(content_to_search.lower().split())

                if query_terms.intersection(content_terms):
                    chunk_id = f"{doc.get('id')}_chunk{i}"
                    content = f"From Document '{doc_title}': {chunk_content}"
                    metadata = {
                        "type": "document_chunk",
                        "document_id": doc.get("id"),
                        "document_title": doc_title,
                        "tags": doc.get("tags", []),
                    }
                    formatted_chunk = self._format_chunk(
                        id=chunk_id,
                        content=content,
                        metadata=metadata
                    )
                    relevant_chunks.append(formatted_chunk)

        return relevant_chunks
