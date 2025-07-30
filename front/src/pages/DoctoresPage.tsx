import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { doctorService, specialtyService } from '../services/api';
import type { Doctor, Especialidad } from '../services/api';

const DoctoresPage: React.FC = () => {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [filteredDoctors, setFilteredDoctors] = useState<Doctor[]>([]);
  const [specialties, setSpecialties] = useState<Especialidad[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const [doctorsData, specialtiesData] = await Promise.all([
          doctorService.getAll(),
          specialtyService.getAll(),
        ]);
        
        setDoctors(doctorsData);
        setFilteredDoctors(doctorsData);
        setSpecialties(specialtiesData);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Filtrar doctores
  useEffect(() => {
    let filtered = doctors;

    // Filtrar por término de búsqueda
    if (searchTerm) {
      filtered = filtered.filter(doctor =>
        doctor.nombre_completo.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doctor.especialidades.some(esp =>
          esp.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }

    // Filtrar por especialidad seleccionada
    if (selectedSpecialty) {
      filtered = filtered.filter(doctor =>
        doctor.especialidades.includes(selectedSpecialty)
      );
    }

    setFilteredDoctors(filtered);
  }, [doctors, searchTerm, selectedSpecialty]);

  const handleSpecialtyFilter = (specialtyName: string) => {
    setSelectedSpecialty(specialtyName === selectedSpecialty ? '' : specialtyName);
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Cargando doctores...</span>
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
            <i className="mdi mdi-doctor text-primary me-3"></i>
            Nuestros Doctores
          </h1>
          <h5 className="text-center text-muted">
            Encuentra al especialista que necesitas entre nuestros {doctors.length} profesionales
          </h5>
        </div>
      </div>

      {/* Filtros */}
      <div className="row mb-4">
        <div className="col-md-8">
          <div className="input-group">
            <span className="input-group-text rounded-start-pill border-0">
              <i className="mdi mdi-magnify "></i>
            </span>
            <input
              type="text"
              className="form-control"
              placeholder="Buscar por nombre o especialidad..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
        <div className="col-md-3 m-auto">
          <select
            className="form-select"
            value={selectedSpecialty}
            onChange={(e) => setSelectedSpecialty(e.target.value)}
          >
            <option value="">Todas las especialidades</option>
            {specialties.map((specialty) => (
              <option key={specialty.id} value={specialty.nombre}>
                {specialty.nombre}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Filtros rápidos por especialidad */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex flex-wrap gap-2">
            <button
              className={`btn btn-sm ${!selectedSpecialty ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setSelectedSpecialty('')}
            >
              Todos
            </button>
            {specialties.slice(0, 8).map((specialty) => (
              <button
                key={specialty.id}
                className={`btn btn-sm ${
                  selectedSpecialty === specialty.nombre ? 'btn-primary' : 'btn-outline-primary'
                }`}
                onClick={() => handleSpecialtyFilter(specialty.nombre)}
              >
                {specialty.nombre}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Resultados */}
      <div className="row mb-4">
        <div className="col-12">
          <p className="text-muted">
            Mostrando {filteredDoctors.length} de {doctors.length} doctores
            {selectedSpecialty && ` en ${selectedSpecialty}`}
            {searchTerm && ` que coinciden con "${searchTerm}"`}
          </p>
        </div>
      </div>

      {/* Lista de doctores */}
      {filteredDoctors.length === 0 ? (
        <div className="row">
          <div className="col-12 text-center">
            <i className="mdi mdi-doctor mdi-xl text-muted mb-3"></i>
            <h4 className="text-muted">No se encontraron doctores</h4>
            <p className="text-muted">
              Intenta ajustar tus filtros de búsqueda
            </p>
          </div>
        </div>
      ) : (
        <div className="row g-4">
          {filteredDoctors.map((doctor) => (
            <div key={doctor.id} className="col-md-6 col-lg-4">
              <div className="card h-100">
                <div className="card-body">
                  <div className="d-flex align-items-center mb-3">
                    <div className="bg-primary bg-opacity-10 rounded-circle p-3 me-3">
                      {doctor.foto_perfil_url ? (
                        <img
                          src={doctor.foto_perfil_url}
                          alt={doctor.nombre_completo}
                          className="rounded-circle"
                          style={{ width: '50px', height: '50px', objectFit: 'cover' }}
                        />
                      ) : (
                        <i className="mdi mdi-doctor text-primary mdi-lg"></i>
                      )}
                    </div>
                    <div className="flex-grow-1">
                      <h5 className="card-title mb-1 text-primary">{doctor.nombre_completo}</h5>
                      <small className="text-muted">
                        <i className="mdi mdi-certificate me-1"></i>
                        Cédula: {doctor.cedula_profesional}
                      </small>
                    </div>
                  </div>

                  <div className="mb-3">
                    <h6 className="fw-semibold mb-2">
                      <i className="mdi mdi-medical-bag me-1"></i>
                      Especialidades:
                    </h6>
                    <div className="d-flex flex-wrap gap-1">
                      {doctor.especialidades.map((esp, index) => (
                        <span key={index} className="badge bg-secondary">
                          {esp}
                        </span>
                      ))}
                    </div>
                  </div>

                  {doctor.telefono && (
                    <div className="mb-2">
                      <small className="text-muted">
                        <i className="mdi mdi-phone me-1"></i>
                        {doctor.telefono}
                      </small>
                    </div>
                  )}

                  {doctor.biografia && (
                    <p className="card-text text-muted small mb-3">
                      {doctor.biografia.length > 120
                        ? `${doctor.biografia.substring(0, 120)}...`
                        : doctor.biografia
                      }
                    </p>
                  )}

                  <div className="d-flex gap-2 mt-auto">
                    <Link
                      to={`/doctor/${doctor.id}`}
                      className="btn btn-outline-primary btn-sm flex-fill"
                    >
                      <i className="mdi mdi-account-details me-1"></i>
                      Ver Perfil
                    </Link>
                    <Link
                      to={`/doctor/${doctor.id}?action=book`}
                      className="btn btn-primary btn-sm flex-fill"
                    >
                      <i className="mdi mdi-calendar-plus me-1"></i>
                      Reservar
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Call to Action */}
      <div className="row m-5">
        <div className="col-12">
          <div className="card border-0">
            <div className="card-body text-center py-4">
              <h4 className="card-title text-primary">¿No encuentras lo que buscas?</h4>
              <p className="card-text text-muted">
                Contáctanos y te ayudaremos a encontrar el especialista adecuado para ti
              </p>
              <div className="d-flex justify-content-center gap-2">
                <Link to="/" className="btn btn-primary">
                  <i className="mdi mdi-home me-2"></i>
                  Volver al Inicio
                </Link>
                <Link to="/especialidades" className="btn btn-outline-primary">
                  <i className="mdi mdi-medical-bag me-2"></i>
                  Ver Especialidades
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctoresPage;

