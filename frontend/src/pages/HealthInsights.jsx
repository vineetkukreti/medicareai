import React from 'react';
import { Link } from 'react-router-dom';

import HealthChat from '../components/HealthChat';

const HealthInsights = () => {
    const userId = localStorage.getItem('userId');

    return (
        <div className="min-h-screen bg-gradient-to-br from-teal-50 via-white to-cyan-50">
            <nav className="bg-white/90 backdrop-blur-md border-b border-teal-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-teal-600 to-cyan-500 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-cyan-500 bg-clip-text text-transparent">Health Insights</span>
                    </Link>
                    <Link to="/" className="text-teal-600 hover:text-teal-700 font-medium flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </Link>
                </div>
            </nav>

            <div className="max-w-4xl mx-auto p-6 mt-10">
                <div className="text-center mb-10">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">Your Personal Health Assistant</h1>
                    <p className="text-lg text-gray-600">Ask questions about your health records, medications, and appointments.</p>
                </div>

                {userId ? (
                    <HealthChat userId={userId} />
                ) : (
                    <div className="text-center p-8 bg-white rounded-2xl shadow-lg border border-red-100">
                        <p className="text-red-500">Please log in to access your health insights.</p>
                        <Link to="/login" className="inline-block mt-4 px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors">
                            Log In
                        </Link>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HealthInsights;
