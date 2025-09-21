import openai
import os

class OpenAIService:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        # Hardcoded API key for quick testing (not recommended for production)
        self.api_key = "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"
        self.model = model
        openai.api_key = self.api_key

    def semantic_search(self, query: str, context: str = "") -> str:
        """
        Use OpenAI's chat completion to perform semantic search or summarization (openai>=1.0.0).
        Returns the model's response as a string.
        """
        prompt = f"""
        You are an intelligent context engine. Given the following query and context, return the most relevant information or summary for the query.
        Query: {query}
        Context: {context}
        """
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
