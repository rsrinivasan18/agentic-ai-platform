import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const HomePage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div>
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-6">Welcome to the Agentic AI Platform</h1>
        <p className="text-xl mb-8">
          Build, deploy, and manage intelligent AI agents to automate tasks and enhance productivity.
        </p>

        {!isAuthenticated && (
          <div className="mb-8 space-x-4">
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Sign Up
            </Link>
            <Link
              to="/login"
              className="bg-gray-700 hover:bg-gray-800 text-white font-bold py-2 px-4 rounded"
            >
              Log In
            </Link>
          </div>
        )}

        {isAuthenticated && (
          <div className="mb-8">
            <Link
              to="/dashboard"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Go to Dashboard
            </Link>
          </div>
        )}
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">RAG Agents</h2>
          <p className="mb-4">
            Create Retrieval-Augmented Generation agents that combine the power of large language models with your own data.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Search Agents</h2>
          <p className="mb-4">
            Build agents that can search the web for information and provide concise, relevant answers.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">ML Agents</h2>
          <p className="mb-4">
            Leverage machine learning models to analyze data, make predictions, and gain insights.
          </p>
        </div>
      </div>

      <div className="mt-16">
        <h2 className="text-2xl font-bold mb-6 text-center">How It Works</h2>
        <div className="flex flex-col md:flex-row justify-between items-center space-y-8 md:space-y-0 md:space-x-8">
          <div className="flex-1 text-center">
            <div className="bg-blue-100 h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-blue-600 text-2xl font-bold">1</span>
            </div>
            <h3 className="text-xl font-bold mb-2">Create an Agent</h3>
            <p>Choose an agent type and configure it to suit your specific needs.</p>
          </div>
          
          <div className="flex-1 text-center">
            <div className="bg-blue-100 h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-blue-600 text-2xl font-bold">2</span>
            </div>
            <h3 className="text-xl font-bold mb-2">Train the Agent</h3>
            <p>Upload data, provide examples, or connect to external sources.</p>
          </div>
          
          <div className="flex-1 text-center">
            <div className="bg-blue-100 h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-blue-600 text-2xl font-bold">3</span>
            </div>
            <h3 className="text-xl font-bold mb-2">Deploy & Use</h3>
            <p>Interact with your agent through the platform or API integrations.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;