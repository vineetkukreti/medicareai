import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const ProfileSettings = () => {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [uploadProgress, setUploadProgress] = useState('');
    const [activeTab, setActiveTab] = useState('profile');
    const [profileData, setProfileData] = useState({
        full_name: '',
        email: '',
        phone_number: '',
        date_of_birth: '',
        gender: '',
        address: '',
        emergency_contact_name: '',
        emergency_contact_phone: ''
    });

    // Get userId from localStorage with validation
    const getUserId = () => {
        const id = localStorage.getItem('userId');
        if (!id || id === 'undefined' || id === 'null') {
            return null;
        }
        return id;
    };

    const userId = getUserId();

    const navigate = useNavigate();

    useEffect(() => {
        // Check if userId is valid
        if (!userId) {
            setError('User session not found. Please log in again.');
            setLoading(false);
            // Redirect is handled by the render return now, but we can keep this for auto-redirect
            const timer = setTimeout(() => {
                navigate('/login');
            }, 2000);
            return () => clearTimeout(timer);
        }

        // Check URL params for tab
        const params = new URLSearchParams(window.location.search);
        const tab = params.get('tab');
        if (tab === 'health-data') {
            setActiveTab('health-data');
        }
        fetchProfile();
    }, [userId, navigate]);

    const fetchProfile = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`http://localhost:8000/api/profile/${userId}`);
            setProfileData({
                full_name: response.data.full_name || '',
                email: response.data.email || '',
                phone_number: response.data.phone_number || '',
                date_of_birth: response.data.date_of_birth || '',
                gender: response.data.gender || '',
                address: response.data.address || '',
                emergency_contact_name: response.data.emergency_contact_name || '',
                emergency_contact_phone: response.data.emergency_contact_phone || ''
            });
            setError('');
        } catch (err) {
            setError('Failed to load profile data.');
            console.error('Error fetching profile:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setProfileData({
            ...profileData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setError('');
        setSuccess('');

        try {
            await axios.put(
                `http://localhost:8000/api/profile/${userId}`,
                {
                    full_name: profileData.full_name,
                    phone_number: profileData.phone_number,
                    date_of_birth: profileData.date_of_birth || null,
                    gender: profileData.gender,
                    address: profileData.address,
                    emergency_contact_name: profileData.emergency_contact_name,
                    emergency_contact_phone: profileData.emergency_contact_phone
                }
            );
            setSuccess('Profile updated successfully!');
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError('Failed to update profile. Please try again.');
            console.error('Error updating profile:', err);
        } finally {
            setSaving(false);
        }
    };

    const handleHealthDataUpload = async (event) => {
        const files = event.target.files;
        if (!files || files.length === 0) return;

        // Validate all files are XML
        for (let file of files) {
            if (!file.name.endsWith('.xml')) {
                setError('Please upload only XML files from Apple Health export.');
                return;
            }
        }

        setUploading(true);
        setUploadProgress(`Uploading ${files.length} file(s)...`);
        setError('');
        setSuccess('');

        let successCount = 0;
        let failCount = 0;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            setUploadProgress(`Processing ${file.name} (${i + 1}/${files.length})...`);

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await axios.post(
                    `http://localhost:8000/api/health/upload?user_id=${userId}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                        },
                    }
                );
                successCount++;
            } catch (err) {
                console.error(`Error uploading ${file.name}:`, err);
                failCount++;
            }
        }

        setUploading(false);
        setUploadProgress('');

        if (successCount > 0 && failCount === 0) {
            setSuccess(`Successfully uploaded ${successCount} file(s)! Your health data has been imported.`);
        } else if (successCount > 0 && failCount > 0) {
            setSuccess(`Uploaded ${successCount} file(s). ${failCount} file(s) failed.`);
        } else {
            setError('Failed to upload health data. Please try again.');
        }

        // Clear file input
        event.target.value = '';

        setTimeout(() => {
            setSuccess('');
        }, 5000);
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600 text-lg">Loading profile...</p>
                </div>
            </div>
        );
    }

    // If no userId, don't render the form (useEffect will redirect)
    if (!userId) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 flex items-center justify-center">
                <div className="text-center p-8 bg-white rounded-2xl shadow-xl">
                    <div className="text-red-500 text-xl font-bold mb-4">Session Expired</div>
                    <p className="text-gray-600 mb-4">Please log in again to access your profile.</p>
                    <Link to="/login" className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        Go to Login
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-blue-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">Profile Settings</span>
                    </Link>
                    <Link to="/" className="text-blue-600 hover:text-blue-700 font-medium flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </Link>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-4xl mx-auto p-6">
                <div className="text-center mb-8 mt-8">
                    <div className="inline-block p-4 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-full mb-4">
                        <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                    </div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-3">Profile Settings</h1>
                    <p className="text-lg text-gray-600">Manage your personal information and emergency contacts</p>
                </div>

                {/* Success Message */}
                {success && (
                    <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        {success}
                    </div>
                )}

                {/* Error Message */}
                {error && (
                    <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        {error}
                    </div>
                )}

                {/* Upload Progress */}
                {uploadProgress && (
                    <div className="mb-6 p-4 bg-blue-100 border border-blue-400 text-blue-700 rounded-lg flex items-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-700 mr-2"></div>
                        {uploadProgress}
                    </div>
                )}

                {/* Tab Navigation */}
                <div className="mb-6">
                    <div className="border-b border-gray-200">
                        <nav className="-mb-px flex space-x-8">
                            <button
                                onClick={() => setActiveTab('profile')}
                                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'profile'
                                    ? 'border-blue-600 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                            >
                                <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                Profile Information
                            </button>
                            <button
                                onClick={() => setActiveTab('health-data')}
                                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'health-data'
                                    ? 'border-green-600 text-green-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                            >
                                <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                                Health Data Upload
                            </button>
                        </nav>
                    </div>
                </div>

                {/* Profile Tab */}
                {activeTab === 'profile' && (
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Personal Information Section */}
                        <div className="bg-white rounded-2xl shadow-xl p-8 border border-blue-100">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                                <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                Personal Information
                            </h2>

                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label>
                                    <input
                                        type="text"
                                        name="full_name"
                                        value={profileData.full_name}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Email (Read-only)</label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={profileData.email}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                                        disabled
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Phone Number</label>
                                    <input
                                        type="tel"
                                        name="phone_number"
                                        value={profileData.phone_number}
                                        onChange={handleChange}
                                        placeholder="+1 (555) 123-4567"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Date of Birth</label>
                                    <input
                                        type="date"
                                        name="date_of_birth"
                                        value={profileData.date_of_birth}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Gender</label>
                                    <select
                                        name="gender"
                                        value={profileData.gender}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        <option value="">Select gender</option>
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                        <option value="Other">Other</option>
                                        <option value="Prefer not to say">Prefer not to say</option>
                                    </select>
                                </div>

                                <div className="md:col-span-2">
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Address</label>
                                    <textarea
                                        name="address"
                                        value={profileData.address}
                                        onChange={handleChange}
                                        rows="3"
                                        placeholder="Street address, city, state, ZIP code"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Emergency Contact Section */}
                        <div className="bg-white rounded-2xl shadow-xl p-8 border border-blue-100">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                                <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                Emergency Contact
                            </h2>

                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Contact Name</label>
                                    <input
                                        type="text"
                                        name="emergency_contact_name"
                                        value={profileData.emergency_contact_name}
                                        onChange={handleChange}
                                        placeholder="Emergency contact full name"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Contact Phone</label>
                                    <input
                                        type="tel"
                                        name="emergency_contact_phone"
                                        value={profileData.emergency_contact_phone}
                                        onChange={handleChange}
                                        placeholder="+1 (555) 987-6543"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Save Button */}
                        <div className="flex justify-end space-x-4">
                            <Link
                                to="/"
                                className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-all"
                            >
                                Cancel
                            </Link>
                            <button
                                type="submit"
                                disabled={saving}
                                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-600 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {saving ? 'Saving...' : 'Save Changes'}
                            </button>
                        </div>
                    </form>
                )}

                {/* Health Data Upload Tab */}
                {activeTab === 'health-data' && (
                    <div className="space-y-6">
                        {/* Upload Section */}
                        <div className="bg-white rounded-2xl shadow-xl p-8 border border-blue-100">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                                <svg className="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                                Upload Apple Health Data
                            </h2>

                            <div className="mb-6">
                                <p className="text-gray-600 mb-4">
                                    Upload your Apple Health export files to import your health data including sleep, activity, vitals, and more.
                                </p>
                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                                    <h3 className="font-semibold text-blue-900 mb-2">How to export from Apple Health:</h3>
                                    <ol className="list-decimal list-inside text-sm text-blue-800 space-y-1">
                                        <li>Open the Health app on your iPhone</li>
                                        <li>Tap your profile picture in the top right</li>
                                        <li>Scroll down and tap "Export All Health Data"</li>
                                        <li>Save the export and upload the XML file(s) here</li>
                                    </ol>
                                </div>
                            </div>

                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-green-500 transition-colors">
                                <input
                                    type="file"
                                    id="health-data-upload"
                                    accept=".xml"
                                    multiple
                                    onChange={handleHealthDataUpload}
                                    disabled={uploading}
                                    className="hidden"
                                />
                                <label
                                    htmlFor="health-data-upload"
                                    className="cursor-pointer"
                                >
                                    <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                    </svg>
                                    <p className="text-lg font-semibold text-gray-700 mb-2">
                                        {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
                                    </p>
                                    <p className="text-sm text-gray-500">
                                        Apple Health XML files (you can select multiple files)
                                    </p>
                                </label>
                            </div>
                        </div>

                        {/* Real-time Sync Section - Coming Soon */}
                        <div className="bg-white rounded-2xl shadow-xl p-8 border border-blue-100">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                                <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                </svg>
                                Real-time Device Sync
                                <span className="ml-3 px-3 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded-full">Coming Soon</span>
                            </h2>

                            <div className="space-y-4">
                                <p className="text-gray-600">
                                    Connect your Apple Watch or iPhone for automatic, real-time health data synchronization.
                                </p>

                                <div className="grid md:grid-cols-2 gap-4">
                                    <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                                        <div className="flex items-center mb-2">
                                            <svg className="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                            <h3 className="font-semibold text-gray-700">Apple Watch</h3>
                                        </div>
                                        <p className="text-sm text-gray-600">Automatic sync of heart rate, activity, and workout data</p>
                                    </div>

                                    <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                                        <div className="flex items-center mb-2">
                                            <svg className="w-6 h-6 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                            </svg>
                                            <h3 className="font-semibold text-gray-700">iPhone</h3>
                                        </div>
                                        <p className="text-sm text-gray-600">Continuous sync of all Health app data</p>
                                    </div>
                                </div>

                                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                                    <p className="text-sm text-blue-800">
                                        <strong>Note:</strong> Real-time sync will require the MediCareAI mobile app. We're working on bringing this feature to you soon!
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Quick Link to Dashboard */}
                        <div className="text-center">
                            <Link
                                to="/health-dashboard"
                                className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-500 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-600 focus:outline-none focus:ring-4 focus:ring-green-300 transition-all shadow-lg"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                                View Health Dashboard
                            </Link>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ProfileSettings;
