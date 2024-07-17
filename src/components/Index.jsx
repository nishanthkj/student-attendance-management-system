// Content.js
import React from 'react';

const Index = () => {
  return (
    <div className="content">
      <h2 style={{ color: 'white', fontFamily: "'Lato', sans-serif" }}>
        Welcome to Student Attendance Management System
      </h2>
      <button className="btn btn-success mark-attendance" onClick={goToAttendancePage}>
        Mark Attendance
      </button>
    </div>
  );

  function goToAttendancePage() {
    // Redirect to another HTML page
    window.location.href = 'attendance.html';
  }
};

export default Index;
