import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const HealthDashboard = () => {
    const navigate = useNavigate();
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploading, setUploading] = useState(false);

    // Get userId from localStorage with validation
    const getUserId = () => {
        const id = localStorage.getItem('userId');
        if (!id || id === 'undefined' || id === 'null') {
            return null;
        }
        return id;
    };

    const userId = getUserId();
    const token = localStorage.getItem('token');

    const config = {
        headers: { Authorization: `Bearer ${token}` }
    };

    useEffect(() => {
        // Check if userId is valid
        if (!userId) {
            setError('User session not found. Please log in again.');
            setLoading(false);
            setTimeout(() => {
                navigate('/login');
            }, 2000);
            return;
        }
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            const response = await axios.get('http://localhost:8000/api/health/dashboard', config);
            setDashboardData(response.data);
            setError('');
        } catch (err) {
            if (err.response?.status === 404) {
                setError('No health data found. Please upload your Apple Health export.');
            } else {
                setError('Failed to load health data.');
            }
            console.error('Error fetching dashboard data:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.xml')) {
            setError('Please upload an XML file from Apple Health export.');
            return;
        }

        setUploading(true);
        setUploadStatus('Uploading and parsing health data...');
        setError('');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(
                'http://localhost:8000/api/health/upload',
                formData,
                {
                    headers: {
                        ...config.headers,
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            setUploadStatus(`Success! Imported ${response.data.summary.sleep_records} sleep records, ${response.data.summary.activity_records} activity records, and ${response.data.summary.vital_records} vital records.`);

            // Refresh dashboard data
            setTimeout(() => {
                fetchDashboardData();
                setUploadStatus('');
            }, 3000);
        } catch (err) {
            setError('Failed to upload health data. Please try again.');
            console.error('Error uploading file:', err);
        } finally {
            setUploading(false);
        }
    };

    const calculateBMI = (weight, height) => {
        if (!weight || !height) return null;
        const heightInMeters = height / 100;
        const bmi = weight / (heightInMeters * heightInMeters);
        return bmi.toFixed(1);
    };

    const calculateAge = (dob) => {
        if (!dob) return null;
        const birthDate = new Date(dob);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age;
    };

    const formatDuration = (minutes) => {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return `${hours}h ${mins}m`;
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-green-600 mx-auto mb-4"></div>
                    <p className="text-gray-600 text-lg">Loading health dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-green-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-500 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-500 bg-clip-text text-transparent">Health Dashboard</span>
                    </Link>
                    <Link to="/" className="text-green-600 hover:text-green-700 font-medium flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </Link>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto p-6">
                {/* Upload Section */}
                <div className="mb-8">
                    <div className="bg-white rounded-2xl shadow-lg p-6 border border-green-100">
                        <h2 className="text-xl font-bold text-gray-900 mb-4">Upload Apple Health Data</h2>
                        <div className="flex items-center space-x-4">
                            <label className="flex-1">
                                <input
                                    type="file"
                                    accept=".xml"
                                    onChange={handleFileUpload}
                                    disabled={uploading}
                                    className="hidden"
                                    id="health-file-upload"
                                />
                                <div className="cursor-pointer px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-500 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-600 transition-all text-center">
                                    {uploading ? 'Uploading...' : 'Choose File'}
                                </div>
                            </label>
                        </div>
                        {uploadStatus && (
                            <div className="mt-4 p-3 bg-green-100 text-green-700 rounded-lg">
                                {uploadStatus}
                            </div>
                        )}
                        {error && !dashboardData && (
                            <div className="mt-4 p-3 bg-yellow-100 text-yellow-700 rounded-lg">
                                {error}
                            </div>
                        )}
                    </div>
                </div>

                {dashboardData && dashboardData.profile && (
                    <>
                        {/* Profile Header */}
                        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-green-100">
                            <div className="flex items-center space-x-6">
                                <div className="w-24 h-24 bg-gradient-to-br from-green-600 to-emerald-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
                                    {dashboardData.profile.biological_sex?.charAt(0) || 'U'}
                                </div>
                                <div className="flex-1">
                                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Health Profile</h1>
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                        <div>
                                            <span className="text-gray-600">Age:</span>
                                            <span className="ml-2 font-semibold">{calculateAge(dashboardData.profile.date_of_birth) || 'N/A'}</span>
                                        </div>
                                        <div>
                                            <span className="text-gray-600">Blood Type:</span>
                                            <span className="ml-2 font-semibold">{dashboardData.profile.blood_type || 'N/A'}</span>
                                        </div>
                                        <div>
                                            <span className="text-gray-600">Height:</span>
                                            <span className="ml-2 font-semibold">{dashboardData.profile.height ? `${dashboardData.profile.height} cm` : 'N/A'}</span>
                                        </div>
                                        <div>
                                            <span className="text-gray-600">Weight:</span>
                                            <span className="ml-2 font-semibold">{dashboardData.profile.current_weight ? `${dashboardData.profile.current_weight} kg` : 'N/A'}</span>
                                        </div>
                                    </div>
                                    {dashboardData.profile.height && dashboardData.profile.current_weight && (
                                        <div className="mt-3">
                                            <span className="text-gray-600 text-sm">BMI:</span>
                                            <span className="ml-2 font-semibold text-lg text-green-600">
                                                {calculateBMI(dashboardData.profile.current_weight, dashboardData.profile.height)}
                                            </span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Today's Overview */}
                        <div className="mb-8">
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">Today's Overview</h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                                {/* Steps */}
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <div className="flex items-center justify-between mb-3">
                                        <h3 className="text-sm font-semibold text-gray-600">Steps</h3>
                                        <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                        </svg>
                                    </div>
                                    <p className="text-3xl font-bold text-gray-900">{dashboardData.today_stats.steps.toLocaleString()}</p>
                                    <p className="text-sm text-gray-500 mt-1">Goal: 10,000</p>
                                </div>

                                {/* Sleep */}
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <div className="flex items-center justify-between mb-3">
                                        <h3 className="text-sm font-semibold text-gray-600">Sleep</h3>
                                        <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                                        </svg>
                                    </div>
                                    <p className="text-3xl font-bold text-gray-900">
                                        {dashboardData.today_stats.sleep_duration ? formatDuration(dashboardData.today_stats.sleep_duration) : '0h 0m'}
                                    </p>
                                    <p className="text-sm text-gray-500 mt-1">Last night</p>
                                </div>

                                {/* Calories */}
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <div className="flex items-center justify-between mb-3">
                                        <h3 className="text-sm font-semibold text-gray-600">Active Calories</h3>
                                        <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
                                        </svg>
                                    </div>
                                    <p className="text-3xl font-bold text-gray-900">{dashboardData.today_stats.active_calories}</p>
                                    <p className="text-sm text-gray-500 mt-1">kcal burned</p>
                                </div>

                                {/* Heart Rate */}
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <div className="flex items-center justify-between mb-3">
                                        <h3 className="text-sm font-semibold text-gray-600">Heart Rate</h3>
                                        <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                        </svg>
                                    </div>
                                    <p className="text-3xl font-bold text-gray-900">
                                        {dashboardData.today_stats.heart_rate || '--'}
                                    </p>
                                    <p className="text-sm text-gray-500 mt-1">bpm</p>
                                </div>
                            </div>
                        </div>

                        {/* Week Trends */}
                        <div className="mb-8">
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">7-Day Trends</h2>
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {/* Steps Trend */}
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <h3 className="text-lg font-bold text-gray-900 mb-4">Daily Steps</h3>
                                    <div className="space-y-2">
                                        {dashboardData.week_trends.daily_steps.map((day, index) => (
                                            <div key={index} className="flex items-center">
                                                <span className="text-sm text-gray-600 w-24">{new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</span>
                                                <div className="flex-1 mx-3">
                                                    <div className="bg-gray-200 rounded-full h-6">
                                                        <div
                                                            className="bg-gradient-to-r from-green-600 to-emerald-500 h-6 rounded-full flex items-center justify-end pr-2"
                                                            style={{ width: `${Math.min((day.steps / 10000) * 100, 100)}%` }}
                                                        >
                                                            <span className="text-xs text-white font-semibold">{day.steps.toLocaleString()}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                    <div className="mt-4 pt-4 border-t border-gray-200">
                                        <p className="text-sm text-gray-600">Total: <span className="font-bold text-green-600">{dashboardData.week_trends.total_steps.toLocaleString()}</span> steps</p>
                                    </div>
                                </div>

                                {/* Sleep Trend */}
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <h3 className="text-lg font-bold text-gray-900 mb-4">Sleep Duration</h3>
                                    <div className="space-y-2">
                                        {dashboardData.week_trends.daily_sleep.map((day, index) => (
                                            <div key={index} className="flex items-center">
                                                <span className="text-sm text-gray-600 w-24">{new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</span>
                                                <div className="flex-1 mx-3">
                                                    <div className="bg-gray-200 rounded-full h-6">
                                                        <div
                                                            className="bg-gradient-to-r from-indigo-600 to-purple-500 h-6 rounded-full flex items-center justify-end pr-2"
                                                            style={{ width: `${Math.min((day.duration / 480) * 100, 100)}%` }}
                                                        >
                                                            <span className="text-xs text-white font-semibold">{formatDuration(day.duration)}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                    <div className="mt-4 pt-4 border-t border-gray-200">
                                        <p className="text-sm text-gray-600">Average: <span className="font-bold text-indigo-600">{formatDuration(Math.round(dashboardData.week_trends.avg_sleep))}</span></p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Month Averages */}
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">30-Day Averages</h2>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <h3 className="text-sm font-semibold text-gray-600 mb-2">Avg Steps/Day</h3>
                                    <p className="text-3xl font-bold text-green-600">{dashboardData.month_averages.avg_steps.toLocaleString()}</p>
                                </div>
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <h3 className="text-sm font-semibold text-gray-600 mb-2">Avg Sleep</h3>
                                    <p className="text-3xl font-bold text-indigo-600">{formatDuration(dashboardData.month_averages.avg_sleep)}</p>
                                </div>
                                <div className="bg-white rounded-xl shadow-lg p-6 border border-green-100">
                                    <h3 className="text-sm font-semibold text-gray-600 mb-2">Avg Heart Rate</h3>
                                    <p className="text-3xl font-bold text-red-600">
                                        {dashboardData.month_averages.avg_heart_rate || '--'} <span className="text-lg">bpm</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default HealthDashboard;
