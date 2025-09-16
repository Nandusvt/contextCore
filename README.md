# ContextCore: A Context Engineering System

ContextCore is a modular framework for engineering, retrieving, and optimizing contextual information for large language models (LLMs). It provides a structured way to gather context from multiple heterogeneous data sources, rank it for relevance, manage token budgets, and personalize it based on user roles and permissions.

---

## 🚀 Core Features

- **Multi-Source Retrieval:** Pluggable architecture to fetch context from various sources like task managers, knowledge graphs, and document stores.
- **Context Optimization:** Pipeline to rank, deduplicate, and intelligently truncate context to fit within a specified token budget.
- **Personalization:** Role-based access control and context filtering to ensure users only receive relevant and permitted information.
- **Configuration Driven:** System behavior and user roles are managed via simple YAML configuration files.
- **Testable and Extensible:** Designed with clear abstractions, making it easy to add new data sources and write comprehensive tests.

---

## 🏗️ Project Structure

```
contextcore/
├── README.md
├── requirements.txt
├── config/
│   ├── context_config.yaml
│   └── user_roles.yaml
├── src/
│   ├── main_context.py
│   ├── data_sources/
│   ├── retrieval/
│   ├── optimization/
│   ├── personalization/
│   └── utils/
├── data/
│   ├── mock/
│   └── schemas/
├── tests/
└── examples/
```

---

## ⚡ Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Examples

Explore the `examples/` directory to see how to use the system.

```bash
python examples/basic_usage.py
```
```bash
python examples/role_based_demo.py
```

---

## 🧩 Configuration

- **System config:** `config/context_config.yaml`  
  Controls token limits, optimization, and data source paths.
- **User roles:** `config/user_roles.yaml`  
  Defines roles, permissions, and tag-based filtering.

---

## 📝 How It Works

1. **Load Configs:** Reads YAML config and user roles.
2. **Initialize Data Sources:** Loads mock data from JSON files.
3. **Query:** User provides a query and role.
4. **Retrieve Context:** Fetches relevant items from each enabled data source.
5. **Personalize:** Filters context based on user role and tags.
6. **Optimize:** Ranks, deduplicates, and fits context to a token budget.
7. **Output:** Returns a formatted string with the final, role-personalized context.

---

## 🧪 Testing

Run the test suite with:

```bash
python -m unittest discover tests/
```

---

## 📦 Example Output

When you run `role_based_demo.py`, you’ll see how the same query produces different context for an engineer, product manager, and guest, based on their role and permissions.

---

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 💡 Inspiration

ContextCore is designed to help LLM applications deliver the right information to the right user, every time.

---