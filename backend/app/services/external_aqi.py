import requests
from app.services.aqi_service import classify_aqi
from app.services.health_service import get_health_advice

OPEN_METEO_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

def fetch_aqi_by_location(lat: float, lon: float):
    """
    Fetch real-time air quality data from Open-Meteo.
    Ref: https://open-meteo.com/en/docs/air-quality-api
    """
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide,ozone,carbon_monoxide",
            "timezone": "auto"
        }
        
        response = requests.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        
        # Map Open-Meteo keys to our internal keys
        aqi_data = {
            "pm25": current.get("pm2_5", 0),
            "pm10": current.get("pm10", 0),
            "no2": current.get("nitrogen_dioxide", 0),
            "so2": current.get("sulphur_dioxide", 0),
            "o3": current.get("ozone", 0),
            "co": current.get("carbon_monoxide", 0), # Open-Meteo gives CO in ug/m3 usually
            "temperature": 25.0, # Not in air-quality API usually, mock or separate call
            "humidity": 50.0 # Mock or separate call
        }
        
        # Calculate AQI (Simplified for demo, usually complex formula)
        # Using a weighted max similar to previous logic
        # NOTE: Open-Meteo also provides 'us_aqi' or 'european_aqi' directly if requested!
        # Let's request 'us_aqi' for simplicity if available, else calc.
        # Checking docs: Open-Meteo has `us_aqi` and `european_aqi` hourly. 
        # But `current` supports specific vars. Let's stick to raw vars for consistency with our 'Model'.
        
        # Heuristic AQI calc
        calculated_aqi = (
            0.5 * aqi_data["pm25"] + 
            0.3 * aqi_data["pm10"] + 
            0.1 * aqi_data["no2"] + 
            0.1 * aqi_data["so2"]
        )
        
        # Classification & Advice
        classification = classify_aqi(calculated_aqi)
        advice = get_health_advice(classification["category"])
        
        return {
            "aqi": calculated_aqi,
            "category": classification["category"],
            "color": classification["color"],
            "advice": advice,
            "components": aqi_data
        }
        
    except Exception as e:
        print(f"Error fetching AQI: {e}")
        # Return fallback or error
        return {
            "aqi": -1,
            "category": "Error",
            "color": "#808080",
            "advice": {"general": "Could not fetch data."},
            "components": {}
        }
