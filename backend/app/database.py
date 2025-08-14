import sqlite3
import os

DB_PATH = "stocks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create companies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            name TEXT,
            exchange TEXT
        )
    ''')
    
    # Top 30 BSE companies
    bse_companies = [
        ("RELIANCE.BO", "Reliance Industries", "BSE"),
        ("TCS.BO", "Tata Consultancy Services", "BSE"),
        ("HDFCBANK.BO", "HDFC Bank", "BSE"),
        ("ICICIBANK.BO", "ICICI Bank", "BSE"),
        ("HINDUNILVR.BO", "Hindustan Unilever", "BSE"),
        ("INFY.BO", "Infosys", "BSE"),
        ("ITC.BO", "ITC", "BSE"),
        ("KOTAKBANK.BO", "Kotak Mahindra Bank", "BSE"),
        ("AXISBANK.BO", "Axis Bank", "BSE"),
        ("LT.BO", "Larsen & Toubro", "BSE"),
        ("SBIN.BO", "State Bank of India", "BSE"),
        ("BAJFINANCE.BO", "Bajaj Finance", "BSE"),
        ("BHARTIARTL.BO", "Bharti Airtel", "BSE"),
        ("ASIANPAINT.BO", "Asian Paints", "BSE"),
        ("HCLTECH.BO", "HCL Technologies", "BSE"),
        ("MARUTI.BO", "Maruti Suzuki", "BSE"),
        ("TITAN.BO", "Titan Company", "BSE"),
        ("ULTRACEMCO.BO", "UltraTech Cement", "BSE"),
        ("SUNPHARMA.BO", "Sun Pharmaceutical", "BSE"),
        ("NESTLEIND.BO", "Nestle India", "BSE"),
        ("ONGC.BO", "Oil & Natural Gas Corp", "BSE"),
        ("POWERGRID.BO", "Power Grid Corp", "BSE"),
        ("NTPC.BO", "NTPC", "BSE"),
        ("INDUSINDBK.BO", "IndusInd Bank", "BSE"),
        ("BAJAJ-AUTO.BO", "Bajaj Auto", "BSE"),
        ("TATAMOTORS.BO", "Tata Motors", "BSE"),
        ("ADANIENT.BO", "Adani Enterprises", "BSE"),
        ("JSWSTEEL.BO", "JSW Steel", "BSE"),
        ("WIPRO.BO", "Wipro", "BSE"),
        ("DRREDDY.BO", "Dr. Reddy's Labs", "BSE")
    ]
    
    # Top NSE companies (NSE symbols without .BO)
    nse_companies = [
        ("RELIANCE.NS", "Reliance Industries", "NSE"),
        ("TCS.NS", "Tata Consultancy Services", "NSE"),
        ("HDFCBANK.NS", "HDFC Bank", "NSE"),
        ("ICICIBANK.NS", "ICICI Bank", "NSE"),
        ("HINDUNILVR.NS", "Hindustan Unilever", "NSE"),
        ("INFY.NS", "Infosys", "NSE"),
        ("ITC.NS", "ITC", "NSE"),
        ("KOTAKBANK.NS", "Kotak Mahindra Bank", "NSE"),
        ("AXISBANK.NS", "Axis Bank", "NSE"),
        ("LT.NS", "Larsen & Toubro", "NSE"),
        ("SBIN.NS", "State Bank of India", "NSE"),
        ("BAJFINANCE.NS", "Bajaj Finance", "NSE"),
        ("BHARTIARTL.NS", "Bharti Airtel", "NSE"),
        ("ASIANPAINT.NS", "Asian Paints", "NSE"),
        ("HCLTECH.NS", "HCL Technologies", "NSE"),
        ("MARUTI.NS", "Maruti Suzuki", "NSE"),
        ("TITAN.NS", "Titan Company", "NSE"),
        ("ULTRACEMCO.NS", "UltraTech Cement", "NSE"),
        ("SUNPHARMA.NS", "Sun Pharmaceutical", "NSE"),
        ("NESTLEIND.NS", "Nestle India", "NSE"),
        ("ONGC.NS", "Oil & Natural Gas Corp", "NSE"),
        ("POWERGRID.NS", "Power Grid Corp", "NSE"),
        ("NTPC.NS", "NTPC", "NSE"),
        ("INDUSINDBK.NS", "IndusInd Bank", "NSE"),
        ("BAJAJ-AUTO.NS", "Bajaj Auto", "NSE"),
        ("TATAMOTORS.NS", "Tata Motors", "NSE"),
        ("ADANIENT.NS", "Adani Enterprises", "NSE"),
        ("JSWSTEEL.NS", "JSW Steel", "NSE"),
        ("WIPRO.NS", "Wipro", "NSE"),
        ("DRREDDY.NS", "Dr. Reddy's Labs", "NSE")
    ]
    
    # Combine both
    all_companies = bse_companies + nse_companies
    
    # Insert into DB
    for symbol, name, exchange in all_companies:
        try:
            cursor.execute(
                "INSERT INTO companies (symbol, name, exchange) VALUES (?, ?, ?)",
                (symbol, name, exchange)
            )
        except sqlite3.IntegrityError:
            pass  # Already exists
    
    conn.commit()
    conn.close()

def get_companies(exchange=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if exchange:
        cursor.execute("SELECT symbol, name, exchange FROM companies WHERE exchange = ?", (exchange,))
    else:
        cursor.execute("SELECT symbol, name, exchange FROM companies")
    companies = cursor.fetchall()
    conn.close()
    return companies

def get_company_by_symbol(symbol):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, name, exchange FROM companies WHERE symbol = ?", (symbol,))
    company = cursor.fetchone()
    conn.close()
    return company

