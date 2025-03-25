import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { agentsService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const AgentDetailPage = () => {
  const { agentId } = useParams();
  const navigate = useNavigate();
  
  const [agent, setAgent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState(null);
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryError, setQueryError] = useState(null);
  
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  useEffect(() => {
    const fetchAgent = async () => {
      try {
        const data = await agentsService.getAgent(agentId);
        setAgent(data);
      } catch (err) {
        console.error('Error fetching agent:', err);
        setError('Failed to load agent details.');
      } finally {
        setLoading(false);
      }
    };

    fetchAgent();
  }, [agentId]);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      return;
    }
    
    setQueryLoading(true);
    setQueryResult(null);
    setQueryError(null);
    
    try {
      let result;
      
      if (agent.type === 'ml') {
        // ML agents might need specific parameters
        result = await agentsService.queryAgent(agentId, '', { 
          data: JSON.parse(query) 
        });
      } else {
        // RAG and Search agents just need the query text
        result = await agentsService.queryAgent(agentId, query);
      }
      
      setQueryResult(result);
    } catch (err) {
      console.error('Error querying agent:', err);
      setQueryError('Failed to get a response from the agent.');
    } finally {
      setQueryLoading(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      return;
    }
    
    setUploadLoading(true);
    setUploadResult(null);
    setUploadError(null);
    
    try {
      const collectionName = agent.config.collection_name;
      
      const result = await agentsService.uploadDocument(
        agentId, 
        file, 
        collectionName
      );
      
      setUploadResult(result);
      setFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('file-upload');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (err) {
      console.error('Error uploading document:', err);
      setUploadError('Failed to upload document.');
    } finally {
      setUploadLoading(false);
    }
  };

  const deleteAgent = async () => {
    if (!window.confirm('Are you sure you want to delete this agent?')) {
      return;
    }

    try {
      await agentsService.deleteAgent(agentId);
      navigate('/agents');
    } catch (err) {
      console.error('Error deleting agent:', err);
      setError('Failed to delete agent. Please try again.');
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="text-center">
        <p className="text-red-600 mb-4">{error}</p>
        <Link to="/agents" className="text-blue-600 hover:text-blue-800">
          Back to Agents
        </Link>
      </div>
    );
  }

  if (!agent) {
    return (
      <div className="text-center">
        <p className="mb-4">Agent not found.</p>
        <Link to="/agents" className="text-blue-600 hover:text-blue-800">
          Back to Agents
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <Link to="/agents" className="text-blue-600 hover:text-blue-800 mb-2 inline-block">
            &larr; Back to Agents
          </Link>
          <h1 className="text-3xl font-bold">{agent.name}</h1>
        </div>
        <button
          onClick={deleteAgent}
          className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded"
        >
          Delete Agent
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="mb-4 flex justify-between">
          <div>
            <span className={`inline-block px-2 py-1 text-xs rounded-full ${
              agent.type === 'rag' ? 'bg-blue-100 text-blue-800' :
              agent.type === 'search' ? 'bg-green-100 text-green-800' :
              'bg-purple-100 text-purple-800'
            }`}>
              {agent.type.toUpperCase()}
            </span>
          </div>
          <div className="text-sm text-gray-500">
            Created: {new Date(agent.created_at).toLocaleDateString()}
          </div>
        </div>
        
        <p className="mb-6">
          {agent.description || 'No description provided.'}
        </p>
        
        <div className="mb-4">
          <h3 className="text-lg font-bold mb-2">Agent Configuration</h3>
          <pre className="bg-gray-100 p-4 rounded overflow-auto">
            {JSON.stringify(agent.config, null, 2)}
          </pre>
        </div>
      </div>

      {/* Document upload section (only for RAG agents) */}
      {agent.type === 'rag' && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Upload Document</h2>
          
          {uploadError && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {uploadError}
            </div>
          )}
          
          {uploadResult && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              {uploadResult.message}
            </div>
          )}
          
          <form onSubmit={handleFileUpload} className="mb-4">
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file-upload">
                Select File
              </label>
              <input
                id="file-upload"
                type="file"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
            </div>
            
            <button
              type="submit"
              className={`bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
                uploadLoading || !file ? 'opacity-50 cursor-not-allowed' : ''
              }`}
              disabled={uploadLoading || !file}
            >
              {uploadLoading ? 'Uploading...' : 'Upload Document'}
            </button>
          </form>
        </div>
      )}

      {/* Query section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">Query Agent</h2>
        
        {queryError && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {queryError}
          </div>
        )}
        
        <form onSubmit={handleQuerySubmit} className="mb-4">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="query">
              {agent.type === 'ml' ? 'Enter JSON data' : 'Ask a question'}
            </label>
            <textarea
              id="query"
              rows="4"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={agent.type === 'ml' ? '{"data": [...], "target_column": "..."}' : 'What would you like to know?'}
              required
            ></textarea>
          </div>
          
          <button
            type="submit"
            className={`bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
              queryLoading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={queryLoading}
          >
            {queryLoading ? 'Processing...' : 'Submit Query'}
          </button>
        </form>
        
        {queryResult && (
          <div className="mt-6">
            <h3 className="text-lg font-bold mb-2">Response</h3>
            
            {/* Display different response formats based on agent type */}
            {agent.type === 'rag' && queryResult.answer && (
              <div className="bg-gray-100 p-4 rounded">
                <p>{queryResult.answer}</p>
                
                {queryResult.source_documents && queryResult.source_documents.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-bold text-sm">Sources:</h4>
                    <ul className="list-disc pl-5 mt-2">
                      {queryResult.source_documents.map((doc, index) => (
                        <li key={index} className="text-sm text-gray-700 mb-1">
                          {doc.content.substring(0, 100)}...
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
            
            {agent.type === 'search' && queryResult.answer && (
              <div className="bg-gray-100 p-4 rounded">
                <p>{queryResult.answer}</p>
                
                {queryResult.search_results && queryResult.search_results.length > 0 && (
                  <div className="mt-4">
                    <h4 className="font-bold text-sm">Sources:</h4>
                    <ul className="list-disc pl-5 mt-2">
                      {queryResult.search_results.map((result, index) => (
                        <li key={index} className="text-sm text-gray-700 mb-2">
                          <a href={result.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                            {result.title}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
            
            {agent.type === 'ml' && (
              <div className="bg-gray-100 p-4 rounded">
                <pre className="whitespace-pre-wrap">{JSON.stringify(queryResult, null, 2)}</pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentDetailPage;