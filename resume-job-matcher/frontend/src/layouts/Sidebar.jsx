import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate, Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { title: 'Dashboard', path: '/', icon: '📊' },
    { title: 'My Resumes', path: '/resumes', icon: '📄' },
    { title: 'Job Openings', path: '/jobs', icon: '💼' },
    { title: 'Match History', path: '/history', icon: '🕒' },
  ];

  return (
    <div className="bg-slate-900 text-white w-64 min-h-screen flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <span>🎯</span> Matcher AI
        </h1>
      </div>
      
      <nav className="flex-1 mt-6">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-6 py-4 hover:bg-slate-800 transition-colors ${
              location.pathname === item.path ? 'bg-blue-600 border-r-4 border-white' : ''
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.title}</span>
          </Link>
        ))}
      </nav>
      
      <div className="p-6 border-t border-slate-800">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center font-bold">
            {user?.email?.[0].toUpperCase() || 'U'}
          </div>
          <div className="truncate">
            <p className="text-sm font-medium">{user?.email || 'User'}</p>
            <p className="text-xs text-slate-400">Standard Plan</p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 py-2 px-4 bg-slate-800 hover:bg-red-600 rounded transition-colors"
        >
          <span>🚪</span> Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
