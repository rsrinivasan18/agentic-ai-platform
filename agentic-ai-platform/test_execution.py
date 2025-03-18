"""
Simple script to test Python execution.
"""

import sys
import os

print("=" * 50)
print("Python Execution Test")
print("=" * 50)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')[:5]}...")
print("=" * 50)
print("Test completed successfully!")
print("=" * 50)
