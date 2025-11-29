import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../../components/Navbar';

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
    const userName = localStorage.getItem('userName') || 'User';

    const config = {
        headers: { Authorization: `Bearer ${token}` }
    };

    useEffect(() => {
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
                // setError('No health data found. Please upload your Apple Health export.');
                // Allow rendering even without data for the new dashboard layout
                setDashboardData({
                    profile: {},
                    today_stats: { steps: 0, sleep_duration: 0, active_calories: 0, heart_rate: 0 },
                    week_trends: { daily_steps: [], daily_sleep: [], total_steps: 0, avg_sleep: 0 },
                    month_averages: { avg_steps: 0, avg_sleep: 0, avg_heart_rate: 0 }
                });
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
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center transition-colors duration-300">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600 dark:text-gray-300 text-lg">Loading your command center...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
            <Navbar />

            <div className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
                {/* Welcome Section */}
                <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                            Good Morning, {userName.split(' ')[0]}! 👋
                        </h1>
                        <p className="text-gray-500 dark:text-gray-400 mt-1">
                            Here's your daily health overview. You're doing great!
                        </p>
                    </div>
                    <div className="mt-4 md:mt-0 flex space-x-3">
                        <Link to="/chatbot" className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg shadow-md transition-colors">
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                            Ask AI Doctor
                        </Link>
                        <Link to="/appointments" className="inline-flex items-center px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 text-sm font-medium rounded-lg shadow-sm transition-colors">
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            Book Appointment
                        </Link>
                    </div>
                </div>

                {/* Quick Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {/* Steps Card */}
                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                            </div>
                            <span className="text-xs font-medium text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-2 py-1 rounded-full">+12% vs yest</span>
                        </div>
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Steps Taken</h3>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                            {dashboardData?.today_stats?.steps?.toLocaleString() || '0'}
                        </p>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-4">
                            <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '65%' }}></div>
                        </div>
                    </div>

                    {/* Sleep Card */}
                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                                </svg>
                            </div>
                            <span className="text-xs font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20 px-2 py-1 rounded-full">Optimal</span>
                        </div>
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Sleep Duration</h3>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                            {dashboardData?.today_stats?.sleep_duration ? formatDuration(dashboardData.today_stats.sleep_duration) : '0h 0m'}
                        </p>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-4">
                            <div className="bg-indigo-500 h-1.5 rounded-full" style={{ width: '85%' }}></div>
                        </div>
                    </div>

                    {/* Heart Rate Card */}
                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-red-100 dark:bg-red-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                </svg>
                            </div>
                            <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Avg BPM</span>
                        </div>
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Heart Rate</h3>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                            {dashboardData?.today_stats?.heart_rate || '--'} <span className="text-sm font-normal text-gray-500">bpm</span>
                        </p>
                        <div className="mt-4 flex items-center space-x-2">
                            <span className="flex h-2 w-2 relative">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                            </span>
                            <span className="text-xs text-gray-500">Live monitoring active</span>
                        </div>
                    </div>

                    {/* Calories Card */}
                    <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
                                <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
                                </svg>
                            </div>
                        </div>
                        <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Active Calories</h3>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                            {dashboardData?.today_stats?.active_calories || '0'} <span className="text-sm font-normal text-gray-500">kcal</span>
                        </p>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-4">
                            <div className="bg-orange-500 h-1.5 rounded-full" style={{ width: '45%' }}></div>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left Column: Appointments & Medications */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Upcoming Appointments */}
                        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-lg font-bold text-gray-900 dark:text-white">Upcoming Appointments</h2>
                                <Link to="/appointments" className="text-sm text-blue-600 hover:text-blue-700 font-medium">View All</Link>
                            </div>

                            {/* Placeholder for appointments list */}
                            <div className="space-y-4">
                                <div className="flex items-start p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-100 dark:border-blue-800">
                                    <div className="flex-shrink-0">
                                        <div className="w-12 h-12 bg-blue-100 dark:bg-blue-800 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-300 font-bold text-lg">
                                            28
                                        </div>
                                        <div className="text-center text-xs font-medium text-blue-600 dark:text-blue-300 mt-1">NOV</div>
                                    </div>
                                    <div className="ml-4 flex-1">
                                        <h3 className="text-sm font-bold text-gray-900 dark:text-white">Dr. Sarah Wilson</h3>
                                        <p className="text-xs text-gray-500 dark:text-gray-400">Cardiologist • Video Consultation</p>
                                        <div className="mt-2 flex items-center text-xs text-gray-500 dark:text-gray-400">
                                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                            10:00 AM - 10:30 AM
                                        </div>
                                    </div>
                                    <button className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium rounded-lg transition-colors">
                                        Join Call
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* Medications */}
                        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-lg font-bold text-gray-900 dark:text-white">Medications Due</h2>
                                <Link to="/medications" className="text-sm text-blue-600 hover:text-blue-700 font-medium">Manage</Link>
                            </div>

                            <div className="space-y-3">
                                <div className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition-colors border border-gray-100 dark:border-gray-700">
                                    <div className="flex items-center">
                                        <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center text-purple-600 dark:text-purple-400">
                                            💊
                                        </div>
                                        <div className="ml-3">
                                            <p className="text-sm font-medium text-gray-900 dark:text-white">Amoxicillin</p>
                                            <p className="text-xs text-gray-500 dark:text-gray-400">500mg • Take with food</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center">
                                        <span className="text-xs font-medium text-orange-500 bg-orange-50 dark:bg-orange-900/20 px-2 py-1 rounded-full mr-3">Due 2:00 PM</span>
                                        <button className="text-gray-400 hover:text-green-600 transition-colors">
                                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Upload & Profile */}
                    <div className="space-y-8">
                        {/* Profile Summary */}
                        <div className="bg-gradient-to-br from-blue-600 to-cyan-600 rounded-2xl shadow-lg p-6 text-white">
                            <div className="flex items-center space-x-4 mb-6">
                                <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center text-2xl font-bold border-2 border-white/30">
                                    {dashboardData?.profile?.biological_sex?.charAt(0) || 'U'}
                                </div>
                                <div>
                                    <h2 className="text-xl font-bold">{userName}</h2>
                                    <p className="text-blue-100 text-sm">Premium Member</p>
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                                    <p className="text-blue-100 text-xs">Blood Type</p>
                                    <p className="text-lg font-bold">{dashboardData?.profile?.blood_type || 'N/A'}</p>
                                </div>
                                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                                    <p className="text-blue-100 text-xs">Age</p>
                                    <p className="text-lg font-bold">{calculateAge(dashboardData?.profile?.date_of_birth) || 'N/A'}</p>
                                </div>
                                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                                    <p className="text-blue-100 text-xs">Height</p>
                                    <p className="text-lg font-bold">{dashboardData?.profile?.height ? `${dashboardData.profile.height}cm` : 'N/A'}</p>
                                </div>
                                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">
                                    <p className="text-blue-100 text-xs">Weight</p>
                                    <p className="text-lg font-bold">{dashboardData?.profile?.current_weight ? `${dashboardData.profile.current_weight}kg` : 'N/A'}</p>
                                </div>
                            </div>
                            <Link to="/profile-settings" className="mt-6 block w-full py-2 bg-white text-blue-600 text-center text-sm font-bold rounded-lg hover:bg-blue-50 transition-colors">
                                Edit Profile
                            </Link>
                        </div>

                        {/* Data Upload Widget */}
                        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6">
                            <h3 className="text-sm font-bold text-gray-900 dark:text-white mb-4">Sync Health Data</h3>
                            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                    <svg className="w-8 h-8 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                    </svg>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">
                                        <span className="font-semibold">Click to upload</span> Apple Health XML
                                    </p>
                                </div>
                                <input
                                    type="file"
                                    className="hidden"
                                    accept=".xml"
                                    onChange={handleFileUpload}
                                    disabled={uploading}
                                />
                            </label>
                            {uploadStatus && (
                                <p className="mt-2 text-xs text-green-600 dark:text-green-400 text-center">{uploadStatus}</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HealthDashboard;
