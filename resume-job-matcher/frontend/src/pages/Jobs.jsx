import React, { useState, useEffect } from 'react';
import { jobService } from '../services/api';

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    description: '',
    required_skills: ''
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const data = await jobService.list();
      setJobs(data);
    } catch (err) {
      console.error("Failed to fetch jobs");
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const skillsArray = formData.required_skills.split(',').map(s => s.trim()).filter(s => s);
      await jobService.create({ ...formData, required_skills: skillsArray });
      setIsModalOpen(false);
      setFormData({ title: '', company: '', location: '', description: '', required_skills: '' });
      fetchJobs();
    } catch (err) {
      alert("Failed to create job");
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Job Openings</h1>
          <p className="text-slate-500 mt-1">Manage and view available job opportunities</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-blue-700 transition-all flex items-center gap-2"
        >
          <span>➕</span> Post New Job
        </button>
      </div>

      {loading ? (
        <div>Loading jobs...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {jobs.map((job) => (
            <div key={job.id} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow relative group">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-800">{job.title}</h3>
                  <p className="text-blue-600 font-medium">{job.company}</p>
                </div>
                <div className="text-slate-400 text-sm flex items-center gap-1">
                  📍 {job.location || 'Remote'}
                </div>
              </div>
              <p className="text-slate-600 text-sm line-clamp-3 mb-6">
                {job.description}
              </p>
              <div className="flex flex-wrap gap-2">
                {job.required_skills?.map((skill, idx) => (
                  <span key={idx} className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs font-semibold">
                    {skill}
                  </span>
                ))}
              </div>
              <button 
                onClick={async () => { if(confirm('Delete job?')) { await jobService.delete(job.id); fetchJobs(); } }}
                className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-600 p-2 transition-opacity"
              >
                🗑️
              </button>
            </div>
          ))}
          {jobs.length === 0 && (
            <div className="col-span-full py-20 text-center bg-white rounded-2xl border border-dashed border-slate-200">
              <p className="text-slate-500">No jobs posted yet. Click "Post New Job" to get started.</p>
            </div>
          )}
        </div>
      )}

      {/* Basic Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white rounded-2xl w-full max-w-2xl p-8 my-auto">
            <h2 className="text-2xl font-bold mb-6 text-slate-800">Post a New Job</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold mb-1">Job Title</label>
                  <input required className="w-full p-3 border rounded-xl" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-1">Company</label>
                  <input required className="w-full p-3 border rounded-xl" value={formData.company} onChange={e => setFormData({...formData, company: e.target.value})} />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Location</label>
                <input className="w-full p-3 border rounded-xl" value={formData.location} onChange={e => setFormData({...formData, location: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Job Description</label>
                <textarea required className="w-full p-3 border rounded-xl h-32" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Required Skills (comma separated)</label>
                <input className="w-full p-3 border rounded-xl" placeholder="React, Python, AWS..." value={formData.required_skills} onChange={e => setFormData({...formData, required_skills: e.target.value})} />
              </div>
              <div className="flex gap-4 pt-4">
                <button type="button" onClick={() => setIsModalOpen(false)} className="flex-1 py-3 border rounded-xl">Cancel</button>
                <button type="submit" className="flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold">Post Job</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Jobs;
