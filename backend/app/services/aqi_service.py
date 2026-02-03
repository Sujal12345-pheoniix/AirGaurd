
def classify_aqi(aqi_value: float) -> dict:
    """
    Classify AQI based on Indian CPCB or US EPA standards. 
    Using a standard scale for this project:
    0–50 Good
    51–100 Satisfactory
    101–200 Moderate
    201–300 Poor
    301–400 Very Poor
    401–500 Severe
    """
    try:
        aqi = float(aqi_value)
    except ValueError:
        return {"category": "Unknown", "color": "#808080"}

    if 0 <= aqi <= 50:
        return {"category": "Good", "color": "#009966"} # Green
    elif 51 <= aqi <= 100:
        return {"category": "Satisfactory", "color": "#FFDE33"} # Yellow
    elif 101 <= aqi <= 200:
        return {"category": "Moderate", "color": "#FF9933"} # Orange
    elif 201 <= aqi <= 300:
        return {"category": "Poor", "color": "#CC0033"} # Red
    elif 301 <= aqi <= 400:
        return {"category": "Very Poor", "color": "#660099"} # Purple
    elif aqi >= 401:
        return {"category": "Severe", "color": "#7E0023"} # Maroon
    else:
        return {"category": "Unknown", "color": "#808080"}
