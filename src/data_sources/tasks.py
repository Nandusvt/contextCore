 #path: src/data_sources/tasks.py

import json
from typing import List, Dict, Any
from .base import BaseContextSource

class TaskContextSource(BaseContextSource):
    """
    Retrieves context from a JSON file representing tasks or tickets.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.source_id = "tasks"
        self.tasks_path = config.get("path")
        if not self.tasks_path:
            raise ValueError("Path for tasks data source is not specified in config.")
        self._load_data()

    def _load_data(self):
        """Loads task data from the JSON file."""
        try:
            with open(self.tasks_path, 'r', encoding='utf-8-sig') as f:
                self.data = json.load(f)
            # If data is a dict with 'tasks' key, use that
            if isinstance(self.data, dict) and 'tasks' in self.data:
                self.data = self.data['tasks']
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError as e:
            self.data = []

    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieves tasks that match keywords in the query.
        A simple keyword match is used for this example.
        """
        query_terms = set(query.lower().split())
        relevant_chunks = []

        for task in self.data:
            content = f"Task: {task.get('title', '')}. Status: {task.get('status', '')}. Description: {task.get('description', '')}"
            content_terms = set(content.lower().split())
            
            # Check for keyword overlap
            if query_terms.intersection(content_terms):
                metadata = {
                    "type": "task",
                    "project": task.get("project"),
                    "assignee": task.get("assignee"),
                    "tags": task.get("tags", []),
                    "original_title": task.get('title')
                }
                formatted_chunk = self._format_chunk(
                    id=task.get("id"),
                    content=content,
                    metadata=metadata
                )
                relevant_chunks.append(formatted_chunk)
        
        return relevant_chunks
