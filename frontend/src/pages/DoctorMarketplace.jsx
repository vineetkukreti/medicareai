import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import BookingModal from '../components/appointments/BookingModal';
import DoctorAvatar from '../components/DoctorAvatar';

const DoctorMarketplace = () => {
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedSpecialty, setSelectedSpecialty] = useState('All');
    const [selectedDoctor, setSelectedDoctor] = useState(null);
    const [showBookingModal, setShowBookingModal] = useState(false);
    const [userAppointments, setUserAppointments] = useState([]);
    const navigate = useNavigate();

    const specialties = ['All', 'General Practitioner', 'Cardiologist', 'Dermatologist', 'Pediatrician', 'Psychiatrist', 'Orthopedic Surgeon'];

    useEffect(() => {
        fetchDoctors();
        fetchUserAppointments();
    }, [selectedSpecialty]);

    const fetchDoctors = async () => {
        try {
            const token = localStorage.getItem('token');
            const params = { available_only: true };
            if (selectedSpecialty !== 'All') {
                params.specialty = selectedSpecialty;
            }

            const response = await axios.get('http://localhost:8000/api/doctors/list', {
                params,
                headers: token ? { Authorization: `Bearer ${token}` } : {}
            });
            setDoctors(response.data);
        } catch (error) {
            console.error('Error fetching doctors:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchUserAppointments = async () => {
        const token = localStorage.getItem('token');
        if (!token) return;
        try {
            const response = await axios.get('http://localhost:8000/api/appointments/my-appointments', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUserAppointments(response.data);
        } catch (error) {
            console.error('Error fetching user appointments:', error);
        }
    };

    const getDoctorStatus = (doctorId) => {
        const appointment = userAppointments.find(
            apt => apt.doctor_id === doctorId && ['pending', 'confirmed'].includes(apt.status)
        );
        return appointment ? appointment.status : null;
    };

    const handleBookClick = (doctor) => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }
        setSelectedDoctor(doctor);
        setShowBookingModal(true);
    };

    const filteredDoctors = doctors.filter(doctor => {
        const matchesSearch = doctor.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase());
        return matchesSearch;
    });

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
            <Navbar />

            <div className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Find Your Doctor</h1>
                    <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        Book appointments with top-rated healthcare professionals. Video consultations available 24/7.
                    </p>
                </div>

                {/* Search and Filter */}
                <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 mb-8">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="flex-1 relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                            </div>
                            <input
                                type="text"
                                placeholder="Search by doctor name or specialty..."
                                className="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-xl leading-5 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className="md:w-64">
                            <select
                                value={selectedSpecialty}
                                onChange={(e) => setSelectedSpecialty(e.target.value)}
                                className="block w-full pl-3 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-xl leading-5 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                            >
                                {specialties.map(specialty => (
                                    <option key={specialty} value={specialty}>{specialty}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>

                {/* Doctors Grid */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-500">Loading doctors...</p>
                    </div>
                ) : filteredDoctors.length === 0 ? (
                    <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700">
                        <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white">No doctors found</h3>
                        <p className="text-gray-500 dark:text-gray-400 mt-1">Try adjusting your search or filters.</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {filteredDoctors.map(doctor => (
                            <div key={doctor.id} className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
                                <div className="p-6">
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="flex items-center">
                                            <DoctorAvatar
                                                image={doctor.profile_image}
                                                name={doctor.full_name}
                                                size="lg"
                                                className="mr-4"
                                            />
                                            <div>
                                                <h3 className="text-lg font-bold text-gray-900 dark:text-white">{doctor.full_name}</h3>
                                                <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">{doctor.specialty}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center bg-green-50 dark:bg-green-900/20 px-2 py-1 rounded-lg">
                                            <span className="text-xs font-bold text-green-700 dark:text-green-300">
                                                {doctor.is_available ? 'Available' : 'Busy'}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="space-y-2 mb-6">
                                        <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                            </svg>
                                            {doctor.experience_years || 0} years experience
                                        </div>
                                        <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                            Next Available: Today
                                        </div>
                                        <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                                            </svg>
                                            ${doctor.hourly_rate || 50} / consultation
                                        </div>
                                    </div>

                                    <div className="flex gap-3">
                                        {(() => {
                                            const status = getDoctorStatus(doctor.id);
                                            if (status === 'pending') {
                                                return (
                                                    <button
                                                        disabled
                                                        className="flex-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 text-center py-2.5 rounded-xl font-medium cursor-not-allowed border border-yellow-200 dark:border-yellow-800"
                                                    >
                                                        Request Pending
                                                    </button>
                                                );
                                            } else if (status === 'confirmed') {
                                                return (
                                                    <button
                                                        onClick={() => navigate('/my-appointments')}
                                                        className="flex-1 bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 text-center py-2.5 rounded-xl font-medium hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors border border-green-200 dark:border-green-800"
                                                    >
                                                        Appointment Confirmed
                                                    </button>
                                                );
                                            } else {
                                                return (
                                                    <button
                                                        onClick={() => handleBookClick(doctor)}
                                                        className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-center py-2.5 rounded-xl font-medium transition-colors shadow-md"
                                                    >
                                                        Book Appointment
                                                    </button>
                                                );
                                            }
                                        })()}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {showBookingModal && selectedDoctor && (
                <BookingModal
                    doctor={selectedDoctor}
                    onClose={() => setShowBookingModal(false)}
                    onSuccess={async () => {
                        await fetchUserAppointments(); // Refresh status
                        setShowBookingModal(false);
                    }}
                />
            )}
        </div>
    );
};

export default DoctorMarketplace;
