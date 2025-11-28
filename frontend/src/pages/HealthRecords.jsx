import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const HealthRecords = () => {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [showUploadModal, setShowUploadModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [recordToDelete, setRecordToDelete] = useState(null);
    const [selectedRecords, setSelectedRecords] = useState([]);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [filterType, setFilterType] = useState('');
    const [searchQuery, setSearchQuery] = useState('');

    // Form state
    const [formData, setFormData] = useState({
        record_type: '',
        title: '',
        description: '',
        record_date: '',
        file_url: '',
        other_type: ''  // For when "Other" is selected
    });
    const [selectedFile, setSelectedFile] = useState(null);

    const navigate = useNavigate();

    const recordTypes = [
        'Lab Result',
        'Prescription',
        'Diagnosis',
        'X-Ray',
        'MRI Scan',
        'CT Scan',
        'Blood Test',
        'Vaccination Record',
        'Medical Report',
        'Other'
    ];

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }
        fetchRecords();
    }, [navigate]);

    const fetchRecords = async () => {
        const token = localStorage.getItem('token');
        setLoading(true);
        try {
            const url = filterType
                ? `http://localhost:8000/api/health-records?record_type=${encodeURIComponent(filterType)}`
                : 'http://localhost:8000/api/health-records';

            const response = await fetch(url, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setRecords(data);
            }
        } catch (err) {
            setError('Failed to fetch health records');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRecords();
    }, [filterType]);

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file size (10MB max)
            if (file.size > 10 * 1024 * 1024) {
                setError('File size must be less than 10MB');
                return;
            }

            // Validate file type
            const allowedTypes = ['.pdf', '.jpg', '.jpeg', '.png', '.docx', '.doc'];
            const fileExt = '.' + file.name.split('.').pop().toLowerCase();
            if (!allowedTypes.includes(fileExt)) {
                setError('File type not allowed. Please upload PDF, JPG, PNG, or DOCX files.');
                return;
            }

            setSelectedFile(file);
            setError('');
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileSelect({ target: { files: [file] } });
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const uploadFile = async () => {
        if (!selectedFile) return null;

        const token = localStorage.getItem('token');
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('http://localhost:8000/api/health-records/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                return data.file_url;
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'File upload failed');
            }
        } catch (err) {
            throw err;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);
        setUploadProgress(0);

        const token = localStorage.getItem('token');

        try {
            // Upload file first if selected
            let fileUrl = formData.file_url;
            if (selectedFile) {
                setUploadProgress(50);
                fileUrl = await uploadFile();
            }

            setUploadProgress(75);

            // Use other_type if "Other" is selected
            const finalRecordType = formData.record_type === 'Other' && formData.other_type
                ? formData.other_type
                : formData.record_type;

            // Create health record
            const response = await fetch('http://localhost:8000/api/health-records', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    record_type: finalRecordType,
                    title: formData.title,
                    description: formData.description,
                    record_date: formData.record_date,
                    file_url: fileUrl
                })
            });

            if (response.ok) {
                setUploadProgress(100);
                setSuccess('Health record added successfully!');
                setFormData({
                    record_type: '',
                    title: '',
                    description: '',
                    record_date: '',
                    file_url: '',
                    other_type: ''
                });
                setSelectedFile(null);
                setShowUploadModal(false);
                fetchRecords();
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to create health record');
            }
        } catch (err) {
            setError('Error creating health record: ' + err.message);
        } finally {
            setLoading(false);
            setUploadProgress(0);
        }
    };


    const handleDeleteClick = (recordId) => {
        setRecordToDelete(recordId);
        setShowDeleteModal(true);
    };

    const confirmDelete = async () => {
        const token = localStorage.getItem('token');

        try {
            const response = await fetch(`http://localhost:8000/api/health-records/${recordToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                setSuccess('Health record deleted successfully');
                setSelectedRecords(selectedRecords.filter(id => id !== recordToDelete));
                fetchRecords();
            } else {
                setError('Failed to delete health record');
            }
        } catch (err) {
            setError('Error deleting health record');
        } finally {
            setShowDeleteModal(false);
            setRecordToDelete(null);
        }
    };

    const handleBulkDelete = async () => {
        if (selectedRecords.length === 0) {
            setError('Please select records to delete');
            return;
        }

        setRecordToDelete('bulk');
        setShowDeleteModal(true);
    };

    const confirmBulkDelete = async () => {
        const token = localStorage.getItem('token');

        try {
            const deletePromises = selectedRecords.map(recordId =>
                fetch(`http://localhost:8000/api/health-records/${recordId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
            );

            await Promise.all(deletePromises);
            setSuccess(`${selectedRecords.length} health record(s) deleted successfully`);
            setSelectedRecords([]);
            fetchRecords();
        } catch (err) {
            setError('Error deleting health records');
        } finally {
            setShowDeleteModal(false);
            setRecordToDelete(null);
        }
    };

    const toggleRecordSelection = (recordId) => {
        setSelectedRecords(prev =>
            prev.includes(recordId)
                ? prev.filter(id => id !== recordId)
                : [...prev, recordId]
        );
    };

    const toggleSelectAll = () => {
        if (selectedRecords.length === filteredRecords.length) {
            setSelectedRecords([]);
        } else {
            setSelectedRecords(filteredRecords.map(r => r.id));
        }
    };

    const handleDownload = (fileUrl, title) => {
        const token = localStorage.getItem('token');
        const fullUrl = `http://localhost:8000${fileUrl}`;

        // Create a temporary link and click it
        const link = document.createElement('a');
        link.href = fullUrl;
        link.download = title;
        link.target = '_blank';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const getRecordIcon = (type) => {
        const icons = {
            'Lab Result': '🧪',
            'Prescription': '💊',
            'Diagnosis': '🩺',
            'X-Ray': '🦴',
            'MRI Scan': '🧠',
            'CT Scan': '📊',
            'Blood Test': '🩸',
            'Vaccination Record': '💉',
            'Medical Report': '📋',
            'Other': '📄'
        };
        return icons[type] || '📄';
    };

    const filteredRecords = records.filter(record =>
        record.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        record.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-blue-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center shadow-md">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">Health Records</span>
                    </Link>
                    <Link to="/" className="text-blue-600 hover:text-blue-700 font-medium flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </Link>
                </div>
            </nav>

            <div className="max-w-6xl mx-auto p-6">
                {/* Success/Error Messages */}
                {success && (
                    <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                        </svg>
                        {success}
                    </div>
                )}

                {error && (
                    <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {error}
                    </div>
                )}

                {/* Actions Bar */}
                <div className="bg-white rounded-xl shadow-sm border border-blue-100 p-6 mb-6">
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div className="flex gap-3">
                            <button
                                onClick={() => setShowUploadModal(true)}
                                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-600 transition-all shadow-lg hover:shadow-xl flex items-center justify-center"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                                </svg>
                                Upload New Record
                            </button>

                            {selectedRecords.length > 0 && (
                                <button
                                    onClick={handleBulkDelete}
                                    className="px-6 py-3 bg-red-50 text-red-600 border-2 border-red-200 font-semibold rounded-lg hover:bg-red-100 transition-all flex items-center justify-center"
                                >
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                    Delete Selected ({selectedRecords.length})
                                </button>
                            )}
                        </div>

                        <div className="flex gap-4 items-center">
                            {filteredRecords.length > 0 && (
                                <label className="flex items-center gap-2 cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={selectedRecords.length === filteredRecords.length && filteredRecords.length > 0}
                                        onChange={toggleSelectAll}
                                        className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    />
                                    <span className="text-sm font-medium text-gray-700">Select All</span>
                                </label>
                            )}

                            <select
                                value={filterType}
                                onChange={(e) => setFilterType(e.target.value)}
                                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">All Types</option>
                                {recordTypes.map((type) => (
                                    <option key={type} value={type}>{type}</option>
                                ))}
                            </select>

                            <input
                                type="text"
                                placeholder="Search records..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                    </div>
                </div>

                {/* Records Grid */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                        <p className="mt-4 text-gray-600">Loading records...</p>
                    </div>
                ) : filteredRecords.length === 0 ? (
                    <div className="text-center py-16 bg-white rounded-xl shadow-sm border border-blue-100">
                        <svg className="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <p className="text-gray-500 text-lg">No health records found</p>
                        <p className="text-gray-400 text-sm mt-2">Upload your first medical document to get started</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredRecords.map((record) => (
                            <div key={record.id} className={`bg-white rounded-xl shadow-sm border ${selectedRecords.includes(record.id) ? 'border-blue-500 ring-1 ring-blue-500' : 'border-blue-100'} p-6 hover:shadow-lg transition-all relative`}>
                                <div className="absolute top-4 right-4">
                                    <input
                                        type="checkbox"
                                        checked={selectedRecords.includes(record.id)}
                                        onChange={() => toggleRecordSelection(record.id)}
                                        className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer"
                                    />
                                </div>

                                <div className="flex items-start justify-between mb-4 pr-8">
                                    <div className="text-4xl">{getRecordIcon(record.record_type)}</div>
                                </div>

                                <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full mb-3">
                                    {record.record_type}
                                </span>

                                <h3 className="text-lg font-bold text-gray-900 mb-2">{record.title}</h3>
                                <p className="text-sm text-gray-600 mb-3 line-clamp-2">{record.description}</p>
                                <p className="text-xs text-gray-500 mb-4">
                                    Date: {new Date(record.record_date).toLocaleDateString()}
                                </p>

                                <div className="flex gap-2">
                                    {record.file_url && (
                                        <button
                                            onClick={() => handleDownload(record.file_url, record.title)}
                                            className="flex-1 px-3 py-2 bg-blue-50 text-blue-600 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium flex items-center justify-center"
                                        >
                                            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                            </svg>
                                            Download
                                        </button>
                                    )}
                                    <button
                                        onClick={() => handleDeleteClick(record.id)}
                                        className="px-3 py-2 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium"
                                    >
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Upload Modal */}
            {showUploadModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="bg-gradient-to-r from-blue-600 to-cyan-500 p-6 rounded-t-2xl">
                            <div className="flex justify-between items-center">
                                <h2 className="text-2xl font-bold text-white">Upload Health Record</h2>
                                <button
                                    onClick={() => setShowUploadModal(false)}
                                    className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
                                >
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <form onSubmit={handleSubmit} className="p-6 space-y-6">
                            {/* File Upload Area */}
                            <div
                                onDrop={handleDrop}
                                onDragOver={handleDragOver}
                                className="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer"
                                onClick={() => document.getElementById('file-input').click()}
                            >
                                <input
                                    id="file-input"
                                    type="file"
                                    onChange={handleFileSelect}
                                    className="hidden"
                                    accept=".pdf,.jpg,.jpeg,.png,.docx,.doc"
                                />
                                <svg className="w-16 h-16 text-blue-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                                {selectedFile ? (
                                    <p className="text-green-600 font-medium">{selectedFile.name}</p>
                                ) : (
                                    <>
                                        <p className="text-gray-600 font-medium mb-2">Drop your file here or click to browse</p>
                                        <p className="text-gray-400 text-sm">PDF, JPG, PNG, DOCX (Max 10MB)</p>
                                    </>
                                )}
                            </div>

                            {uploadProgress > 0 && (
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div
                                        className="bg-blue-600 h-2 rounded-full transition-all"
                                        style={{ width: `${uploadProgress}%` }}
                                    ></div>
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Record Type *
                                </label>
                                <select
                                    value={formData.record_type}
                                    onChange={(e) => setFormData({ ...formData, record_type: e.target.value })}
                                    required
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="">Select type...</option>
                                    {recordTypes.map((type) => (
                                        <option key={type} value={type}>{type}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Show text input when "Other" is selected */}
                            {formData.record_type === 'Other' && (
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Specify Record Type *
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.other_type}
                                        onChange={(e) => setFormData({ ...formData, other_type: e.target.value })}
                                        required
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        placeholder="e.g., Dental Record, Allergy Test, etc."
                                    />
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Title *
                                </label>
                                <input
                                    type="text"
                                    value={formData.title}
                                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                    required
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    placeholder="e.g., Blood Test Results - January 2024"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Description *
                                </label>
                                <textarea
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    required
                                    rows="3"
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                                    placeholder="Brief description of the medical record..."
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Record Date *
                                </label>
                                <input
                                    type="date"
                                    value={formData.record_date}
                                    onChange={(e) => setFormData({ ...formData, record_date: e.target.value })}
                                    required
                                    max={new Date().toISOString().split('T')[0]}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>

                            <div className="flex gap-3">
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="flex-1 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
                                >
                                    {loading ? 'Uploading...' : 'Upload Record'}
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setShowUploadModal(false)}
                                    disabled={loading}
                                    className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-all disabled:opacity-50"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Delete Confirmation Modal */}
            {showDeleteModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
                        <div className="text-center mb-6">
                            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Confirm Delete</h3>
                            <p className="text-gray-600">
                                {recordToDelete === 'bulk'
                                    ? `Are you sure you want to delete ${selectedRecords.length} selected record(s)?`
                                    : 'Are you sure you want to delete this health record?'}
                                <br />
                                <span className="text-sm text-red-500 mt-2 block">This action cannot be undone.</span>
                            </p>
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={recordToDelete === 'bulk' ? confirmBulkDelete : confirmDelete}
                                className="flex-1 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors shadow-lg"
                            >
                                Delete
                            </button>
                            <button
                                onClick={() => {
                                    setShowDeleteModal(false);
                                    setRecordToDelete(null);
                                }}
                                className="flex-1 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-colors"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HealthRecords;
