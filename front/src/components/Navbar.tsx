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

  // Solo mantenemos el CSS que Bootstrap no puede hacer: el efecto de desenfoque.
  const customStyles = `
    .backdrop-blur {
      -webkit-backdrop-filter: blur(10px);
      backdrop-filter: blur(10px);
    }
  `;

  // Clases comunes para los elementos de la barra de navegación para no repetirlas.
  const navElementClasses = "backdrop-blur bg-dark bg-opacity-50 rounded-pill px-3 py-2 m-1 text-white text-decoration-none d-inline-flex align-items-center";

  return (
    <>
      <style>{customStyles}</style>
      <nav className="navbar navbar-expand-lg sticky-top bg-transparent py-2">
        <div className="container-fluid">
          <Link className="fs-5 fw-semibold bg-primary rounded-pill px-2 py-1 m-1 text-white text-decoration-none d-inline-flex align-items-center" to="/">
            <i className="mdi mdi-heart-pulse me-2"></i> MediCitas
          </Link>
          <button
            className="navbar-toggler backdrop-blur bg-dark bg-opacity-50 p-2"
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
                <Link className={navElementClasses} to="/">
                  <i className="mdi mdi-home me-2"></i> Inicio
                </Link>
              </li>
              <li className="nav-item">
                <Link className={navElementClasses} to="/doctores">
                  <i className="mdi mdi-doctor me-2"></i> Doctores
                </Link>
              </li>
              <li className="nav-item">
                <Link className={navElementClasses} to="/especialidades">
                  <i className="mdi mdi-medical-bag me-2"></i> Especialidades
                </Link>
              </li>
            </ul>
            
            <ul className="navbar-nav ms-auto">
              {isAuthenticated ? (
                <>
                  <li className="nav-item">
                    <Link className={navElementClasses} to="/mis-citas">
                      <i className="mdi mdi-calendar-clock me-2"></i> Mis Citas
                    </Link>
                  </li>
                  <li className="nav-item dropdown">
                    <a
                      className={`${navElementClasses} dropdown-toggle`}
                      href="#"
                      role="button"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      <i className="mdi mdi-account-circle me-2"></i> {user?.nombre_completo}
                    </a>
                    <ul className="dropdown-menu dropdown-menu-end backdrop-blur bg-dark bg-opacity-50 border-light border-opacity-25 mt-2">
                      <li>
                        <Link className="dropdown-item text-white" to="/mis-citas">
                          <i className="mdi mdi-account me-2"></i> Mi Perfil
                        </Link>
                      </li>
                      {user?.rol === 'Doctor' && (
                        <li>
                          <a className="dropdown-item text-white" href="#">
                            <i className="mdi mdi-stethoscope me-2"></i> Panel Doctor
                          </a>
                        </li>
                      )}
                      <li><hr className="dropdown-divider border-light border-opacity-25" /></li>
                      <li>
                        <button className="dropdown-item text-white" onClick={handleLogout}>
                          <i className="mdi mdi-logout me-2"></i> Cerrar Sesión
                        </button>
                      </li>
                    </ul>
                  </li>
                </>
              ) : (
                <>
                  <li className="nav-item">
                    <Link className={navElementClasses} to="/login">
                      <i className="mdi mdi-login me-2"></i> Iniciar Sesión
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className={navElementClasses} to="/registro">
                      <i className="mdi mdi-account-plus me-2"></i> Registrarse
                    </Link>
                  </li>
                </>
              )}
              <li className="nav-item d-flex align-items-center m-1">
                <ThemeSwitcher />
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
