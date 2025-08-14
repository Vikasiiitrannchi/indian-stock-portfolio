import pandas as pd

def calculate_sma(series, window):
    """Calculate Simple Moving Average"""
    return series.rolling(window=window).mean()