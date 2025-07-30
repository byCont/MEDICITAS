
import React from 'react';

const DoctorPageSkeleton: React.FC = () => {
  return (
    <div className="col-md-6 col-lg-4">
      <div className="card h-100 placeholder-glow">
        <div className="card-body">
          <div className="d-flex align-items-center mb-3">
            <div className="bg-light rounded-circle p-3 me-3">
              <span className="placeholder rounded-circle" style={{ width: '50px', height: '50px' }}></span>
            </div>
            <div className="flex-grow-1">
              <h5 className="card-title placeholder-glow">
                <span className="placeholder col-8"></span>
              </h5>
              <small className="placeholder col-6"></small>
            </div>
          </div>

          <div className="mb-3">
            <h6 className="placeholder-glow">
              <span className="placeholder col-4"></span>
            </h6>
            <div className="d-flex flex-wrap gap-1">
              <span className="placeholder col-3"></span>
              <span className="placeholder col-4"></span>
            </div>
          </div>

          <p className="card-text placeholder-glow">
            <span className="placeholder col-7"></span>
            <span className="placeholder col-4"></span>
            <span className="placeholder col-4"></span>
            <span className="placeholder col-6"></span>
          </p>

          <div className="d-flex gap-2 mt-auto">
            <span className="placeholder col-5"></span>
            <span className="placeholder col-5"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorPageSkeleton;
