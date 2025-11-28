import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const SymptomChecker = () => {
    const [formData, setFormData] = useState({
        symptoms: '',
        age: '',
        gender: ''
    });
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResult(null);

        try {
            const response = await fetch('http://localhost:8000/api/symptoms/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    symptoms: formData.symptoms,
                    age: formData.age ? parseInt(formData.age) : null,
                    gender: formData.gender || null
                }),
            });

            if (response.ok) {
                const data = await response.json();
                setResult(data);
            } else {
                throw new Error('Failed to analyze symptoms');
            }
        } catch (error) {
            setResult({
                possible_conditions: ['Unable to analyze symptoms. Please ensure the backend is running.'],
                recommendations: 'Please try again later or consult a healthcare professional.',
                severity: 'medium'
            });
        } finally {
            setIsLoading(false);
        }
    };

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'low':
                return 'bg-green-100 text-green-800 border-green-300';
            case 'high':
                return 'bg-red-100 text-red-800 border-red-300';
            default:
                return 'bg-yellow-100 text-yellow-800 border-yellow-300';
        }
    };

    const getSeverityIcon = (severity) => {
        switch (severity) {
            case 'low':
                return '✓';
            case 'high':
                return '⚠';
            default:
                return 'ℹ';
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-purple-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-500 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">Symptom Checker</span>
                    </Link>
                    <Link to="/" className="text-purple-600 hover:text-purple-700 font-medium flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </Link>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-4xl mx-auto p-6">
                {/* Header Section */}
                <div className="text-center mb-10 mt-8">
                    <div className="inline-block p-4 bg-gradient-to-br from-purple-600 to-pink-500 rounded-full mb-4">
                        <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                        </svg>
                    </div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-3">AI Symptom Checker</h1>
                    <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                        Describe your symptoms and get AI-powered insights about possible conditions and recommendations.
                    </p>
                </div>

                {/* Form */}
                <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-purple-100">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label htmlFor="symptoms" className="block text-sm font-semibold text-gray-700 mb-2">
                                Describe Your Symptoms *
                            </label>
                            <textarea
                                id="symptoms"
                                name="symptoms"
                                value={formData.symptoms}
                                onChange={handleChange}
                                rows="5"
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                placeholder="E.g., I have a headache, fever, and sore throat for the past 2 days..."
                                required
                            />
                            <p className="text-xs text-gray-500 mt-2">Be as detailed as possible for better analysis</p>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6">
                            <div>
                                <label htmlFor="age" className="block text-sm font-semibold text-gray-700 mb-2">
                                    Age (Optional)
                                </label>
                                <input
                                    type="number"
                                    id="age"
                                    name="age"
                                    value={formData.age}
                                    onChange={handleChange}
                                    min="0"
                                    max="120"
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                    placeholder="Enter your age"
                                />
                            </div>

                            <div>
                                <label htmlFor="gender" className="block text-sm font-semibold text-gray-700 mb-2">
                                    Gender (Optional)
                                </label>
                                <select
                                    id="gender"
                                    name="gender"
                                    value={formData.gender}
                                    onChange={handleChange}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                                >
                                    <option value="">Select gender</option>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading || !formData.symptoms.trim()}
                            className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-pink-600 focus:outline-none focus:ring-4 focus:ring-purple-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            {isLoading ? (
                                <span className="flex items-center justify-center">
                                    <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                    </svg>
                                    Analyzing Symptoms...
                                </span>
                            ) : (
                                '🔍 Analyze Symptoms'
                            )}
                        </button>
                    </form>

                    <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-sm text-yellow-800 flex items-start">
                            <svg className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                            <span>
                                <strong>Important:</strong> This tool provides general information only and is not a substitute for professional medical advice.
                                If you're experiencing a medical emergency, call emergency services immediately.
                            </span>
                        </p>
                    </div>
                </div>

                {/* Results */}
                {result && (
                    <div className="bg-white rounded-2xl shadow-xl p-8 border border-purple-100 animate-fade-in">
                        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                            <svg className="w-8 h-8 mr-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Analysis Results
                        </h2>

                        {/* Severity Badge */}
                        <div className="mb-6">
                            <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold border-2 ${getSeverityColor(result.severity)}`}>
                                <span className="text-xl mr-2">{getSeverityIcon(result.severity)}</span>
                                Severity: {result.severity.charAt(0).toUpperCase() + result.severity.slice(1)}
                            </span>
                        </div>

                        {/* Possible Conditions */}
                        <div className="mb-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                                <svg className="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                                Possible Conditions
                            </h3>
                            <ul className="space-y-2">
                                {result.possible_conditions.map((condition, index) => (
                                    <li key={index} className="flex items-start p-3 bg-purple-50 rounded-lg border border-purple-100">
                                        <span className="text-purple-600 mr-2 mt-0.5">•</span>
                                        <span className="text-gray-700">{condition}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* Recommendations */}
                        <div className="mb-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                                <svg className="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                Recommendations
                            </h3>
                            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                                <p className="text-gray-700 leading-relaxed">{result.recommendations}</p>
                            </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex flex-col sm:flex-row gap-4 mt-8">
                            <Link
                                to="/chatbot"
                                className="flex-1 py-3 px-6 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-600 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all text-center shadow-lg hover:shadow-xl"
                            >
                                💬 Chat with AI Doctor
                            </Link>
                            <Link
                                to="/appointments"
                                className="flex-1 py-3 px-6 bg-gradient-to-r from-purple-600 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-pink-600 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all text-center shadow-lg hover:shadow-xl"
                            >
                                📅 Book Appointment
                            </Link>
                        </div>

                        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-sm text-red-800 flex items-start">
                                <svg className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                </svg>
                                <span>
                                    <strong>Disclaimer:</strong> This analysis is AI-generated and should not be considered a medical diagnosis.
                                    Always consult with a qualified healthcare professional for accurate diagnosis and treatment.
                                </span>
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SymptomChecker;
