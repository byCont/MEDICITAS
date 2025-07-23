import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import './styles.scss';

const App: React.FC = () => {
  return (
    <div className="d-flex flex-column vh-100">
      <Navbar />
      <main className="flex-shrink-0">
        <HomePage />
      </main>
      <Footer />
    </div>
  );
};

export default App;

