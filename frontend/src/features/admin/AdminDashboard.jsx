import React, { useState, useEffect } from 'react';
import AdminLayout from './components/AdminLayout';
import DashboardOverview from './components/DashboardOverview';
import PatientTable from './components/PatientTable';
import DoctorTable from './components/DoctorTable';

const AdminDashboard = () => {
    const [activeTab, setActiveTab] = useState('overview');
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (activeTab === 'overview') {
            fetchStats();
        }
    }, [activeTab]);

    const fetchStats = async () => {
        try {
            const token = localStorage.getItem('admin_token');
            const response = await fetch('http://localhost:8000/api/admin/stats', {
                headers: { Authorization: `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setStats(data);
            }
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        } finally {
            setLoading(false);
        }
    };

    const renderContent = () => {
        switch (activeTab) {
            case 'overview':
                return <DashboardOverview stats={stats} />;
            case 'patients':
                return <PatientTable />;
            case 'doctors':
                return <DoctorTable />;
            default:
                return <DashboardOverview stats={stats} />;
        }
    };

    return (
        <AdminLayout activeTab={activeTab} setActiveTab={setActiveTab}>
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-gray-900 capitalize">
                    {activeTab === 'overview' ? 'Dashboard Overview' : `${activeTab} Management`}
                </h1>
                <p className="text-gray-500 mt-1">
                    {activeTab === 'overview'
                        ? 'Welcome back, Admin. Here is what is happening today.'
                        : `Manage and view all ${activeTab} in the system.`}
                </p>
            </div>
            {renderContent()}
        </AdminLayout>
    );
};

export default AdminDashboard;
