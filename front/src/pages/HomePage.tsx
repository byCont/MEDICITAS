import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { specialtyService, doctorService, Doctor, Especialidad } from '../services/api';
import './pages.scss';

const HomePage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState<Doctor[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [specialties, setSpecialties] = useState<Especialidad[]>([]);
  const navigate = useNavigate();

  // Cargar especialidades al montar el componente
  useEffect(() => {
    const loadSpecialties = async () => {
      try {
        const data = await specialtyService.getAll();
        setSpecialties(data.slice(0, 6)); // Mostrar solo las primeras 6
      } catch (error) {
        console.error('Error loading specialties:', error);
      }
    };

    loadSpecialties();
  }, []);

  // Manejar búsqueda
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setIsSearching(true);
    try {
      const results = await doctorService.searchBySpecialty(searchTerm);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching doctors:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  // Buscar por especialidad específica
  const handleSpecialtyClick = async (specialtyName: string) => {
    setSearchTerm(specialtyName);
    setIsSearching(true);
    try {
      const results = await doctorService.searchBySpecialty(specialtyName);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching doctors:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="container mt-4">
      {/* Hero Section */}
      <div className="row mb-5 position-relative">
        <div className="col-12 text-center position-relative hero-section">
          <div className="container position-relative">
            <h1 className="display-4 fw-bold mb-4 mt-6" style={{textShadow: '0 0 5px var(--bs-primary-b)'}}>
              Encuentra la cita<br/>de tu vida
            </h1>
            
            {/* Barra de búsqueda */}
            <form onSubmit={handleSearch} className="row g-2 justify-content-center mb-4">
              <div className="col-md-8">
                <div className="subject-search">
                  <div className="p-0">
                    <div className="input-group input-group-lg">
                      <span className="input-group-text bg-transparent border-0">
                        <i className="mdi mdi-magnify"></i>
                      </span>
                      <input
                        type="text"
                        className="form-control border-0 shadow-none"
                        placeholder="¿De qué necesitas la cita?"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                      />
                      <button 
                        className="btn btn-primary px-4" 
                        type="submit" 
                        disabled={isSearching}
                      >
                        {isSearching ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                            Buscando...
                          </>
                        ) : (
                          'Buscar'
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </form>

            {/* Filtros rápidos por especialidad */}
            <div className="row g-2 justify-content-center">
              <div className="col-auto">
                <Link
                  className="btn btn-sm btn-outline-primary rounded-pill"
                  to="/especialidades"
                >
                  Todas
                </Link>
              </div>
              {specialties.slice(0, 8).map((specialty) => (
                <div key={specialty.id} className="col-auto">
                  <button
                    type="button"
                    className="btn btn-sm btn-outline-primary rounded-pill"
                    onClick={() => handleSpecialtyClick(specialty.nombre)}
                  >
                    {specialty.nombre}
                  </button>
                </div>
              ))}
            </div>

            {/* Estadísticas */}
            <div className="row g-2 mb-4 justify-content-end">
              <div className="col-auto">
                <div className=" rounded-4 bg-white border-0 shadow-sm">
                  <div className="card-body text-center p-2">
                    <i className="mdi mdi-doctor mdi-1x text-dark mb-1"></i>
                    <h4 className="fw-bold mb-0 text-dark">+500</h4>
                    <small className="text-dark">Especialistas</small>
                  </div>
                </div>
              </div>
              <div className="col-auto">
                <div className=" rounded-4 bg-white border-0 shadow-sm">
                  <div className="card-body text-center p-2">
                    <i className="mdi mdi-heart-pulse mdi-1x text-dark mb-1"></i>
                    <h4 className="fw-bold mb-0 text-dark">+50</h4>
                    <small className="text-dark">Especialidades</small>
                  </div>
                </div>
              </div>
              <div className="col-auto">
                <div className=" rounded-4 bg-white border-0 shadow-sm">
                  <div className="card-body text-center p-2">
                    <i className="mdi mdi-clock mdi-1x text-dark mb-1"></i>
                    <h4 className="fw-bold mb-0 text-dark">24/7</h4>
                    <small className="text-dark">Disponibilidad</small>
                  </div>
                </div>
              </div>
            </div>

        </div>
      </div>

      {/* Resultados de búsqueda */}
      {searchResults.length > 0 && (
        <div className="row mb-5">
          <div className="col-12">
            <h2 className="mb-4">
              Especialistas recomendados para "{searchTerm}"
            </h2>
            <div className="row g-4">
              {searchResults.map((doctor) => (
                <div key={doctor.id} className="col-md-6 col-lg-4">
                  <div className="card h-100">
                    <div className="card-body">
                      <div className="d-flex align-items-center mb-3">
                        {doctor.foto_perfil_url && (
                          <img
                            src={doctor.foto_perfil_url}
                            alt={doctor.nombre_completo}
                            className="rounded-circle img-fluid me-1"
                            style={{ width: '50px', height: '50px', objectFit: 'cover' }}
                            loading="lazy"
                          />
                        )}
                        <div>
                          <h5 className="card-title mb-1 text-primary">{doctor.nombre_completo}</h5>
                          <small className="text-muted">Cédula: {doctor.cedula_profesional}</small>
                        </div>
                      </div>
                      
                      <div className="mb-3">
                        <h6 className="fw-semibold mb-2">Especialidades:</h6>
                        <div className="d-flex flex-wrap gap-1">
                          {doctor.especialidades.map((esp, index) => (
                            <span key={index} className="badge bg-secondary">
                              {esp}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      {doctor.biografia && (
                        <p className="card-text text-muted small">
                          {doctor.biografia.length > 100 
                            ? `${doctor.biografia.substring(0, 100)}...` 
                            : doctor.biografia
                          }
                        </p>
                      )}
                      
                      <div className="d-flex gap-2 mt-auto">
                        <Link to={`/doctor/${doctor.id}`} className="btn btn-outline-primary btn-sm flex-fill">
                          Ver Perfil
                        </Link>
                        <Link to={`/doctor/${doctor.id}?action=book`} className="btn btn-primary btn-sm flex-fill">
                          <i className="mdi mdi-calendar-plus me-1"></i>
                          Reservar
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Especialidades populares */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="text-center mb-4">
            <h2 className="fw-bold">Especialidades Populares</h2>
            <p className="text-muted">Encuentra especialistas en las áreas médicas más solicitadas</p>
          </div>

          <div className="row g-4">
            {specialties.map((specialty) => (
              <div key={specialty.id} className="col-md-6 col-lg-4">
                <div 
                  className="card h-100 cursor-pointer"
                  onClick={() => handleSpecialtyClick(specialty.nombre)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="card-body text-center">
                    <i className="mdi mdi-medical-bag mdi-xl text-primary mb-3"></i>
                    <h5 className="card-title">{specialty.nombre}</h5>
                    <p className="card-text text-muted">
                      {specialty.descripcion || 'Especialidad médica disponible'}
                    </p>
                    <small className="text-primary">Ver especialistas →</small>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-4">
            <Link to="/especialidades" className="btn btn-outline-primary">
              Ver todas las especialidades
            </Link>
          </div>
        </div>
      </div>

      {/* Acciones rápidas */}
      <div className="row mb-5">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">
                <i className="mdi mdi-calendar-plus text-primary me-2"></i>
                Agendar Nueva Cita
              </h5>
              <p className="card-text">Busca un especialista y agenda una nueva cita médica.</p>
              <Link to="/doctores" className="btn btn-primary">Agendar Cita</Link>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">
                <i className="mdi mdi-calendar-clock text-primary me-2"></i>
                Mis Próximas Citas
              </h5>
              <p className="card-text">Consulta tus próximas citas y gestiona tus recordatorios.</p>
              <Link to="/mis-citas" className="btn btn-primary">Ver Citas</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="row">
        <div className="col-12">
          <div className="card bg-primary text-white">
            <div className="card-body text-center py-5">
              <h2 className="card-title">¿Eres un profesional de la salud?</h2>
              <p className="card-text lead">
                Únete a nuestra plataforma y conecta con miles de pacientes
              </p>
              <Link to="/registro-doctor" className="btn btn-light btn-lg">
                Registrarse como Doctor
              </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
