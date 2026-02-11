import os
import requests
from typing import List
from .base import BaseVCS

class GitHubVCS(BaseVCS):
    def get_inventory(self, project: str) -> List[str]:
        # For GitHub, 'project' is often the organization name
        # In a real scenario, this would use API calls to list repos within the organization/user.
        return [f"{project}-gh-repo-1", f"{project}-gh-repo-2"]

    def get_clone_url(self, repo_name: str, auth_method: str, project: str) -> str:
        # For GitHub, 'project' is the organization or user name
        org_or_user = project 
        if auth_method == "ssh":
            return f"git@github.com:{org_or_user}/{repo_name}.git"
        
        # Default to PAT (or if auth_method == "pat")
        pat = os.environ.get("GITHUB_TOKEN", "") # Get PAT from env var, default to empty string
        # If PAT is empty, git will prompt for credentials.
        if pat:
            return f"https://{pat}@github.com/{org_or_user}/{repo_name}.git"
        else:
            return f"https://github.com/{org_or_user}/{repo_name}.git"

    def create_repo(self, repo_name: str, project: str) -> bool:
        print(f"SIMULATING: Creating GitHub repo '{repo_name}' in project/org '{project}'.")
        return True