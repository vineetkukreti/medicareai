import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Appointments = () => {
    const [activeTab, setActiveTab] = useState('book');
    const [appointments, setAppointments] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [specialties, setSpecialties] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    // Form state
    const [formData, setFormData] = useState({
        doctor_name: '',
        specialty: '',
        appointment_date: '',
        reason: '',
        notes: ''
    });

    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }
        fetchDoctors();
        fetchAppointments();
    }, [navigate]);

    const fetchDoctors = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch('http://localhost:8000/api/appointments/doctors/list', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setDoctors(data.doctors);
                setSpecialties(data.specialties);
            }
        } catch (err) {
            console.error('Failed to fetch doctors:', err);
        }
    };

    const fetchAppointments = async () => {
        const token = localStorage.getItem('token');
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/appointments', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setAppointments(data);
            }
        } catch (err) {
            setError('Failed to fetch appointments');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleDoctorChange = (e) => {
        const selectedDoctor = doctors.find(d => d.name === e.target.value);
        setFormData({
            ...formData,
            doctor_name: e.target.value,
            specialty: selectedDoctor ? selectedDoctor.specialty : ''
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        const token = localStorage.getItem('token');

        try {
            const response = await fetch('http://localhost:8000/api/appointments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    ...formData,
                    appointment_date: new Date(formData.appointment_date).toISOString()
                })
            });

            if (response.ok) {
                setSuccess('Appointment booked successfully! Check your email for confirmation.');
                setFormData({
                    doctor_name: '',
                    specialty: '',
                    appointment_date: '',
                    reason: '',
                    notes: ''
                });
                fetchAppointments();
                setTimeout(() => {
                    setActiveTab('my-appointments');
                }, 2000);
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to book appointment');
            }
        } catch (err) {
            setError('Error booking appointment: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleCancelAppointment = async (appointmentId) => {
        if (!window.confirm('Are you sure you want to cancel this appointment?')) {
            return;
        }

        const token = localStorage.getItem('token');

        try {
            const response = await fetch(`http://localhost:8000/api/appointments/${appointmentId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                setSuccess('Appointment cancelled successfully');
                fetchAppointments();
            } else {
                setError('Failed to cancel appointment');
            }
        } catch (err) {
            setError('Error cancelling appointment');
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'scheduled':
                return 'bg-blue-100 text-blue-800';
            case 'completed':
                return 'bg-green-100 text-green-800';
            case 'cancelled':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const upcomingAppointments = appointments.filter(apt =>
        apt.status === 'scheduled' && new Date(apt.appointment_date) > new Date()
    );

    const pastAppointments = appointments.filter(apt =>
        apt.status === 'completed' || (apt.status === 'scheduled' && new Date(apt.appointment_date) <= new Date())
    );

    const cancelledAppointments = appointments.filter(apt => apt.status === 'cancelled');

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-blue-100 shadow-sm">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center shadow-md">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">Appointments</span>
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

                {/* Tabs */}
                <div className="bg-white rounded-2xl shadow-xl border border-blue-100 overflow-hidden">
                    <div className="border-b border-gray-200 px-6">
                        <nav className="-mb-px flex space-x-8">
                            <button
                                onClick={() => setActiveTab('book')}
                                className={`${activeTab === 'book'
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center`}
                            >
                                <svg className={`w-5 h-5 mr-2 ${activeTab === 'book' ? 'text-blue-500' : 'text-gray-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                                </svg>
                                Book Appointment
                            </button>
                            <button
                                onClick={() => setActiveTab('my-appointments')}
                                className={`${activeTab === 'my-appointments'
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center`}
                            >
                                <svg className={`w-5 h-5 mr-2 ${activeTab === 'my-appointments' ? 'text-blue-500' : 'text-gray-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                                My Appointments ({upcomingAppointments.length})
                            </button>
                        </nav>
                    </div>

                    <div className="p-8">
                        {/* Book Appointment Tab */}
                        {activeTab === 'book' && (
                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                                            Select Doctor
                                        </label>
                                        <select
                                            name="doctor_name"
                                            value={formData.doctor_name}
                                            onChange={handleDoctorChange}
                                            required
                                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        >
                                            <option value="">Choose a doctor...</option>
                                            {doctors.map((doctor, index) => (
                                                <option key={index} value={doctor.name}>
                                                    {doctor.name} - {doctor.specialty}
                                                </option>
                                            ))}
                                        </select>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                                            Specialty
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.specialty}
                                            readOnly
                                            className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50"
                                            placeholder="Auto-filled based on doctor"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Appointment Date & Time
                                    </label>
                                    <input
                                        type="datetime-local"
                                        name="appointment_date"
                                        value={formData.appointment_date}
                                        onChange={handleInputChange}
                                        required
                                        min={new Date().toISOString().slice(0, 16)}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Reason for Visit
                                    </label>
                                    <textarea
                                        name="reason"
                                        value={formData.reason}
                                        onChange={handleInputChange}
                                        required
                                        rows="3"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                                        placeholder="Describe your symptoms or reason for the appointment..."
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Additional Notes (Optional)
                                    </label>
                                    <textarea
                                        name="notes"
                                        value={formData.notes}
                                        onChange={handleInputChange}
                                        rows="2"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                                        placeholder="Any additional information..."
                                    />
                                </div>

                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center"
                                >
                                    {loading ? (
                                        <>
                                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                            </svg>
                                            Booking...
                                        </>
                                    ) : (
                                        <>
                                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                                            </svg>
                                            Book Appointment
                                        </>
                                    )}
                                </button>
                            </form>
                        )}

                        {/* My Appointments Tab */}
                        {activeTab === 'my-appointments' && (
                            <div className="space-y-6">
                                {/* Upcoming Appointments */}
                                <div>
                                    <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                                        <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        Upcoming Appointments
                                    </h3>
                                    {upcomingAppointments.length === 0 ? (
                                        <div className="text-center py-12 bg-gray-50 rounded-lg">
                                            <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                            </svg>
                                            <p className="text-gray-500">No upcoming appointments</p>
                                        </div>
                                    ) : (
                                        <div className="space-y-4">
                                            {upcomingAppointments.map((apt) => (
                                                <div key={apt.id} className="bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                                                    <div className="flex justify-between items-start">
                                                        <div className="flex-1">
                                                            <div className="flex items-center mb-2">
                                                                <h4 className="text-lg font-bold text-gray-900">{apt.doctor_name}</h4>
                                                                <span className={`ml-3 px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(apt.status)}`}>
                                                                    {apt.status}
                                                                </span>
                                                            </div>
                                                            <p className="text-sm text-gray-600 mb-1">
                                                                <span className="font-semibold">Specialty:</span> {apt.specialty}
                                                            </p>
                                                            <p className="text-sm text-gray-600 mb-1">
                                                                <span className="font-semibold">Date:</span> {formatDate(apt.appointment_date)}
                                                            </p>
                                                            <p className="text-sm text-gray-600 mb-2">
                                                                <span className="font-semibold">Reason:</span> {apt.reason}
                                                            </p>
                                                            {apt.notes && (
                                                                <p className="text-sm text-gray-500 italic">
                                                                    Notes: {apt.notes}
                                                                </p>
                                                            )}
                                                        </div>
                                                        <button
                                                            onClick={() => handleCancelAppointment(apt.id)}
                                                            className="ml-4 px-4 py-2 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 transition-colors font-medium text-sm"
                                                        >
                                                            Cancel
                                                        </button>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>

                                {/* Past Appointments */}
                                {pastAppointments.length > 0 && (
                                    <div>
                                        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                                            <svg className="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                            Past Appointments
                                        </h3>
                                        <div className="space-y-4">
                                            {pastAppointments.map((apt) => (
                                                <div key={apt.id} className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                                                    <div className="flex items-center mb-2">
                                                        <h4 className="text-lg font-bold text-gray-700">{apt.doctor_name}</h4>
                                                        <span className={`ml-3 px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(apt.status)}`}>
                                                            {apt.status}
                                                        </span>
                                                    </div>
                                                    <p className="text-sm text-gray-600">
                                                        {apt.specialty} • {formatDate(apt.appointment_date)}
                                                    </p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Appointments;
