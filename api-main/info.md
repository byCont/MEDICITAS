DESCRIPCION:
Nombre plataforma: MediCitas.
Slogan plataforma: "Especialistas para ti, cuando lo necesitas."
Ojbetivo del sistema: Plataforma de reservas para consultas médicas, Una plataforma donde los pacientes pueden encontrar y agedar citas con doctores especializados.


FUNCIONALIDADES:

El sistema permitirá:
Registrar Usuarios: Que pueden tener el rol de Paciente, Doctor o Administrador.
Gestionar Doctores: Los doctores tendrán un perfil especial con su cédula profesional y sus especialidades.
Catalogar Especialidades: Una lista de todas las especialidades médicas disponibles (Cardiología, Dermatología, etc.).
Agendar Citas: Un paciente podrá solicitar una cita con un doctor en una fecha y hora específicas, basada en una especialidad.
Gestionar el Estado de la Cita: Las citas podrán ser programadas, confirmadas, completadas o canceladas.

CONEXIÓN CON NEON:

snippet: postgresql://neondb_owner:npg_byzju3LW8wID@ep-rough-sun-ae9zqym8-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

TABLAS POSTGRESQL

-- Creación de un ENUM para los roles de usuario.
-- Usar un tipo ENUM es más eficiente y seguro que un VARCHAR.
CREATE TYPE tipo_rol AS ENUM ('Paciente', 'Doctor', 'Administrador');

-- Creación de un ENUM para el estado de las citas.
CREATE TYPE estado_cita AS ENUM ('Programada', 'Confirmada', 'Completada', 'Cancelada', 'No Asistió');


-- Tabla principal para todos los usuarios del sistema.
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    rol tipo_rol NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE usuarios IS 'Almacena la información de todos los usuarios, tanto pacientes como doctores y administradores.';


-- Tabla de especialidades médicas (el "catálogo").
CREATE TABLE especialidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE especialidades IS 'Catálogo de especialidades médicas que se ofrecen en la plataforma.';


-- Tabla de perfiles específicos para los doctores.
-- Se separa de la tabla de usuarios para mantener la información específica del rol.
CREATE TABLE perfiles_doctores (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    cedula_profesional VARCHAR(50) NOT NULL UNIQUE,
    biografia TEXT,
    foto_perfil_url VARCHAR(255),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE perfiles_doctores IS 'Información adicional y profesional exclusiva de los usuarios con rol de Doctor.';


-- Tabla pivote para la relación muchos-a-muchos entre doctores y especialidades.
-- Un doctor puede tener varias especialidades, y una especialidad puede ser atendida por varios doctores.
CREATE TABLE doctor_especialidades (
    doctor_id INTEGER NOT NULL REFERENCES perfiles_doctores(id) ON DELETE CASCADE,
    especialidad_id INTEGER NOT NULL REFERENCES especialidades(id) ON DELETE CASCADE,
    PRIMARY KEY (doctor_id, especialidad_id)
);
COMMENT ON TABLE doctor_especialidades IS 'Tabla de enlace que define qué especialidades tiene cada doctor.';


-- La tabla central del sistema: las citas médicas.
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE SET NULL,
    doctor_id INTEGER NOT NULL REFERENCES perfiles_doctores(id) ON DELETE CASCADE,
    especialidad_id INTEGER NOT NULL REFERENCES especialidades(id) ON DELETE RESTRICT,
    fecha_hora TIMESTAMP WITH TIME ZONE NOT NULL,
    duracion_minutos INTEGER NOT NULL DEFAULT 30,
    estado estado_cita NOT NULL DEFAULT 'Programada',
    motivo_consulta TEXT,
    notas_doctor TEXT, -- Notas que el doctor añade después de la consulta.
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Restricción para evitar que un doctor tenga dos citas al mismo tiempo.
    CONSTRAINT uq_doctor_fecha_hora UNIQUE (doctor_id, fecha_hora)
);
COMMENT ON TABLE citas IS 'Registra cada una de las citas médicas agendadas en el sistema.';

--Tabla para las reseñas, vinculada a una cita completada.
CREATE TABLE resenas (
    id SERIAL PRIMARY KEY,
    cita_id INTEGER NOT NULL UNIQUE REFERENCES citas(id) ON DELETE CASCADE, -- Una reseña por cita
    paciente_id INTEGER NOT NULL REFERENCES usuarios(id),
    doctor_id INTEGER NOT NULL REFERENCES perfiles_doctores(id),
    calificacion SMALLINT NOT NULL CHECK (calificacion BETWEEN 1 AND 5), -- e.g., 1 a 5 estrellas
    comentario TEXT,
    es_anonima BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE resenas IS 'Almacena las calificaciones y comentarios de los pacientes sobre una cita completada.';

CREATE TYPE tipo_notificacion AS ENUM ('Email', 'SMS', 'Push');
CREATE TYPE evento_notificacion AS ENUM ('Cita_Programada', 'Cita_Confirmada', 'Cita_Cancelada', 'Recordatorio_24h', 'Recordatorio_1h');

--Tabla para registrar todas las notificaciones (email, SMS, push).
CREATE TABLE notificaciones (
    id BIGSERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    cita_id INTEGER REFERENCES citas(id), -- Puede no estar asociada a una cita
    tipo tipo_notificacion NOT NULL,
    evento evento_notificacion NOT NULL,
    contenido TEXT NOT NULL,
    enviada_exitosamente BOOLEAN DEFAULT FALSE,
    fecha_envio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE notificaciones IS 'Registro de todas las comunicaciones automáticas enviadas a los usuarios.';