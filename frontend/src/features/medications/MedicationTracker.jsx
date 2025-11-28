import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const MedicationTracker = () => {
    const [medications, setMedications] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [editingMedication, setEditingMedication] = useState(null);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [formData, setFormData] = useState({
        medication_name: '',
        dosage: '',
        frequency: '',
        start_date: '',
        notes: ''
    });

    // Get user ID and token from localStorage
    const userId = localStorage.getItem('userId');
    const token = localStorage.getItem('token');

    // Axios config with auth header
    const config = {
        headers: { Authorization: `Bearer ${token}` }
    };

    // Fetch medications on component mount
    useEffect(() => {
        fetchMedications();
    }, []);

    const fetchMedications = async () => {
        try {
            setLoading(true);
            const response = await axios.get('http://localhost:8000/api/medications', config);
            setMedications(response.data);
            setError('');
        } catch (err) {
            setError('Failed to load medications. Please try again.');
            console.error('Error fetching medications:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (editingMedication) {
                // Update existing medication
                await axios.put(
                    `http://localhost:8000/api/medications/${editingMedication.id}`,
                    formData,
                    config
                );
                setSuccess('Medication updated successfully!');
            } else {
                // Create new medication
                await axios.post(
                    'http://localhost:8000/api/medications',
                    formData,
                    config
                );
                setSuccess('Medication added successfully!');
            }

            // Refresh medications list
            await fetchMedications();

            // Reset form
            setFormData({
                medication_name: '',
                dosage: '',
                frequency: '',
                start_date: '',
                notes: ''
            });
            setShowForm(false);
            setEditingMedication(null);

            // Clear success message after 3 seconds
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError(editingMedication ? 'Failed to update medication.' : 'Failed to add medication.');
            console.error('Error saving medication:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleEdit = (medication) => {
        setEditingMedication(medication);
        setFormData({
            medication_name: medication.medication_name,
            dosage: medication.dosage,
            frequency: medication.frequency,
            start_date: medication.start_date,
            notes: medication.notes || ''
        });
        setShowForm(true);
        setError('');
    };

    const handleDelete = async (medicationId) => {
        setLoading(true);
        setError('');

        try {
            await axios.delete(`http://localhost:8000/api/medications/${medicationId}`, config);
            setSuccess('Medication deleted successfully!');

            // Refresh medications list
            await fetchMedications();
            setShowDeleteConfirm(null);

            // Clear success message after 3 seconds
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            setError('Failed to delete medication.');
            console.error('Error deleting medication:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleCancelForm = () => {
        setShowForm(false);
        setEditingMedication(null);
        setFormData({
            medication_name: '',
            dosage: '',
            frequency: '',
            start_date: '',
            notes: ''
        });
        setError('');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-green-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-500 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-500 bg-clip-text text-transparent">Medication Tracker</span>
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
            <div className="max-w-6xl mx-auto p-6">
                <div className="text-center mb-10 mt-8">
                    <div className="inline-block p-4 bg-gradient-to-br from-green-600 to-emerald-500 rounded-full mb-4">
                        <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                    </div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-3">Medication Tracker</h1>
                    <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                        Never miss a dose! Track your medications and get timely reminders.
                    </p>
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

                {/* Add Medication Button */}
                <div className="mb-8">
                    <button
                        onClick={() => {
                            setShowForm(!showForm);
                            if (!showForm) {
                                setEditingMedication(null);
                                setFormData({
                                    medication_name: '',
                                    dosage: '',
                                    frequency: '',
                                    start_date: '',
                                    notes: ''
                                });
                            }
                        }}
                        className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-500 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-600 focus:outline-none focus:ring-4 focus:ring-green-300 transition-all shadow-lg"
                    >
                        + Add New Medication
                    </button>
                </div>

                {/* Add/Edit Medication Form */}
                {showForm && (
                    <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-green-100">
                        <h2 className="text-2xl font-bold text-gray-900 mb-6">
                            {editingMedication ? 'Edit Medication' : 'Add New Medication'}
                        </h2>
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Medication Name *</label>
                                    <input
                                        type="text"
                                        name="medication_name"
                                        value={formData.medication_name}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Dosage *</label>
                                    <input
                                        type="text"
                                        name="dosage"
                                        value={formData.dosage}
                                        onChange={handleChange}
                                        placeholder="e.g., 500mg"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Frequency *</label>
                                    <select
                                        name="frequency"
                                        value={formData.frequency}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                        required
                                    >
                                        <option value="">Select frequency</option>
                                        <option value="once daily">Once daily</option>
                                        <option value="twice daily">Twice daily</option>
                                        <option value="three times daily">Three times daily</option>
                                        <option value="as needed">As needed</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">Start Date *</label>
                                    <input
                                        type="date"
                                        name="start_date"
                                        value={formData.start_date}
                                        onChange={handleChange}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                        required
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">Notes (Optional)</label>
                                <textarea
                                    name="notes"
                                    value={formData.notes}
                                    onChange={handleChange}
                                    rows="3"
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                    placeholder="Any special instructions..."
                                />
                            </div>
                            <div className="flex space-x-4">
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="flex-1 py-3 bg-gradient-to-r from-green-600 to-emerald-500 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {loading ? 'Saving...' : (editingMedication ? 'Update Medication' : 'Add Medication')}
                                </button>
                                <button
                                    type="button"
                                    onClick={handleCancelForm}
                                    disabled={loading}
                                    className="flex-1 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                {/* Medications List */}
                <div className="grid md:grid-cols-2 gap-6">
                    {loading && medications.length === 0 ? (
                        <div className="col-span-2 text-center py-16 bg-white rounded-2xl shadow-lg border border-green-100">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
                            <p className="text-gray-500 text-lg mt-4">Loading medications...</p>
                        </div>
                    ) : medications.length === 0 ? (
                        <div className="col-span-2 text-center py-16 bg-white rounded-2xl shadow-lg border border-green-100">
                            <svg className="w-20 h-20 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                            </svg>
                            <p className="text-gray-500 text-lg">No medications added yet</p>
                            <p className="text-gray-400 text-sm mt-2">Click "Add New Medication" to get started</p>
                        </div>
                    ) : (
                        medications.map((med) => (
                            <div key={med.id} className="bg-white rounded-xl shadow-lg p-6 border border-green-100 hover:shadow-xl transition-shadow">
                                <div className="flex justify-between items-start mb-4">
                                    <h3 className="text-xl font-bold text-gray-900">{med.medication_name}</h3>
                                    <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">Active</span>
                                </div>
                                <div className="space-y-2 text-sm text-gray-600 mb-4">
                                    <p><strong>Dosage:</strong> {med.dosage}</p>
                                    <p><strong>Frequency:</strong> {med.frequency}</p>
                                    <p><strong>Start Date:</strong> {med.start_date}</p>
                                    {med.notes && <p><strong>Notes:</strong> {med.notes}</p>}
                                </div>
                                {/* Action Buttons */}
                                <div className="flex space-x-2 pt-4 border-t border-gray-200">
                                    <button
                                        onClick={() => handleEdit(med)}
                                        className="flex-1 px-4 py-2 bg-emerald-50 text-emerald-700 font-medium rounded-lg hover:bg-emerald-100 border border-emerald-200 transition-colors flex items-center justify-center"
                                    >
                                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => setShowDeleteConfirm(med.id)}
                                        className="flex-1 px-4 py-2 bg-gray-50 text-gray-600 font-medium rounded-lg hover:bg-gray-100 border border-gray-200 hover:text-red-600 hover:border-red-200 transition-colors flex items-center justify-center"
                                    >
                                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {/* Delete Confirmation Modal */}
            {showDeleteConfirm && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 animate-fade-in">
                        <div className="text-center">
                            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                                <svg className="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <h3 className="text-lg font-bold text-gray-900 mb-2">Delete Medication</h3>
                            <p className="text-sm text-gray-600 mb-6">
                                Are you sure you want to delete this medication? This action cannot be undone.
                            </p>
                            <div className="flex space-x-3">
                                <button
                                    onClick={() => setShowDeleteConfirm(null)}
                                    disabled={loading}
                                    className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={() => handleDelete(showDeleteConfirm)}
                                    disabled={loading}
                                    className="flex-1 px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {loading ? 'Deleting...' : 'Delete'}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MedicationTracker;
