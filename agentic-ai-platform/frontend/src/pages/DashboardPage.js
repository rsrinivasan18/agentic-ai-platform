import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { agentsService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const DashboardPage = () => {
  const { user } = useAuth();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await agentsService.getAgents();
        setAgents(data);
      } catch (err) {
        console.error('Error fetching agents:', err);
        setError('Failed to load agents. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Link 
          to="/agents/create"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Create New Agent
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">Welcome, {user?.username || 'User'}!</h2>
        <p>
          This is your dashboard for the Agentic AI Platform. Here you can manage your agents and see their activity.
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <h2 className="text-2xl font-bold mb-4">Your Agents</h2>
      
      {agents.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-6 text-center">
          <p className="mb-4">You don't have any agents yet.</p>
          <Link 
            to="/agents/create"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Create Your First Agent
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <Link
              key={agent.id}
              to={`/agents/${agent.id}`}
              className="agent-card bg-white rounded-lg shadow-md p-6 hover:shadow-lg"
            >
              <h3 className="text-xl font-bold mb-2">{agent.name}</h3>
              <div className="mb-2">
                <span className="inline-block bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded">
                  {agent.type.toUpperCase()}
                </span>
              </div>
              <p className="text-gray-600 mb-4">
                {agent.description || 'No description provided.'}
              </p>
              <div className="text-sm text-gray-500">
                Created: {new Date(agent.created_at).toLocaleDateString()}
              </div>
            </Link>
          ))}
        </div>
      )}

      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-4">Quick Stats</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold mb-2">Total Agents</h3>
            <p className="text-3xl font-bold text-blue-600">{agents.length}</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold mb-2">Agent Types</h3>
            <div>
              <div className="flex justify-between mb-1">
                <span>RAG</span>
                <span>{agents.filter(a => a.type === 'rag').length}</span>
              </div>
              <div className="flex justify-between mb-1">
                <span>Search</span>
                <span>{agents.filter(a => a.type === 'search').length}</span>
              </div>
              <div className="flex justify-between">
                <span>ML</span>
                <span>{agents.filter(a => a.type === 'ml').length}</span>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold mb-2">Recent Activity</h3>
            <p className="text-gray-600">
              {agents.length > 0 
                ? 'Your agents are ready to use.' 
                : 'Create an agent to get started.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;