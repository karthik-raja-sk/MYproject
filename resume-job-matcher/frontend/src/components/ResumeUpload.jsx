/**
 * Drag-and-drop resume upload component.
 * Handles file validation and upload progress.
 */
import React, { useState } from 'react';
import { uploadResume } from '../services/api';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const validateFile = (file) => {
    // Check file type
    if (!file.name.endsWith('.pdf')) {
      throw new Error('Only PDF files are allowed');
    }

    // Check file size (5MB limit)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (file.size > maxSize) {
      throw new Error('File size must be less than 5MB');
    }

    // Check if file is empty
    if (file.size === 0) {
      throw new Error('File is empty');
    }

    return true;
  };

  const handleFile = async (file) => {
    setError(null);
    setUploadProgress(0);

    try {
      // Validate file
      validateFile(file);

      // Start upload
      setIsUploading(true);
      setUploadProgress(30); // Simulated progress

      const response = await uploadResume(file);

      setUploadProgress(100);
      
      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess(response);
      }

      // Reset after success
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 1000);

    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className={`
          border-4 border-dashed rounded-lg p-12 text-center transition-all
          ${isDragging ? 'border-primary bg-blue-50 scale-105' : 'border-gray-300 bg-white'}
          ${isUploading ? 'opacity-60' : 'hover:border-primary cursor-pointer'}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && document.getElementById('file-input').click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileInput}
          disabled={isUploading}
        />

        {/* Upload Icon */}
        <div className="mb-4">
          <svg
            className="mx-auto h-16 w-16 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>

        {/* Text */}
        <div className="mb-4">
          <p className="text-xl font-semibold text-gray-700 mb-2">
            {isUploading ? 'Uploading Resume...' : 'Drop your resume here'}
          </p>
          <p className="text-sm text-gray-500">
            or click to browse • PDF only • Max 5MB
          </p>
        </div>

        {/* Progress Bar */}
        {isUploading && (
          <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600 font-medium">
              ⚠️ {error}
            </p>
          </div>
        )}

        {/* Upload Status */}
        {isUploading && (
          <div className="mt-4">
            <div className="inline-flex items-center space-x-2 text-primary">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary"></div>
              <span className="text-sm font-medium">Processing your resume...</span>
            </div>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Tips for best results:</h3>
        <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
          <li>Use a well-formatted PDF resume</li>
          <li>Include clear sections (Skills, Experience, Education)</li>
          <li>List technical skills explicitly</li>
          <li>Avoid scanned images (text must be selectable)</li>
        </ul>
      </div>
    </div>
  );
};

export default ResumeUpload;
