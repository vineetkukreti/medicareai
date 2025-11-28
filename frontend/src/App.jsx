import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LandingPage } from './features/landing';
import { ChatBot } from './features/chat';
import { SymptomChecker, HealthInsights, HealthDashboard, ProfileSettings } from './features/dashboard';
import { MedicationTracker } from './features/medications';
import { HealthRecords } from './features/health-records';
import { Appointments } from './features/appointments';
import { Login, Signup } from './features/auth';
import { AdminDashboard } from './features/admin';

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
