"""
Script to check imports and debug module issues.
"""

import os
import sys

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")

# Print Python path
print(f"Python path: {sys.path}")

# Try to inspect document_loader.py
document_loader_path = os.path.join("src", "rag", "document_loader.py")
if os.path.exists(document_loader_path):
    print(f"\nFile exists: {document_loader_path}")

    # Print file content
    print("\nFile content:")
    with open(document_loader_path, "r") as f:
        content = f.read()
        print(content)

    # Check if function is defined
    if "def load_and_split_documents" in content:
        print("\nload_and_split_documents function is defined in the file.")
    else:
        print(
            "\nWARNING: load_and_split_documents function is NOT defined in the file."
        )
else:
    print(f"\nERROR: File does not exist: {document_loader_path}")

# Try basic import test
print("\nTrying basic imports...")
try:
    from src.config import settings

    print("✓ Successfully imported settings")
except Exception as e:
    print(f"✗ Failed to import settings: {str(e)}")

try:
    from src.rag import document_loader

    print("✓ Successfully imported document_loader module")

    # Print all defined functions in the module
    functions = [
        name
        for name in dir(document_loader)
        if callable(getattr(document_loader, name)) and not name.startswith("_")
    ]
    print(f"Functions defined in document_loader: {functions}")
except Exception as e:
    print(f"✗ Failed to import document_loader: {str(e)}")
