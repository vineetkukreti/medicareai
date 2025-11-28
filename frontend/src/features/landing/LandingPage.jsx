import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const LandingPage = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const navigate = useNavigate();
  const [contactForm, setContactForm] = useState({ name: '', email: '', message: '' });
  const [contactStatus, setContactStatus] = useState('');
  // Helper to safely get item from localStorage
  const getSafeStorageItem = (key) => {
    const item = localStorage.getItem(key);
    if (!item || item === 'undefined' || item === 'null') return '';
    return item;
  };

  const [userEmail, setUserEmail] = useState(getSafeStorageItem('userEmail'));
  const [userName, setUserName] = useState(getSafeStorageItem('userName'));

  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('user_role');

    if (token && role === 'user') {
      setIsLoggedIn(true);

      // Check if we have valid user details in localStorage
      const storedEmail = getSafeStorageItem('userEmail');
      const storedName = getSafeStorageItem('userName');

      // If either is missing or invalid, fetch from API
      if (!storedEmail || !storedName) {
        // Only fetch if we have a token
        if (token) {
          axios.get('http://localhost:8000/api/auth/profile', {
            headers: { Authorization: `Bearer ${token}` }
          })
            .then(response => {
              const email = response.data.email;
              const fullName = response.data.full_name;

              if (email) {
                setUserEmail(email);
                localStorage.setItem('userEmail', email);
              }

              if (fullName) {
                setUserName(fullName);
                localStorage.setItem('userName', fullName);
              }
            })
            .catch(err => {
              console.error('Error fetching user profile:', err);
              // Optionally, handle error by logging out or setting a default email
              if (!userEmail) setUserEmail('user@example.com');
            });
        }
      } else {
        // If userEmail is already in localStorage, just set it
        setUserEmail(storedEmail);
        setUserName(storedName);
      }
    } else {
      // If not logged in or not a 'user' role, ensure isLoggedIn is false
      setIsLoggedIn(false);
      setUserEmail(''); // Clear email if not logged in
      setUserName('');
    }
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showUserDropdown && !event.target.closest('.user-dropdown-container')) {
        setShowUserDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showUserDropdown]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('userId');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    setIsLoggedIn(false);
    setUserEmail('');
    setShowUserDropdown(false);
    navigate('/login');
  };

  const handleContactChange = (e) => {
    setContactForm({ ...contactForm, [e.target.name]: e.target.value });
  };

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    setContactStatus('Sending...');
    try {
      const response = await fetch('http://localhost:8000/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(contactForm),
      });
      if (response.ok) {
        setContactStatus('Message sent successfully!');
        setContactForm({ name: '', email: '', message: '' });
      } else {
        setContactStatus('Failed to send message.');
      }
    } catch (error) {
      setContactStatus('Error sending message.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 font-sans text-gray-900">
      {/* Navbar */}
      <nav className="bg-white/90 backdrop-blur-md fixed w-full z-20 top-0 left-0 border-b border-blue-100 shadow-sm">
        <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
          <Link to="/" className="flex items-center space-x-3 rtl:space-x-reverse">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <span className="self-center text-2xl font-bold whitespace-nowrap bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">MediCareAI</span>
          </Link>
          <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
            {isLoggedIn ? (
              <div className="relative user-dropdown-container">
                <button
                  onClick={() => setShowUserDropdown(!showUserDropdown)}
                  className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 focus:ring-4 focus:outline-none focus:ring-blue-200 font-medium rounded-lg text-sm px-3 py-2 transition-all"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-full flex items-center justify-center text-white font-bold">
                    {(userName && userName !== 'undefined' ? userName : (userEmail && userEmail !== 'undefined' ? userEmail : 'U')).charAt(0).toUpperCase()}
                  </div>
                  <svg className={`w-4 h-4 transition-transform ${showUserDropdown ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {/* Dropdown Menu */}
                {showUserDropdown && (
                  <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-blue-100 py-2 animate-fade-in">
                    {/* User Info */}
                    <div className="px-4 py-3 border-b border-gray-100">
                      <p className="text-sm font-semibold text-gray-900 truncate">
                        {userName && userName !== 'undefined' ? userName : (userEmail && userEmail !== 'undefined' ? userEmail : 'User')}
                      </p>
                      <p className="text-xs text-gray-500">Manage your account</p>
                    </div>

                    {/* Menu Items */}
                    <Link
                      to="/health-dashboard"
                      onClick={() => setShowUserDropdown(false)}
                      className="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-blue-50 transition-colors"
                    >
                      <svg className="w-5 h-5 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      Health Dashboard
                    </Link>

                    <Link
                      to="/profile-settings"
                      onClick={() => setShowUserDropdown(false)}
                      className="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-blue-50 transition-colors"
                    >
                      <svg className="w-5 h-5 mr-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Profile Settings
                    </Link>

                    <Link
                      to="/profile-settings?tab=health-data"
                      onClick={() => setShowUserDropdown(false)}
                      className="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-blue-50 transition-colors"
                    >
                      <svg className="w-5 h-5 mr-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      Upload Health Data
                    </Link>

                    <div className="border-t border-gray-100 my-1"></div>

                    <button
                      onClick={handleLogout}
                      className="flex items-center w-full px-4 py-3 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link to="/login" className="text-blue-700 hover:bg-blue-50 focus:ring-4 focus:outline-none focus:ring-blue-200 font-medium rounded-lg text-sm px-4 py-2 text-center transition-all">Login</Link>
                <Link to="/signup" className="text-white bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center ml-2 transition-all">Sign Up</Link>
              </>
            )}
          </div>
          <div className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
            <ul className="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-transparent">
              <li>
                <Link to="/" className="block py-2 px-3 text-blue-700 rounded md:bg-transparent md:p-0 font-semibold" aria-current="page">Home</Link>
              </li>
              <li>
                <a href="#features" className="block py-2 px-3 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-600 md:p-0 transition-colors">Features</a>
              </li>
              <li>
                <a href="#contact" className="block py-2 px-3 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-600 md:p-0 transition-colors">Contact</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-cyan-600 pt-32 pb-20 px-4 relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-white rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-cyan-300 rounded-full blur-3xl animate-pulse delay-1000"></div>
        </div>

        <div className="max-w-screen-xl mx-auto text-center relative z-10">
          <div className="inline-block mb-4 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white text-sm font-semibold">
            🏥 AI-Powered Healthcare Assistant
          </div>
          <h1 className="mb-6 text-4xl font-extrabold tracking-tight leading-none text-white md:text-5xl lg:text-6xl drop-shadow-lg">
            Your <span className="text-cyan-300">Personal Health</span><br />Companion, Powered by AI
          </h1>
          <p className="mb-8 text-lg font-normal text-blue-100 lg:text-xl sm:px-16 lg:px-48">
            Get instant medical advice, symptom analysis, medication reminders, and 24/7 AI chatbot support for all your health concerns.
          </p>
          <div className="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
            <Link to="/chatbot" className="inline-flex justify-center items-center py-3 px-6 text-base font-medium text-center text-blue-700 rounded-lg bg-white hover:bg-blue-50 focus:ring-4 focus:ring-blue-300 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
              💬 Chat with AI Doctor
              <svg className="w-4 h-4 ms-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <Link to="/symptom-checker" className="inline-flex justify-center items-center py-3 px-6 text-base font-medium text-center text-white rounded-lg border-2 border-white hover:bg-white hover:text-blue-700 focus:ring-4 focus:ring-blue-300 transition-all">
              🔍 Check Symptoms
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-white">24/7</div>
              <div className="text-blue-200 text-sm">AI Support</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white">100K+</div>
              <div className="text-blue-200 text-sm">Users Helped</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white">99%</div>
              <div className="text-blue-200 text-sm">Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-screen-xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Comprehensive Healthcare Features</h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">Everything you need to manage your health in one intelligent platform</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 - AI Chatbot */}
            <Link to="/chatbot" className="group p-8 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl border border-blue-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">AI Medical Chatbot</h3>
              <p className="text-gray-600 leading-relaxed">24/7 intelligent health assistant powered by advanced AI. Get instant answers to your medical questions.</p>
            </Link>

            {/* Feature 2 - Symptom Checker */}
            <Link to="/symptom-checker" className="group p-8 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border border-purple-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Symptom Checker</h3>
              <p className="text-gray-600 leading-relaxed">AI-powered symptom analysis to help identify potential health conditions and get recommendations.</p>
            </Link>

            {/* Feature 3 - Medication Tracker */}
            <Link to="/medications" className="group p-8 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border border-green-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-green-600 to-emerald-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Medication Tracker</h3>
              <p className="text-gray-600 leading-relaxed">Never miss a dose with smart medication reminders and comprehensive tracking.</p>
            </Link>

            {/* Feature 4 - Health Records */}
            <Link to="/health-records" className="group p-8 bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl border border-orange-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-orange-600 to-red-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Health Records</h3>
              <p className="text-gray-600 leading-relaxed">Securely store and manage all your medical records, lab results, and prescriptions in one place.</p>
            </Link>

            {/* Feature 5 - Appointments */}
            <Link to="/appointments" className="group p-8 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl border border-indigo-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-indigo-600 to-blue-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Appointment Booking</h3>
              <p className="text-gray-600 leading-relaxed">Schedule and manage appointments with healthcare providers effortlessly.</p>
            </Link>

            {/* Feature 6 - Health Insights */}
            <Link to="/health-insights" className="group p-8 bg-gradient-to-br from-teal-50 to-cyan-50 rounded-2xl border border-teal-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-600 to-cyan-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Health Insights</h3>
              <p className="text-gray-600 leading-relaxed">Get personalized health tips, wellness advice, and preventive care recommendations.</p>
            </Link>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-screen-md mx-auto px-4">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">Get in Touch</h2>
          <p className="text-center text-gray-600 mb-8">Have questions? We're here to help!</p>
          <form onSubmit={handleContactSubmit} className="space-y-6 bg-white p-8 rounded-2xl shadow-xl border border-blue-100">
            <div>
              <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">Your Name</label>
              <input type="text" id="name" name="name" value={contactForm.name} onChange={handleContactChange} className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-3 border transition-all" required />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">Your Email</label>
              <input type="email" id="email" name="email" value={contactForm.email} onChange={handleContactChange} className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-3 border transition-all" required />
            </div>
            <div>
              <label htmlFor="message" className="block text-sm font-semibold text-gray-700 mb-2">Message</label>
              <textarea id="message" name="message" rows="4" value={contactForm.message} onChange={handleContactChange} className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-3 border transition-all" required></textarea>
            </div>
            <button type="submit" className="w-full text-white bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-lg text-sm px-5 py-3 text-center transition-all shadow-lg hover:shadow-xl">Send Message</button>
            {contactStatus && <p className="text-center text-sm font-medium text-blue-600 mt-2">{contactStatus}</p>}
          </form>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="w-full max-w-screen-xl mx-auto p-8">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div className="col-span-2">
              <Link to="/" className="flex items-center mb-4 space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">MediCareAI</span>
              </Link>
              <p className="text-gray-400 mb-4">Your AI-powered health companion, providing 24/7 medical assistance and personalized healthcare solutions.</p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-4">Quick Links</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#features" className="hover:text-blue-400 transition-colors">Features</a></li>
                <li><Link to="/chatbot" className="hover:text-blue-400 transition-colors">AI Chatbot</Link></li>
                <li><Link to="/symptom-checker" className="hover:text-blue-400 transition-colors">Symptom Checker</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-4">Legal</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-blue-400 transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Terms of Service</a></li>
                <li><a href="#contact" className="hover:text-blue-400 transition-colors">Contact</a></li>
              </ul>
            </div>
          </div>
          <hr className="border-gray-800 mb-6" />
          <div className="text-center text-gray-400 text-sm">
            <p>© 2024 <span className="text-blue-400 font-semibold">MediCareAI</span>. All Rights Reserved.</p>
            <p className="mt-2 text-xs">⚠️ This is an AI assistant and not a replacement for professional medical advice.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
