import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LoginPage: React.FC = () => {
  const [formData, setFormData] = useState({
    email: 'juan.perez@gmail.com',
    password: 'password123',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/';

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

    try {
      await login(formData);
      navigate(from, { replace: true });
    } catch (error: any) {
      console.error('Login error:', error);
      setError(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        'Error al iniciar sesión. Verifica tus credenciales.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center mb-5">
        <div className="col-md-6 col-lg-4">
          <div className="card border-0">
            <div className="card-body">
              <div className="text-center mb-4">
                <i className="mdi mdi-heart-pulse mdi-xl text-primary mb-3"></i>
                <h2 className="card-title text-primary">Iniciar Sesión</h2>
                <p className="text-muted">Accede a tu cuenta de MediCitas</p>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  <i className="mdi mdi-alert-circle me-2"></i>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">
                    <i className="mdi mdi-email me-2"></i>
                    Correo Electrónico
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

                <div className="mb-3">
                  <label htmlFor="password" className="form-label">
                    <i className="mdi mdi-lock me-2"></i>
                    Contraseña
                  </label>
                  <div className="input-group">
                    <input
                      type={showPassword ? "text" : "password"}
                      className="form-control"
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      placeholder="Tu contraseña"
                    />
                    <button
                      className="btn btn-sm btn-outline-primary rounded-end-pill bg-solid"
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      <i className={`mdi ${showPassword ? 'mdi-eye-off' : 'mdi-eye'}`}></i>
                    </button>
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
                        Iniciando sesión...
                      </>
                    ) : (
                      <>
                        <i className="mdi mdi-login me-2"></i>
                        Iniciar Sesión
                      </>
                    )}
                  </button>
                </div>
              </form>

              <hr className="my-4" />

              <div className="text-center col-8 mx-auto">
                <p className="mb-2">¿No tienes una cuenta?</p>
                <div className="d-grid gap-2">
                  <Link to="/registro" className="btn btn-outline-primary btn-sm">
                    <i className="mdi mdi-account-plus me-2"></i>
                    Registrarse como Paciente
                  </Link>
                  <Link to="/registro-doctor" className="btn btn-outline-primary btn-sm">
                    <i className="mdi mdi-stethoscope me-2"></i>
                    Registrarse como Doctor
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

