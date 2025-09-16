from typing import List, Dict, Any

class RoleHandler:
    """
    Manages user roles and applies personalization rules to the context.
    """

    def __init__(self, roles_config: Dict[str, Any]):
        """
        Initializes the RoleHandler with role definitions.
        
        Args:
            roles_config (Dict[str, Any]): The loaded user roles configuration.
        """
        self.roles = roles_config.get("roles", {})

    def get_permissions(self, role: str) -> Dict[str, Any]:
        """
        Retrieves the permission set for a given role.
        
        Args:
            role (str): The name of the role (e.g., 'engineer').
            
        Returns:
            Dict[str, Any]: The permissions dictionary for that role.
            
        Raises:
            ValueError: If the role is not defined in the configuration.
        """
        if role not in self.roles:
            raise ValueError(f"Role '{role}' is not defined in user_roles.yaml.")
        return self.roles[role].get("permissions", {})

    def filter_context_by_role(self, chunks: List[Dict[str, Any]], role: str) -> List[Dict[str, Any]]:
        """
        Filters a list of context chunks based on the user's role permissions.
        This implementation filters based on tags.
        
        Args:
            chunks (List[Dict[str, Any]]): The list of context chunks.
            role (str): The user's role.
            
        Returns:
            List[Dict[str, Any]]: A filtered list of chunks the user is allowed to see.
        """
        try:
            permissions = self.get_permissions(role)
        except ValueError:
            return [] # Return empty if role is invalid

        allowed_tags = set(permissions.get("filter_by_tags", []))
        if not allowed_tags:
            return chunks # If no tags are specified, allow all

        permitted_chunks = []
        for chunk in chunks:
            chunk_tags = set(chunk.get("metadata", {}).get("tags", []))
            # If a chunk has no tags, or if its tags intersect with allowed tags, permit it.
            if not chunk_tags or chunk_tags.intersection(allowed_tags):
                permitted_chunks.append(chunk)
                
        return permitted_chunks
