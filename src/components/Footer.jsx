// Footer.js
import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-light text-center py-3">
      <div className="container">
        <p>&copy; 2024 Student Attendance Management System</p>
        <div className="wrapper">
          <a href="#" className="icon facebook">
            <div className="tooltip">Facebook</div>
            <span>
              <i className="fab fa-facebook-f"></i>
            </span>
          </a>
          <a href="#" className="icon twitter">
            <div className="tooltip">Twitter</div>
            <span>
              <i className="fab fa-twitter"></i>
            </span>
          </a>
          <a href="#" className="icon instagram">
            <div className="tooltip">Instagram</div>
            <span>
              <i className="fab fa-instagram"></i>
            </span>
          </a>
          <a href="#" className="icon github">
            <div className="tooltip">Github</div>
            <span>
              <i className="fab fa-github"></i>
            </span>
          </a>
          <a href="#" className="icon youtube">
            <div className="tooltip">Youtube</div>
            <span>
              <i className="fab fa-youtube"></i>
            </span>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
