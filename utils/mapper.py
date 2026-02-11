import yaml
import json # Import json module
from pathlib import Path
from typing import Dict, Any, List
from utils.vcs.factory import VCSFactory

def generate_repo_map(config: Dict[str, Any], src_project_for_inventory: str):
    """
    Generates a mapping of repositories from source to destination.
    Writes the mapping to the file specified in the config.
    The generated map uses a list of dictionaries format with src_project and dest_project.
    """
    src_config = config.get('src', {})
    repos_config = config.get('repos', {})
    
    map_file_path = repos_config.get('map')
    if not map_file_path:
        print("No repository map file specified in config.")
        return

    # Use a default dest_project for initial map generation, to be edited by user
    default_dest_project = config.get('dest', {}).get('config', {}).get('default_project_for_map', 'my-dest-project')

    repo_map_list: List[Dict[str, str]] = []
    
    # Check if we should inventory the source
    get_inventory = src_config.get('get_inventory', False)
    
    if get_inventory:
        try:
            src_vcs = VCSFactory.get_vcs(src_config['vcs'], src_config.get('config', {}))
            # Pass the project for inventory discovery
            src_repos = src_vcs.get_inventory(src_project_for_inventory) 
            print(f"Discovered {len(src_repos)} repositories from {src_config['vcs']} in project '{src_project_for_inventory}'.")
        except Exception as e:
            print(f"Error getting inventory from {src_config.get('vcs')}: {e}")
            src_repos = [] # Fallback to empty list on error
    else:
        print("Inventory discovery disabled in config. Generating empty map template.")
        # If discovery is disabled, create a template entry
        src_repos = ["example-source-repo"] 

    for repo in src_repos:
        repo_map_list.append({
            "src_repo": repo,
            "src_project": src_project_for_inventory,
            "dest_repo": repo, # Default to same name
            "dest_project": default_dest_project
        })

    # Write to file
    output_path = Path(map_file_path)
    
    # Ensure directory exists
    if output_path.parent != Path('.'):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(repo_map_list, f, indent=2) # Use json.dump
    
    print(f"Repository mapping generated at: {output_path.resolve()}")
