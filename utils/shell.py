import subprocess
import os
from typing import Optional

def run_command(command: str, description: str):
    """
    Runs a shell command and raises an exception on failure.

    Args:
        command (str): The command to execute.
        description (str): A human-readable description for logging.
    
    Returns:
        str: The stdout from the command.
    """
    print(f"Executing: {description}...")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        if result.stdout and len(result.stdout) < 500:
            print(result.stdout)
        return result.stdout
    except FileNotFoundError:
        raise Exception(f"Command not found. Ensure the executable is in your PATH.")
    except subprocess.CalledProcessError as e:
        error_message = (
            f"Error executing: {description}\n"
            f"Command: {command}\n"
            f"Return Code: {e.returncode}\n"
            f"Stdout: {e.stdout}\n"
            f"Stderr: {e.stderr}"
        )
        raise Exception(error_message)

