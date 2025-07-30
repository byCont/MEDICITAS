
import React from 'react';

const DoctorCardSkeleton: React.FC = () => {
  return (
    <div className="col-md-12 col-lg-12">
      <div className="card h-100 placeholder-glow">
        <div className="card-body">
          <div className="d-flex flex-column flex-md-row">
            <div className="flex-grow-1 me-md-4">
              <div className="d-flex flex-column flex-sm-row align-items-sm-center mb-3">
                <div className="me-3 mb-2 mb-sm-0" style={{ flexShrink: 0 }}>
                  <span className="placeholder rounded-circle" style={{ width: '80px', height: '80px' }}></span>
                </div>
                <div className="text-center text-sm-start">
                  <span className="placeholder col-8 mb-1"></span>
                  <span className="placeholder col-6"></span>
                </div>
              </div>
              
              <div className="mb-1">
                <span className="placeholder col-3 me-2"></span>
                <div className="d-inline-block">
                  <span className="placeholder col-2 me-1 mb-1"></span>
                  <span className="placeholder col-2 me-1 mb-1"></span>
                </div>
              </div>
              
              <p className="card-text placeholder-glow">
                <span className="placeholder col-7"></span>
                <span className="placeholder col-4"></span>
                <span className="placeholder col-4"></span>
                <span className="placeholder col-6"></span>
              </p>
            </div>
            
            <div className="d-flex flex-column justify-content-center align-items-center align-items-md-end" style={{ minWidth: '140px' }}>
              <span className="placeholder col-5 mb-2"></span>
              <span className="placeholder col-5"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorCardSkeleton;
