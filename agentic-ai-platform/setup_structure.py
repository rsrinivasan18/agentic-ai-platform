"""
Creates the basic directory structure for the Agentic AI Platform backend.
"""

import os
from pathlib import Path


def create_backend_structure():
    print("Creating backend directory structure...")

    # Main directories
    directories = [
        "backend",
        "backend/api",
        "backend/api/routes",
        "backend/core",
        "backend/db",
        "backend/models",
        "backend/schemas",
        "backend/services",
        "backend/utils",
        "backend/tests",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create __init__.py in each directory
        init_file = Path(directory) / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    print("Backend directory structure created successfully.")


if __name__ == "__main__":
    create_backend_structure()
