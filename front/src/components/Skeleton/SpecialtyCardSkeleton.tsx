
import React from 'react';

const SpecialtyCardSkeleton: React.FC = () => {
  return (
    <div className="col-md-6 col-lg-4">
      <div className="card h-100 placeholder-glow">
        <div className="card-body text-center">
          <span className="placeholder col-6 mb-2"></span>
          <h6 className="card-title placeholder-glow">
            <span className="placeholder col-8"></span>
          </h6>
          <small className="placeholder col-4"></small>
        </div>
      </div>
    </div>
  );
};

export default SpecialtyCardSkeleton;
