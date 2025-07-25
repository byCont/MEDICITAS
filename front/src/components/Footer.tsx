import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="py-3 mt-auto bg-solid">
      <div className="container">
        <div className="row">
          {/* Brand and description */}
          <div className="col-lg-4 col-md-6 mb-4">
            <div className="d-flex align-items-center mb-3">
              <i className="mdi mdi-heart-pulse mdi-xl text-primary me-2"></i>
              <h5 className="fw-bold">MediCitas</h5>
            </div>
            <p className="text-muted">
              Conectamos pacientes con los mejores profesionales médicos para un cuidado de salud de calidad.
            </p>
            <div className="d-flex gap-3">
              <a href="#" >
                <i className="mdi mdi-facebook mdi-lg"></i>
              </a>
              <a href="#">
                <i className="mdi mdi-twitter mdi-lg"></i>
              </a>
              <a href="#">
                <i className="mdi mdi-instagram mdi-lg"></i>
              </a>
              <a href="#">
                <i className="mdi mdi-linkedin mdi-lg"></i>
              </a>
            </div>
          </div>

          {/* Quick links */}
          <div className="col-lg-2 col-md-6 mb-4">
            <h6 className="fw-bold mb-3">Enlaces Rápidos</h6>
            <ul className="list-unstyled">
              <li className="mb-2">
                <a href="/home" className="text-muted text-decoration-none">
                  <i className="mdi mdi-chevron-right me-1"></i>
                  Inicio
                </a>
              </li>
              <li className="mb-2">
                <a href="/especialidades" className="text-muted text-decoration-none">
                  <i className="mdi mdi-chevron-right me-1"></i>
                  Especialidades
                </a>
              </li>
              <li className="mb-2">
                <a href="/doctores" className="text-muted text-decoration-none">
                  <i className="mdi mdi-chevron-right me-1"></i>
                  Médicos
                </a>
              </li>
              <li className="mb-2">
                <a href="#" className="text-muted text-decoration-none">
                  <i className="mdi mdi-chevron-right me-1"></i>
                  Sobre Nosotros
                </a>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div className="col-lg-3 col-md-6 mb-4">
            <h6 className="fw-bold mb-3">Servicios</h6>
            <ul className="list-unstyled">
              <li className="mb-2">
                <a href="#" className="text-muted text-decoration-none">
                  <i className="mdi mdi-account-check me-2"></i>
                  Consultas Personalizadas
                </a>
              </li>
              <li className="mb-2">
                <a href="#" className="text-muted text-decoration-none">
                  <i className="mdi mdi-video me-2"></i>
                  Consultas Online
                </a>
              </li>
              <li className="mb-2">
                <a href="#" className="text-muted text-decoration-none">
                  <i className="mdi mdi-calendar-check me-2"></i>
                  Horarios Flexibles
                </a>
              </li>
              <li className="mb-2">
                <a href="#" className="text-muted text-decoration-none">
                  <i className="mdi mdi-certificate me-2"></i>
                  Médicos Certificados
                </a>
              </li>
            </ul>
          </div>

          {/* Contact info */}
          <div className="col-lg-3 col-md-6 mb-4">
            <h6 className="fw-bold mb-3">Contacto</h6>
            <ul className="list-unstyled">
              <li className="mb-2 d-flex text-muted align-items-center">
                <i className="mdi mdi-map-marker me-2"></i>
                <span>Manizales, Colombia</span>
              </li>
              <li className="mb-2 d-flex text-muted align-items-center">
                <i className="mdi mdi-phone me-2"></i>
                <span>(+57) 312 345 0000</span>
              </li>
              <li className="mb-2 d-flex text-muted align-items-center">
                <i className="mdi mdi-email me-2"></i>
                <span>info&#64;medicitas.com</span>
              </li>
              <li className="mb-2 d-flex text-muted align-items-center">
                <i className="mdi mdi-clock me-2"></i>
                <span>Lun - Vie: 9:00 - 18:00</span>
              </li>
            </ul>
          </div>
        </div>

        <hr className="my-2 border-secondary" />

        {/* Copyright */}
        <div className="row align-items-center">
          <div className="col-md-6">
            <p className="text-muted mb-0">
              &copy; {new Date().getFullYear()} MediCitas. Todos los derechos reservados.
            </p>
          </div>
          <div className="col-md-6 text-md-end">
            <a href="#" className="text-muted text-decoration-none me-3">Política de Privacidad</a>
            <a href="#" className="text-muted text-decoration-none">Términos de Servicio</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
