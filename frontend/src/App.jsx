import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ChatBot from './pages/ChatBot';
import SymptomChecker from './pages/SymptomChecker';
import MedicationTracker from './pages/MedicationTracker';
import HealthRecords from './pages/HealthRecords';
import Appointments from './pages/Appointments';
import HealthInsights from './pages/HealthInsights';
import Login from './pages/Login';
import Signup from './pages/Signup';
import AdminDashboard from './pages/AdminDashboard';
import HealthDashboard from './pages/HealthDashboard';
import ProfileSettings from './pages/ProfileSettings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/chatbot" element={<ChatBot />} />
        <Route path="/symptom-checker" element={<SymptomChecker />} />
        <Route path="/medications" element={<MedicationTracker />} />
        <Route path="/health-records" element={<HealthRecords />} />
        <Route path="/appointments" element={<Appointments />} />
        <Route path="/health-insights" element={<HealthInsights />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/health-dashboard" element={<HealthDashboard />} />
        <Route path="/profile-settings" element={<ProfileSettings />} />
      </Routes>
    </Router>
  );
}

export default App;
