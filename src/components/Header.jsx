// Header.js
import React from 'react';

const Header = () => {
  return (
    <header className="d-flex justify-content-between align-items-center">
      <div className="header-title">
        <a className="navbar-brand" style={{ color: '#020202' }} href="#">
          Neuro Kode
        </a>
      </div>
      <button className="btn btn-success login-button" onClick={goToLoginPage}>
        Login
      </button>
    </header>
  );

  function goToLoginPage() {
    // Redirect to another HTML page
    window.location.href = 'login.html';
  }
};

export default Header;
