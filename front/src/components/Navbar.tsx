import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import ThemeSwitcher from './ThemeSwitcher';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <nav className="navbar navbar-expand-lg bg-solid">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          <i className="mdi mdi-heart-pulse"></i> MediCitas
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                <i className="mdi mdi-home"></i> Inicio
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/doctores">
                <i className="mdi mdi-doctor"></i> Doctores
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/especialidades">
                <i className="mdi mdi-medical-bag"></i> Especialidades
              </Link>
            </li>
          </ul>
          
          <ul className="navbar-nav ms-auto">
            {isAuthenticated ? (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/mis-citas">
                    <i className="mdi mdi-calendar-clock"></i> Mis Citas
                  </Link>
                </li>
                <li className="nav-item dropdown">
                  <a
                    className="nav-link dropdown-toggle"
                    href="#"
                    role="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    <i className="mdi mdi-account-circle"></i> {user?.nombre_completo}
                  </a>
                  <ul className="dropdown-menu">
                    <li>
                      <a className="dropdown-item" href="#">
                        <i className="mdi mdi-account"></i> Mi Perfil
                      </a>
                    </li>
                    {user?.rol === 'Doctor' && (
                      <li>
                        <a className="dropdown-item" href="#">
                          <i className="mdi mdi-stethoscope"></i> Panel Doctor
                        </a>
                      </li>
                    )}
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <button className="dropdown-item" onClick={handleLogout}>
                        <i className="mdi mdi-logout"></i> Cerrar Sesión
                      </button>
                    </li>
                  </ul>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    <i className="mdi mdi-login"></i> Iniciar Sesión
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/registro">
                    <i className="mdi mdi-account-plus"></i> Registrarse
                  </Link>
                </li>
              </>
            )}
            <li className="nav-item">
              <ThemeSwitcher />
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
