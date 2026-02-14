/**
 * Main application component.
 * Orchestrates resume upload and match display flow.
 */
import React, { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import ResultsView from './components/ResultsView';
import { generateMatches } from './services/api';

function App() {
  const [uploadedResume, setUploadedResume] = useState(null);
  const [matchData, setMatchData] = useState(null);
  const [isGeneratingMatches, setIsGeneratingMatches] = useState(false);
  const [error, setError] = useState(null);

  const handleUploadSuccess = async (resumeData) => {
    setUploadedResume(resumeData);
    setError(null);
    
    // Automatically generate matches
    try {
      setIsGeneratingMatches(true);
      const matches = await generateMatches(resumeData.id);
      setMatchData(matches);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to generate matches');
    } finally {
      setIsGeneratingMatches(false);
    }
  };

  const handleReset = () => {
    setUploadedResume(null);
    setMatchData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🎯 AI Resume-Job Matcher
          </h1>
          <p className="text-xl text-white opacity-90">
            Upload your resume and find your perfect job match using AI
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {!uploadedResume ? (
            // Upload Phase
            <ResumeUpload onUploadSuccess={handleUploadSuccess} />
          ) : (
            // Results Phase
            <div>
              {/* Success Banner */}
              <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="bg-green-100 rounded-full p-3">
                      <svg
                        className="w-6 h-6 text-green-600"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800">
                        Resume Uploaded Successfully!
                      </h3>
                      <p className="text-sm text-gray-600">
                        {uploadedResume.message}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={handleReset}
                    className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    Upload Another
                  </button>
                </div>
              </div>

              {/* Loading State */}
              {isGeneratingMatches && (
                <div className="bg-white rounded-lg shadow-lg p-12 text-center">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary mx-auto mb-4"></div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    Finding Your Perfect Matches...
                  </h3>
                  <p className="text-gray-600">
                    Our AI is analyzing thousands of job postings to find the best fits for you
                  </p>
                </div>
              )}

              {/* Error State */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-semibold text-red-800 mb-2">
                    ⚠️ Error Generating Matches
                  </h3>
                  <p className="text-red-600">{error}</p>
                </div>
              )}

              {/* Results */}
              {matchData && !isGeneratingMatches && (
                <ResultsView matchData={matchData} />
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-white opacity-75">
          <p className="text-sm">
            Built with ❤️ using FastAPI, React, and Sentence-Transformers
          </p>
          <p className="text-xs mt-2">
            B.Tech IT Mini-Project • 2024
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
