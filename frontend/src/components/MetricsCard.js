import React from 'react';

const MetricsCard = ({ title, value, isCurrency = false }) => {
  const formatValue = () => {
    if (value === null || value === undefined) return 'N/A';
    
    if (isCurrency) {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 2
      }).format(value);
    }
    
    return value;
  };

  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <p>{formatValue()}</p>
    </div>
  );
};

export default MetricsCard;