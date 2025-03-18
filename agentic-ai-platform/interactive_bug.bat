@echo off
echo Running Python in interactive mode for debugging...

:: Activate conda environment
call conda activate agentic-ai-platform

:: Run Python with commands to check environment
python -c "import sys; print('Python version:', sys.version); import langchain; print('langchain version:', langchain.__version__); print('Test completed successfully!')"

echo.
echo If you see no output above, there might be an issue with Python's stdout/stderr handling.
echo Press any key to continue with manual interactive Python...
pause > nul

:: Start interactive Python
python