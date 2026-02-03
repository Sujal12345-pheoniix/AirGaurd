import os
import google.generativeai as genai
from typing import Optional

class ChatService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # using gemini-pro for text-only chat
            self.model = genai.GenerativeModel('gemini-pro')
            
        self.system_prompt = """
        You are AirGuard, an intelligent AI assistant dedicated to Air Quality Index (AQI) and health advice.
        
        Your responsibilities:
        1. Answer questions strictly related to AQI, air pollution, health precautions, and environmental safety.
        2. If a user asks about a general topic (e.g., "Write me a poem", "Who is the president"), politely decline and steer them back to air quality.
        3. Provide actionable, scientifically accurate advice based on general knowledge about air quality impact on health.
        4. Be concise, empathetic, and professional.
        
        For example:
        User: "Is it safe to go jogging?"
        You: "It depends on the current AQI. Generally, if AQI is below 100, it is safe for most people. If it is above 150, sensitive groups should avoid outdoor exertion. Check your local AQI first!"
        
        User: "What is the capital of France?"
        You: "I am specialized in Air Quality and Health. Please ask me about pollution, masks, or health tips!"
        """

    async def generate_response(self, user_message: str) -> str:
        if not self.model:
            return self._fallback_response(user_message)
            
        try:
            # Construct the full prompt with system context
            # Gemini Pro doesn't have a rigid "system" role in the same way as GPT-4, 
            # but pre-pending instructions works well.
            full_prompt = f"{self.system_prompt}\n\nUser: {user_message}\nAirGuard:"
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return self._fallback_response(user_message, error=True)

    def _fallback_response(self, message: str, error: bool = False) -> str:
        """
        Fallback logic strictly for when AI is unavailable.
        """
        msg = message.lower()
        prefix = "[AI Unavailable] " if error else ""
        
        if "safe" in msg and "outside" in msg:
            return prefix + "It depends on your local AQI. Generally, if AQI is below 100, it is safe."
        elif "precautions" in msg:
            return prefix + "Wear a N95 mask if AQI > 200. Avoid outdoor exercise if AQI > 300."
        elif "aqi" in msg and "tomorrow" in msg:
            return prefix + "Tomorrow's AQI is predicted to act similarly to today's trend unless weather changes."
        elif "jogging" in msg or "run" in msg:
            return prefix + "Early morning is usually best, unless smog is high. Check specific AQI."
        else:
            return prefix + "I can help with AQI queries. Try asking 'Is it safe outside?' (Chatbot running in offline mode)"

# Global instance
chat_service = ChatService()
