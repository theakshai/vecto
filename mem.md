## Current State of Work: `mem.md`

### Work Completed:

1.  **Config Parser & Validator (`utils/config.py`):**
    *   Implemented `validate()` and `parse()` functions.
    *   Validation for `src` and `dest` VCS, authentication methods (`ssh`, `pat`), `pipeline`, and `get_inventory`.
    *   Mandatory `config` block for both `src` and `dest`.
    *   Azure DevOps-specific validation for `org_url` (must contain `dev.azure.com`).
    *   Removed `project` key validation from `config.yml` (now expected in `repos_map.json`).
    *   Removed `ssh_key_path` validation and related logic.
    *   Removed `default_src_project_for_map` and `default_dest_project_for_map` validation.

2.  **VCS Abstraction (`utils/vcs/`):**
    *   Defined `BaseVCS` with abstract methods: `get_inventory(project)`, `get_clone_url(repo_name, auth_method, project)`, `create_repo(repo_name, project)`.
    *   Implemented `AzureDevOpsVCS` and `GitHubVCS` (mocked API calls, but functional logic).
    *   `VCSFactory` to instantiate correct VCS client.

3.  **Mapper (`utils/mapper.py`):**
    *   Modified `generate_repo_map` to output `repos_map.json` in the new `list[dict]` format: `{"src_repo": "...", "src_project": "...", "dest_repo": "...", "dest_project": "..."}`.
    *   Requires `src_project_for_inventory` as an argument for discovery.

4.  **Shell Command Runner (`utils/shell.py`):**
    *   Implemented a real `subprocess`-based `run_command` function.

5.  **Migration Logic (`migration/main.py`):**
    *   Implemented `migration()` function to read `config.yml` and `repos_map.json`.
    *   Iterates through `repos_map.json` (list of dicts).
    *   Calls VCS-specific methods (`create_repo`, `get_clone_url`) using `src_project` and `dest_project` from the map entry.
    *   Simulates `git clone`, `git remote set-url`, `git push --mirror` using `run_command`.

6.  **Main Application (`main.py`):**
    *   Loads `config.yml`.
    *   **Currently assumes `repos_map.json` is user-provided (map generation logic removed).**
    *   Calls `migration()`.

7.  **Configuration File (`utils/config.yml`):**
    *   Updated to reflect current schema, pointing to `repos_map.json`.
    *   `get_inventory` is `true` for src.

8.  **Test Suite (`tests/test_config.py`, `tests/test_mapper.py`):**
    *   Extensive unit tests covering `config.py` validation.
    *   `test_mapper.py` for map generation logic.

### Current Outstanding Issue:

*   **`Error: Invalid or missing configuration.`**
    *   This error persists when running `uv run python main.py`, indicating that the `validate()` function in `utils/config.py` is still returning `False`.
    *   Previous debugging attempts for `repos.map` revealed `{'map': None}` from `yaml.safe_load`, but recreating `config.yml` did not resolve it.
    *   The latest `validate()` function removed debug prints and should be failing at a specific `return False` within its logic.

### Next Steps to Resolve Outstanding Issue:

1.  **Add granular debug prints back to `utils/config.py`'s `validate()` function.** Specifically, add a `print()` statement *before every `return False`* in the `validate()` function.
2.  **Run `uv run python main.py` again.**
3.  **Analyze the debug output** to pinpoint the exact validation check that is failing.
4.  **Based on the identified failure point:**
    *   Correct the `config.yml` if it's found to be genuinely invalid for that rule.
    *   Adjust the validation logic in `utils/config.py` if the rule itself is incorrect or too strict for the intended schema.
