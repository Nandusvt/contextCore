
import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.main_context import ContextEngineer
from src.services.openai_service import OpenAIService
from src.services.conversation_memory import ConversationMemory

def main():
    parser = argparse.ArgumentParser(description="Intelligent Context Engineering CLI")
    parser.add_argument('-r', '--role', type=str, required=True, help='User role (e.g., engineer, product_manager, guest)')
    parser.add_argument('-q', '--query', type=str, required=True, help='Query string for context retrieval')
    parser.add_argument('--config', type=str, default='config/context_config.yaml', help='Path to context config YAML')
    parser.add_argument('--roles', type=str, default='config/user_roles.yaml', help='Path to user roles YAML')
    args = parser.parse_args()

    # Step 1: Aggregate context from all sources using ContextEngineer
    engineer = ContextEngineer(config_path=args.config, roles_path=args.roles)
    context_chunks = engineer.build_context(args.query, user_role=args.role)


    memory = ConversationMemory()
    recent_history = [item for item in memory.get_recent_history() if item['role'] == args.role]

    # For Guest role, filter out memory entries that mention restricted/internal content
    if args.role.lower() == "guest":
        restricted_keywords = [
            "quantumleap", "engineer", "database schema", "backend", "jwt", "oauth2", "refactor", "architecture"
        ]
        def is_public(entry):
            text = f"{entry['query']} {entry['response']}".lower()
            return not any(keyword in text for keyword in restricted_keywords)
        recent_history = [item for item in recent_history if is_public(item)]

    history_str = "\n".join([
        f"Role: {item['role']}\nQuery: {item['query']}\nResponse: {item['response']}" for item in recent_history
    ])

    openai_service = OpenAIService()
    full_context = f"Recent Conversation History:\n{history_str}\n\nCurrent Context:\n{context_chunks}"

    # If Guest and query asks for 'single word', force a one-word answer
    if args.role.lower() == "guest" and "single word" in args.query.lower():
        result = openai_service.semantic_search(
            args.query + " (Respond with only a single word, no explanation.)",
            context=full_context
        )
        # Post-process to ensure only a single word is output
        result = result.strip().split()[0] if result.strip() else ""
    else:
        result = openai_service.semantic_search(args.query, context=full_context)
    print(result)
    memory.add_interaction(args.role, args.query, result)

if __name__ == "__main__":
    main()
