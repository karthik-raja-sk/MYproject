import React, { useState, useEffect } from 'react';
import { matchService } from '../services/api';

const MatchHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await matchService.getHistory();
        setHistory(data);
      } catch (err) {
        console.error("Failed to fetch match history");
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <div>Loading results...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800 mb-2">My Best Job Matches</h1>
      <p className="text-slate-500 mb-8">AI-powered analysis of your resume against current openings</p>

      <div className="space-y-6">
        {history.map((match, idx) => (
          <div key={idx} className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-6">
              <div className="flex flex-col md:flex-row justify-between gap-6">
                
                {/* Job Info */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="bg-blue-100 text-blue-600 px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider">
                      {match.overall_score >= 80 ? '🔥 Hot Match' : 'Potential Match'}
                    </span>
                    <span className="text-slate-400 text-sm">📍 {match.location || 'Remote'}</span>
                  </div>
                  <h3 className="text-2xl font-bold text-slate-800">{match.job_title}</h3>
                  <p className="text-slate-600 text-lg mb-4">{match.company}</p>
                  
                  <blockquote className="border-l-4 border-slate-100 pl-4 py-1 text-slate-500 text-sm mb-6 bg-slate-50 rounded-r-lg italic">
                    "{match.explanation}"
                  </blockquote>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div>
                      <p className="text-sm font-bold text-slate-700 mb-2 flex items-center gap-2">
                        <span className="text-green-500">✅</span> Matched Skills
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {match.matching_skills?.map((skill, sIdx) => (
                          <span key={sIdx} className="bg-green-50 text-green-700 border border-green-100 px-3 py-1 rounded-lg text-xs font-semibold">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-sm font-bold text-slate-700 mb-2 flex items-center gap-2">
                        <span className="text-orange-400">⚡</span> Skill Gaps
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {match.missing_skills?.map((skill, sIdx) => (
                          <span key={sIdx} className="bg-orange-50 text-orange-700 border border-orange-100 px-3 py-1 rounded-lg text-xs font-semibold text-opacity-80">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Score Circle/Bar */}
                <div className="w-full md:w-64 flex flex-col items-center justify-center p-6 bg-slate-50 rounded-2xl border border-slate-100">
                  <div className="relative w-32 h-32 flex items-center justify-center mb-4">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="64"
                        cy="64"
                        r="58"
                        stroke="currentColor"
                        strokeWidth="10"
                        fill="transparent"
                        className="text-slate-200"
                      />
                      <circle
                        cx="64"
                        cy="64"
                        r="58"
                        stroke="currentColor"
                        strokeWidth="10"
                        fill="transparent"
                        strokeDasharray={364}
                        strokeDashoffset={364 - (364 * match.overall_score) / 100}
                        className={match.overall_score >= 80 ? 'text-green-500' : match.overall_score >= 60 ? 'text-blue-500' : 'text-orange-500'}
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-3xl font-black text-slate-800">{match.overall_score.toFixed(0)}%</span>
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">Match</span>
                    </div>
                  </div>
                  
                  <div className="w-full space-y-3">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-500">Semantic AI</span>
                      <span className="font-bold text-slate-700">{(match.semantic_similarity * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-200 h-1.5 rounded-full">
                      <div className="bg-blue-400 h-full rounded-full" style={{ width: `${match.semantic_similarity * 100}%` }}></div>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-500">Skill Overlap</span>
                      <span className="font-bold text-slate-700">{match.skill_match_score.toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-200 h-1.5 rounded-full">
                      <div className="bg-purple-400 h-full rounded-full" style={{ width: `${match.skill_match_score}%` }}></div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        ))}

        {history.length === 0 && (
          <div className="py-20 text-center bg-white rounded-2xl border border-dashed border-slate-200">
            <div className="text-6xl mb-6">🔍</div>
            <h3 className="text-xl font-bold text-slate-800 mb-2">No matches found yet</h3>
            <p className="text-slate-500 mb-8">Upload a new resume to see how you stack up against current jobs.</p>
            <button className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-blue-700 transition-all">
              Upload Resume
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchHistory;
