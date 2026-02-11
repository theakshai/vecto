import pytest
import yaml
import os
from pathlib import Path
from utils import config
from utils.config import validate, parse

@pytest.fixture
def mock_config_path(tmp_path):
    config_file = tmp_path / "config.yml"
    def _mock():
        if config_file.exists():
            return config_file
        return None
    return _mock

def test_validate_valid_config(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "auth": "ssh",
            "pipeline": True,
            "get_inventory": True, # set to true for this test
            "config": {
                "org_url": "https://dev.azure.com/myorg",
                "default_src_project_for_map": "my-ado-project" # Optional now
            }
        },
        "dest": {
            "vcs": "Github",
            "auth": "ssh",
            "config": { # Mandatory but can be empty or have other keys
                "example_key": "example_value",
                "default_dest_project_for_map": "my-gh-project" # Optional now
            }
        },
        "repos": {
            "map": "repos_map.json"
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is True

def test_validate_minimal_config(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {
                "org_url": "https://dev.azure.com/myorg",
            }
        },
        "dest": {
            "vcs": "Github",
            "config": {} # Mandatory but can be empty
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is True

def test_validate_missing_config_block(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps", # Missing config block
        },
        "dest": {
            "vcs": "Github",
            "config": {}
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

# Removed test_validate_missing_default_src_project_for_map
# Removed test_validate_missing_default_dest_project_for_map

def test_validate_invalid_vcs(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {"vcs": "InvalidVCS", "config": {}},
        "dest": {"vcs": "Github", "config": {}}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is False

def test_validate_invalid_auth(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {"vcs": "AzureDevOps", "auth": "password", "config": {"org_url": "https://dev.azure.com/myorg"}},
        "dest": {"vcs": "Github", "config": {}}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is False

def test_validate_missing_file(tmp_path, monkeypatch, mock_config_path):
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

def test_validate_azure_config_valid(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {
                "org_url": "https://dev.azure.com/myorg",
            }
        },
        "dest": {
            "vcs": "Github",
            "config": {}
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is True

def test_validate_azure_config_missing_url(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {}
        },
        "dest": {
            "vcs": "Github",
            "config": {}
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

def test_validate_azure_config_invalid_url(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {
                "org_url": "https://visualstudio.com/myorg",
            }
        },
        "dest": {
            "vcs": "Github",
            "config": {}
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

def test_validate_dest_azure_invalid(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "Github",
            "config": {}
        },
        "dest": {
            "vcs": "AzureDevOps",
            "config": {} # Missing org_url
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

def test_validate_github_with_config(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {
                "org_url": "https://dev.azure.com/myorg",
                }
        },
        "dest": {
            "vcs": "Github",
            "config": {
                "some_other_key": "value"
            } # Should be valid
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is True

def test_validate_pat_auth(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "Github",
            "auth": "pat",
            "config": {}
        },
        "dest": {
            "vcs": "Github",
            "auth": "pat",
            "config": {}
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is True

def test_parse_invalid_returns_empty(tmp_path, monkeypatch, mock_config_path):
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert parse() == {}

# Test case for a non-Azure VCS with mandatory but empty config
def test_validate_github_mandatory_empty_config(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "Github",
            "config": {}
        },
        "dest": {
            "vcs": "Github",
            "config": {}
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is True
