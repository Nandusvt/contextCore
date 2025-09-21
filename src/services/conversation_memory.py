import json
import os
from typing import List, Dict

class ConversationMemory:
    def __init__(self, memory_file: str = "conversation_memory.json", max_history: int = 10):
        self.memory_file = memory_file
        self.max_history = max_history
        self.history = self._load_memory()

    def _load_memory(self) -> List[Dict]:
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except Exception:
                    return []
        return []

    def add_interaction(self, role: str, query: str, response: str):
        self.history.append({
            "role": role,
            "query": query,
            "response": response
        })
        # Keep only the most recent max_history items
        self.history = self.history[-self.max_history:]
        self._save_memory()

    def get_recent_history(self) -> List[Dict]:
        return self.history[-self.max_history:]

    def _save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)
