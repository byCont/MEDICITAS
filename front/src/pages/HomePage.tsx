import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Agendar Nueva Cita</h5>
              <p className="card-text">Busca un especialista y agenda una nueva cita médica.</p>
              <a href="#" className="btn btn-primary">Agendar Cita</a>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Mis Próximas Citas</h5>
              <p className="card-text">Consulta tus próximas citas y gestiona tus recordatorios.</p>
              <a href="#" className="btn btn-primary">Ver Citas</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
