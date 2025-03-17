@echo off
echo Setting up conda environment for Agentic AI Platform...

:: Create conda environment
call conda create -n agentic-ai-platform python=3.10 -y
echo Conda environment created.

:: Activate conda environment
call conda activate agentic-ai-platform
echo Conda environment activated.

:: Install packages
call pip install -r requirements.txt
echo Required packages installed.

echo.
echo Conda environment setup complete!
echo You can now open this project in VSCode.
echo.
echo To activate this environment in the future, run: conda activate agentic-ai-platform
