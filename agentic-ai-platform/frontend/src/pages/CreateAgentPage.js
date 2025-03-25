import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { agentsService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const AgentsPage = () => {
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

  const deleteAgent = async (agentId) => {
    if (!window.confirm('Are you sure you want to delete this agent?')) {
      return;
    }

    try {
      await agentsService.deleteAgent(agentId);
      setAgents(agents.filter(agent => agent.id !== agentId));
    } catch (err) {
      console.error('Error deleting agent:', err);
      setError('Failed to delete agent. Please try again.');
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Agents</h1>
        <Link 
          to="/agents/create"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Create New Agent
        </Link>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

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
            <div
              key={agent.id}
              className="bg-white rounded-lg shadow-md overflow-hidden"
            >
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold">{agent.name}</h3>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    agent.type === 'rag' ? 'bg-blue-100 text-blue-800' :
                    agent.type === 'search' ? 'bg-green-100 text-green-800' :
                    'bg-purple-100 text-purple-800'
                  }`}>
                    {agent.type.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-600 mb-4">
                  {agent.description || 'No description provided.'}
                </p>
                <div className="text-sm text-gray-500 mb-4">
                  Created: {new Date(agent.created_at).toLocaleDateString()}
                </div>
                <div className="flex justify-between">
                  <Link
                    to={`/agents/${agent.id}`}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    View Details
                  </Link>
                  <button
                    onClick={() => deleteAgent(agent.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AgentsPage;