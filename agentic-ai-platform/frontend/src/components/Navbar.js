import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="bg-gray-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              Agentic AI Platform
            </Link>
          </div>

          {/* Desktop menu */}
          <div className="hidden md:flex space-x-6">
            <NavLink to="/" 
              className={({ isActive }) => 
                isActive ? "text-blue-400" : "hover:text-blue-300"
              }
            >
              Home
            </NavLink>
            
            {isAuthenticated ? (
              <>
                <NavLink to="/dashboard" 
                  className={({ isActive }) => 
                    isActive ? "text-blue-400" : "hover:text-blue-300"
                  }
                >
                  Dashboard
                </NavLink>
                <NavLink to="/agents" 
                  className={({ isActive }) => 
                    isActive ? "text-blue-400" : "hover:text-blue-300"
                  }
                >
                  Agents
                </NavLink>
                <button 
                  onClick={logout} 
                  className="hover:text-blue-300"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" 
                  className={({ isActive }) => 
                    isActive ? "text-blue-400" : "hover:text-blue-300"
                  }
                >
                  Login
                </NavLink>
                <NavLink to="/register" 
                  className={({ isActive }) => 
                    isActive ? "text-blue-400" : "hover:text-blue-300"
                  }
                >
                  Register
                </NavLink>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button onClick={toggleMenu} className="text-white focus:outline-none">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <NavLink to="/" 
              className={({ isActive }) => 
                isActive ? "block text-blue-400 py-2" : "block hover:text-blue-300 py-2"
              }
              onClick={() => setIsMenuOpen(false)}
            >
              Home
            </NavLink>
            
            {isAuthenticated ? (
              <>
                <NavLink to="/dashboard" 
                  className={({ isActive }) => 
                    isActive ? "block text-blue-400 py-2" : "block hover:text-blue-300 py-2"
                  }
                  onClick={() => setIsMenuOpen(false)}
                >
                  Dashboard
                </NavLink>
                <NavLink to="/agents" 
                  className={({ isActive }) => 
                    isActive ? "block text-blue-400 py-2" : "block hover:text-blue-300 py-2"
                  }
                  onClick={() => setIsMenuOpen(false)}
                >
                  Agents
                </NavLink>
                <button 
                  onClick={() => {
                    logout();
                    setIsMenuOpen(false);
                  }} 
                  className="block hover:text-blue-300 py-2 w-full text-left"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" 
                  className={({ isActive }) => 
                    isActive ? "block text-blue-400 py-2" : "block hover:text-blue-300 py-2"
                  }
                  onClick={() => setIsMenuOpen(false)}
                >
                  Login
                </NavLink>
                <NavLink to="/register" 
                  className={({ isActive }) => 
                    isActive ? "block text-blue-400 py-2" : "block hover:text-blue-300 py-2"
                  }
                  onClick={() => setIsMenuOpen(false)}
                >
                  Register
                </NavLink>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;