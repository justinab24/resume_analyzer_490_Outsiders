import React from 'react';
import '../stylesheet/spinner.css';

const Spinner = () => (
  <div className="overlay">
    <div className="drawing">
      <div className="loading-dot"></div>
    </div>
  </div>
);

export default Spinner;
