from abc import ABC, abstractmethod
from typing import List, Optional

class BaseVCS(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def get_inventory(self, project: str) -> List[str]:
        """
        Get the list of available repositories from a specific project.
        
        Args:
            project (str): The project name to get the inventory from.

        Returns:
            List[str]: A list of repository names/identifiers.
        """
        pass

    @abstractmethod
    def get_clone_url(self, repo_name: str, auth_method: str, project: str) -> str:
        """
        Construct the clone URL for a repository in a specific project.

        Args:
            repo_name (str): The name of the repository.
            auth_method (str): The authentication method ('ssh' or 'pat').
            project (str): The project name the repository belongs to.

        Returns:
            str: The full clone URL.
        """
        pass

    @abstractmethod
    def create_repo(self, repo_name: str, project: str) -> bool:
        """
        Create a new repository in the VCS within a specific project.

        Args:
            repo_name (str): The name of the repository to create.
            project (str): The project name to create the repository in.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        pass
