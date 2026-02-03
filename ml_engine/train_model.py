import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
from preprocessing import clean_data, feature_engineering

# 1. Generate Synthetic Data
def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
    
    data = {
        'date': dates,
        'pm25': np.random.uniform(10, 300, n_samples),
        'pm10': np.random.uniform(20, 400, n_samples),
        'no2': np.random.uniform(5, 100, n_samples),
        'so2': np.random.uniform(5, 50, n_samples),
        'co': np.random.uniform(0.1, 5, n_samples),
        'o3': np.random.uniform(10, 150, n_samples),
        'temperature': np.random.uniform(5, 45, n_samples),
        'humidity': np.random.uniform(20, 90, n_samples),
        'wind_speed': np.random.uniform(0, 20, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Simulate AQI dependency (simplified formula approximation)
    df['aqi'] = (
        0.5 * df['pm25'] + 
        0.3 * df['pm10'] + 
        0.1 * df['no2'] + 
        0.1 * df['so2'] +
        np.random.normal(0, 10, n_samples) # Noise
    )
    
    return df

if __name__ == "__main__":
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    print("Preprocessing...")
    df = clean_data(df)
    df = feature_engineering(df)
    
    # Define features and target
    target = 'aqi'
    features = [c for c in df.columns if c != target]
    
    X = df[features]
    y = df[target]
    
    print(f"Training with {X.shape[0]} samples and {X.shape[1]} features.")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training XGBoost Regressor...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        objective='reg:squarederror'
    )
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"R²: {r2:.2f}")
    
    print("Saving model...")
    joblib.dump(model, 'ml_engine/aqi_xgboost_model.joblib')
    print("Model saved to ml_engine/aqi_xgboost_model.joblib")
