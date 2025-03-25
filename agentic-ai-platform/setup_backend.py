"""
Master setup script for the Agentic AI Platform backend.
This script creates all necessary files and directories.
"""

import os
import shutil
from pathlib import Path


def main():
    print("Setting up Agentic AI Platform backend...")

    # Step 1: Create directory structure
    print("\nStep 1: Creating directory structure...")
    import setup_structure

    setup_structure.create_backend_structure()

    # Step 2: Copy all the files we've created to their proper locations
    print("\nStep 2: Setting up backend files...")

    # Ensure backend/.env exists from .env.example
    env_example = Path("backend/.env.example")
    env_file = Path("backend/.env")
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"Created {env_file} from {env_example}")

    print("\nAgentic AI Platform backend setup completed successfully!")
    print("\nNext steps:")
    print("1. Update backend/.env with your API keys and settings")
    print("2. Install dependencies with: cd backend && pip install -r requirements.txt")
    print("3. Start the server with: cd backend && uvicorn main:app --reload")
    print("4. Access the API documentation at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
