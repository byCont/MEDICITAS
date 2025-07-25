import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    nombre_completo: '',
    email: '',
    password: '',
    confirmPassword: '',
    telefono: '',
    fecha_nacimiento: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const { registerPatient } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
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

    try {
      const userData = {
        nombre_completo: formData.nombre_completo,
        email: formData.email,
        password: formData.password,
        telefono: formData.telefono || undefined,
        fecha_nacimiento: formData.fecha_nacimiento || undefined,
      };

      await registerPatient(userData);
      setSuccess(true);
      
      // Redirigir al login después de 2 segundos
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (error: any) {
      console.error('Registration error:', error);
      setError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        'Error al registrar usuario. Intenta nuevamente.'
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
            <div className="card">
              <div className="card-body text-center">
                <i className="mdi mdi-check-circle mdi-xl text-success mb-3"></i>
                <h3 className="text-success">¡Registro Exitoso!</h3>
                <p className="text-muted">
                  Tu cuenta ha sido creada correctamente. Serás redirigido al login en unos segundos.
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
        <div className="col-md-8 col-lg-6">
          <div className="card border-0 mb-5">
            <div className="card-body">
              <div className="text-center mb-4">
                <i className="mdi mdi-account-plus mdi-xl text-primary mb-3"></i>
                <h2 className="card-title text-primary">Registro de Paciente</h2>
                <p className="text-muted">Crea tu cuenta para agendar citas médicas</p>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  <i className="mdi mdi-alert-circle me-2"></i>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row">
                  <div className="col-md-12 mb-3">
                    <label htmlFor="nombre_completo" className="form-label">
                      <i className="mdi mdi-account me-2"></i>
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
                      placeholder="Tu nombre completo"
                    />
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="email" className="form-label">
                      <i className="mdi mdi-email me-2"></i>
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
                      placeholder="tu@email.com"
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="telefono" className="form-label">
                      <i className="mdi mdi-phone me-2"></i>
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
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="password" className="form-label">
                      <i className="mdi mdi-lock me-2"></i>
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
                      <i className="mdi mdi-lock-check me-2"></i>
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

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="fecha_nacimiento" className="form-label">
                      <i className="mdi mdi-calendar me-2"></i>
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

                <div className="d-grid">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Registrando...
                      </>
                    ) : (
                      <>
                        <i className="mdi mdi-account-plus me-2"></i>
                        Crear Cuenta
                      </>
                    )}
                  </button>
                </div>
              </form>

              <hr className="my-4" />

              <div className="text-center">
                <p className="mb-2">¿Ya tienes una cuenta?</p>
                <Link to="/login" className="btn btn-outline-primary">
                  <i className="mdi mdi-login me-2"></i>
                  Iniciar Sesión
                </Link>
              </div>

              <div className="text-center mt-3">
                <p className="text-muted small">
                  ¿Eres un profesional de la salud?{' '}
                  <Link to="/registro-doctor" className="text-primary">
                    Regístrate como Doctor
                  </Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;

