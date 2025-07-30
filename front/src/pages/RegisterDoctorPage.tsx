import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { specialtyService } from '../services/api';
import type { Especialidad } from '../services/api';

const RegisterDoctorPage: React.FC = () => {
  const [formData, setFormData] = useState({
    // Datos del usuario
    nombre_completo: '',
    email: '',
    password: '',
    confirmPassword: '',
    telefono: '',
    fecha_nacimiento: '',
    // Datos del perfil
    cedula_profesional: '',
    biografia: '',
    foto_perfil_url: '',
    // Especialidades
    especialidades_ids: [] as number[],
  });
  const [specialties, setSpecialties] = useState<Especialidad[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const { registerDoctor } = useAuth();
  const navigate = useNavigate();

  // Cargar especialidades
  useEffect(() => {
    const loadSpecialties = async () => {
      try {
        const data = await specialtyService.getAll();
        setSpecialties(data);
      } catch (error) {
        console.error('Error loading specialties:', error);
      }
    };

    loadSpecialties();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSpecialtyChange = (specialtyId: number) => {
    const currentIds = formData.especialidades_ids;
    if (currentIds.includes(specialtyId)) {
      setFormData({
        ...formData,
        especialidades_ids: currentIds.filter(id => id !== specialtyId),
      });
    } else {
      setFormData({
        ...formData,
        especialidades_ids: [...currentIds, specialtyId],
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validaciones
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      setLoading(false);
      return;
    }

    if (formData.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      setLoading(false);
      return;
    }

    if (formData.especialidades_ids.length === 0) {
      setError('Debe seleccionar al menos una especialidad');
      setLoading(false);
      return;
    }

    try {
      const doctorData = {
        usuario: {
          nombre_completo: formData.nombre_completo,
          email: formData.email,
          password: formData.password,
          telefono: formData.telefono || undefined,
          fecha_nacimiento: formData.fecha_nacimiento || undefined,
        },
        perfil: {
          cedula_profesional: formData.cedula_profesional,
          biografia: formData.biografia || undefined,
          foto_perfil_url: formData.foto_perfil_url || undefined,
        },
        especialidades_ids: formData.especialidades_ids,
      };

      await registerDoctor(doctorData);
      setSuccess(true);
      
      // Redirigir al login después de 3 segundos
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error: any) {
      console.error('Doctor registration error:', error);
      setError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        'Error al registrar doctor. Intenta nuevamente.'
      );
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card border-0">
              <div className="card-body text-center">
                <i className="mdi mdi-check-circle mdi-xl text-success mb-3"></i>
                <h3 className="text-success">¡Registro de Doctor Exitoso!</h3>
                <p className="text-muted">
                  Tu cuenta de doctor ha sido creada correctamente. Serás redirigido al login en unos segundos.
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
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-10 col-lg-8 ">
          <div className="card border-0 mb-5">
            <div className="card-body">
              <div className="text-center mb-4">
                <i className="mdi mdi-stethoscope mdi-xl text-primary mb-3"></i>
                <h2 className="card-title text-primary">Registro de Doctor</h2>
                <p className="text-muted">Únete a nuestra plataforma como profesional de la salud</p>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  <i className="mdi mdi-alert-circle me-2"></i>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {/* Información Personal */}
                <div className="mb-4">
                  <h5 className="text-primary mb-3">
                    <i className="mdi mdi-account me-2"></i>
                    Información Personal
                  </h5>
                  
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="nombre_completo" className="form-label">
                        Nombre Completo *
                      </label>
                      <input
                        type="text"
                        className="form-control"
                        id="nombre_completo"
                        name="nombre_completo"
                        value={formData.nombre_completo}
                        onChange={handleChange}
                        required
                        placeholder="Dr. Juan Pérez"
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="email" className="form-label">
                        Correo Electrónico *
                      </label>
                      <input
                        type="email"
                        className="form-control"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        placeholder="doctor@email.com"
                      />
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="telefono" className="form-label">
                        Teléfono
                      </label>
                      <input
                        type="tel"
                        className="form-control"
                        id="telefono"
                        name="telefono"
                        value={formData.telefono}
                        onChange={handleChange}
                        placeholder="+1234567890"
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="fecha_nacimiento" className="form-label">
                        Fecha de Nacimiento
                      </label>
                      <input
                        type="date"
                        className="form-control"
                        id="fecha_nacimiento"
                        name="fecha_nacimiento"
                        value={formData.fecha_nacimiento}
                        onChange={handleChange}
                      />
                    </div>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="password" className="form-label">
                        Contraseña *
                      </label>
                      <input
                        type="password"
                        className="form-control"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                        placeholder="Mínimo 8 caracteres"
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="confirmPassword" className="form-label">
                        Confirmar Contraseña *
                      </label>
                      <input
                        type="password"
                        className="form-control"
                        id="confirmPassword"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                        placeholder="Repite tu contraseña"
                      />
                    </div>
                  </div>
                </div>

                {/* Información Profesional */}
                <div className="mb-4">
                  <h5 className="text-primary mb-3">
                    <i className="mdi mdi-certificate me-2"></i>
                    Información Profesional
                  </h5>
                  
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label htmlFor="cedula_profesional" className="form-label">
                        Cédula Profesional *
                      </label>
                      <input
                        type="text"
                        className="form-control"
                        id="cedula_profesional"
                        name="cedula_profesional"
                        value={formData.cedula_profesional}
                        onChange={handleChange}
                        required
                        placeholder="123456789"
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label htmlFor="foto_perfil_url" className="form-label">
                        URL de Foto de Perfil
                      </label>
                      <input
                        type="url"
                        className="form-control"
                        id="foto_perfil_url"
                        name="foto_perfil_url"
                        value={formData.foto_perfil_url}
                        onChange={handleChange}
                        placeholder="https://ejemplo.com/foto.jpg"
                      />
                    </div>
                  </div>

                  <div className="mb-3">
                    <label htmlFor="biografia" className="form-label">
                      Biografía Profesional
                    </label>
                    <textarea
                      className="form-control rounded-4"
                      id="biografia"
                      name="biografia"
                      rows={4}
                      value={formData.biografia}
                      onChange={handleChange}
                      placeholder="Describe tu experiencia, formación y especialización..."
                    />
                  </div>
                </div>

                {/* Especialidades */}
                <div className="mb-4">
                  <h5 className="text-primary mb-3">
                    <i className="mdi mdi-medical-bag me-2"></i>
                    Especialidades *
                  </h5>
                  <p className="text-muted small mb-3">
                    Selecciona al menos una especialidad médica
                  </p>
                  
                  <div className="row">
                    {specialties.map((specialty) => (
                      <div key={specialty.id} className="col-md-6 col-lg-4 mb-2">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id={`specialty-${specialty.id}`}
                            checked={formData.especialidades_ids.includes(specialty.id)}
                            onChange={() => handleSpecialtyChange(specialty.id)}
                          />
                          <label className="form-check-label" htmlFor={`specialty-${specialty.id}`}>
                            {specialty.nombre}
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="d-grid">
                  <button
                    type="submit"
                    className="btn btn-primary btn-lg"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Registrando Doctor...
                      </>
                    ) : (
                      <>
                        <i className="mdi mdi-stethoscope me-2"></i>
                        Crear Cuenta de Doctor
                      </>
                    )}
                  </button>
                </div>
              </form>

              <hr className="my-4" />

              <div className="text-center">
                <p className="mb-2">¿Ya tienes una cuenta?</p>
                <Link to="/login" className="btn btn-outline-primary me-2">
                  <i className="mdi mdi-login me-2"></i>
                  Iniciar Sesión
                </Link>
                <Link to="/registro" className="btn btn-outline-primary">
                  <i className="mdi mdi-account-plus me-2"></i>
                  Registro de Paciente
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterDoctorPage;

