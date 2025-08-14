import React, { useState, useEffect } from 'react';
import StockChart from './components/StockChart';
import CompanyList from './components/CompanyList';
import MetricsCard from './components/MetricsCard';
import ExchangeFilter from './components/ExchangeFilter';
import { fetchCompanies, fetchStockData } from './services/api';
import './App.css';

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [exchangeFilter, setExchangeFilter] = useState('all');

  useEffect(() => {
    const getCompanies = async () => {
      try {
        const data = await fetchCompanies();
        setCompanies(data);
        
        if (data.length > 0) {
          getStockData(data[0].symbol);
        } else {
          setLoading(false);
        }
      } catch (err) {
        setError('Failed to load companies. Please try again later.');
        setLoading(false);
      }
    };

    getCompanies();
  }, []);

  const getStockData = async (symbol) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchStockData(symbol);
      setSelectedStock(data);
    } catch (err) {
      setError(`Failed to load stock data for ${symbol}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  const filteredCompanies = exchangeFilter === 'all' 
    ? companies 
    : companies.filter(company => company.exchange === exchangeFilter);

  return (
    <div className="app">
      <div className="dashboard">
        <div className="sidebar">
          <ExchangeFilter 
            currentFilter={exchangeFilter} 
            onFilterChange={setExchangeFilter} 
          />
          <CompanyList 
            companies={filteredCompanies} 
            selectedSymbol={selectedStock?.symbol} 
            onSelect={getStockData} 
          />
        </div>
        
        <div className="main-content">
          {error ? (
            <div className="error-message">
              <h3>Error Loading Data</h3>
              <p>{error}</p>
              <p>Please try selecting another stock</p>
            </div>
          ) : loading ? (
            <div className="loader">
              <div className="spinner"></div>
              <p>Loading stock data...</p>
            </div>
          ) : selectedStock ? (
            <>
              <div className="stock-header">
                <h1>{selectedStock.name}</h1>
                <h2>{selectedStock.symbol.replace('.BO', '').replace('.NS', '')} | {selectedStock.exchange}</h2>
              </div>
              
              <StockChart stockData={selectedStock} />
              
              <div className="metrics">
                <MetricsCard 
                  title="Current Price" 
                  value={selectedStock.metrics?.current_price} 
                  isCurrency 
                />
                <MetricsCard 
                  title="52-Week High" 
                  value={selectedStock.metrics?.['52_week_high']} 
                  isCurrency 
                />
                <MetricsCard 
                  title="52-Week Low" 
                  value={selectedStock.metrics?.['52_week_low']} 
                  isCurrency 
                />
                <MetricsCard 
                  title="50-Day SMA" 
                  value={selectedStock.indicators?.sma_50} 
                  isCurrency 
                />
                <MetricsCard 
                  title="200-Day SMA" 
                  value={selectedStock.indicators?.sma_200} 
                  isCurrency 
                />
                <MetricsCard 
                  title="Market Cap" 
                  value={selectedStock.metrics?.market_cap 
                    ? `${(selectedStock.metrics.market_cap / 10000000).toFixed(0)} Cr` 
                    : 'N/A'} 
                />
                <MetricsCard 
                  title="P/E Ratio" 
                  value={selectedStock.metrics?.pe_ratio?.toFixed(2) || 'N/A'} 
                />
                <MetricsCard 
                  title="Dividend Yield" 
                  value={selectedStock.metrics?.dividend_yield 
                    ? `${(selectedStock.metrics.dividend_yield * 100).toFixed(2)}%` 
                    : 'N/A'} 
                />
              </div>
            </>
          ) : (
            <div className="no-data">
              <p>No stock data available</p>
              <p>Select a company from the list</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;