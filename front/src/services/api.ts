import axios from 'axios';

// Configuración base de la API
const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token de autenticación
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Tipos TypeScript
export interface Usuario {
  id: number;
  nombre_completo: string;
  email: string;
  telefono?: string;
  fecha_nacimiento?: string;
  rol: 'Paciente' | 'Doctor' | 'Administrador';
  activo: boolean;
  email_verificado: boolean;
  ultimo_acceso?: string;
  fecha_creacion: string;
}

export interface Especialidad {
  id: number;
  nombre: string;
  descripcion?: string;
  fecha_creacion: string;
}

export interface Resena {
  id: number;
  paciente_id: number;
  paciente_nombre: string;
  doctor_id: number;
  calificacion: number;
  comentario?: string;
  fecha: string;
}

export interface Doctor {
  id: number;
  nombre_completo: string;
  email: string;
  telefono?: string;
  cedula_profesional: string;
  biografia?: string;
  foto_perfil_url?: string;
  especialidades: string[];
  resenas?: Resena[];
}

export interface Cita {
  id: number;
  paciente_id: number;
  doctor_id: number;
  especialidad_id: number;
  fecha_hora: string;
  duracion_minutos: number;
  estado: 'Programada' | 'Confirmada' | 'Completada' | 'Cancelada' | 'No Asistió';
  motivo_consulta?: string;
  fecha_creacion: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterPatientData {
  nombre_completo: string;
  email: string;
  password: string;
  telefono?: string;
  fecha_nacimiento?: string;
}

export interface RegisterDoctorData {
  usuario: {
    nombre_completo: string;
    email: string;
    password: string;
    telefono?: string;
    fecha_nacimiento?: string;
  };
  perfil: {
    cedula_profesional: string;
    biografia?: string;
    foto_perfil_url?: string;
  };
  especialidades_ids: number[];
}

export interface CreateCitaData {
  doctor_id: number;
  especialidad_id: number;
  fecha_hora: string;
  motivo_consulta?: string;
  duracion_minutos?: number;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// Servicios de autenticación
export const authService = {
  // Registro de paciente
  registerPatient: async (userData: RegisterPatientData): Promise<Usuario> => {
    const response = await apiClient.post('/auth/registro/paciente', userData);
    return response.data;
  },

  // Registro de doctor
  registerDoctor: async (doctorData: RegisterDoctorData): Promise<any> => {
    const response = await apiClient.post('/auth/registro/doctor', doctorData);
    return response.data;
  },

  // Login
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', credentials);
    const { access_token, refresh_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    return response.data;
  },

  // Logout
  logout: async (): Promise<void> => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await apiClient.post('/auth/logout', { refresh_token: refreshToken });
      } catch (error) {
        console.error('Error during logout:', error);
      }
    }
    
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  // Obtener usuario actual
  getCurrentUser: async (): Promise<Usuario> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  // Verificar si el usuario está autenticado
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },
};

// Servicios de especialidades
export const specialtyService = {
  // Obtener todas las especialidades
  getAll: async (): Promise<Especialidad[]> => {
    const response = await apiClient.get('/especialidades/');
    return response.data;
  },
};

// Servicios de doctores
export const doctorService = {
  // Obtener todos los doctores
  getAll: async (): Promise<Doctor[]> => {
    const response = await apiClient.get('/doctores/');
    return response.data;
  },

  // Buscar doctores por especialidad
  searchBySpecialty: async (specialtyName: string): Promise<Doctor[]> => {
    const response = await apiClient.get('/doctores/');
    const doctors = response.data;
    
    if (!specialtyName) return doctors;
    
    return doctors.filter((doctor: Doctor) =>
      doctor.especialidades.some((esp: string) =>
        esp.toLowerCase().includes(specialtyName.toLowerCase())
      )
    );
  },
};

// Servicios de citas
export const appointmentService = {
  // Crear nueva cita
  create: async (appointmentData: CreateCitaData): Promise<Cita> => {
    const response = await apiClient.post('/citas/', appointmentData);
    return response.data;
  },

  // Obtener mis citas
  getMyCitas: async (): Promise<Cita[]> => {
    const response = await apiClient.get('/mis-citas/');
    return response.data;
  },
};

// Servicios generales
export const generalService = {
  // Health check
  healthCheck: async (): Promise<any> => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Obtener estadísticas (solo admin)
  getStats: async (): Promise<any> => {
    const response = await apiClient.get('/stats');
    return response.data;
  },
};

export default apiClient;
