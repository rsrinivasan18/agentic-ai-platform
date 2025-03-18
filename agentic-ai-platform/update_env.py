"""
Script to update .env file with new environment variables needed for Phase 2.
"""

import os
from dotenv import load_dotenv

# Load existing environment variables
load_dotenv()

# Check if .env file exists
if not os.path.exists(".env"):
    print("No .env file found. Creating a new one.")
    with open(".env", "w") as f:
        f.write("# Agentic AI Platform Environment Variables\n\n")

# Read existing .env content
with open(".env", "r") as f:
    env_content = f.read()

# New environment variables to add
new_vars = {"SERPAPI_API_KEY": "# Get your API key at https://serpapi.com/"}

# Add new variables if they don't exist
additions = []
for key, comment in new_vars.items():
    if key not in env_content:
        additions.append(f"\n# Search Agent Configuration\n{key}={comment}\n")

# Write updated content
if additions:
    with open(".env", "a") as f:
        for addition in additions:
            f.write(addition)
    print("Added new environment variables to .env file:")
    for key in new_vars.keys():
        if key not in env_content:
            print(f"  - {key}")
else:
    print("No new environment variables needed.")

print(
    "\nPlease update your .env file with actual values for the new environment variables."
)
