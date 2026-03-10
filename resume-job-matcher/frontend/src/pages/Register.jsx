import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    password: '',
    confirm_password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirm_password) {
      return setError("Passwords do not match");
    }
    
    setError('');
    setLoading(true);
    try {
      await register({
        email: formData.email,
        full_name: formData.full_name,
        password: formData.password
      });
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4">
      <div className="bg-white w-full max-w-md rounded-2xl shadow-2xl overflow-hidden my-12">
        <div className="p-8 text-center bg-purple-600 text-white">
          <h1 className="text-3xl font-bold">Create Account</h1>
          <p className="mt-2 text-purple-100">Join thousands of job seekers today</p>
        </div>
        
        <form onSubmit={handleSubmit} className="p-8 space-y-5">
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm border border-red-100">
              ⚠️ {error}
            </div>
          )}
          
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Full Name</label>
            <input
              type="text"
              name="full_name"
              required
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-purple-500 outline-none transition-all"
              placeholder="John Doe"
              value={formData.full_name}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Email Address</label>
            <input
              type="email"
              name="email"
              required
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-purple-500 outline-none transition-all"
              placeholder="name@company.com"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Password</label>
            <input
              type="password"
              name="password"
              required
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-purple-500 outline-none transition-all"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Confirm Password</label>
            <input
              type="password"
              name="confirm_password"
              required
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-purple-500 outline-none transition-all"
              placeholder="••••••••"
              value={formData.confirm_password}
              onChange={handleChange}
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 rounded-xl font-bold text-white shadow-lg transition-all ${
              loading ? 'bg-slate-400 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-700 active:scale-95'
            }`}
          >
            {loading ? 'Creating Account...' : 'Get Started'}
          </button>
          
          <p className="text-center text-slate-500 text-sm pt-4 border-t border-slate-100">
            Already have an account?{' '}
            <Link to="/login" className="text-purple-600 font-bold hover:underline">
              Log In
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Register;
