@echo off
echo Setting up Git repository for Agentic AI Platform...

:: Initialize Git repository
git init
echo Git repository initialized.

:: Add .gitignore file
copy ..\gitignore.txt .gitignore
echo .gitignore file added.

:: Add all files to Git
git add .
echo Files added to Git.

:: Make initial commit
git commit -m "Initial project setup"
echo Initial commit created.

:: Instructions for connecting to GitHub
echo.
echo To connect to GitHub:
echo 1. Create a new repository on GitHub
echo 2. Run the following commands:
echo    git remote add origin https://github.com/rsrinivasan18/agentic-ai-platform.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Replace 'your-username' with your GitHub username.
