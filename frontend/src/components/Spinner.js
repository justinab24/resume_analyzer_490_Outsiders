import React from 'react';
import '../stylesheet/spinner.css';

const Spinner = ({ 'data-testid': testId }) => (
  <div className="spinner" data-testid={testId}></div>
);

export default Spinner;