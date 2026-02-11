'''
The supported schema for the config.yml

src:
    vcs: 
        - Name of the source VCS. 
        - allowed_values: AzureDevops, Github, Gitlab, Bitbucket, SVN
        config:
            - specific configuration for the vcs
    auth: 
        - authentication method to get the repositories from the VCS
        - allowed_values: ssh
    pipeline: 
        - do we need to migrate the pipelines? this involves change the pipeline config based on the vcs. Default to False
        - allowed_values: True, False
    get_inventory: 
        - does this tool get the available repositories form the vcs. Default to False
        - allowed_values: True, False
dest:
    vcs: 
        - Name of the destination VCS. 
        - values: AzureDevops, Github, Gitlab, Bitbucket, SVN
        config:
            - specific configuration for the vcs
    auth: 
        - authentication method to get the repositories from the VCS
        - allowed_values: ssh
repos:
    map: 
        - points to a file, which has the map between source and dest repos
'''
import yaml
from pathlib import Path
from typing import Optional, Dict, Any


def _get_config_path() -> Optional[Path]:
    '''Find the config.yml file in the current directory or utils directory.'''
    search_paths = [
        Path("config.yml"),
        Path("utils/config.yml"),
        Path(__file__).parent / "config.yml"
    ]
    for path in search_paths:
        if path.exists():
            return path
    return None


def validate() -> bool:
    '''
    Validate the config.yml to the schema above

    Input: auto find the config.yml file in the current directory or find the config.yml file to the directory it points

    Output: True or False
    '''
    config_path = _get_config_path()
    if not config_path:
        print("DEBUG: Validation failed at config_path not found.")
        return False

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"DEBUG: Validation failed at YAML loading: {e}")
        return False

    if not config or not isinstance(config, dict):
        print("DEBUG: Validation failed at config empty or not dict.")
        return False

    allowed_vcs = {"AzureDevops", "AzureDevOps", "Github", "Gitlab", "Bitbucket", "SVN"}
    allowed_auth = {"ssh", "pat"}

    # Validate src
    src = config.get('src')
    if not isinstance(src, dict):
        print("DEBUG: Validation failed at src not dict.")
        return False
    
    # config block is mandatory
    src_config = src.get('config')
    if not isinstance(src_config, dict):
        print("DEBUG: Validation failed at src.config not dict.")
        return False
    
    if src.get('vcs') not in allowed_vcs:
        print(f"DEBUG: Validation failed at src.vcs invalid: {src.get('vcs')}.")
        return False

    if 'auth' in src and src['auth'] not in allowed_auth:
        print(f"DEBUG: Validation failed at src.auth invalid: {src.get('auth')}.")
        return False

    if 'pipeline' in src and not isinstance(src['pipeline'], bool):
        print("DEBUG: Validation failed at src.pipeline not bool.")
        return False

    get_inventory = src.get('get_inventory', False)
    if not isinstance(get_inventory, bool): # Ensure get_inventory is boolean
        print("DEBUG: Validation failed at src.get_inventory not bool.")
        return False

    # default_src_project_for_map is NOT mandatory

    if src.get('vcs') in ["AzureDevops", "AzureDevOps"]:
        if not _validate_azure_config(src):
            print("DEBUG: Validation failed at Azure specific src config.")
            return False

    # Validate dest
    dest = config.get('dest')
    if not isinstance(dest, dict):
        print("DEBUG: Validation failed at dest not dict.")
        return False

    # config block is mandatory
    dest_config = dest.get('config')
    if not isinstance(dest_config, dict):
        print("DEBUG: Validation failed at dest.config not dict.")
        return False

    if dest.get('vcs') not in allowed_vcs:
        print(f"DEBUG: Validation failed at dest.vcs invalid: {dest.get('vcs')}.")
        return False

    if 'auth' in dest and dest['auth'] not in allowed_auth:
        print(f"DEBUG: Validation failed at dest.auth invalid: {dest.get('auth')}.")
        return False
    
    # default_dest_project_for_map is NOT mandatory

    if dest.get('vcs') in ["AzureDevops", "AzureDevOps"]:
        if not _validate_azure_config(dest):
            print("DEBUG: Validation failed at Azure specific dest config.")
            return False

    # Validate repos
    repos = config.get('repos')
    if not isinstance(repos, dict) or 'map' not in repos or not isinstance(repos['map'], str):
        print("DEBUG: Validation failed at repos section structure or map key.")
        return False

    return True


def _validate_azure_config(section_config: Dict[str, Any]) -> bool:
    """Helper to validate Azure DevOps specific configuration."""
    conf = section_config.get('config')
    if not isinstance(conf, dict): # This check is now redundant due to earlier validation, but safe.
        return False
    
    org_url = conf.get('org_url')
    if not org_url or not isinstance(org_url, str):
        return False
    
    if "dev.azure.com" not in org_url:
        return False
        
    return True

def parse() -> dict:
    '''
    Parse the config.yml file and get the values

    Input: auto find the config.yml file in the current directory or find the config.yml file to the directory it points

    Output: dict of values 
    '''
    if not validate():
        return {}

    config_path = _get_config_path()
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}

    # Set defaults as specified in the schema
    if 'src' in config:
        if 'pipeline' not in config['src']:
            config['src']['pipeline'] = False
        if 'get_inventory' not in config['src']:
            config['src']['get_inventory'] = False

    return config
