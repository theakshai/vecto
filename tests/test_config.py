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
            "get_inventory": False,
            "config": {
                "org_url": "https://dev.azure.com/myorg"
            }
        },
        "dest": {
            "vcs": "Github",
            "auth": "ssh"
        },
        "repos": {
            "map": "repos_map.yml"
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is True
    parsed = parse()
    assert parsed["src"]["vcs"] == "AzureDevOps"
    assert parsed["src"]["pipeline"] is True
    assert parsed["src"]["get_inventory"] is False

def test_validate_minimal_config(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {
                "org_url": "https://dev.azure.com/myorg"
            }
        },
        "dest": {"vcs": "Github"}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is True

def test_validate_invalid_vcs(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {"vcs": "InvalidVCS"},
        "dest": {"vcs": "Github"}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is False

def test_validate_invalid_auth(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {"vcs": "AzureDevOps", "auth": "password"},
        "dest": {"vcs": "Github"}
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
            "config": {"org_url": "https://dev.azure.com/myorg"}
        },
        "dest": {"vcs": "Github"}
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
        "dest": {"vcs": "Github"}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

def test_validate_azure_config_invalid_url(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "AzureDevOps",
            "config": {"org_url": "https://visualstudio.com/myorg"}
        },
        "dest": {"vcs": "Github"}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is False

def test_validate_dest_azure_invalid(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {
            "vcs": "Github",
            "auth": "ssh"
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
            "config": {"org_url": "https://dev.azure.com/myorg"}
        },
        "dest": {
            "vcs": "Github",
            "config": {"some_other_key": "value"} # Should be valid
        }
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert validate() is True

def test_parse_invalid_returns_empty(tmp_path, monkeypatch, mock_config_path):
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert parse() == {}
