import React, { useState } from 'react';
import { resumeService, matchService } from '../services/api';
import { useNavigate } from 'react-router-dom';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type === 'application/pdf') {
      setFile(selected);
      setError('');
    } else {
      setFile(null);
      setError('Please select a valid PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setUploading(true);
    setError('');
    try {
      const res = await resumeService.upload(file);
      // Automatically run matching after upload
      await matchService.run(res.id);
      navigate('/history');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload resume.');
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 text-center">
        <div className="w-20 h-20 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-3xl mx-auto mb-6">
          📄
        </div>
        <h2 className="text-2xl font-bold text-slate-800 mb-2">Upload Your Resume</h2>
        <p className="text-slate-500 mb-8">We'll analyze your skills and find the best job matches for you using AI.</p>
        
        <div 
          className="border-2 border-dashed border-slate-200 rounded-2xl p-12 mb-8 hover:border-blue-400 hover:bg-blue-50 transition-all cursor-pointer group"
          onClick={() => document.getElementById('resume-input').click()}
        >
          <input
            type="file"
            id="resume-input"
            hidden
            accept=".pdf"
            onChange={handleFileChange}
          />
          <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">📤</div>
          <p className="text-slate-600 font-medium">
            {file ? file.name : 'Click to browse or drag and drop your PDF resume'}
          </p>
          <p className="text-xs text-slate-400 mt-2">Maximum file size: 5MB</p>
        </div>
        
        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm mb-6">
            {error}
          </div>
        )}
        
        <button
          disabled={!file || uploading}
          onClick={handleUpload}
          className={`w-full py-4 rounded-xl font-bold text-white shadow-lg transition-all ${
            uploading || !file ? 'bg-slate-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
          }`}
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Resume...
            </span>
          ) : 'Upload & Start Matching'}
        </button>
      </div>
    </div>
  );
};

export default ResumeUpload;
