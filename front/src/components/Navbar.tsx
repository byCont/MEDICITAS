import React from 'react';
import ThemeSwitcher from './ThemeSwitcher';

const Navbar: React.FC = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-solid">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">
          MediCitas
        </a>
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
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <a className="nav-link" href="#">
                <i className="mdi mdi-home"></i> Inicio
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">
                <i className="mdi mdi-calendar-clock"></i> Citas
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">
                <i className="mdi mdi-account-circle"></i> Perfil
              </a>
            </li>
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
