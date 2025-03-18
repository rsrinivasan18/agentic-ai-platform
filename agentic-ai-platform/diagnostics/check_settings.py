"""
Check if settings.py is correctly set up
"""

import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Check if settings.py exists
settings_path = os.path.join("src", "config", "settings.py")
if os.path.exists(settings_path):
    print(f"\nFile exists: {settings_path}")

    # Print file content
    print("\nFile content:")
    with open(settings_path, "r") as f:
        content = f.read()
        print(content)

    # Check if variables are defined
    if "CHUNK_SIZE" in content and "CHUNK_OVERLAP" in content:
        print("\nCHUNK_SIZE and CHUNK_OVERLAP are defined in the file.")
    else:
        print("\nWARNING: CHUNK_SIZE and/or CHUNK_OVERLAP are NOT defined in the file.")
else:
    print(f"\nERROR: File does not exist: {settings_path}")

# Try to import
print("\nAttempting to import settings module...")
try:
    from src.config import settings

    print("Successfully imported settings module")

    # Check if variables exist
    if hasattr(settings, "CHUNK_SIZE") and hasattr(settings, "CHUNK_OVERLAP"):
        print(f"CHUNK_SIZE = {settings.CHUNK_SIZE}")
        print(f"CHUNK_OVERLAP = {settings.CHUNK_OVERLAP}")
    else:
        print("WARNING: CHUNK_SIZE and/or CHUNK_OVERLAP not found in settings module")
except Exception as e:
    print(f"Error importing settings: {str(e)}")
    import traceback

    traceback.print_exc()
