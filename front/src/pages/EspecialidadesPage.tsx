import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { specialtyService, doctorService, Especialidad } from '../services/api';

const EspecialidadesPage: React.FC = () => {
  const [specialties, setSpecialties] = useState<Especialidad[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredSpecialties, setFilteredSpecialties] = useState<Especialidad[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const loadSpecialties = async () => {
      try {
        const data = await specialtyService.getAll();
        setSpecialties(data);
        setFilteredSpecialties(data);
      } catch (error) {
        console.error('Error loading specialties:', error);
      } finally {
        setLoading(false);
      }
    };

    loadSpecialties();
  }, []);

  // Filtrar especialidades por término de búsqueda
  useEffect(() => {
    if (searchTerm) {
      const filtered = specialties.filter(specialty =>
        specialty.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (specialty.descripcion && specialty.descripcion.toLowerCase().includes(searchTerm.toLowerCase()))
      );
      setFilteredSpecialties(filtered);
    } else {
      setFilteredSpecialties(specialties);
    }
  }, [specialties, searchTerm]);

  const handleSpecialtyClick = async (specialtyName: string) => {
    // Redirigir a la página de doctores con filtro de especialidad
    navigate(`/doctores?specialty=${encodeURIComponent(specialtyName)}`);
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Cargando especialidades...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      {/* Header */}
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="display-5 fw-bold text-center mb-2">
            <i className="mdi mdi-medical-bag text-primary me-3"></i>
            Especialidades Médicas
          </h1>
          <h5 className="text-center text-muted">
            Explora nuestras {specialties.length} especialidades médicas disponibles
          </h5>
        </div>
      </div>

      {/* Barra de búsqueda */}
      <div className="row mb-4">
        <div className="col-md-8 mx-auto">
          <div className="input-group">
            <span className="input-group-text rounded-start-pill border-0">
              <i className="mdi mdi-magnify"></i>
            </span>
            <input
              type="text"
              className="form-control form-control-lg"
              placeholder="Buscar especialidad..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Resultados */}
      <div className="row mb-4">
        <div className="col-12">
          <p className="text-muted">
            Mostrando {filteredSpecialties.length} de {specialties.length} especialidades
            {searchTerm && ` que coinciden con "${searchTerm}"`}
          </p>
        </div>
      </div>

      {/* Lista de especialidades */}
      {filteredSpecialties.length === 0 ? (
        <div className="row">
          <div className="col-12 text-center">
            <i className="mdi mdi-medical-bag mdi-xl text-muted mb-3"></i>
            <h4 className="text-muted">No se encontraron especialidades</h4>
            <p className="text-muted">
              Intenta ajustar tu búsqueda
            </p>
          </div>
        </div>
      ) : (
        <div className="row g-4">
          {filteredSpecialties.map((specialty) => (
            <div key={specialty.id} className="col-md-6 col-lg-4">
              <div 
                className="card h-100 cursor-pointer"
                onClick={() => handleSpecialtyClick(specialty.nombre)}
                style={{ cursor: 'pointer' }}
              >
                <div className="card-body text-center">
                  <div className="d-flex align-items-center justify-content-center bg-primary bg-opacity-10 rounded-circle mx-auto mb-3" style={{ width: '80px', height: '80px' }}>
                    <i className="mdi mdi-medical-bag mdi-xl text-primary"></i>
                  </div>
                  
                  <h5 className="card-title text-primary">{specialty.nombre}</h5>
                  
                  <p className="card-text text-muted">
                    {specialty.descripcion || 'Especialidad médica disponible en nuestra plataforma'}
                  </p>
                  
                  <div className="mt-auto">
                    <small className="text-primary fw-semibold">
                      <i className="mdi mdi-arrow-right me-1"></i>
                      Ver especialistas
                    </small>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Información adicional */}
      <div className="row mt-5">
        <div className="col-12">
          <div className="card border-0">
            <div className="card-body">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <h4 className="card-title text-primary mb-2">
                    <i className="mdi mdi-information text-primary me-2"></i>
                    ¿Necesitas ayuda para elegir?
                  </h4>
                  <p className="card-text text-muted mb-0">
                    Si no estás seguro de qué especialista necesitas, nuestro equipo puede ayudarte 
                    a encontrar el profesional adecuado para tu consulta.
                  </p>
                </div>
                <div className="col-md-4 text-center">
                  <Link to="/doctores" className="btn btn-primary">
                    <i className="mdi mdi-doctor me-2"></i>
                    Ver Todos los Doctores
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Especialidades más populares */}
      <div className="row mt-5">
        <div className="col-12">
          <h3 className="text-center mb-4">Especialidades Más Solicitadas</h3>
          <div className="row g-3">
            {specialties.slice(0, 6).map((specialty) => (
              <div key={specialty.id} className="col-md-4 col-lg-2">
                <button
                  className="btn btn-outline-primary w-100"
                  onClick={() => handleSpecialtyClick(specialty.nombre)}
                >
                  {specialty.nombre}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="row m-5">
        <div className="col-12">
          <div className="card border-0 bg-primary text-white">
            <div className="card-body text-center py-4">
              <h4 className="card-title">¿Eres un especialista?</h4>
              <p className="card-text text-white">
                Únete a nuestra plataforma y conecta con pacientes que necesitan tu experiencia
              </p>
              <Link to="/registro-doctor" className="btn btn-light">
                <i className="mdi mdi-stethoscope me-2"></i>
                Registrarse como Doctor
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EspecialidadesPage;

