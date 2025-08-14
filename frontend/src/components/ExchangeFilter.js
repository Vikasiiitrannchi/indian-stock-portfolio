import React from 'react';

const ExchangeFilter = ({ currentFilter, onFilterChange }) => {
  return (
    <div className="exchange-filter">
      <h2>Indian Stocks</h2>
      <div className="filter-options">
        <button 
          className={currentFilter === 'all' ? 'active' : ''}
          onClick={() => onFilterChange('all')}
        >
          All
        </button>
        <button 
          className={currentFilter === 'BSE' ? 'active' : ''}
          onClick={() => onFilterChange('BSE')}
        >
          BSE
        </button>
        <button 
          className={currentFilter === 'NSE' ? 'active' : ''}
          onClick={() => onFilterChange('NSE')}
        >
          NSE
        </button>
      </div>
    </div>
  );
};

export default ExchangeFilter;