"""
Script to create __init__.py files in all required directories.
"""

import os

# Directories that need __init__.py files
directories = ["src", "src/config", "src/rag", "src/llm", "src/agents", "src/api"]

# Create __init__.py in each directory
for directory in directories:
    init_file = os.path.join(directory, "__init__.py")

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    # Create __init__.py file if it doesn't exist
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("# Module initialization\n")
        print(f"Created {init_file}")
    else:
        print(f"{init_file} already exists")

print("\nAll __init__.py files created successfully!")
