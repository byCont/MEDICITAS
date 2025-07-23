import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-solid text-center py-3">
      <div className="container">
        <p className="text-muted mb-0">
          &copy; {new Date().getFullYear()} MediCitas. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
