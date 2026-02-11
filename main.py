from utils import config
from migration.main import migration
import sys

def main():
    print("Vecto - VCS Migration Tool")
    
    # 1. Parse Config
    conf = config.parse()
    if not conf:
        print("Error: Invalid or missing configuration.")
        sys.exit(1)
        
    print(f"Loaded configuration for migration from {conf['src']['vcs']} to {conf['dest']['vcs']}")
    
    # 2. Skip Map Generation - Assume repos_map.json is provided by user
    print("Assuming repos_map.json is provided by the user.")

    # 3. Perform Migration
    migration_success = migration()

    if migration_success:
        print("\nMigration process completed successfully.")
    else:
        print("\nMigration process completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
