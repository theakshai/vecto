import os
import requests
from typing import List
from .base import BaseVCS

class AzureDevOpsVCS(BaseVCS):
    def get_inventory(self, project: str) -> List[str]:
        # In a real scenario, this would use API calls to list repos within the project
        # For now, return mock data.
        return [f"{project}-azure-repo-1", f"{project}-azure-repo-2", f"{project}-azure-repo-3"]

    def get_clone_url(self, repo_name: str, auth_method: str, project: str) -> str:
        org_url = self.config["org_url"]
        
        if auth_method == "ssh":
            # e.g. git@ssh.dev.azure.com:v3/{organization}/{project}/{repository}
            org_name = org_url.split('/')[-1]
            return f"git@ssh.dev.azure.com:v3/{org_name}/{project}/{repo_name}"
        
        # Default to PAT (or if auth_method == "pat")
        pat = os.environ.get("ADO_PAT", "") # Get PAT from env var, default to empty string
        # e.g. https://<PAT>@dev.azure.com/{organization}/{project}/_git/{repository}
        # If PAT is empty, git will prompt for credentials.
        if pat:
             return f"https://{pat}@{org_url.replace('https://', '')}/{project}/_git/{repo_name}"
        else:
             return f"https://{org_url.replace('https://', '')}/{project}/_git/{repo_name}"

    def create_repo(self, repo_name: str, project: str) -> bool:
        print(f"SIMULATING: Creating Azure DevOps repo '{repo_name}' in project '{project}'.")
        return True
