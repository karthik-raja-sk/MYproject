/**
 * Match results dashboard.
 * Displays job matches with scores and skill gap analysis.
 */
import React from 'react';

const ResultsView = ({ matchData }) => {
  if (!matchData || matchData.total_matches === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No matches found</p>
      </div>
    );
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-blue-600 bg-blue-100';
    if (score >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreBadge = (score) => {
    if (score >= 80) return '🎯 Excellent Match';
    if (score >= 60) return '✅ Good Match';
    if (score >= 40) return '⚡ Fair Match';
    return '📊 Stretch Goal';
  };

  return (
    <div className="w-full max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Match Results for {matchData.resume_filename}
        </h2>
        <p className="text-gray-600">
          Found <span className="font-semibold text-primary">{matchData.total_matches}</span> matching jobs
        </p>
      </div>

      {/* Match Cards */}
      <div className="space-y-6">
        {matchData.matches.map((match, index) => (
          <div
            key={match.id}
            className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
          >
            {/* Card Header */}
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-2xl font-bold text-gray-400">#{index + 1}</span>
                    <h3 className="text-xl font-bold text-gray-800">{match.job_title}</h3>
                  </div>
                  <p className="text-gray-600 mb-1">
                    🏢 {match.company} • 📍 {match.location}
                  </p>
                </div>

                {/* Overall Score */}
                <div className="text-center ml-4">
                  <div className={`text-4xl font-bold px-6 py-3 rounded-lg ${getScoreColor(match.overall_score)}`}>
                    {match.overall_score.toFixed(0)}%
                  </div>
                  <p className="text-xs text-gray-500 mt-2">{getScoreBadge(match.overall_score)}</p>
                </div>
              </div>
            </div>

            {/* Match Details */}
            <div className="p-6 bg-gray-50">
              {/* Score Breakdown */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <p className="text-sm text-gray-500 mb-1">Semantic Match</p>
                  <div className="flex items-center">
                    <div className="flex-1">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-500 h-2 rounded-full"
                          style={{ width: `${match.semantic_similarity * 100}%` }}
                        />
                      </div>
                    </div>
                    <span className="ml-3 font-semibold text-gray-700">
                      {(match.semantic_similarity * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <p className="text-sm text-gray-500 mb-1">Skill Match</p>
                  <div className="flex items-center">
                    <div className="flex-1">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${match.skill_match_score}%` }}
                        />
                      </div>
                    </div>
                    <span className="ml-3 font-semibold text-gray-700">
                      {match.skill_match_score.toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* AI Explanation */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <p className="text-sm text-gray-700 leading-relaxed">
                  <span className="font-semibold text-blue-900">AI Analysis:</span> {match.explanation}
                </p>
              </div>

              {/* Skills Breakdown */}
              <div className="grid grid-cols-2 gap-4">
                {/* Matching Skills */}
                <div>
                  <h4 className="font-semibold text-green-900 mb-3 flex items-center">
                    <span className="mr-2">✅</span> Matching Skills ({match.matching_skills.length})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {match.matching_skills.length > 0 ? (
                      match.matching_skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-gray-500 italic">No matching skills</p>
                    )}
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <h4 className="font-semibold text-red-900 mb-3 flex items-center">
                    <span className="mr-2">📚</span> Skills to Learn ({match.missing_skills.length})
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {match.missing_skills.length > 0 ? (
                      match.missing_skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-gray-500 italic">No skill gaps!</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <div className="mt-6 pt-4 border-t border-gray-200">
                <button className="w-full bg-primary hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
                  View Full Job Details →
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsView;
