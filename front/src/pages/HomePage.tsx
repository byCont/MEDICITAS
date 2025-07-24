import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { specialtyService, doctorService, Doctor, Especialidad } from '../services/api';

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
      <div className="row mb-5">
        <div className="col-12 text-center">
          <h1 className="display-4 fw-bold mb-4">
            Especialistas para ti, <span className="text-primary">cuando lo necesitas</span>
          </h1>
          <p className="lead mb-4">
            Encuentra y reserva citas con los mejores profesionales de la salud 
            de manera fácil y rápida.
          </p>

          {/* Barra de búsqueda */}
          <form onSubmit={handleSearch} className="row g-2 justify-content-center mb-4">
            <div className="col-md-6">
              <div className="input-group">
                <span className="input-group-text">
                  <i className="mdi mdi-magnify"></i>
                </span>
                <input
                  type="text"
                  className="form-control form-control-lg"
                  placeholder="Buscar por especialidad (ej: Cardiología, Dermatología...)"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button 
                  className="btn btn-primary btn-lg" 
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
          </form>

          {/* Estadísticas */}
          <div className="row g-4 mb-5">
            <div className="col-md-4">
              <div className="text-center">
                <i className="mdi mdi-doctor mdi-xl text-primary mb-2"></i>
                <h3 className="fw-bold">500+</h3>
                <p className="text-muted">Doctores Especialistas</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="text-center">
                <i className="mdi mdi-heart-pulse mdi-xl text-primary mb-2"></i>
                <h3 className="fw-bold">50+</h3>
                <p className="text-muted">Especialidades Médicas</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="text-center">
                <i className="mdi mdi-clock mdi-xl text-primary mb-2"></i>
                <h3 className="fw-bold">24/7</h3>
                <p className="text-muted">Disponibilidad</p>
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
              Resultados de búsqueda para "{searchTerm}"
            </h2>
            <div className="row g-4">
              {searchResults.map((doctor) => (
                <div key={doctor.id} className="col-md-6 col-lg-4">
                  <div className="card h-100">
                    <div className="card-body">
                      <div className="d-flex align-items-center mb-3">
                        <div className="bg-primary bg-opacity-10 rounded-circle p-3 me-3">
                          <i className="mdi mdi-doctor text-primary mdi-lg"></i>
                        </div>
                        <div>
                          <h5 className="card-title mb-1">{doctor.nombre_completo}</h5>
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
  );
};

export default HomePage;
