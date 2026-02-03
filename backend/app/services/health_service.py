
def get_health_advice(category: str) -> dict:
    """
    Return health advice based on AQI category.
    """
    category = category.lower()
    
    advice_db = {
        "good": {
            "general": "Air quality is considered satisfactory, and air pollution poses little or no risk.",
            "children": "Enjoy your usual outdoor activities.",
            "elderly": "Enjoy your usual outdoor activities.",
            "sensitive": "None.",
            "mask": "Not required",
            "outdoor_activity": "Ideal for outdoor activities."
        },
        "satisfactory": {
            "general": "Air quality is acceptable. However, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.",
            "children": "Okay to play outside.",
            "elderly": "Okay to be outside.",
            "sensitive": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
            "mask": "Not required usually",
            "outdoor_activity": "Good time for jogging."
        },
        "moderate": {
            "general": "Members of sensitive groups may experience health effects. The general public is not likely to be affected.",
            "children": "Limit prolonged outdoor exertion.",
            "elderly": "Limit prolonged outdoor exertion.",
            "sensitive": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
            "mask": "Recommended for sensitive groups",
            "outdoor_activity": "Reduce prolonged or heavy exertion. Take more breaks during outdoor activities."
        },
        "poor": {
            "general": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.",
            "children": "Avoid prolonged or heavy exertion.",
            "elderly": "Avoid prolonged or heavy exertion.",
            "sensitive": "Avoid prolonged or heavy exertion. Move activities indoors or reschedule.",
            "mask": "N95 mask recommended",
            "outdoor_activity": "Avoid heavy exertion. Move activities indoors."
        },
        "very poor": {
            "general": "Health warnings of emergency conditions. The entire population is more likely to be affected.",
            "children": "Avoid all outdoor exertion.",
            "elderly": "Avoid all outdoor exertion.",
            "sensitive": "Avoid all physical activity outdoors.",
            "mask": "N95 mask mandatory if outside",
            "outdoor_activity": "Avoid all physical activity outdoors."
        },
        "severe": {
            "general": "Health alert: everyone may experience more serious health effects.",
            "children": "Stay indoors and keep activity levels low.",
            "elderly": "Stay indoors and keep activity levels low.",
            "sensitive": "Remain indoors and keep activity levels low.",
            "mask": "N95 mask mandatory. Avoid going out.",
            "outdoor_activity": "Do not go outdoors."
        }
    }
    
    return advice_db.get(category, {
        "general": "No data available.",
        "children": "No data available.",
        "elderly": "No data available.",
        "sensitive": "No data available.",
        "mask": "N/A",
        "outdoor_activity": "N/A"
    })
