from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from datetime import datetime, timedelta
from .database import init_db, get_companies, get_company_by_symbol
from .utils import calculate_sma
from pydantic import BaseModel
import pandas as pd
from typing import Optional


app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

class StockData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None

@app.on_event("startup")
async def startup_event():
    # Pre-populate companies on startup
    pass

@app.get("/companies")
async def list_companies():
    companies = get_companies()
    return [
        {"symbol": c[0], "name": c[1], "exchange": c[2]}
        for c in companies
    ]

@app.get("/stock/{symbol}")
async def get_stock_data(symbol: str):
    try:
        # Get 1-year historical data
        end_date = datetime.today()
        start_date = end_date - timedelta(days=400)  # Extra days for SMA calculation
        
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {symbol}. Try a different stock."
            )
        
        # Calculate SMAs
        hist['SMA_50'] = calculate_sma(hist['Close'], 50)
        hist['SMA_200'] = calculate_sma(hist['Close'], 200)
        
        # Get additional metrics
        info = stock.info
        metrics = {
            "52_week_high": info.get('fiftyTwoWeekHigh'),
            "52_week_low": info.get('fiftyTwoWeekLow'),
            "avg_volume": info.get('averageVolume'),
            "pe_ratio": info.get('trailingPE'),
            "market_cap": info.get('marketCap'),
            "dividend_yield": info.get('dividendYield'),
            "current_price": info.get('currentPrice')
        }
        
        # Format data
        data = []
        for date, row in hist.iterrows():
            data.append(StockData(
                date=date.strftime("%Y-%m-%d"),
                open=round(row['Open'], 2),
                high=round(row['High'], 2),
                low=round(row['Low'], 2),
                close=round(row['Close'], 2),
                volume=row['Volume'],
                sma_50=round(row['SMA_50'], 2) if not pd.isna(row['SMA_50']) else None,
                sma_200=round(row['SMA_200'], 2) if not pd.isna(row['SMA_200']) else None
            ))
        
        # Get company info
        company = get_company_by_symbol(symbol)
        company_name = company[1] if company else symbol
        
        # Get latest SMAs
        latest_sma_50 = None
        latest_sma_200 = None
        if not hist['SMA_50'].isnull().all():
            latest_sma_50 = round(hist['SMA_50'].dropna().iloc[-1], 2)
        if not hist['SMA_200'].isnull().all():
            latest_sma_200 = round(hist['SMA_200'].dropna().iloc[-1], 2)
        
        return {
            "symbol": symbol,
            "name": company_name,
            "data": data,
            "metrics": metrics,
            "indicators": {
                "sma_50": latest_sma_50,
                "sma_200": latest_sma_200
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)