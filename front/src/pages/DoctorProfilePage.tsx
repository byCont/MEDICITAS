import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { doctorService, appointmentService, specialtyService, Doctor, Especialidad } from '../services/api';

const DoctorProfilePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();
  
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [specialties, setSpecialties] = useState<Especialidad[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showBookingForm, setShowBookingForm] = useState(false);
  
  // Estado del formulario de reserva
  const [bookingData, setBookingData] = useState({
    especialidad_id: '',
    fecha_hora: '',
    motivo_consulta: '',
    duracion_minutos: 30,
  });
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [doctorsData, specialtiesData] = await Promise.all([
          doctorService.getAll(),
          specialtyService.getAll(),
        ]);
        
        const foundDoctor = doctorsData.find(d => d.id === parseInt(id || '0'));
        if (!foundDoctor) {
          setError('Doctor no encontrado');
          return;
        }
        
        setDoctor(foundDoctor);
        setSpecialties(specialtiesData);
        
        // Si viene con action=book, mostrar formulario de reserva
        if (searchParams.get('action') === 'book') {
          setShowBookingForm(true);
        }
      } catch (error) {
        console.error('Error loading doctor:', error);
        setError('Error al cargar la información del doctor');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      loadData();
    }
  }, [id, searchParams]);

  const handleBookingChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setBookingData({
      ...bookingData,
      [e.target.name]: e.target.value,
    });
  };

  const handleBookingSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      navigate('/login', { state: { from: location } });
      return;
    }

    if (user?.rol !== 'Paciente') {
      setBookingError('Solo los pacientes pueden reservar citas');
      return;
    }

    setBookingLoading(true);
    setBookingError('');

    try {
      const appointmentData = {
        doctor_id: parseInt(id || '0'),
        especialidad_id: parseInt(bookingData.especialidad_id),
        fecha_hora: bookingData.fecha_hora,
        motivo_consulta: bookingData.motivo_consulta || undefined,
        duracion_minutos: bookingData.duracion_minutos,
      };

      await appointmentService.create(appointmentData);
      setBookingSuccess(true);
      
      // Redirigir a mis citas después de 2 segundos
      setTimeout(() => {
        navigate('/mis-citas');
      }, 2000);
    } catch (error: any) {
      console.error('Booking error:', error);
      setBookingError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        'Error al reservar la cita. Intenta nuevamente.'
      );
    } finally {
      setBookingLoading(false);
    }
  };

  // Obtener especialidades del doctor con sus IDs
  const getDoctorSpecialtiesWithIds = () => {
    if (!doctor || !specialties.length) return [];
    
    return specialties.filter(specialty => 
      doctor.especialidades.includes(specialty.nombre)
    );
  };

  // Generar horarios disponibles (ejemplo básico)
  const generateAvailableSlots = () => {
    const slots = [];
    const today = new Date();
    
    for (let i = 1; i <= 14; i++) { // Próximos 14 días
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      
      // Horarios de 9:00 a 17:00, cada 30 minutos
      for (let hour = 9; hour < 17; hour++) {
        for (let minute = 0; minute < 60; minute += 30) {
          const slotDate = new Date(date);
          slotDate.setHours(hour, minute, 0, 0);
          
          // Saltar fines de semana
          if (slotDate.getDay() === 0 || slotDate.getDay() === 6) continue;
          
          slots.push(slotDate.toISOString().slice(0, 16));
        }
      }
    }
    
    return slots;
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Cargando perfil del doctor...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error || !doctor) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          <i className="mdi mdi-alert-circle me-2"></i>
          {error || 'Doctor no encontrado'}
        </div>
      </div>
    );
  }

  if (bookingSuccess) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <div className="card-body text-center">
                <i className="mdi mdi-check-circle mdi-xl text-success mb-3"></i>
                <h3 className="text-success">¡Cita Reservada Exitosamente!</h3>
                <p className="text-muted">
                  Tu cita con {doctor.nombre_completo} ha sido programada. 
                  Serás redirigido a tus citas en unos segundos.
                </p>
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Cargando...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Perfil del doctor */}
        <div className="col-lg-8">
          <div className="card">
            <div className="card-body">
              <div className="row">
                <div className="col-md-4 text-center">
                  <div className="mb-3">
                    {doctor.foto_perfil_url ? (
                      <img
                        src={doctor.foto_perfil_url}
                        alt={doctor.nombre_completo}
                        className="rounded-circle img-fluid"
                        style={{ width: '150px', height: '150px', objectFit: 'cover' }}
                      />
                    ) : (
                      <div className="bg-primary bg-opacity-10 rounded-circle p-4 mx-auto" style={{ width: '150px', height: '150px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <i className="mdi mdi-doctor text-primary" style={{ fontSize: '4rem' }}></i>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="col-md-8">
                  <h1 className="display-6 fw-bold mb-2">{doctor.nombre_completo}</h1>
                  
                  <div className="mb-3">
                    <span className="badge bg-primary me-2">
                      <i className="mdi mdi-certificate me-1"></i>
                      Cédula: {doctor.cedula_profesional}
                    </span>
                  </div>

                  <div className="mb-3">
                    <h6 className="fw-semibold mb-2">
                      <i className="mdi mdi-medical-bag me-1"></i>
                      Especialidades:
                    </h6>
                    <div className="d-flex flex-wrap gap-2">
                      {doctor.especialidades.map((esp, index) => (
                        <span key={index} className="badge bg-secondary">
                          {esp}
                        </span>
                      ))}
                    </div>
                  </div>

                  {doctor.telefono && (
                    <div className="mb-2">
                      <i className="mdi mdi-phone text-primary me-2"></i>
                      <span>{doctor.telefono}</span>
                    </div>
                  )}

                  <div className="mb-3">
                    <i className="mdi mdi-email text-primary me-2"></i>
                    <span>{doctor.email}</span>
                  </div>

                  <div className="d-flex gap-2">
                    <button
                      className="btn btn-primary"
                      onClick={() => setShowBookingForm(true)}
                    >
                      <i className="mdi mdi-calendar-plus me-2"></i>
                      Reservar Cita
                    </button>
                    <button className="btn btn-outline-primary">
                      <i className="mdi mdi-message me-2"></i>
                      Contactar
                    </button>
                  </div>
                </div>
              </div>

              {doctor.biografia && (
                <div className="row mt-4">
                  <div className="col-12">
                    <h5 className="fw-semibold mb-3">
                      <i className="mdi mdi-account-details text-primary me-2"></i>
                      Sobre el Doctor
                    </h5>
                    <p className="text-muted">{doctor.biografia}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Formulario de reserva */}
        <div className="col-lg-4">
          {showBookingForm && (
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">
                  <i className="mdi mdi-calendar-plus text-primary me-2"></i>
                  Reservar Cita
                </h5>
              </div>
              <div className="card-body">
                {!isAuthenticated ? (
                  <div className="text-center">
                    <p className="text-muted mb-3">
                      Debes iniciar sesión para reservar una cita
                    </p>
                    <button
                      className="btn btn-primary"
                      onClick={() => navigate('/login', { state: { from: location } })}
                    >
                      <i className="mdi mdi-login me-2"></i>
                      Iniciar Sesión
                    </button>
                  </div>
                ) : (
                  <form onSubmit={handleBookingSubmit}>
                    {bookingError && (
                      <div className="alert alert-danger" role="alert">
                        <i className="mdi mdi-alert-circle me-2"></i>
                        {bookingError}
                      </div>
                    )}

                    <div className="mb-3">
                      <label htmlFor="especialidad_id" className="form-label">
                        Especialidad *
                      </label>
                      <select
                        className="form-select"
                        id="especialidad_id"
                        name="especialidad_id"
                        value={bookingData.especialidad_id}
                        onChange={handleBookingChange}
                        required
                      >
                        <option value="">Selecciona una especialidad</option>
                        {getDoctorSpecialtiesWithIds().map((specialty) => (
                          <option key={specialty.id} value={specialty.id}>
                            {specialty.nombre}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="mb-3">
                      <label htmlFor="fecha_hora" className="form-label">
                        Fecha y Hora *
                      </label>
                      <select
                        className="form-select"
                        id="fecha_hora"
                        name="fecha_hora"
                        value={bookingData.fecha_hora}
                        onChange={handleBookingChange}
                        required
                      >
                        <option value="">Selecciona fecha y hora</option>
                        {generateAvailableSlots().slice(0, 20).map((slot) => (
                          <option key={slot} value={slot}>
                            {new Date(slot).toLocaleDateString('es-ES', {
                              weekday: 'short',
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="mb-3">
                      <label htmlFor="duracion_minutos" className="form-label">
                        Duración
                      </label>
                      <select
                        className="form-select"
                        id="duracion_minutos"
                        name="duracion_minutos"
                        value={bookingData.duracion_minutos}
                        onChange={handleBookingChange}
                      >
                        <option value={30}>30 minutos</option>
                        <option value={60}>60 minutos</option>
                      </select>
                    </div>

                    <div className="mb-3">
                      <label htmlFor="motivo_consulta" className="form-label">
                        Motivo de la consulta
                      </label>
                      <textarea
                        className="form-control"
                        id="motivo_consulta"
                        name="motivo_consulta"
                        rows={3}
                        value={bookingData.motivo_consulta}
                        onChange={handleBookingChange}
                        placeholder="Describe brevemente el motivo de tu consulta..."
                      />
                    </div>

                    <div className="d-grid gap-2">
                      <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={bookingLoading}
                      >
                        {bookingLoading ? (
                          <>
                            <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                            Reservando...
                          </>
                        ) : (
                          <>
                            <i className="mdi mdi-calendar-check me-2"></i>
                            Confirmar Reserva
                          </>
                        )}
                      </button>
                      <button
                        type="button"
                        className="btn btn-outline-secondary"
                        onClick={() => setShowBookingForm(false)}
                      >
                        Cancelar
                      </button>
                    </div>
                  </form>
                )}
              </div>
            </div>
          )}

          {/* Información adicional */}
          <div className="card mt-3">
            <div className="card-body">
              <h6 className="card-title">
                <i className="mdi mdi-information text-primary me-2"></i>
                Información de Citas
              </h6>
              <ul className="list-unstyled mb-0">
                <li className="mb-2">
                  <i className="mdi mdi-clock text-muted me-2"></i>
                  <small>Duración estándar: 30-60 min</small>
                </li>
                <li className="mb-2">
                  <i className="mdi mdi-calendar text-muted me-2"></i>
                  <small>Disponible Lun-Vie 9:00-17:00</small>
                </li>
                <li className="mb-2">
                  <i className="mdi mdi-phone text-muted me-2"></i>
                  <small>Confirmación por teléfono</small>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorProfilePage;

