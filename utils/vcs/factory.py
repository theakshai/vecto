from typing import Dict, Any, Type
from .base import BaseVCS
from .azure_devops import AzureDevOpsVCS
from .github import GitHubVCS

class VCSFactory:
    _registry = {
        "AzureDevOps": AzureDevOpsVCS,
        "AzureDevops": AzureDevOpsVCS,
        "Github": GitHubVCS,
    }

    @staticmethod
    def get_vcs(name: str, config: Dict[str, Any] = {}) -> BaseVCS:
        vcs_class = VCSFactory._registry.get(name)
        if not vcs_class:
            raise ValueError(f"Unsupported VCS: {name}. Supported: {list(VCSFactory._registry.keys())}")
        return vcs_class(config)
