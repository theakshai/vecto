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
            "get_inventory": False
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
    assert parsed["dest"]["vcs"] == "Github"

def test_validate_minimal_config(tmp_path, monkeypatch, mock_config_path):
    config_data = {
        "src": {"vcs": "AzureDevOps"},
        "dest": {"vcs": "Github"}
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    
    assert validate() is True
    parsed = parse()
    assert parsed["src"]["vcs"] == "AzureDevOps"
    assert parsed["src"]["pipeline"] is False
    assert parsed["src"]["get_inventory"] is False

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

def test_parse_invalid_returns_empty(tmp_path, monkeypatch, mock_config_path):
    monkeypatch.setattr(config, "_get_config_path", mock_config_path)
    assert parse() == {}
