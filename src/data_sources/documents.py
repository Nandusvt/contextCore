#path: src/data_sources/documents.py

import json
import os
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
        """Loads document data from JSON or plain text files."""
        self.data = []
        if not os.path.exists(self.docs_path):
            return

        # If file has .txt extension or JSON parsing fails, treat as plain text
        _, ext = os.path.splitext(self.docs_path)
        ext = (ext or '').lower()
        if ext == '.txt':
            # Try multiple encodings for robustness
            texts = []
            for enc in ('utf-8', 'utf-8-sig', 'latin-1'):
                try:
                    with open(self.docs_path, 'r', encoding=enc) as f:
                        texts.append(f.read())
                        break
                except Exception:
                    continue
            text = next((t for t in texts if isinstance(t, str)), '')
            # Create a single document entry; chunk later in retrieve or pre-split here
            self.data = [{
                'id': os.path.basename(self.docs_path),
                'title': os.path.basename(self.docs_path),
                'chunks': self._chunk_text(text),
                'tags': ['public']
            }]
            return

        # Try JSON load
        try:
            with open(self.docs_path, 'r', encoding='utf-8-sig') as f:
                self.data = json.load(f)
            if isinstance(self.data, dict) and 'documents' in self.data:
                self.data = self.data['documents']
        except json.JSONDecodeError:
            # Fallback: treat file as plain text
            # Fallback to reading as text with encoding fallbacks
            texts = []
            for enc in ('utf-8', 'utf-8-sig', 'latin-1'):
                try:
                    with open(self.docs_path, 'r', encoding=enc) as f:
                        texts.append(f.read())
                        break
                except Exception:
                    continue
            text = next((t for t in texts if isinstance(t, str)), '')
            self.data = [{
                'id': os.path.basename(self.docs_path),
                'title': os.path.basename(self.docs_path),
                'chunks': self._chunk_text(text),
                'tags': ['public']
            }]
        except FileNotFoundError:
            self.data = []

    def _chunk_text(self, text: str, max_chars: int = 800) -> List[str]:
        """Naive chunking by paragraphs/sentences into ~max_chars chunks."""
        if not isinstance(text, str) or not text.strip():
            return []
        # Split on double newlines first, then fallback to single newline; then by sentences.
        parts = [p.strip() for p in text.replace('\r\n', '\n').split('\n\n') if p.strip()]
        if not parts:
            parts = [p.strip() for p in text.split('\n') if p.strip()]
        if not parts:
            parts = [text.strip()]

        chunks: List[str] = []
        buf = ''
        for p in parts:
            # Further split paragraphs by sentences to keep chunks more balanced
            sentences = [s.strip() for s in p.replace('! ', '!\n').replace('? ', '?\n').replace('. ', '.\n').split('\n') if s.strip()]
            for s in sentences:
                if len(buf) + len(s) + 1 <= max_chars:
                    buf = (buf + ' ' + s).strip() if buf else s
                else:
                    if buf:
                        chunks.append(buf)
                    buf = s
        if buf:
            chunks.append(buf)
        return chunks

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

        # If no matches found, return up to first 3 chunks as a fallback to indicate data is loaded
        if not relevant_chunks:
            preview = []
            for doc in self.data:
                doc_title = doc.get('title', '')
                for i, chunk_content in enumerate(doc.get('chunks', [])[:3]):
                    chunk_id = f"{doc.get('id')}_chunk{i}"
                    content = f"From Document '{doc_title}': {chunk_content}"
                    metadata = {
                        "type": "document_chunk",
                        "document_id": doc.get("id"),
                        "document_title": doc_title,
                        "tags": doc.get("tags", []),
                        "note": "fallback_preview"
                    }
                    preview.append(self._format_chunk(id=chunk_id, content=content, metadata=metadata))
                    if len(preview) >= 3:
                        break
                if len(preview) >= 3:
                    break
            return preview

        return relevant_chunks

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        """Return all document chunks without filtering by query."""
        all_chunks: List[Dict[str, Any]] = []
        for doc in self.data:
            doc_title = doc.get('title', '')
            for i, chunk_content in enumerate(doc.get('chunks', []) or []):
                chunk_id = f"{doc.get('id')}_chunk{i}"
                content = f"From Document '{doc_title}': {chunk_content}"
                metadata = {
                    "type": "document_chunk",
                    "document_id": doc.get("id"),
                    "document_title": doc_title,
                    "tags": doc.get("tags", []),
                }
                all_chunks.append(self._format_chunk(id=chunk_id, content=content, metadata=metadata))
        return all_chunks

    def get_raw_text(self) -> str:
        """Concatenate all chunk texts into a single string for simple local extraction."""
        parts: List[str] = []
        for doc in self.data:
            for chunk_content in (doc.get('chunks', []) or []):
                if isinstance(chunk_content, str):
                    parts.append(chunk_content)
        return "\n".join(parts)
