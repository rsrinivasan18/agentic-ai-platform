import React from 'react';
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
