import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import RegisterDoctorPage from './pages/RegisterDoctorPage';
import DoctoresPage from './pages/DoctoresPage';
import DoctorProfilePage from './pages/DoctorProfilePage';
import MisCitasPage from './pages/MisCitasPage';
import EspecialidadesPage from './pages/EspecialidadesPage';
import ProtectedRoute from './components/ProtectedRoute';
import './styles.scss';

const App: React.FC = () => {
  return (
<AuthProvider>
        <div className="d-flex flex-column">
          <Navbar />
          <main className="flex-shrink-0">
            <Routes>
              {/* Rutas públicas */}
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/registro" element={<RegisterPage />} />
              <Route path="/registro-doctor" element={<RegisterDoctorPage />} />
              <Route path="/doctores" element={<DoctoresPage />} />
              <Route path="/doctor/:id" element={<DoctorProfilePage />} />
              <Route path="/especialidades" element={<EspecialidadesPage />} />
              
              {/* Rutas protegidas */}
              <Route 
                path="/mis-citas" 
                element={
                  <ProtectedRoute>
                    <MisCitasPage />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
          <Footer />
        </div>
</AuthProvider>
  );
};

export default App;

