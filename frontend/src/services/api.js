const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const fetchCompanies = async () => {
  const response = await fetch(`${API_BASE}/companies`);
  if (!response.ok) {
    throw new Error('Failed to fetch companies');
  }
  return response.json();
};

export const fetchStockData = async (symbol) => {
  const response = await fetch(`${API_BASE}/stock/${symbol}`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch stock data');
  }
  return response.json();
};