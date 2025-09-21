import yaml
import os
from typing import Dict, Any

def load_config(path: str) -> Dict[str, Any]:
    """
    Loads the main system configuration from a YAML file.
    
    Args:
        path (str): The path to the context_config.yaml file.
        
    Returns:
        Dict[str, Any]: The loaded configuration as a dictionary.
    """
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

            # Optional: allow overriding data source paths via environment variables
            # Useful for pointing 'documents' at a custom file without editing YAML
            ds = config.get("data_sources", {}) or {}
            # Documents override
            docs_path = os.environ.get("CONTEXTCORE_DOCS_PATH")
            if docs_path and "documents" in ds:
                ds["documents"]["path"] = docs_path
            # Tasks override (optional)
            tasks_path = os.environ.get("CONTEXTCORE_TASKS_PATH")
            if tasks_path and "tasks" in ds:
                ds["tasks"]["path"] = tasks_path
            # Graphiti override (optional)
            graph_path = os.environ.get("CONTEXTCORE_GRAPH_PATH")
            if graph_path and "graphiti" in ds:
                ds["graphiti"]["path"] = graph_path

            # Optional: allow persistent local overrides via config/local_overrides.yaml
            try:
                overrides_path = os.path.join(os.path.dirname(path), "local_overrides.yaml")
                if os.path.exists(overrides_path):
                    with open(overrides_path, 'r') as lf:
                        local_overrides = yaml.safe_load(lf) or {}
                        lods = local_overrides.get("data_sources", {}) or {}
                        for key in ("documents", "tasks", "graphiti"):
                            if key in lods and isinstance(lods[key], dict) and lods[key].get("path"):
                                ds.setdefault(key, {})
                                ds[key]["path"] = lods[key]["path"]
            except Exception:
                # ignore local override load errors silently
                pass

            config["data_sources"] = ds
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file at {path}: {e}")
        return {}

def load_user_roles(path: str) -> Dict[str, Any]:
    """
    Loads the user role definitions from a YAML file.
    
    Args:
        path (str): The path to the user_roles.yaml file.
        
    Returns:
        Dict[str, Any]: The loaded roles as a dictionary.
    """
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: User roles file not found at {path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file at {path}: {e}")
        return {}
