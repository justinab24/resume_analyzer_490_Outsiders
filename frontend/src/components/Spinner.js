import React from 'react';
import '../stylesheet/spinner.css';
import '../stylesheet/spinner.css';

const Spinner = ({ 'data-testid': testId }) => (
  <div className="overlay" data-testid={testId}>
    <div className="drawing">
      <div className="loading-dot"></div>
    </div>
  </div>
);

export default Spinner;