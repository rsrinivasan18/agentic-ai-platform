"""
Script to create the frontend directory structure and core files for the Agentic AI Platform.
"""

import os
from pathlib import Path
import json
import shutil


def create_frontend_structure():
    """Create the frontend directory structure."""
    print("Creating frontend directory structure...")

    # Main directories
    directories = [
        "frontend",
        "frontend/public",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/services",
        "frontend/src/hooks",
        "frontend/src/context",
        "frontend/src/utils",
        "frontend/src/assets",
        "frontend/src/styles",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("Frontend directory structure created successfully.")


def create_package_json():
    """Create package.json file."""
    package_data = {
        "name": "agentic-ai-platform-frontend",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "@testing-library/jest-dom": "^5.16.5",
            "@testing-library/react": "^13.4.0",
            "@testing-library/user-event": "^13.5.0",
            "axios": "^1.4.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.14.1",
            "react-scripts": "5.0.1",
            "tailwindcss": "^3.3.2",
            "web-vitals": "^2.1.4",
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
        },
        "eslintConfig": {"extends": ["react-app", "react-app/jest"]},
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version",
            ],
        },
    }

    with open("frontend/package.json", "w") as f:
        json.dump(package_data, f, indent=2)

    print("Created package.json")


def create_dockerfile():
    """Create Dockerfile for the frontend."""
    content = """FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . ./

EXPOSE 3000

CMD ["npm", "start"]
"""

    with open("frontend/Dockerfile", "w") as f:
        f.write(content)

    print("Created Dockerfile")


def create_env_files():
    """Create environment files for development and production."""
    # Create .env.development
    with open("frontend/.env.development", "w") as f:
        f.write("REACT_APP_API_URL=http://localhost:8000/api\n")

    # Create .env.production
    with open("frontend/.env.production", "w") as f:
        f.write("REACT_APP_API_URL=/api\n")

    print("Created environment files")


def create_index_html():
    """Create index.html file."""
    content = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Agentic AI Platform - A platform for building and deploying AI agents"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>Agentic AI Platform</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""

    with open("frontend/public/index.html", "w") as f:
        f.write(content)

    print("Created index.html")


def create_manifest_json():
    """Create manifest.json file."""
    content = """{
  "short_name": "Agentic AI",
  "name": "Agentic AI Platform",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
"""

    with open("frontend/public/manifest.json", "w") as f:
        f.write(content)

    print("Created manifest.json")


def create_index_js():
    """Create index.js file."""
    content = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
"""

    with open("frontend/src/index.js", "w") as f:
        f.write(content)

    print("Created index.js")


def create_app_js():
    """Create App.js file."""
    content = """import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AgentsPage from './pages/AgentsPage';
import AgentDetailPage from './pages/AgentDetailPage';
import CreateAgentPage from './pages/CreateAgentPage';
import NotFoundPage from './pages/NotFoundPage';

// Components
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* Public routes */}
        <Route index element={<HomePage />} />
        <Route path="login" element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />
        } />
        <Route path="register" element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />
        } />

        {/* Protected routes */}
        <Route path="dashboard" element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        } />
        <Route path="agents" element={
          <ProtectedRoute>
            <AgentsPage />
          </ProtectedRoute>
        } />
        <Route path="agents/create" element={
          <ProtectedRoute>
            <CreateAgentPage />
          </ProtectedRoute>
        } />
        <Route path="agents/:agentId" element={
          <ProtectedRoute>
            <AgentDetailPage />
          </ProtectedRoute>
        } />

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
"""

    with open("frontend/src/App.js", "w") as f:
        f.write(content)

    print("Created App.js")


def main():
    """Main function to set up the frontend."""
    print("Setting up frontend for Agentic AI Platform...")

    # Create directory structure
    create_frontend_structure()

    # Create core files
    create_package_json()
    create_dockerfile()
    create_env_files()

    # Create public files
    create_index_html()
    create_manifest_json()

    # Create core source files
    create_index_js()
    create_app_js()

    print("\nFrontend core setup completed!")
    print(
        "The remaining components, pages, hooks, services, and style files are already set up."
    )
    print("\nTo initialize the React project:")
    print("1. cd frontend")
    print("2. npm install")
    print("3. npm start")
    print("\nThe frontend will be available at http://localhost:3000")


if __name__ == "__main__":
    main()
