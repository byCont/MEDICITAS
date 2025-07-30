
import React from 'react';

const EspecialidadCardSkeleton: React.FC = () => {
  return (
    <div className="col-md-6 col-lg-4">
      <div className="card h-100 placeholder-glow">
        <div className="card-body text-center">
          <div className="d-flex align-items-center justify-content-center bg-light rounded-circle mx-auto mb-3" style={{ width: '80px', height: '80px' }}>
            <span className="placeholder col-6"></span>
          </div>
          <h5 className="card-title placeholder-glow">
            <span className="placeholder col-8"></span>
          </h5>
          <p className="card-text placeholder-glow">
            <span className="placeholder col-7"></span>
            <span className="placeholder col-4"></span>
          </p>
          <div className="mt-auto">
            <small className="placeholder col-5"></small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EspecialidadCardSkeleton;
