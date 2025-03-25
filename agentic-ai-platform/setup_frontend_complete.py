"""
Script to create the frontend directory structure for the Agentic AI Platform.
This script completes the frontend setup and creates all necessary files.
"""

import os
from pathlib import Path
import json
import subprocess
import shutil


def create_frontend_structure():
    print("Creating frontend directory structure...")

    # Main directories
    directories = [
        "frontend",
        "frontend/public",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/services",
        "frontend/src/hooks",
        "frontend/src/context",
        "frontend/src/utils",
        "frontend/src/assets",
        "frontend/src/styles",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("Frontend directory structure created successfully.")


def create_package_json():
    package_data = {
        "name": "agentic-ai-platform-frontend",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "@testing-library/jest-dom": "^5.16.5",
            "@testing-library/react": "^13.4.0",
            "@testing-library/user-event": "^13.5.0",
            "axios": "^1.4.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.14.1",
            "react-scripts": "5.0.1",
            "tailwindcss": "^3.3.2",
            "web-vitals": "^2.1.4",
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
        },
        "eslintConfig": {"extends": ["react-app", "react-app/jest"]},
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version",
            ],
        },
    }

    with open("frontend/package.json", "w") as f:
        json.dump(package_data, f, indent=2)

    print("Created package.json")


def main():
    print("Setting up frontend for Agentic AI Platform...")

    # Step 1: Create directory structure
    create_frontend_structure()

    # Step 2: Create package.json and other config files
    create_package_json()

    print("\nFrontend setup completed!")
    print("\nTo initialize the React project:")
    print("1. cd frontend")
    print("2. npm install")
    print("3. npm start")
    print("\nThe frontend will be available at http://localhost:3000")


if __name__ == "__main__":
    main()
