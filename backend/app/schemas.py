from pydantic import BaseModel
from typing import Optional, List

# Input for AQI Prediction
class AQIPredictionInput(BaseModel):
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    temperature: float
    humidity: float
    wind_speed: float

# Output for AQI Prediction
class AQIPredictionOutput(BaseModel):
    aqi: float
    category: str
    color: str
    advice: dict

# Input for Chatbot
class ChatInput(BaseModel):
    message: str
    location: Optional[str] = None

# Output for Chatbot
class ChatOutput(BaseModel):
    response: str

# Input for Location AQI
class LocationInput(BaseModel):
    latitude: float
    longitude: float
