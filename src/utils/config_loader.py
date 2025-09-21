import yaml
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
