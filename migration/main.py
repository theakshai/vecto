import yaml
import os
from pathlib import Path
import tempfile
import shutil
import json # Import json module

from utils.config import parse as parse_config
from utils.vcs.factory import VCSFactory
from utils.shell import run_command

def migration():
    '''
    Migrate repositories from one repo to another repo from once vcs to another vcs. It will decide the src and dest repo from the config.yml and do the migration. The main use of this ditincition is to perform the different auth to clone the repos

    Input: config.yml, and repo_maps.json

    Output: State of the migration either True / False
    '''
    print("Starting migration process...")
    config = parse_config()
    if not config:
        print("Error: Invalid or missing configuration. Aborting migration.")
        return False

    map_file_path = config.get("repos", {}).get("map")
    if not map_file_path or not Path(map_file_path).exists():
        print(f"Error: Repository map file '{map_file_path}' not found. Aborting.")
        return False

    with open(map_file_path, 'r') as f:
        repo_map = json.load(f) # Use json.load

    if not repo_map:
        print("Repository map is empty. Nothing to migrate.")
        return True

    src_vcs = VCSFactory.get_vcs(config['src']['vcs'], config['src'].get('config', {}))
    dest_vcs = VCSFactory.get_vcs(config['dest']['vcs'], config['dest'].get('config', {}))
    
    src_auth = config['src'].get('auth', 'pat') # Default to pat if not specified
    dest_auth = config['dest'].get('auth', 'pat')

    overall_success = True
    work_dir = tempfile.mkdtemp(prefix="vecto-migration-")
    print(f"Created temporary working directory: {work_dir}")

    # The repo_map is now a list of dictionaries
    for repo_entry in repo_map:
        src_repo = repo_entry.get('src_repo')
        src_project = repo_entry.get('src_project')
        dest_repo = repo_entry.get('dest_repo')
        dest_project = repo_entry.get('dest_project')

        if not all([src_repo, src_project, dest_repo, dest_project]):
            print(f"ERROR: Invalid repo map entry: {repo_entry}. Skipping.")
            overall_success = False
            continue

        print(f"\n--- Migrating '{src_repo}' (Project: {src_project}) to '{dest_repo}' (Project: {dest_project}) ---")
        try:
            # 1. Create destination repo
            if not dest_vcs.create_repo(dest_repo, dest_project):
                raise Exception(f"Failed to create destination repo '{dest_repo}' in project '{dest_project}'.")

            # 2. Clone source repo
            src_clone_url = src_vcs.get_clone_url(src_repo, src_auth, src_project)
            repo_local_path = Path(work_dir) / src_repo
            
            clone_cmd = f"git clone --mirror {src_clone_url} {repo_local_path}"
            run_command(clone_cmd, f"Cloning source repository '{src_repo}'.")

            # 3. Set new remote and push
            dest_push_url = dest_vcs.get_clone_url(dest_repo, dest_auth, dest_project)
            
            remote_cmd = f"git -C {repo_local_path} remote set-url origin {dest_push_url}"
            run_command(remote_cmd, f"Setting new remote URL for '{src_repo}'.")

            push_cmd = f"git -C {repo_local_path} push --mirror"
            run_command(push_cmd, f"Pushing '{src_repo}' to destination.")
            
            print(f"SUCCESS: Migrated '{src_repo}' (Project: {src_project}) to '{dest_repo}' (Project: {dest_project}).")

        except Exception as e:
            print(f"ERROR: Failed to migrate '{src_repo}' (Project: {src_project}): {e}")
            overall_success = False

    # Cleanup
    print("Cleaning up temporary directory...")
    shutil.rmtree(work_dir)

    return overall_success
