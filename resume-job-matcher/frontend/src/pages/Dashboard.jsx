import React, { useState, useEffect } from 'react';
import { matchService } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await matchService.getStats();
        setStats(data);
      } catch (err) {
        console.error("Failed to fetch dashboard stats");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  const cards = [
    { title: 'Total Resumes', value: stats?.total_resumes || 0, icon: '📄', color: 'bg-blue-500' },
    { title: 'Jobs Analyzed', value: stats?.total_matches || 0, icon: '💼', color: 'bg-purple-500' },
    { title: 'Best Match Score', value: `${stats?.best_score?.toFixed(1) || 0}%`, icon: '🎯', color: 'bg-green-500' },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800 mb-8">Welcome back, {stats?.username}!</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {cards.map((card, idx) => (
          <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-6">
            <div className={`${card.color} w-14 h-14 rounded-lg flex items-center justify-center text-2xl text-white shadow-lg`}>
              {card.icon}
            </div>
            <div>
              <p className="text-sm text-slate-500 font-medium uppercase tracking-wider">{card.title}</p>
              <p className="text-3xl font-bold text-slate-800">{card.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-800">Recent Match Activity</h2>
          <button className="text-blue-600 text-sm font-semibold hover:underline">View All</button>
        </div>
        <div className="p-6">
          {/* Placeholder for table or list */}
          <p className="text-slate-500 italic">Historical data visualization coming soon...</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
