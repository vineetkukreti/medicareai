import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LandingPage } from './features/landing';
import { ChatBot } from './features/chat';
import { SymptomChecker, HealthInsights, HealthDashboard, ProfileSettings } from './features/dashboard';
import { MedicationTracker } from './features/medications';
import { HealthRecords } from './features/health-records';
import { Appointments } from './features/appointments';
import PatientAppointments from './features/appointments/PatientAppointments';
import { Login, Signup } from './features/auth';
import { AdminDashboard } from './features/admin';
import Onboarding from './pages/Onboarding';
import DoctorMarketplace from './pages/DoctorMarketplace';
import ConsultationRoom from './pages/ConsultationRoom';
import DoctorLogin from './features/doctors/DoctorLogin';
import DoctorRegister from './features/doctors/DoctorRegister';
import DoctorDashboard from './features/doctors/DoctorDashboard';
import DoctorSettings from './features/doctors/DoctorSettings';
import { ThemeProvider } from './context/ThemeContext';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/chatbot" element={<ProtectedRoute><ChatBot /></ProtectedRoute>} />
          <Route path="/symptom-checker" element={<ProtectedRoute><SymptomChecker /></ProtectedRoute>} />
          <Route path="/medications" element={<ProtectedRoute><MedicationTracker /></ProtectedRoute>} />
          <Route path="/health-records" element={<ProtectedRoute><HealthRecords /></ProtectedRoute>} />
          <Route path="/appointments" element={<ProtectedRoute><Appointments /></ProtectedRoute>} />
          <Route path="/my-appointments" element={<ProtectedRoute><PatientAppointments /></ProtectedRoute>} />
          <Route path="/doctors" element={<ProtectedRoute><DoctorMarketplace /></ProtectedRoute>} />
          <Route path="/find-doctors" element={<ProtectedRoute><DoctorMarketplace /></ProtectedRoute>} />
          <Route path="/consultation-room/:id" element={<ProtectedRoute><ConsultationRoom /></ProtectedRoute>} />
          <Route path="/health-insights" element={<ProtectedRoute><HealthInsights /></ProtectedRoute>} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/health-dashboard" element={<ProtectedRoute><HealthDashboard /></ProtectedRoute>} />
          <Route path="/profile-settings" element={<ProtectedRoute><ProfileSettings /></ProtectedRoute>} />
          <Route path="/doctor/login" element={<DoctorLogin />} />
          <Route path="/doctor/register" element={<DoctorRegister />} />
          <Route path="/doctor/dashboard" element={<DoctorDashboard />} />
          <Route path="/doctor/settings" element={<DoctorSettings />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
