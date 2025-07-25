import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { appointmentService, Cita } from '../services/api';

const MisCitasPage: React.FC = () => {
  const [citas, setCitas] = useState<Cita[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    const loadCitas = async () => {
      try {
        const data = await appointmentService.getMyCitas();
        setCitas(data);
      } catch (error: any) {
        console.error('Error loading citas:', error);
        setError('Error al cargar las citas');
      } finally {
        setLoading(false);
      }
    };

    loadCitas();
  }, []);

  const getEstadoBadgeClass = (estado: string) => {
    switch (estado) {
      case 'Programada':
        return 'bg-warning';
      case 'Confirmada':
        return 'bg-info';
      case 'Completada':
        return 'bg-success';
      case 'Cancelada':
        return 'bg-danger';
      case 'No Asistió':
        return 'bg-secondary';
      default:
        return 'bg-secondary';
    }
  };

  const formatFecha = (fechaString: string) => {
    const fecha = new Date(fechaString);
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const isPastAppointment = (fechaString: string) => {
    return new Date(fechaString) < new Date();
  };

  const citasProgramadas = citas.filter(cita => 
    ['Programada', 'Confirmada'].includes(cita.estado) && !isPastAppointment(cita.fecha_hora)
  );
  
  const citasPasadas = citas.filter(cita => 
    ['Completada', 'Cancelada', 'No Asistió'].includes(cita.estado) || isPastAppointment(cita.fecha_hora)
  );

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Cargando citas...</span>
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
          <h1 className="display-5 fw-bold mb-2">
            <i className="mdi mdi-calendar-clock text-primary me-3"></i>
            Mis Citas
          </h1>
          <p className="text-muted fw-semibold lead">
            Gestiona tus citas médicas, {user?.nombre_completo}
          </p>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger" role="alert">
          <i className="mdi mdi-alert-circle me-2"></i>
          {error}
        </div>
      )}

      {/* Estadísticas rápidas */}
      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card bg-primary text-white">
            <div className="card-body text-center">
              <i className="mdi mdi-calendar-check mdi-lg mb-2"></i>
              <h4>{citasProgramadas.length}</h4>
              <p className="mb-0">Citas Próximas</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card bg-success text-white">
            <div className="card-body text-center">
              <i className="mdi mdi-calendar-check mdi-lg mb-2"></i>
              <h4>{citas.filter(c => c.estado === 'Completada').length}</h4>
              <p className="mb-0">Citas Completadas</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card bg-info text-white">
            <div className="card-body text-center">
              <i className="mdi mdi-calendar-multiple mdi-lg mb-2"></i>
              <h4>{citas.length}</h4>
              <p className="mb-0">Total de Citas</p>
            </div>
          </div>
        </div>
      </div>

      {citas.length === 0 ? (
        <div className="row">
          <div className="col-12 text-center">
            <div className="card">
              <div className="card-body py-5">
                <i className="mdi mdi-calendar-blank mdi-xl text-muted mb-3"></i>
                <h4 className="text-muted">No tienes citas programadas</h4>
                <p className="text-muted mb-4">
                  ¡Es hora de cuidar tu salud! Agenda tu primera cita con nuestros especialistas.
                </p>
                <Link to="/doctores" className="btn btn-primary">
                  <i className="mdi mdi-calendar-plus me-2"></i>
                  Agendar Nueva Cita
                </Link>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Citas próximas */}
          {citasProgramadas.length > 0 && (
            <div className="row mb-5">
              <div className="col-12">
                <h3 className="mb-3">
                  <i className="mdi mdi-calendar-clock text-primary me-2"></i>
                  Próximas Citas ({citasProgramadas.length})
                </h3>
                <div className="row g-4">
                  {citasProgramadas.map((cita) => (
                    <div key={cita.id} className="col-md-6 col-lg-4">
                      <div className="card border-primary">
                        <div className="card-body">
                          <div className="d-flex justify-content-between align-items-start mb-3">
                            <h5 className="card-title mb-0">
                              <i className="mdi mdi-doctor text-primary me-2"></i>
                              Cita #{cita.id}
                            </h5>
                            <span className={`badge ${getEstadoBadgeClass(cita.estado)}`}>
                              {cita.estado}
                            </span>
                          </div>
                          
                          <div className="mb-2">
                            <small className="text-muted">
                              <i className="mdi mdi-calendar me-1"></i>
                              {formatFecha(cita.fecha_hora)}
                            </small>
                          </div>
                          
                          <div className="mb-2">
                            <small className="text-muted">
                              <i className="mdi mdi-clock me-1"></i>
                              Duración: {cita.duracion_minutos} minutos
                            </small>
                          </div>

                          {cita.motivo_consulta && (
                            <div className="mb-3">
                              <small className="text-muted">
                                <i className="mdi mdi-note-text me-1"></i>
                                <strong>Motivo:</strong> {cita.motivo_consulta}
                              </small>
                            </div>
                          )}

                          <div className="d-flex gap-2">
                            <button className="btn btn-outline-primary btn-sm flex-fill">
                              <i className="mdi mdi-information me-1"></i>
                              Detalles
                            </button>
                            <button className="btn btn-outline-danger btn-sm">
                              <i className="mdi mdi-cancel me-1"></i>
                              Cancelar
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Historial de citas */}
          {citasPasadas.length > 0 && (
            <div className="row">
              <div className="col-12">
                <h3 className="mb-3">
                  <i className="mdi mdi-history text-secondary me-2"></i>
                  Historial de Citas ({citasPasadas.length})
                </h3>
                <div className="row g-4">
                  {citasPasadas.map((cita) => (
                    <div key={cita.id} className="col-md-6 col-lg-4">
                      <div className="card">
                        <div className="card-body">
                          <div className="d-flex justify-content-between align-items-start mb-3">
                            <h6 className="card-title mb-0">
                              <i className="mdi mdi-doctor text-muted me-2"></i>
                              Cita #{cita.id}
                            </h6>
                            <span className={`badge ${getEstadoBadgeClass(cita.estado)}`}>
                              {cita.estado}
                            </span>
                          </div>
                          
                          <div className="mb-2">
                            <small className="text-muted">
                              <i className="mdi mdi-calendar me-1"></i>
                              {formatFecha(cita.fecha_hora)}
                            </small>
                          </div>

                          {cita.motivo_consulta && (
                            <div className="mb-3">
                              <small className="text-muted">
                                <i className="mdi mdi-note-text me-1"></i>
                                <strong>Motivo:</strong> {cita.motivo_consulta}
                              </small>
                            </div>
                          )}

                          <button className="btn btn-outline-secondary btn-sm w-100">
                            <i className="mdi mdi-eye me-1"></i>
                            Ver Detalles
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Call to Action */}
      <div className="row m-5">
        <div className="col-12">
          <div className="card">
            <div className="card-body text-center py-4">
              <h4 className="card-title text-primary">¿Necesitas agendar una nueva cita?</h4>
              <p className="card-text text-muted">
                Encuentra al especialista que necesitas y agenda tu cita en minutos
              </p>
              <div className="d-flex justify-content-center gap-2">
                <Link to="/doctores" className="btn btn-primary">
                  <i className="mdi mdi-calendar-plus me-2"></i>
                  Agendar Nueva Cita
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

export default MisCitasPage;

