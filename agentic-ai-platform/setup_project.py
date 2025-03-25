"""
Master setup script for the Agentic AI Platform.
This script orchestrates the setup of both backend and frontend.
"""

import os
import subprocess
import sys
from pathlib import Path


def check_prerequisites():
    """Check if necessary tools are installed."""
    print("Checking prerequisites...")

    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (
        python_version.major == 3 and python_version.minor < 10
    ):
        print("Error: Python 3.10 or higher is required.")
        sys.exit(1)
    print(
        "✓ Python version: {}.{}.{}".format(
            python_version.major, python_version.minor, python_version.micro
        )
    )

    # Check if pip is installed
    try:
        subprocess.run(
            ["pip", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("✓ pip is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: pip is not installed or not in PATH.")
        sys.exit(1)

    # Check if node is installed (optional for backend-only setup)
    try:
        subprocess.run(
            ["node", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("✓ Node.js is installed")
        node_installed = True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("! Node.js is not installed. Frontend setup will be skipped.")
        node_installed = False

    return node_installed


def setup_backend():
    """Set up the backend."""
    print("\nSetting up backend...")

    # Run backend structure setup
    if not os.path.exists("setup_structure.py"):
        print("Error: setup_structure.py not found.")
        return False

    try:
        subprocess.run(["python", "setup_structure.py"], check=True)
        print("✓ Backend structure created")

        # Install backend dependencies
        os.chdir("backend")
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Backend dependencies installed")
        os.chdir("..")

        return True
    except subprocess.SubprocessError as e:
        print(f"Error setting up backend: {e}")
        return False


def setup_frontend(node_installed):
    """Set up the frontend."""
    if not node_installed:
        print("\nSkipping frontend setup (Node.js not installed)")
        return False

    print("\nSetting up frontend...")

    # Run frontend setup
    if not os.path.exists("setup_frontend_complete.py"):
        print("Error: setup_frontend_complete.py not found.")
        return False

    try:
        subprocess.run(["python", "setup_frontend_complete.py"], check=True)
        print("✓ Frontend structure created")

        # Install frontend dependencies
        os.chdir("frontend")
        subprocess.run(["npm", "install"], check=True)
        print("✓ Frontend dependencies installed")
        os.chdir("..")

        return True
    except subprocess.SubprocessError as e:
        print(f"Error setting up frontend: {e}")
        return False


def main():
    """Main setup function."""
    print("=== Agentic AI Platform Setup ===\n")

    # Check prerequisites
    node_installed = check_prerequisites()

    # Setup backend
    backend_success = setup_backend()

    # Setup frontend
    frontend_success = setup_frontend(node_installed) if backend_success else False

    # Print summary
    print("\n=== Setup Summary ===")
    print(f"Backend setup: {'Successful' if backend_success else 'Failed'}")
    if node_installed:
        print(f"Frontend setup: {'Successful' if frontend_success else 'Failed'}")
    else:
        print("Frontend setup: Skipped (Node.js not installed)")

    # Print next steps
    print("\n=== Next Steps ===")
    if backend_success:
        print("1. Update backend/.env with your API keys and settings")
        print("2. Start the backend server: cd backend && uvicorn main:app --reload")
        print("3. Access the API documentation at: http://localhost:8000/docs")

    if frontend_success:
        print("4. Start the frontend development server: cd frontend && npm start")
        print("5. Access the frontend at: http://localhost:3000")

    print("\nAlternatively, if you have Docker installed:")
    print("- Run the entire application: docker-compose up")


if __name__ == "__main__":
    main()
