
import React from 'react';

const CitaCardSkeleton: React.FC = () => {
  return (
    <div className="col-md-6 col-lg-4">
      <div className="card placeholder-glow">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-start mb-3">
            <h5 className="card-title placeholder-glow mb-0">
              <span className="placeholder col-6"></span>
            </h5>
            <span className="placeholder col-3"></span>
          </div>
          
          <div className="mb-2">
            <small className="placeholder-glow">
              <span className="placeholder col-8"></span>
            </small>
          </div>
          
          <div className="mb-2">
            <small className="placeholder-glow">
              <span className="placeholder col-7"></span>
            </small>
          </div>

          <div className="mb-3">
            <small className="placeholder-glow">
              <span className="placeholder col-9"></span>
            </small>
          </div>

          <div className="d-flex gap-2">
            <span className="placeholder col-6"></span>
            <span className="placeholder col-4"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CitaCardSkeleton;
