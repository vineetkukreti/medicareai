import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ThemeToggle from '../../components/ThemeToggle';
import DoctorAvatar from '../../components/DoctorAvatar';

const PatientAppointments = () => {
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchAppointments();
    }, []);

    const fetchAppointments = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:8000/api/appointments/my-appointments', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setAppointments(response.data);
        } catch (error) {
            console.error('Error fetching appointments:', error);
            if (error.response?.status === 401) {
                navigate('/login');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = async (appointmentId) => {
        if (!window.confirm('Are you sure you want to cancel this appointment?')) return;

        try {
            const token = localStorage.getItem('token');
            await axios.delete(`http://localhost:8000/api/appointments/${appointmentId}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            fetchAppointments();
        } catch (error) {
            console.error('Error cancelling appointment:', error);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
            case 'confirmed': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
            case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
            case 'cancelled': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-2xl font-bold text-gray-900 dark:text-white">My Appointments</h1>
                    <div className="flex items-center space-x-4">
                        <button
                            onClick={() => navigate('/find-doctors')}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            Book New Appointment
                        </button>
                    </div>
                </div>

                {loading ? (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-500">Loading your appointments...</p>
                    </div>
                ) : appointments.length === 0 ? (
                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-12 text-center">
                        <div className="w-16 h-16 bg-blue-50 dark:bg-blue-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                            <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white">No appointments yet</h3>
                        <p className="text-gray-500 dark:text-gray-400 mt-2 mb-6">Book your first appointment with a specialist today.</p>
                        <button
                            onClick={() => navigate('/find-doctors')}
                            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                        >
                            Find a Doctor
                        </button>
                    </div>
                ) : (
                    <div className="grid gap-6">
                        {appointments.map((appt) => (
                            <div key={appt.id} className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
                                <div className="flex flex-col md:flex-row justify-between md:items-center">
                                    <div className="flex items-start space-x-4 mb-4 md:mb-0">
                                        <DoctorAvatar
                                            image={appt.doctor_image}
                                            name={appt.doctor_name}
                                            size="md"
                                            className="flex-shrink-0"
                                        />
                                        <div>
                                            <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                                                Dr. {appt.doctor_name}
                                            </h3>
                                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                                {appt.specialty || 'Specialist'}
                                            </p>
                                            <div className="flex items-center mt-2 text-sm text-gray-600 dark:text-gray-300">
                                                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                </svg>
                                                {new Date(appt.appointment_date).toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                                                <span className="mx-2">•</span>
                                                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                                {appt.start_time} - {appt.end_time}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex flex-col items-end space-y-3">
                                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(appt.status)}`}>
                                            {appt.status.charAt(0).toUpperCase() + appt.status.slice(1)}
                                        </span>

                                        {appt.status === 'confirmed' && (
                                            <a
                                                href={appt.meeting_link || '#'}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className={`px-4 py-2 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700 transition-colors flex items-center ${!appt.meeting_link && 'opacity-50 cursor-not-allowed'}`}
                                                onClick={(e) => !appt.meeting_link && e.preventDefault()}
                                            >
                                                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10zm2-2h4m-4-4h4" />
                                                </svg>
                                                Join Video Call
                                            </a>
                                        )}

                                        {appt.status === 'pending' && (
                                            <button
                                                onClick={() => handleCancel(appt.id)}
                                                className="text-red-600 hover:text-red-700 text-sm font-medium"
                                            >
                                                Cancel Request
                                            </button>
                                        )}
                                    </div>
                                </div>
                                {appt.reason && (
                                    <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
                                        <p className="text-sm text-gray-600 dark:text-gray-300">
                                            <span className="font-medium text-gray-900 dark:text-white">Reason for visit:</span> {appt.reason}
                                        </p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PatientAppointments;
