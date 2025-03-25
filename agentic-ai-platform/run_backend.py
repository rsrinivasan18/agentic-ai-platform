"""
Script to run the Agentic AI Platform backend without requiring npm/Node.js.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def check_dependencies():
    """Check if the required Python packages are installed."""
    print("Checking Python dependencies...")

    required_packages = [
        "fastapi",
        "uvicorn",
        "motor",
        "pymongo",
        "python-multipart",
        "python-jose",
        "passlib",
        "bcrypt",
        "pydantic",
        "email-validator",
        "python-dotenv",
        "langchain",
        "langchain-community",
        "chromadb",
        "sentence-transformers",
        "openai",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_").split("[")[0])
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", *missing_packages])
        print("All required packages installed!")
    else:
        print("All required packages are already installed.")


def setup_env_file():
    """Set up the .env file if it doesn't exist."""
    env_path = Path("backend/.env")
    env_example_path = Path("backend/.env.example")

    if not env_path.exists() and env_example_path.exists():
        # Copy example env file
        with open(env_example_path, "r") as example_file:
            content = example_file.read()

        # Ask for OpenAI API key
        openai_key = input("Enter your OpenAI API key (or press Enter to skip): ")
        if openai_key:
            content = content.replace("your_openai_api_key_here", openai_key)

        # Write to .env file
        with open(env_path, "w") as env_file:
            env_file.write(content)

        print(f"Created {env_path} from example template")
    elif not env_path.exists():
        # Create minimal .env file
        content = """# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=True

# MongoDB Settings
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=agentic_ai_platform

# Vector DB Settings
CHROMA_PERSIST_DIRECTORY=./chroma_db

# LLM Settings
OPENAI_API_KEY=
DEFAULT_LLM_MODEL=gpt-3.5-turbo
DEFAULT_EMBEDDING_MODEL=all-MiniLM-L6-v2

# JWT Settings
JWT_SECRET=supersecretkey
JWT_EXPIRATION=10080  # 1 week in minutes
"""

        # Ask for OpenAI API key
        openai_key = input("Enter your OpenAI API key (or press Enter to skip): ")
        if openai_key:
            content = content.replace("OPENAI_API_KEY=", f"OPENAI_API_KEY={openai_key}")

        # Create directory if it doesn't exist
        env_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to .env file
        with open(env_path, "w") as env_file:
            env_file.write(content)

        print(f"Created {env_path}")


def run_backend():
    """Run the FastAPI backend."""
    backend_path = Path("backend")
    if not backend_path.exists() or not (backend_path / "main.py").exists():
        print("Backend directory or main.py not found.")
        print("Please run setup_structure.py first to create the backend structure.")
        return False

    print("\nStarting the FastAPI backend...")
    try:
        # Change to backend directory
        os.chdir("backend")

        # Run uvicorn server
        server_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        print("Backend server started at http://localhost:8000")
        print("API documentation available at http://localhost:8000/docs")

        # Open browser to documentation
        webbrowser.open("http://localhost:8000/docs")

        print("\nPress Ctrl+C to stop the server...")

        # Keep the server running and print output
        while True:
            line = server_process.stdout.readline()
            if not line and server_process.poll() is not None:
                break
            if line:
                print(line.strip())

        return True
    except KeyboardInterrupt:
        print("\nStopping the server...")
        return True
    except Exception as e:
        print(f"Error running backend: {e}")
        return False
    finally:
        # Change back to original directory
        os.chdir("..")


def main():
    """Main function."""
    print("=== Agentic AI Platform Backend Runner ===\n")

    # Check dependencies
    check_dependencies()

    # Setup .env file
    setup_env_file()

    # Run backend
    run_backend()


if __name__ == "__main__":
    main()
