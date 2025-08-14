import React from 'react';
import { Line } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js';

ChartJS.register(
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend
);

const StockChart = ({ stockData }) => {
  if (!stockData || !stockData.data || stockData.data.length === 0) {
    return (
      <div className="chart-error">
        <p>No chart data available</p>
        <p>Please select a different company</p>
      </div>
    );
  }
  
  // Prepare data for chart
  const chartData = {
    labels: stockData.data.map(item => item.date),
    datasets: [
      {
        label: 'Closing Price',
        data: stockData.data.map(item => item.close),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        tension: 0.1,
      },
      {
        label: '50-Day SMA',
        data: stockData.data.map(item => item.sma_50),
        borderColor: 'rgb(255, 99, 132)',
        borderDash: [5, 5],
        pointRadius: 0,
      },
      {
        label: '200-Day SMA',
        data: stockData.data.map(item => item.sma_200),
        borderColor: 'rgb(54, 162, 235)',
        borderDash: [5, 5],
        pointRadius: 0,
      }
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${stockData.name} Stock Price with Moving Averages`,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 2
              }).format(context.parsed.y);
            }
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          maxTicksLimit: 10,
        },
        grid: {
          display: false
        }
      },
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value) {
            return '₹' + value;
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index',
    }
  };

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
};

export default StockChart;