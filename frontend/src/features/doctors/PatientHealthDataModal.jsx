import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DoctorPatientChat from './DoctorPatientChat';

const PatientHealthDataModal = ({ patientId, patientName, onClose }) => {
    const [activeTab, setActiveTab] = useState('medications');
    const [showChat, setShowChat] = useState(false);
    const [medications, setMedications] = useState([]);
    const [healthRecords, setHealthRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchData();
    }, [patientId]);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            const headers = { Authorization: `Bearer ${token}` };

            const [medsRes, recordsRes] = await Promise.all([
                axios.get(`http://localhost:8000/api/doctors/patients/${patientId}/medications`, { headers }),
                axios.get(`http://localhost:8000/api/doctors/patients/${patientId}/health-records`, { headers })
            ]);

            setMedications(medsRes.data);
            setHealthRecords(recordsRes.data);
        } catch (err) {
            console.error("Error fetching patient data:", err);
            setError("Failed to load patient data. Ensure you have a booked appointment with this patient.");
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString();
    };

    const handleView = async (fileUrl) => {
        try {
            const filename = fileUrl.split('/').pop();
            const token = localStorage.getItem('token');

            const response = await axios.get(`http://localhost:8000/api/doctors/patients/${patientId}/health-records/download/${filename}`, {
                headers: { Authorization: `Bearer ${token}` },
                responseType: 'blob'
            });

            // Create blob URL and open in new tab
            const file = new Blob([response.data], { type: response.headers['content-type'] });
            const fileURL = URL.createObjectURL(file);
            window.open(fileURL, '_blank');

            // Note: We can't easily revoke the object URL here since the new tab needs it.
            // Browsers will clean it up when the document is unloaded, but for long-lived apps 
            // with many opens, this *could* be a memory leak. 
            // A timeout revocation is a common workaround.
            setTimeout(() => URL.revokeObjectURL(fileURL), 60000);
        } catch (err) {
            console.error("View failed:", err);
            alert("Failed to view file. Please try downloading it instead.");
        }
    };

    const handleDownload = async (fileUrl, title) => {
        try {
            const filename = fileUrl.split('/').pop();
            const token = localStorage.getItem('token');

            const response = await axios.get(`http://localhost:8000/api/doctors/patients/${patientId}/health-records/download/${filename}`, {
                headers: { Authorization: `Bearer ${token}` },
                responseType: 'blob'
            });

            // Create blob link to download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename); // or use title + extension
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            console.error("Download failed:", err);
            alert("Failed to download file. Please try again.");
        }
    };

    return (
        <>
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6" role="dialog" aria-modal="true">
                <div
                    className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
                    onClick={onClose}
                ></div>

                <div className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden">
                    {/* Header */}
                    <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-900">
                        <div>
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Patient Health Data</h2>
                            <p className="text-sm text-gray-500 dark:text-gray-400">Viewing records for <span className="font-semibold">{patientName}</span></p>
                        </div>
                        <div className="flex items-center space-x-4">
                            <button
                                onClick={() => setShowChat(true)}
                                className="flex items-center px-3 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                                </svg>
                                Chat with AI
                            </button>
                            <button onClick={onClose} className="text-gray-400 hover:text-gray-500 focus:outline-none">
                                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    {/* Tabs */}
                    <div className="border-b border-gray-200 dark:border-gray-700 px-6">
                        <nav className="-mb-px flex space-x-8">
                            <button
                                onClick={() => setActiveTab('medications')}
                                className={`${activeTab === 'medications'
                                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                                    } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
                            >
                                Medications ({medications.length})
                            </button>
                            <button
                                onClick={() => setActiveTab('records')}
                                className={`${activeTab === 'records'
                                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                                    } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
                            >
                                Health Records ({healthRecords.length})
                            </button>
                        </nav>
                    </div>

                    {/* Content */}
                    <div className="flex-1 overflow-y-auto p-6 bg-white dark:bg-gray-800">
                        {loading ? (
                            <div className="flex justify-center items-center h-48">
                                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                            </div>
                        ) : error ? (
                            <div className="bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 p-4 rounded-lg text-center">
                                {error}
                            </div>
                        ) : (
                            <>
                                {activeTab === 'medications' && (
                                    <div className="space-y-4">
                                        {medications.length === 0 ? (
                                            <p className="text-center text-gray-500 dark:text-gray-400 py-8">No medications found for this patient.</p>
                                        ) : (
                                            <div className="grid gap-4 md:grid-cols-2">
                                                {medications.map((med) => (
                                                    <div key={med.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                                                        <div className="flex justify-between items-start mb-2">
                                                            <h3 className="font-bold text-gray-900 dark:text-white">{med.medication_name}</h3>
                                                            <span className={`px-2 py-1 text-xs rounded-full ${med.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'}`}>
                                                                {med.is_active ? 'Active' : 'Inactive'}
                                                            </span>
                                                        </div>
                                                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-1"><span className="font-medium">Dosage:</span> {med.dosage}</p>
                                                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-1"><span className="font-medium">Frequency:</span> {med.frequency}</p>
                                                        {med.notes && <p className="text-sm text-gray-500 dark:text-gray-400 italic mt-2">{med.notes}</p>}
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}

                                {activeTab === 'records' && (
                                    <div className="space-y-4">
                                        {healthRecords.length === 0 ? (
                                            <p className="text-center text-gray-500 dark:text-gray-400 py-8">No health records found for this patient.</p>
                                        ) : (
                                            <div className="space-y-4">
                                                {healthRecords.map((record) => (
                                                    <div key={record.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                                                        <div className="flex justify-between items-start">
                                                            <div>
                                                                <div className="flex items-center gap-2 mb-1">
                                                                    <span className="px-2 py-0.5 bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 text-xs rounded uppercase font-bold">
                                                                        {record.record_type}
                                                                    </span>
                                                                    <span className="text-xs text-gray-500 dark:text-gray-400">{formatDate(record.record_date)}</span>
                                                                </div>
                                                                <h3 className="font-bold text-gray-900 dark:text-white mb-2">{record.title || "Untitled Record"}</h3>
                                                                {record.description && (
                                                                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">{record.description}</p>
                                                                )}
                                                            </div>
                                                            {record.file_url && (
                                                                <div className="flex items-center space-x-2 ml-4">
                                                                    <button
                                                                        onClick={() => handleView(record.file_url)}
                                                                        className="p-2 bg-blue-50 dark:bg-blue-900/30 rounded-lg text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors"
                                                                        title="View File"
                                                                    >
                                                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                                                        </svg>
                                                                    </button>
                                                                    <button
                                                                        onClick={() => handleDownload(record.file_url, record.title)}
                                                                        className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                                                                        title="Download File"
                                                                    >
                                                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                                                        </svg>
                                                                    </button>
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </>
                        )}
                    </div>

                    <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 flex justify-end">
                        <button
                            onClick={onClose}
                            className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 font-medium transition-colors"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>

            {showChat && (
                <DoctorPatientChat
                    patientId={patientId}
                    patientName={patientName}
                    onClose={() => setShowChat(false)}
                />
            )}
        </>
    );
};

export default PatientHealthDataModal;
