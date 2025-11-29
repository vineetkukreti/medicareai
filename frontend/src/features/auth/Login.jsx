import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ThemeToggle from '../../components/ThemeToggle';

const Login = () => {
    const [formData, setFormData] = useState({
        username: '', // OAuth2 expects 'username' for email
        password: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const [role, setRole] = useState('patient'); // 'patient' or 'doctor'

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const form = e.target;
        const emailValue = form.elements.username.value;
        const passwordValue = form.elements.password.value;

        // Admin Login (Special Case)
        if (emailValue === 'admin@gmail.com' && passwordValue === 'admin') {
            try {
                console.log('🔐 Attempting admin login...');
                const response = await fetch('http://localhost:8000/api/auth/admin/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: emailValue, password: passwordValue }),
                });

                console.log('📡 Admin login response status:', response.status);

                if (response.ok) {
                    const data = await response.json();
                    console.log('✅ Admin login successful, data:', data);
                    localStorage.setItem('admin_token', data.access_token);
                    localStorage.setItem('user_role', 'admin');
                    navigate('/admin/dashboard');
                    return;
                } else {
                    const errorText = await response.text();
                    console.error('❌ Admin login failed, status:', response.status, 'response:', errorText);
                    throw new Error('Admin login failed');
                }
            } catch (err) {
                console.error('💥 Admin login error:', err);
                setError('Admin login failed. Please try again.');
                setLoading(false);
                return; // Important: prevent fallthrough to patient login
            }
        }


        try {
            if (role === 'doctor') {
                // Doctor Login
                const response = await fetch('http://localhost:8000/api/doctors/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: emailValue, password: passwordValue }),
                });

                if (!response.ok) {
                    throw new Error('Invalid doctor credentials');
                }

                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user_role', 'doctor');
                localStorage.setItem('doctor_id', data.doctor_id);
                localStorage.setItem('userEmail', data.email);
                localStorage.setItem('userName', data.full_name);
                navigate('/doctor/dashboard');
            } else {
                // Patient Login
                const formBody = new URLSearchParams();
                formBody.append('username', emailValue);
                formBody.append('password', passwordValue);

                const response = await fetch('http://localhost:8000/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: formBody,
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || 'Invalid credentials');
                }

                const data = await response.json();

                if (!data.user_id) {
                    throw new Error('Login failed: Invalid response from server.');
                }

                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user_role', 'user');
                localStorage.setItem('userId', data.user_id.toString());
                localStorage.setItem('userEmail', data.email);
                localStorage.setItem('userName', data.full_name || '');
                navigate('/');
            }
        } catch (err) {
            console.error('Login error:', err);
            setError(err.message || 'Login failed. Please check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8 transition-colors duration-300 relative">
            <div className="absolute top-4 right-4">
                <ThemeToggle />
            </div>
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <Link to="/" className="flex items-center justify-center space-x-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg">
                        <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                    </div>
                    <span className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">MediCareAI</span>
                </Link>
                <h2 className="text-center text-3xl font-extrabold text-gray-900 dark:text-white">
                    {role === 'doctor' ? 'Doctor Login' : 'Welcome Back'}
                </h2>
                <p className="mt-2 text-center text-sm text-gray-600">
                    {role === 'doctor' ? 'Access your practice dashboard' : 'Sign in to access your health dashboard'}
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                {/* Role Selection */}
                <div className="bg-white dark:bg-gray-800 p-1 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 mb-6 flex">
                    <button
                        onClick={() => setRole('patient')}
                        className={`flex-1 py-2 text-sm font-medium rounded-lg shadow-sm transition-all ${role === 'patient'
                            ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-gray-700'
                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                            }`}
                    >
                        Patient
                    </button>
                    <button
                        onClick={() => setRole('doctor')}
                        className={`flex-1 py-2 text-sm font-medium rounded-lg shadow-sm transition-all ${role === 'doctor'
                            ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-gray-700'
                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                            }`}
                    >
                        Doctor
                    </button>
                </div>

                <div className="bg-white dark:bg-gray-800 py-8 px-4 shadow-xl sm:rounded-2xl sm:px-10 border border-blue-100 dark:border-gray-700">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="email" className="block text-sm font-semibold text-gray-700">
                                Email address
                            </label>
                            <div className="mt-1">
                                <input
                                    id="email"
                                    name="username"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    value={formData.username}
                                    onChange={handleChange}
                                    className="appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                                    placeholder="you@example.com"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-semibold text-gray-700">
                                Password
                            </label>
                            <div className="mt-1">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="current-password"
                                    required
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start">
                                <svg className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <div className="flex-1">
                                    <p className="font-semibold">Login Failed</p>
                                    <p className="text-sm">{error}</p>
                                </div>
                            </div>
                        )}

                        <div>
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-lg text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-0.5"
                            >
                                {loading ? (
                                    <>
                                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Signing in...
                                    </>
                                ) : (
                                    'Sign in'
                                )}
                            </button>
                        </div>
                    </form>

                    <div className="mt-6">
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-300"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white text-gray-500">New to MediCareAI?</span>
                            </div>
                        </div>

                        <div className="mt-6">
                            <Link
                                to="/signup"
                                className="w-full flex justify-center py-3 px-4 border-2 border-blue-200 rounded-lg shadow-sm text-sm font-semibold text-blue-600 bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all"
                            >
                                Create new account
                            </Link>
                        </div>
                    </div>

                    <div className="mt-6 text-center">
                        <p className="text-xs text-gray-500">
                            Admin? Use <span className="font-mono bg-gray-100 px-2 py-1 rounded">admin@gmail.com</span> / <span className="font-mono bg-gray-100 px-2 py-1 rounded">admin</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
