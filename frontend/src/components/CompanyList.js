import React from 'react';

const CompanyList = ({ companies, selectedSymbol, onSelect }) => {
  return (
    <div className="company-list">
      <ul>
        {companies.map(company => (
          <li 
            key={company.symbol} 
            onClick={() => onSelect(company.symbol)}
            className={selectedSymbol === company.symbol ? 'active' : ''}
          >
            <div className="company-info">
              <span className="company-name">{company.name}</span>
              <span className="company-exchange">{company.exchange}</span>
            </div>
            <span className="company-symbol">
              {company.symbol.replace('.BO', '').replace('.NS', '')}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CompanyList;