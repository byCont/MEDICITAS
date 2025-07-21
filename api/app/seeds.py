from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from app.main import Usuario, Especialidad, PerfilDoctor, DoctorEspecialidad, Cita, Resena, Notificacion, pwd_context
from app.main import TipoRol, EstadoCita, TipoNotificacion, EventoNotificacion

def crear_semillas_completas(db: Session):
    """
    Crear datos de semilla más completos para la base de datos MediCitas
    """
    
    # Verificar si ya existen datos
    if db.query(Usuario).count() > 0:
        print("Ya existen datos en la base de datos. Omitiendo creación de semillas.")
        return
    
    print("Creando semillas para la base de datos...")
    
    # 1. Crear Especialidades
    especialidades_data = [
        ("Cardiología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del corazón y sistema cardiovascular."),
        ("Dermatología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades de la piel, cabello y uñas."),
        ("Neurología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades del sistema nervioso."),
        ("Pediatría", "Especialidad médica que se ocupa de la salud y el cuidado médico de bebés, niños y adolescentes."),
        ("Ginecología", "Especialidad médica que se ocupa de la salud del sistema reproductor femenino."),
        ("Traumatología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de lesiones del sistema musculoesquelético."),
        ("Oftalmología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de las enfermedades de los ojos."),
        ("Psiquiatría", "Especialidad médica que se ocupa del diagnóstico y tratamiento de los trastornos mentales."),
        ("Medicina Interna", "Especialidad médica que se ocupa del diagnóstico y tratamiento de enfermedades internas del adulto."),
        ("Endocrinología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de enfermedades del sistema endocrino."),
        ("Gastroenterología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de enfermedades del aparato digestivo."),
        ("Neumología", "Especialidad médica que se ocupa del diagnóstico y tratamiento de enfermedades del sistema respiratorio."),
    ]
    
    especialidades = []
    for nombre, descripcion in especialidades_data:
        especialidad = Especialidad(nombre=nombre, descripcion=descripcion)
        especialidades.append(especialidad)
        db.add(especialidad)
    
    db.commit()
    print(f"✓ Creadas {len(especialidades)} especialidades")
    
    # 2. Crear Usuarios (Administradores)
    administradores = [
        Usuario(
            nombre_completo="Admin Principal",
            email="admin@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3000000000",
            fecha_nacimiento=date(1970, 1, 1),
            rol=TipoRol.ADMINISTRADOR
        ),
        Usuario(
            nombre_completo="Admin Soporte",
            email="soporte@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3000000001",
            fecha_nacimiento=date(1975, 6, 15),
            rol=TipoRol.ADMINISTRADOR
        ),
    ]
    
    for admin in administradores:
        db.add(admin)
    
    # 3. Crear Usuarios (Pacientes)
    pacientes = [
        Usuario(
            nombre_completo="Juan Carlos Pérez González",
            email="juan.perez@gmail.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3001234567",
            fecha_nacimiento=date(1985, 3, 15),
            rol=TipoRol.PACIENTE
        ),
        Usuario(
            nombre_completo="María Fernanda García López",
            email="maria.garcia@gmail.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3007654321",
            fecha_nacimiento=date(1990, 7, 22),
            rol=TipoRol.PACIENTE
        ),
        Usuario(
            nombre_completo="Carlos Alberto Rodríguez Martínez",
            email="carlos.rodriguez@gmail.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3002345678",
            fecha_nacimiento=date(1978, 11, 3),
            rol=TipoRol.PACIENTE
        ),
        Usuario(
            nombre_completo="Ana Sofía Hernández Vargas",
            email="ana.hernandez@gmail.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3008765432",
            fecha_nacimiento=date(1992, 4, 28),
            rol=TipoRol.PACIENTE
        ),
        Usuario(
            nombre_completo="Luis Miguel Torres Sánchez",
            email="luis.torres@gmail.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3003456789",
            fecha_nacimiento=date(1987, 9, 12),
            rol=TipoRol.PACIENTE
        ),
    ]
    
    for paciente in pacientes:
        db.add(paciente)
    
    # 4. Crear Usuarios (Doctores)
    doctores = [
        Usuario(
            nombre_completo="Dr. Carlos Eduardo Mendoza Rivera",
            email="carlos.mendoza@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3101234567",
            fecha_nacimiento=date(1975, 12, 8),
            rol=TipoRol.DOCTOR
        ),
        Usuario(
            nombre_completo="Dra. Ana María Rodríguez Castillo",
            email="ana.rodriguez@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3109876543",
            fecha_nacimiento=date(1980, 5, 18),
            rol=TipoRol.DOCTOR
        ),
        Usuario(
            nombre_completo="Dr. Miguel Ángel Ramírez Delgado",
            email="miguel.ramirez@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3105678901",
            fecha_nacimiento=date(1972, 8, 25),
            rol=TipoRol.DOCTOR
        ),
        Usuario(
            nombre_completo="Dra. Laura Patricia Jiménez Morales",
            email="laura.jimenez@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3106789012",
            fecha_nacimiento=date(1985, 2, 14),
            rol=TipoRol.DOCTOR
        ),
        Usuario(
            nombre_completo="Dr. Fernando José Guerrero Ospina",
            email="fernando.guerrero@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3107890123",
            fecha_nacimiento=date(1978, 10, 30),
            rol=TipoRol.DOCTOR
        ),
        Usuario(
            nombre_completo="Dra. Patricia Elena Vásquez Cruz",
            email="patricia.vasquez@medicitas.com",
            password_hash=pwd_context.hash("password123"),
            telefono="3108901234",
            fecha_nacimiento=date(1982, 6, 7),
            rol=TipoRol.DOCTOR
        ),
    ]
    
    for doctor in doctores:
        db.add(doctor)
    
    db.commit()
    print(f"✓ Creados {len(administradores)} administradores, {len(pacientes)} pacientes, {len(doctores)} doctores")
    
    # 5. Crear Perfiles de Doctores
    perfiles_doctores = [
        PerfilDoctor(
            usuario_id=3,  # Dr. Carlos Eduardo Mendoza Rivera
            cedula_profesional="12345678",
            biografia="Especialista en Cardiología con 15 años de experiencia. Graduado de la Universidad Nacional de Colombia. Especialista en cirugía cardiovascular y medicina preventiva.",
            foto_perfil_url="https://example.com/fotos/carlos-mendoza.jpg"
        ),
        PerfilDoctor(
            usuario_id=4,  # Dra. Ana María Rodríguez Castillo
            cedula_profesional="87654321",
            biografia="Especialista en Dermatología y Neurología. Más de 12 años de experiencia en el tratamiento de enfermedades de la piel y trastornos neurológicos.",
            foto_perfil_url="https://example.com/fotos/ana-rodriguez.jpg"
        ),
        PerfilDoctor(
            usuario_id=5,  # Dr. Miguel Ángel Ramírez Delgado
            cedula_profesional="11223344",
            biografia="Especialista en Pediatría con enfoque en desarrollo infantil. 20 años de experiencia atendiendo niños y adolescentes.",
            foto_perfil_url="https://example.com/fotos/miguel-ramirez.jpg"
        ),
        PerfilDoctor(
            usuario_id=6,  # Dra. Laura Patricia Jiménez Morales
            cedula_profesional="55667788",
            biografia="Especialista en Ginecología y Obstetricia. Dedicada al cuidado integral de la salud femenina con 10 años de experiencia.",
            foto_perfil_url="https://example.com/fotos/laura-jimenez.jpg"
        ),
        PerfilDoctor(
            usuario_id=7,  # Dr. Fernando José Guerrero Ospina
            cedula_profesional="99887766",
            biografia="Especialista en Traumatología y Ortopedia. Experto en cirugía de columna y articulaciones con 18 años de experiencia.",
            foto_perfil_url="https://example.com/fotos/fernando-guerrero.jpg"
        ),
        PerfilDoctor(
            usuario_id=8,  # Dra. Patricia Elena Vásquez Cruz
            cedula_profesional="33445566",
            biografia="Especialista en Oftalmología y Psiquiatría. Enfoque integral en salud mental y visual con 14 años de experiencia.",
            foto_perfil_url="https://example.com/fotos/patricia-vasquez.jpg"
        ),
    ]
    
    for perfil in perfiles_doctores:
        db.add(perfil)
    
    db.commit()
    print(f"✓ Creados {len(perfiles_doctores)} perfiles de doctores")
    
    # 6. Asociar Especialidades con Doctores
    doctor_especialidades = [
        # Dr. Carlos Eduardo Mendoza Rivera - Cardiología
        DoctorEspecialidad(doctor_id=1, especialidad_id=1),
        DoctorEspecialidad(doctor_id=1, especialidad_id=9),  # También Medicina Interna
        
        # Dra. Ana María Rodríguez Castillo - Dermatología y Neurología
        DoctorEspecialidad(doctor_id=2, especialidad_id=2),
        DoctorEspecialidad(doctor_id=2, especialidad_id=3),
        
        # Dr. Miguel Ángel Ramírez Delgado - Pediatría
        DoctorEspecialidad(doctor_id=3, especialidad_id=4),
        
        # Dra. Laura Patricia Jiménez Morales - Ginecología
        DoctorEspecialidad(doctor_id=4, especialidad_id=5),
        
        # Dr. Fernando José Guerrero Ospina - Traumatología
        DoctorEspecialidad(doctor_id=5, especialidad_id=6),
        
        # Dra. Patricia Elena Vásquez Cruz - Oftalmología y Psiquiatría
        DoctorEspecialidad(doctor_id=6, especialidad_id=7),
        DoctorEspecialidad(doctor_id=6, especialidad_id=8),
    ]
    
    for de in doctor_especialidades:
        db.add(de)
    
    db.commit()
    print(f"✓ Asociadas {len(doctor_especialidades)} especialidades con doctores")
    
    # 7. Crear Citas de Ejemplo
    # Fechas para las citas (próximas semanas)
    base_date = datetime.now() + timedelta(days=1)
    
    citas = [
        # Citas programadas
        Cita(
            paciente_id=9,  # Juan Carlos Pérez González
            doctor_id=1,    # Dr. Carlos Eduardo Mendoza Rivera
            especialidad_id=1,  # Cardiología
            fecha_hora=base_date + timedelta(days=2, hours=9),
            duracion_minutos=45,
            motivo_consulta="Chequeo general cardiológico y evaluación de presión arterial",
            estado=EstadoCita.PROGRAMADA
        ),
        Cita(
            paciente_id=10,  # María Fernanda García López
            doctor_id=2,     # Dra. Ana María Rodríguez Castillo
            especialidad_id=2,  # Dermatología
            fecha_hora=base_date + timedelta(days=3, hours=14),
            duracion_minutos=30,
            motivo_consulta="Evaluación de lunares y manchas en la piel",
            estado=EstadoCita.CONFIRMADA
        ),
        Cita(
            paciente_id=11,  # Carlos Alberto Rodríguez Martínez
            doctor_id=3,     # Dr. Miguel Ángel Ramírez Delgado
            especialidad_id=4,  # Pediatría
            fecha_hora=base_date + timedelta(days=5, hours=10),
            duracion_minutos=30,
            motivo_consulta="Control de crecimiento y desarrollo de menor",
            estado=EstadoCita.PROGRAMADA
        ),
        
        # Citas completadas (para poder crear reseñas)
        Cita(
            paciente_id=12,  # Ana Sofía Hernández Vargas
            doctor_id=4,     # Dra. Laura Patricia Jiménez Morales
            especialidad_id=5,  # Ginecología
            fecha_hora=datetime.now() - timedelta(days=7, hours=11),
            duracion_minutos=60,
            motivo_consulta="Control ginecológico anual",
            estado=EstadoCita.COMPLETADA,
            notas_doctor="Examen normal. Se recomienda control en 6 meses."
        ),
        Cita(
            paciente_id=13,  # Luis Miguel Torres Sánchez
            doctor_id=5,     # Dr. Fernando José Guerrero Ospina
            especialidad_id=6,  # Traumatología
            fecha_hora=datetime.now() - timedelta(days=3, hours=15),
            duracion_minutos=45,
            motivo_consulta="Dolor en rodilla derecha tras actividad deportiva",
            estado=EstadoCita.COMPLETADA,
            notas_doctor="Lesión menor de ligamento. Reposo 2 semanas y fisioterapia."
        ),
        
        # Citas canceladas
        Cita(
            paciente_id=9,   # Juan Carlos Pérez González
            doctor_id=6,     # Dra. Patricia Elena Vásquez Cruz
            especialidad_id=7,  # Oftalmología
            fecha_hora=base_date + timedelta(days=1, hours=16),
            duracion_minutos=30,
            motivo_consulta="Revisión de la vista",
            estado=EstadoCita.CANCELADA
        ),
    ]
    
    for cita in citas:
        db.add(cita)
    
    db.commit()
    print(f"✓ Creadas {len(citas)} citas de ejemplo")
    
    # 8. Crear Reseñas para las citas completadas
    resenas = [
        Resena(
            cita_id=4,  # Cita completada de Ana Sofía
            paciente_id=12,
            doctor_id=4,
            calificacion=5,
            comentario="Excelente atención de la Dra. Jiménez. Muy profesional y amable.",
            es_anonima=False
        ),
        Resena(
            cita_id=5,  # Cita completada de Luis Miguel
            paciente_id=13,
            doctor_id=5,
            calificacion=4,
            comentario="Buen diagnóstico y tratamiento. El doctor fue muy claro en las explicaciones.",
            es_anonima=False
        ),
    ]
    
    for resena in resenas:
        db.add(resena)
    
    db.commit()
    print(f"✓ Creadas {len(resenas)} reseñas")
    
    # 9. Crear Notificaciones de Ejemplo
    notificaciones = [
        # Notificación de cita programada
        Notificacion(
            usuario_id=9,  # Juan Carlos Pérez González
            cita_id=1,
            tipo=TipoNotificacion.EMAIL,
            evento=EventoNotificacion.CITA_PROGRAMADA,
            contenido="Su cita con Dr. Carlos Eduardo Mendoza Rivera ha sido programada para el día {fecha}".format(
                fecha=(base_date + timedelta(days=2, hours=9)).strftime("%d/%m/%Y a las %H:%M")
            ),
            enviada_exitosamente=True
        ),
        
        # Notificación de cita confirmada
        Notificacion(
            usuario_id=10,  # María Fernanda García López
            cita_id=2,
            tipo=TipoNotificacion.SMS,
            evento=EventoNotificacion.CITA_CONFIRMADA,
            contenido="Su cita con Dra. Ana María Rodríguez Castillo ha sido confirmada",
            enviada_exitosamente=True
        ),
        
        # Recordatorio 24 horas
        Notificacion(
            usuario_id=11,  # Carlos Alberto Rodríguez Martínez
            cita_id=3,
            tipo=TipoNotificacion.PUSH,
            evento=EventoNotificacion.RECORDATORIO_24H,
            contenido="Recordatorio: Tiene una cita mañana con Dr. Miguel Ángel Ramírez Delgado",
            enviada_exitosamente=True
        ),
        
        # Notificación de cita cancelada
        Notificacion(
            usuario_id=9,  # Juan Carlos Pérez González
            cita_id=6,
            tipo=TipoNotificacion.EMAIL,
            evento=EventoNotificacion.CITA_CANCELADA,
            contenido="Su cita con Dra. Patricia Elena Vásquez Cruz ha sido cancelada",
            enviada_exitosamente=True
        ),
    ]
    
    for notificacion in notificaciones:
        db.add(notificacion)
    
    db.commit()
    print(f"✓ Creadas {len(notificaciones)} notificaciones")
    
    print("\n🎉 ¡Semillas creadas exitosamente!")
    print("📊 Resumen de datos creados:")
    print(f"   - {len(especialidades)} especialidades")
    print(f"   - {len(administradores)} administradores")
    print(f"   - {len(pacientes)} pacientes") 
    print(f"   - {len(doctores)} doctores")
    print(f"   - {len(perfiles_doctores)} perfiles de doctores")
    print(f"   - {len(doctor_especialidades)} asociaciones doctor-especialidad")
    print(f"   - {len(citas)} citas")
    print(f"   - {len(resenas)} reseñas")
    print(f"   - {len(notificaciones)} notificaciones")
    
    return True

if __name__ == "__main__":
    # Script para ejecutar las semillas directamente
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        crear_semillas_completas(db)