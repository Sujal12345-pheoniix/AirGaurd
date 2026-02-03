import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data cleaning: drop duplicates, handle missing values.
    """
    df = df.drop_duplicates()
    df = df.ffill().bfill() # Simple imputation
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add rolling averages, lag features.
    Assuming df has a datetime index or column 'date'.
    """
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df.set_index('date', inplace=True)
    
    # Lag features
    for col in ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']:
        if col in df.columns:
            df[f'{col}_lag1'] = df[col].shift(1)
            df[f'{col}_rolling_mean_3'] = df[col].rolling(window=3).mean()
    
    # Drop rows with NaN created by lag/rolling
    df = df.dropna()
    return df
